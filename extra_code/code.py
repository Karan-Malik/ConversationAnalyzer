from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

import openai
import os
import pandas as pd
import time
import pickle
import json


AUDIO_FILE = "test.wav"
DG_KEY='f8402ca391ee0f2f203dfeda4e8851eff7886c40'
openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0,
    )
    return response.choices[0].message["content"]   


def main():
    try:
        deepgram = DeepgramClient(DG_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        convo=response.to_json(indent=4)
        json_dict = json.loads(convo)
        print("JSON data loaded successfully as dictionary:")

        with open('json.pickle', 'wb') as file:
            pickle.dump(json_dict, file)
        with open('json.pickle', 'rb') as file:
            loaded_dict = pickle.load(file)

        transcript=loaded_dict['results']['channels'][0]['alternatives'][0]['transcript']
        prompt = transcript+'\n\n'+'This is a conversation between 2 people. You should be able to deduce who is speaking by analysing the conversation. Go through the conversation and give me insights about the speaker, about what they like, what they did and what do their personalities seem like.'

        response = get_completion(prompt)
        print(response)



    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()

