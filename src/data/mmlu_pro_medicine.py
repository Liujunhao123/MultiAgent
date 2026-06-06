import pandas as pd
from pathlib import Path

import pyarrow.ipc as ipc

try:
    from datasets import load_dataset
except ImportError:
    load_dataset = None

# def load_data(args, split='validation'):
#     split = 'validation' if split == 'test' else split
#     dataset = load_dataset('Rowan/hellaswag', cache_dir=args.data_dir)[split]
#     dataset = pd.DataFrame(dataset)
#     if split == 'train':
#         dataset = dataset.sample(frac=1, random_state=0).reset_index(drop=True).head(args.data_size)
#     else :
#         dataset = dataset.sample(frac=1, random_state=0).reset_index(drop=True).head(300)

#     questions, labels = [], []
#     choices = "ABCD"
#     template = 'Can you choose the option that best follows:\n"{}"?\n(A) {}\n(B) {}\n(C) {}\n(D) {}\n\n'
#     for ctx, options, answer in zip(dataset['ctx'], dataset['endings'], dataset['label']):
#         if len(options) != 4 :
#             continue
#         question = template.format(ctx, options[0], options[1], options[2], options[3])
#         label = f"({choices[int(answer)]})"
#         questions.append(question)
#         labels.append(label)
    
#     return questions, labels

def load_data(args, split='validation'):
    split = 'validation' if split == 'train' else 'test'
    if load_dataset is not None:
        dataset = load_dataset('cais/mmlu', 'professional_medicine', cache_dir=args.data_dir)[split]
        dataset = pd.DataFrame(dataset)
    else:
        cache_root = Path.home() / ".cache" / "huggingface" / "datasets" / "cais___mmlu" / "professional_medicine"
        matches = list(cache_root.glob(f"0.0.0/*/mmlu-{split}.arrow"))
        if not matches:
            raise FileNotFoundError(f"MMLU professional_medicine cached split not found under {cache_root}")
        dataset = ipc.open_stream(str(matches[0])).read_all().to_pandas()
    if args.data_size:
        dataset = dataset.head(args.data_size)
    
    questions, labels = [], []
    choices = "ABCD"
    template = '{}\n(A) {}\n(B) {}\n(C) {}\n(D) {}\n\n'
    for query, options, answer in zip(dataset['question'], dataset['choices'], dataset['answer']):
        if len(options) != 4 :
            continue
        question = template.format(query, options[0], options[1], options[2], options[3])
        label = f"({choices[int(answer)]})"
        questions.append(question)
        labels.append(label)

    return questions, labels
