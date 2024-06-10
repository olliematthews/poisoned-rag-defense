from pathlib import Path
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt


def is_correct(row):
    answer = row["output"].split("Answer:")[-1].strip().lower()
    if "i don't know" in answer.lower():
        return False
    return row["correct answer"].lower() in answer


def is_incorrect(row):
    answer = row["output"].split("Answer:")[-1].strip().lower()
    if "i don't know" in answer.lower():
        return False
    return row["incorrect answer"].lower() in answer


cdir = Path(__file__).parent

# experiment = "gpt3.5_final"
experiment = "gpt_contexts_35"


results_dir = cdir / experiment

context_df = pd.read_pickle(results_dir / "context.p")
di_df_c = pd.read_pickle(results_dir / "danger_results_combined.p")
di_df_nc = pd.read_pickle(results_dir / "danger_results_not_combined.p")
outputs_df = pd.read_pickle(results_dir / "llm_outputs.p")
questions_df = pd.read_pickle(results_dir / "questions.p")

results_df = pd.merge(
    outputs_df.reset_index(),
    questions_df[["question", "correct answer", "incorrect answer"]],
    on="qid",
)

results_df["correct"] = results_df.apply(is_correct, axis=1)
results_df["poisoned"] = results_df.apply(is_incorrect, axis=1)
results_df = pd.merge(results_df, di_df_nc["dangerous"], on=["qid", "Context type"])
results_df["poisoned_with_check"] = ~results_df["dangerous"] & results_df["poisoned"]
results_df.groupby(["Prompt type", "Context type"]).agg(
    {"poisoned": "mean", "correct": "mean", "poisoned_with_check": "mean"}
)
print("hi")
