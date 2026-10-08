# AI: models, prompts and evaluation

Only if the project has an AI part. If it doesn't, delete this folder in your first pull request.

**بالعربي:** الفولدر ده للمشاريع اللي فيها جزء AI بس. لو مشروعكم مفيهوش، امسحوه في أول pull request.

## Read this first

[AI-CONCEPTS.md](AI-CONCEPTS.md): how AI work is done in real products. Lineage, model versions, data leakage, and measuring before believing.

## Start here

Pick the kind of AI work first, because the folder looks different:

**You train your own model** (e.g. a classifier or a risk model):

```
ai/
├── data/README.md     # where the data comes from and how to download it (data files are NOT in git)
├── train.py           # training is a script, not a notebook
├── evaluate.py        # metrics vs. a simple baseline
├── notebooks/         # exploration only
└── model-card.md      # what it predicts, the data, the metrics, known limits
```

**You use an LLM API** (e.g. a chatbot or an assistant):

```
ai/
├── examples.md        # 30+ example inputs and the output each should give
├── prompts/           # prompts, versioned like code
├── evaluate.py        # runs the examples and prints how many pass
└── report.md          # the latest results
```

## Rules for this folder

- **No model files or datasets in git.** CI blocks `.pkl`, `.pt`, `.h5`, `.onnx` and files over 5 MB. Attach models to a GitHub Release instead.
- **No API keys in git or in the app.** The backend calls the AI; keys live in `.env`.
- **Always compare with a baseline**, and put the numbers in the pull request.
- **Split data the honest way.** Time-series → train on the past, test on the future. Map/location data → split by region.
