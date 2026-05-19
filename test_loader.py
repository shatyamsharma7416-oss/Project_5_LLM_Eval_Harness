from pydantic import BaseModel, Field, ValidationError
from rich.console import Console
from rich.prompt import Prompt
import questionary
from enum import Enum
import json


console = Console()
prompt = Prompt()

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Tag(str, Enum):
    FACTUAL = "factual"
    GEOGRAPHY = "geography"
    SUMMARIZATION = "summarization"
    REASONING = "reasoning"
    MATH = "math"

class Test_validate(BaseModel):
    id: str
    input: str
    expected: str
    tags: list[Tag] = Field(min_length=1, max_length=2)
    difficulty: Difficulty


def loader(file_location):
    with open(file_location, 'r') as f:
        test_cases = json.load(f)

    while True:
        difficulty_levels = questionary.checkbox(
            "What Question difficulty you want to include?",
            choices=[
                "Easy",
                "Medium",
                "Hard",
            ],
            default="Easy"
        ).ask()

        tags = questionary.checkbox(
            "What Question Type you want to include?",
            choices=[
                "Factual",
                "Geography",
                "Summarization",
                "Reasoning",
                "Math"
            ],
            default="Factual"
        ).ask()

        difficulty_levels = set(x.lower() for x in difficulty_levels)
        tags = set(x.lower() for x in tags)
        print(len(difficulty_levels), len(tags))

        if len(difficulty_levels)>=1 and len(tags)>=1:
            break
    
    success, failed = 0,0
    filtered_cases = []
    for case in test_cases:
        try:
            Test_validate.model_validate(case)
            # if case validation is True than check used filteration
            if case["difficulty"] in difficulty_levels:
                if not(set(case["tags"]).isdisjoint(tags)):    #  -----> True if any common items in sets
                    filtered_cases.append(case)

            success += 1
        except ValidationError as e:
            console.print(f"Validation failed:\n{e}\n\n[red]ID[/]: [bold]{case['id']}[/]\n")
            failed += 1


    console.print("\n[green][bold]======Summary=======[/][/]\n")
    console.print(f"[green]Validation Success: {success}[/]")
    console.print(f"[red]Validation Failed : {failed}[/]")
    console.print(f"\n[bold]Loaded {len(test_cases)} test cases. Filtered to {len(filtered_cases)}.[/]\n")

    return filtered_cases


