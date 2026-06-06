import pandas as pd
import re
from pathlib import Path

import pyarrow.ipc as ipc

try:
    from datasets import load_dataset
except ImportError:
    load_dataset = None

ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")

def extract_answer(full_ans_text: str) -> str:
    match = ANS_RE.search(full_ans_text)
    if match:
        match_str = match.group(1).strip()
        match_str = match_str.replace(",", "")
        return int(match_str.strip())
    return None


def _load_cached_split(split):
    cache_root = Path.home() / ".cache" / "huggingface" / "datasets" / "openai___gsm8k" / "main"
    split_name = "test" if split in ["test", "validation"] else split
    matches = list(cache_root.glob(f"0.0.0/*/gsm8k-{split_name}.arrow"))
    if not matches:
        raise FileNotFoundError(f"GSM8K cached split not found under {cache_root}")
    return ipc.open_stream(str(matches[0])).read_all().to_pandas()

def load_data(args, split='validation'):

    if load_dataset is not None:
        dataset = load_dataset('openai/gsm8k', 'main', cache_dir=args.data_dir)[split]
        dataset = pd.DataFrame(dataset)
    else:
        dataset = _load_cached_split(split)
    if split == 'train':
        dataset = dataset.sample(frac=1, random_state=0).reset_index(drop=True)
    else :
        dataset = dataset.sample(frac=1, random_state=0).reset_index(drop=True).head(args.data_size)
    
    questions, labels = [], []
    for question, answer in zip(dataset['question'], dataset['answer']) :
        label = extract_answer(answer)

        questions.append(question)
        labels.append(label)

    return questions, labels
