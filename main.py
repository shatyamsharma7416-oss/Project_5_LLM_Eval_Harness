import os
import json
import time
import pathlib
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from dotenv import load_dotenv
from openai import OpenAI

from test_loader import loader
from runner import test_output
from Evaluator import evaluate_score
from summary import save_summary


load_dotenv()
console = Console()

def save_response(answers: list, timestamp: str):
    with open(f"results/run_{timestamp}.jsonl", 'a') as f:
        for answer in answers:
            f.write(json.dumps(answer) + '\n')


def main():
    """
    All features is being called from here
    """
    print()
    console.print(Panel(f"[green]LLM Evaluatior[/]\n", border_style="green"))

    file_location = Prompt.ask("[bold]Provide your file location[/]")
    while True:
        try:
            file_location = pathlib.Path(file_location)
            cases = loader(file_location)

        except FileNotFoundError:
            file_location = Prompt.ask("[bold]Please Provide a valid file location[/]")
        else:
            break

    llm_answer = test_output(cases)

    answers_scores = evaluate_score(llm_answer)
    timestamp = str(time.time())
    save_response(answers_scores, timestamp)
    save_summary(timestamp)


if __name__ == "__main__":
    main()
