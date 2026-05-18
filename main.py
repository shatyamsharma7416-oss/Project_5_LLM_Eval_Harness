import os
import tomllib
import json
import time
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
from openai import OpenAI

from test_loader import loader
from runner import test_output
from Evaluator import evaluate_score

load_dotenv()
console = Console()
ACTIVE_MODEL = "glm"

with open("llm_config.toml", 'rb') as f:
    llm_config = tomllib.load(f)

model = llm_config['models'][ACTIVE_MODEL]
client = OpenAI(
    base_url= model["url"],
    api_key= os.getenv(model["api"])
)

def save_response(answers: list):
    with open(f"results/run_{time.time()}.jsonl", 'a') as f:
        for answer in answers:
            f.write(json.dumps(answer) + '\n')

# def save_summary(answers: list):



def main():
    print()
    console.print(Panel(f"[green]LLM Evaluatior[/]\n[dim]Model: {model["name"]}", border_style="green"))

    cases = loader()
    print(cases)

    llm_answer = test_output(cases)

    answers_scores = evaluate_score(llm_answer)

    save_response(answers_scores)


    # response = client.chat.completions.create(
    #     model=model["name"],
    #     messages=[
    #         {"role": "user", "content": "Hi who are you who made you?"}
    #     ]
    # )

    # print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
