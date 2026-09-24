# 05 — AI & MLOps concepts (for teams with an AI part)

Most course ML ends at `model.predict(X)` in a notebook. In a real product, that's roughly where the work starts: the model has to be reproduced, versioned, served by a backend, and trusted by someone who didn't train it.

You don't need MLOps tools for a graduation project. You need the **ideas** behind them. This page explains five of them and gives you a simple way to apply each one.

---

## The five ideas

### 1. Lineage: every model can say where it came from

Imagine your model scored 0.86 last month and 0.81 today. What changed: the data, the code, the parameters? If you can't answer, you can't fix it.

**Minimum:** every trained model has a small record next to it:

```json
{
  "model_version": "v0.3.0",
  "git_commit": "a1b2c3d",
  "data_version": "firms_2020-2025_egypt_v2",
  "params": {"n_estimators": 300, "max_depth": 8},
  "metrics": {"roc_auc": 0.84, "pr_auc": 0.41, "brier": 0.09},
  "baseline_metrics": {"roc_auc": 0.71},
  "trained_at": "2027-01-10",
  "training_seconds": 212
}
```

Always log **params and metrics together**. Metrics without params can't be reproduced; params without metrics are useless.

*Industry tool for this:* MLflow tracking, Weights & Biases.

### 2. The model is a reference, not a file

The backend shouldn't contain `load("models/final_v2_REAL.pkl")`. It should ask for a **version** from configuration:

```
MODEL_VERSION=v0.3.0    # in .env
```

**Test:** can you switch to a different model, or roll back to the last good one, **without changing code**? If yes, you have a rollback. If no, every model change is a code change.

**Where the model file lives (never in git):**

- **GitHub Releases:** attach the model file to a release tag. Simple and free, and a good fit for most student projects.
- **Hugging Face Hub**, cloud storage, or DVC remote for bigger files.

CI will fail if a `.pkl` / `.pt` / `.h5` / `.onnx` file is committed. That's on purpose.

*Industry tool for this:* a model registry (MLflow Registry) with aliases like `production`.

### 3. Preprocessing travels with the model

The scaler, encoder, tokenizer or feature function is **part of the model**. If training scaled the features and serving forgot to, the model doesn't crash. It returns confident, wrong numbers, and every offline metric still looks fine.

**Minimum:**

- Put preprocessing and model in **one object** (e.g. a scikit-learn `Pipeline`) and save that.
- Feature-building code lives in **one module** imported by both training and serving. Never copy-paste it.
- The API accepts raw input (`lat`, `lon`, `date`), not pre-made features. The backend asks the model artifact to turn raw input into features.

### 4. Measure before you believe

- **Always have a baseline.** "Predict the historical average for that area" or "always say Low". If your model doesn't clearly beat it, the model isn't adding anything.
- **Know your noise.** Train the same model twice with different seeds. If scores differ by 0.02, a 0.01 "improvement" isn't real.
- **Use metrics that fit the problem.** Rare events (fires, floods) → accuracy is misleading (99% by always saying "no fire"). Use precision/recall, PR-AUC, and calibration (Brier score) if you show probabilities.
- **A check that can't fail isn't a check.** Break something on purpose and confirm your test catches it.

### 5. Your code runs in more places than your laptop

The same training script runs on your laptop, a teammate's laptop, Colab, CI and a Docker container. They differ in ways you can't see.

- Paths and settings come from config, not `C:\Users\Ahmed\Desktop\data.csv`.
- `localhost` inside Docker means the container itself, not your machine.
- A file on your disk may be gitignored and missing everywhere else.
- Pin library versions. "Works on my machine" usually means different versions.

---

## Data leakage: the mistake that makes you look great until the demo

Leakage means information from the test set sneaks into training. Your metrics go **up**, so nothing looks wrong.

Common forms:

- **Fitting a scaler/encoder on all data before splitting.** Split first. `fit` on train only, `transform` everywhere else.
- **Random split on time-series data.** If you predict tomorrow's risk, train on the past and test on the future. A random split lets the model "see the future".
- **Random split on spatial data.** Neighboring grid cells are almost identical. If one is in train and its neighbor in test, you're testing on near-copies. Split by region or use spatial blocks.
- **Features that only exist after the event.** "Burned area" can't predict whether a fire will happen.

> For hazard and earth-observation projects, time-based and region-based splits are required, not optional.

---

## Be honest about what the model can do

A risk model gives **probabilities under the conditions it was trained on**, not certainties. In the app and in your presentation:

- Show risk levels and confidence, not "a fire WILL happen".
- Say what data and region it was trained on, and where it's likely to be wrong.
- If something isn't scientifically established (for example, predicting the exact time and place of earthquakes), don't present it as a prediction feature. Exploratory research is fine; label it as research.

---

## Levels: what to aim for

| | Level 1 — required | Level 2 — strong project | Level 3 — bonus |
|---|---|---|---|
| **Code** | Notebooks for exploration only; training is a script (`python train.py`) | Config file for params; fixed random seeds | CI runs a tiny training smoke test |
| **Data** | Data source, date range and processing documented in a data card | Dataset versioned by name/hash; download script instead of manual steps | DVC for data versioning |
| **Evaluation** | Baseline + proper split (time/region where relevant) | Seeds noise measured; metric table in the PR | Automated check: new model must beat current by a margin |
| **Artifact** | Preprocessing + model saved as one object, **not in git** | Run record JSON (lineage) + model card | MLflow tracking + registry |
| **Serving** | Backend loads model by `MODEL_VERSION`; input validated | Model loaded once at startup; `/health` reports model version | Load test: latency numbers for your endpoint |

---

## Model card template

Create `docs/model-card.md` for each model you ship:

```markdown
# Model card — <name> <version>

**What it predicts:** …  
**Intended use / not intended for:** …  
**Training data:** source, region, date range, size, how labels were made  
**Split:** how (time / region / random) and why  
**Metrics:** table vs. baseline, on the held-out set  
**Known limitations:** where it's likely wrong (regions, seasons, missing data)  
**Lineage:** git commit, data version, params  
```

---

*Further reading, if you want to go deeper: "Designing Machine Learning Systems" (Chip Huyen), MLflow and DVC documentation, the MLOps MENA community sessions.*
