# Conversation Analyzer

This project analyzes conversations between multiple speakers and provide insights into their personalities, emotions, biases, and intentions.

## Features

- Transcribes audio conversations to text
- Analyzes the text to provide insights on character analysis, emotional analysis, biases, and intentions
- Hosted using Flask
- Deployed on Google Cloud Platform (GCP)
- Provides a RESTful API for easy integration into other applications

### Link to web-app hosted on GCP: https://conversationanalyzer.wl.r.appspot.com/
### RestAPI end point: https://conversationanalyzer.wl.r.appspot.com/api/analyze

## Challenges Faced

- **Dependency Resolution**: One of the challenges encountered was resolving dependencies, especially when deploying the application on GCP. Ensuring that all required libraries and packages are installed and configured correctly was time-consuming.
  
- **Prompt Optimization**: Experimenting with different prompts to extract meaningful insights was also challenging. It required iterative testing and refinement to come up with prompts that could generate relevant and valuable responses from the GPT 3.5.

## Instructions

#### Running the server
Use the link: https://conversationanalyzer.wl.r.appspot.com/

Upload a .wav/.mp3 file and click upload to see the analysis of the conversation.

#### Using API endpoint
Send a POST request to the following endpoint with the audio file as form data: https://conversationanalyzer.wl.r.appspot.com/api/analyze

Example of how to do this can be seen in the file extra_code/apitest.py

#### Running code locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Karan-Malik/conversation-analyzer.git
   ```

2. Install requirements:

   ```bash
   git clone https://github.com/Karan-Malik/conversation-analyzer.git
   ```

3. Run the Flask application

   Windows:
   ```bash
   set FLASK_APP=sentiment.py
   flask run
   ```
   Mac OS/Linux:
   ```bash
   export FLASK_APP=sentiment.py
   flask run
   ```
4. Access application on local host at: http://127.0.0.1:5000/


##Technologies Used
1. Flask
2. Google Cloud Platform
3. Deepgram API
4. OpenAI API (GPT 3.5)
