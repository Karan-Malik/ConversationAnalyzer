import requests

# Specify the path to your audio file
audio_file_path = 'path/to/your/audio/file.wav'

# Create a dictionary to hold the file data
files = {'audio_file': open('/Users/karanmalik/Downloads/M_0025_11y10m_1.wav', 'rb')}

# Send the POST request to the API endpoint
response = requests.post('https://conversationanalyzer.wl.r.appspot.com/api/analyze', files=files)

# Check if the request was successful
if response.status_code == 200:
    # Print the response JSON
    print(response.json())
else:
    # Print the error message
    print(response.json())