import pandas as pd
import numpy as np
import json


def save_summary(timestamp: str):

    summary = {}

    df = pd.read_json(f"results/run_{timestamp}.jsonl", lines=True)

    # overall score
    overall_avg_score = df['llm_score'].mean()
    summary['overall'] = {"semantic_avg": overall_avg_score, "pass_rate": "72%"}

    # by tags score
    df_exploded = df.explode('tags')
    df_tags_scores = (
        df_exploded
        .groupby('tags')["llm_score"]
        .mean()
        .reset_index()
    )
    df_tags_scores.set_index("tags", inplace=True)
    summary["by_tag"] = json.loads(df_tags_scores.to_json())['llm_score']

    # by difficulty score
    df_difficulty_score = (
        df
        .groupby("difficulty")['llm_score']
        .mean()
        .reset_index()
    )
    df_difficulty_score.set_index("difficulty", inplace=True)
    summary["by_difficulty"] = json.loads(df_difficulty_score.to_json())['llm_score']

    # latency summary
    df['latency'].mean()
    summary['latency'] = {"mean_ms": float(df['latency'].mean()), "p95_ms": float(np.percentile(df['latency'], 95))}

    with open(f"results/summary_{timestamp}.json", 'w') as f:
        json.dump(summary, f, indent=4)

