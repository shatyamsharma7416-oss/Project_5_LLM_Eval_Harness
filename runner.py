from dotenv import load_dotenv
from openai import OpenAI
import tomllib
import time
import json
import os

load_dotenv()

with open("llm_config.toml", 'rb') as f:
    config = tomllib.load(f)


ACTIVE_MODEL = "gemini"
model_config = config["models"][ACTIVE_MODEL]

client = OpenAI(
    base_url=model_config["url"],
    api_key=os.getenv(model_config['api'])
)

def sys_prompt(tags):
    if "summarization" in tags:
        prompt = """
        Summarize the text into exactly as the given format:
        {
           "answer": "place your summary here"
        }
        """
    else:
        prompt = """
        Answer the following question in given format
        {
            "answer": "Here you will place your answer"
        }
        """
    
    return prompt

def test_output(test_cases: list) -> list:
    answers = []
    for case in test_cases:
        PROMPT = sys_prompt(case['tags'])

        print("\n\033[94mLLM is generating answer....!\033[0m\n")

        start = time.time()
        response = client.chat.completions.create(
            model= model_config['name'],
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": case["input"]}
            ],
            response_format={"type": "json_object"}
        )
        latency = (time.time() - start)

        reply = json.loads(response.choices[0].message.content)
        reply = reply['answer']

        answer = {"input": case['input'], "expected": case['expected'], "actual": reply, "latency": latency}
        answers.append(answer)

    return answers
