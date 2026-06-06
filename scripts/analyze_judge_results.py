import argparse
import json
from collections import Counter
from pathlib import Path


def _is_valid(answer):
    return answer not in ("", None)


def _all_valid(answers):
    return all(_is_valid(answer) for answer in answers)


def _majority_fraction(answers):
    valid = [answer for answer in answers if _is_valid(answer)]
    if not valid:
        return 0.0
    return Counter(valid).most_common(1)[0][1] / len(answers)


def _unanimous(answers):
    valid = [answer for answer in answers if _is_valid(answer)]
    return len(valid) == len(answers) and len(set(valid)) == 1


def _mean(values):
    return sum(values) / len(values) if values else 0.0


def analyze_file(path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line)["0"])

    total = len(rows)
    judge_correct = 0
    vote_correct = 0
    judge_valid = 0
    all_agent_valid = 0
    unanimous = 0
    judge_vote_agree = 0
    judge_fix = 0
    judge_harm = 0
    majority_fractions = []

    for row in rows:
        aggregation = row.get("aggregation", {})
        agent_answers = aggregation.get("agent_vote_final_answers", [])
        vote_answer = aggregation.get("agent_vote_answer", "")
        judge_answer = row.get("debate_answer", "")

        judge_is_correct = bool(row.get("debate_answer_iscorr", False))
        vote_is_correct = bool(aggregation.get("agent_vote_iscorr", False))

        judge_correct += judge_is_correct
        vote_correct += vote_is_correct
        judge_valid += _is_valid(judge_answer)
        all_agent_valid += _all_valid(agent_answers)
        unanimous += _unanimous(agent_answers)
        judge_vote_agree += judge_answer == vote_answer
        judge_fix += (not vote_is_correct) and judge_is_correct
        judge_harm += vote_is_correct and (not judge_is_correct)
        majority_fractions.append(_majority_fraction(agent_answers))

    return {
        "dataset": path.stem.split("_100__")[0],
        "samples": total,
        "judge_acc": judge_correct / total,
        "agent_vote_acc": vote_correct / total,
        "judge_valid_rate": judge_valid / total,
        "all_agent_valid_rate": all_agent_valid / total,
        "agent_unanimous_rate": unanimous / total,
        "avg_majority_fraction": _mean(majority_fractions),
        "judge_vote_agreement": judge_vote_agree / total,
        "judge_fix_rate": judge_fix / total,
        "judge_harm_rate": judge_harm / total,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--history-dir", default="out/judge_100/history")
    parser.add_argument("--output", default="out/judge_100/metrics.tsv")
    args = parser.parse_args()

    history_dir = Path(args.history_dir)
    rows = [analyze_file(path) for path in sorted(history_dir.glob("*_JUDGE.jsonl"))]
    columns = [
        "dataset",
        "samples",
        "judge_acc",
        "agent_vote_acc",
        "judge_valid_rate",
        "all_agent_valid_rate",
        "agent_unanimous_rate",
        "avg_majority_fraction",
        "judge_vote_agreement",
        "judge_fix_rate",
        "judge_harm_rate",
    ]

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write("\t".join(columns) + "\n")
        for row in rows:
            values = []
            for column in columns:
                value = row[column]
                if isinstance(value, float):
                    value = f"{value:.4f}"
                values.append(str(value))
            f.write("\t".join(values) + "\n")

    print("\t".join(columns))
    for row in rows:
        print("\t".join(f"{row[column]:.4f}" if isinstance(row[column], float) else str(row[column]) for column in columns))


if __name__ == "__main__":
    main()
