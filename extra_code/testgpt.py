import openai

import os

import pandas as pd

import time

openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=0,

    )

    return response.choices[0].message["content"]   

prompt = "what is a bank?"

response = get_completion(prompt)

print(response)
