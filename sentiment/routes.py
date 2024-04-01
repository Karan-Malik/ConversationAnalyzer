from sentiment import app
from flask import Flask, render_template, request, jsonify, url_for, redirect,flash
from sentiment.forms import AudioForm
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

import openai
import os
import time
import pickle
import json

DG_KEY='f8402ca391ee0f2f203dfeda4e8851eff7886c40'
openai.api_key = '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'

UPLOAD_FOLDER = 'data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0,
    )
    return response.choices[0].message["content"]   

final=''


@app.route('/',methods=['GET','POST'])
def itemBasedRec():
    form=AudioForm()
    
    if form.validate_on_submit():
        audio_file = form.audio_file.data
        if audio_file:
            filename = audio_file.filename
            audio_file.save(os.path.join('data/', filename))
            print(os.getcwd())
            #print(os.path.join('/data', filename))
            f='data/'+filename
            deepgram = DeepgramClient(DG_KEY)

            with open(f, "rb") as file:
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
            if os.path.exists('json.pickle'):
                os.remove('json.pickle')
            with open('json.pickle', 'wb') as file:
                pickle.dump(json_dict, file)
            with open('json.pickle', 'rb') as file:
                loaded_dict = pickle.load(file)

            transcript=loaded_dict['results']['channels'][0]['alternatives'][0]['transcript']
            prompt='''This is a conversation between 2 people. You should be able to deduce who is speaking by analysing the conversation.
            Answer these questions for me, do not focus on summarizing the conversation, but rather things that might be hidden on the first listen:
            1. Character Analysis: Based on the conversation, analyze the personality traits of each speaker. Discuss their demeanor, interests, emotional state, and any hidden motivations they might have.
            2. Theme of the Conversation: Identify recurring themes and motifs in the conversation. Discuss the significance of these themes and how they reflect the speakers' values, concerns, and experiences.
            3. Emotional Analysis: Explore the emotional subtext underlying the conversation. Highlight moments of tension, vulnerability, humor, and empathy. Discuss how these emotions influence the dynamics between the speakers.
            4. Bias and Perspective: Explore the cognitive biases and perspectives displayed by the speakers. Discuss how their preconceptions, beliefs, and worldviews influence their interpretation of events and their interactions with each other
            5. Intent and Subterfuge Analysis: Analyze the speakers' intentions and potential subterfuge in the conversation. Identify instances of deception, manipulation, or ulterior motives. Discuss the implications of these behaviors on the overall interaction.
            Make sure the answers are not redundant and each point is separate without any heading.. 
            Important: Add a backslash n only after each point ends, all points should always be in the same line'''
            prompt= transcript+'\n\n'+prompt

            response = get_completion(prompt)
            global final

            final=response.split('\n')
            final=[x[2:-2] for x in final if len(x)>35]
            return redirect(url_for('results'))

    return render_template('item_based.html',form=form)


@app.route('/results',methods=['GET','POST'])
def results():
    global final
    print(final)
    print(type(final))
    if type(final)!=list or len(final)<5:
        flag=0
    else:
        flag=1
    return render_template('results.html',response=final,flag=flag)


@app.route('/api/analyze', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        audio_file = request.files['audio_file']
        if audio_file:
            filename = audio_file.filename
            audio_file.save(os.path.join('data/', filename))
            f = 'data/' + filename
            deepgram = DeepgramClient(DG_KEY)
            with open(f, "rb") as file:
                buffer_data = file.read()
            payload = {
                "buffer": buffer_data,
            }
            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
            )
            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
            convo = response.to_json(indent=4)
            json_dict = json.loads(convo)
            if os.path.exists('json.pickle'):
                os.remove('json.pickle')
            with open('json.pickle', 'wb') as file:
                pickle.dump(json_dict, file)
            with open('json.pickle', 'rb') as file:
                loaded_dict = pickle.load(file)
            transcript = loaded_dict['results']['channels'][0]['alternatives'][0]['transcript']
            prompt='''This is a conversation between 2 people. You should be able to deduce who is speaking by analysing the conversation.
            Answer these questions for me, do not focus on summarizing the conversation, but rather things that might be hidden on the first listen:
            1. Character Analysis: Based on the conversation, analyze the personality traits of each speaker. Discuss their demeanor, interests, emotional state, and any hidden motivations they might have.
            2. Theme of the Conversation: Identify recurring themes and motifs in the conversation. Discuss the significance of these themes and how they reflect the speakers' values, concerns, and experiences.
            3. Emotional Analysis: Explore the emotional subtext underlying the conversation. Highlight moments of tension, vulnerability, humor, and empathy. Discuss how these emotions influence the dynamics between the speakers.
            4. Bias and Perspective: Explore the cognitive biases and perspectives displayed by the speakers. Discuss how their preconceptions, beliefs, and worldviews influence their interpretation of events and their interactions with each other
            5. Intent and Subterfuge Analysis: Analyze the speakers' intentions and potential subterfuge in the conversation. Identify instances of deception, manipulation, or ulterior motives. Discuss the implications of these behaviors on the overall interaction.
            Make sure the answers are not redundant and each point is separate without any heading.. 
            Important: Add a backslash n only after each point ends, all points should always be in the same line'''
            prompt = transcript + '\n\n' + prompt
            response = get_completion(prompt)
            return jsonify(response=final)
    return jsonify(error="Invalid request"), 400
