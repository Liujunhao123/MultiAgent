# MultiAgent

一个用于多智能体大语言模型决策实验的项目。项目支持多个智能体对同一道题独立作答，并通过多数投票或裁判聚合生成最终答案，可用于比较不同聚合策略在数学推理、文字题和选择题任务上的表现。

## 功能特点

- 支持多个智能体并行回答同一道题。
- 支持多数投票聚合和裁判聚合两种决策方式。
- 支持算术题、GSM8K、医学选择题等任务。
- 支持 OpenAI-compatible Chat Completions 接口。
- 自动记录每题回答历史、最终答案和准确率。
- 提供额外分析指标，例如答案有效率、一致率、修正率和误改率。

## 环境准备

建议使用 Python 3.10 或以上版本。

可根据 `environment.yaml` 创建环境：

```powershell
conda env create -f environment.yaml
conda activate venv
```

## 快速运行

将下面命令中的 `<API_BASE>` 和 `<MODEL_NAME>` 替换为自己的模型服务地址和模型名称。

```powershell
python src\main.py `
  --model <MODEL_NAME> `
  --api_base <API_BASE> `
  --api_model <MODEL_NAME> `
  --num_agents 5 `
  --data arithmetics `
  --data_size 100 `
  --debate_rounds 0 `
  --aggregation judge `
  --out_dir out\judge_100
```

常用参数说明：

- `--num_agents`：智能体数量。
- `--data`：数据集名称，例如 `arithmetics`、`gsm8k`、`pro_medicine`。
- `--data_size`：测试题目数量。
- `--debate_rounds`：辩论轮数，设为 `0` 表示只进行独立回答和聚合。
- `--aggregation vote`：使用多数投票。
- `--aggregation judge`：使用裁判聚合。
- `--out_dir`：实验结果输出目录。

## 实验结果分析

运行实验后，结果会保存到：

```text
out/<run_name>/logs.tsv
out/<run_name>/history/
```

可以使用分析脚本统计更多过程指标：

```powershell
python scripts\analyze_judge_results.py `
  --history-dir out\judge_100\history `
  --output out\judge_100\metrics.tsv
```

输出指标包括：

- `judge_acc`：裁判聚合准确率。
- `agent_vote_acc`：同批智能体多数投票准确率。
- `judge_valid_rate`：裁判答案可解析比例。
- `agent_unanimous_rate`：智能体完全一致比例。
- `judge_vote_agreement`：裁判答案与多数投票一致比例。
- `judge_fix_rate`：裁判修正多数投票错误的比例。
- `judge_harm_rate`：裁判将多数投票正确答案改错的比例。

## 项目结构

```text
src/
  main.py                 # 实验入口
  evaluator.py            # 答案抽取与评估
  model/                  # 模型调用逻辑
  data/                   # 数据加载逻辑
scripts/
  analyze_judge_results.py
out/
  # 实验输出，默认不提交到版本库
```

## 注意事项

- 不要将真实 API Key、内网地址或个人路径提交到版本库。
- 如果使用远程模型服务，请用环境变量或本地配置保存敏感信息。
- 大规模实验会产生较多模型调用，请先用小样本确认流程正常。
- `out/` 目录默认用于保存实验输出，建议只提交汇总后的结果表，不提交完整模型回答历史。
