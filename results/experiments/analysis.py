from pathlib import Path
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt


def is_correct(row):
    answer = row["output"].split("Answer:")[-1].strip().lower()
    return row["correct answer"].lower() in answer


def is_incorrect(row):
    answer = row["output"].split("Answer:")[-1].strip().lower()
    return row["incorrect answer"].lower() in answer


cdir = Path(__file__).parent


def load_df(results_path):
    with open(results_path) as fd:
        data = json.load(fd)
    dataset_questions = pd.read_json(
        f"results/target_queries/{data['args']['eval_dataset']}.json"
    )
    dataset_questions.set_index("id", inplace=True)
    results = pd.DataFrame(data["results"]).join(dataset_questions, on="question_id")
    results["correct"] = results.apply(is_correct, axis=1)
    results["poisoned"] = results.apply(is_incorrect, axis=1)
    return results


results_original_prompt_3p5 = load_df(cdir / "experiment_3_100q" / "results_3.json")
results_refined_prompt_3p5 = load_df(cdir / "experiment_3_100q" / "results_2.json")
results_cot_prompt_3p5 = load_df(cdir / "experiment_3_100q" / "results_4.json")
# results_gpt4 = load_df(cdir / "experiment_2" / "results_2.json")
# results_cot_gpt3p5 = load_df(cdir / "experiment_2" / "results_3.json")
# results_cot_gpt3p5_prompt2 = load_df(cdir / "experiment_2" / "results_4.json")
# results_cot_gpt4 = load_df(cdir / "experiment_2" / "results_5.json")
# results_cot_gpt4_prompt2 = load_df(cdir / "experiment_2" / "results_6.json")
# results_cot_gpt3p5_reprompt = load_df(cdir / "experiment_2" / "results_6.json")


def filter(db):
    return np.mean(db[db["query_type"] == "Context with gt and poisoning"]["poisoned"])


# results = {
#     "original prompt": filter(results_original_prompt),
#     "refined prompt": filter(results_original_prompt),
#     "cot prompting": filter(results_cot_gpt3p5_prompt2),
# }
# plt.bar(results.keys(), results.values())
# plt.savefig("image.png")
print("HI")
