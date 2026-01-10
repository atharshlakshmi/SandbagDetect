# SandbagDetect

SandbagDetect is a lightweight experiment repository that evaluates whether large language models exhibit "sandbagging" — i.e., providing weaker answers in evaluation-style prompts compared with casual prompts — across a set of 50 prompt pairs. The project is designed to be simple to run locally: provide API keys for the models you want to test, and run `src/experiments.py` to produce per-pair logs and a model comparison CSV.

By: Atharshlakshmi Vijayakumar, Balakrishnan Vaisiya

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Repo structure](#repository-structure)
- [How it works](#how-it-works)
- [Running your own models](#running-your-own-models)
- [Remarks](#remarks)

## Installation

Create and activate a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then log in to Hugging Face to access gated models:

```bash
hf auth login
```

You'll be prompted to enter your HF API token (get one from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)).

## Usage

1. Add your model API keys into the .env file as in ```.env.example```:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

2. Run the experiments (will iterate models and write per-model logs):

```bash
python src/experiments.py
```

Notes:
- Per-pair logs and model comparison CSVs are written to `~/reports/experiment_logs` by default.

## Tech Stack

- **Python 3.x** — Core language
- **PyTorch** — Deep learning framework for local model inference
- **Transformers** — Hugging Face library for loading and running LLMs
- **Google Generative AI SDK** — Gemini API integration
- **Lambda Labs GPUs** — GPU compute for model experiments (optional, for larger models)
- **Pandas** — Data manipulation and CSV output

## Repository Structure

```
SandbagDetect/
├── README.md
├── requirements.txt
├── prompts/
│   ├── sandbagging_question_pairs.json
│   └── generatePrompts.py
├── scripts/
│   └── test_logger.py
├── src/
│   ├── experiments.py
│   ├── logger.py
│   ├── metrics.py
│   └── utils.py
└── reports/  # generated output (writes to home/reports/experiment_logs by default)
```

## How it works

- The repo loads 50 prompt pairs from `prompts/sandbagging_question_pairs.json`.
- For each pair it runs two prompts (evaluation-style and casual-style) through the same model using a single adapter function (`call_LLM`).
- It records both responses and computes per-pair metrics: correctness (binary/score), length ratio, semantic similarity, and a `sandbagging_flag` indicating whether the casual response was better than the evaluation response.
- Per-pair results are appended to a per-model CSV. After all pairs, aggregated experiment metrics are computed and appended to a `model_comparison.csv` for cross-model analysis.

## Running your own models

- Implement or adapt `call_LLM(model_name, prompt, **kwargs)` in `src/utils.py` to call your model provider. The rest of the code expects `call_LLM` to return a text response string.
- Add API keys, if applicable, into your `.env` file.
- Update the list of models in `src/experiments.py`.

## Remarks

This experiment was built for the Apart Research Hackathon Sprint.


