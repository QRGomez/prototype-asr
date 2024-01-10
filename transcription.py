import requests
import preprocess
import checkType
import os

file_input = "audios/sample_video.mp4" #INPUT VAR
file_type = checkType.get_file_type(file_input)
file_name, file_extension = os.path.splitext(file_input)

AUDIODIR= 'audios/' #Directory of audio uploads / extractions.

if file_type and "audio" in file_type: #AUDIqO INPUT
    file_input = preprocess.MP32Wav(file_input,AUDIODIR,(file_name+".wav")) # extract audio & convert to wav
    with open(file_input, 'rb') as file: # READS AND POSTS THE INPUT FILE TO API 
        files = {'file': (file_input, file, 'audio/wav')}
        response = requests.post("http://127.0.0.1:8000/transcribe", files=files)
    
    os.remove(file_input)

elif file_type and "video" in file_type: #VIDEO INPUT
    file_input = preprocess.Video2Wav(file_input,AUDIODIR,(file_name+".wav")) # extract audio & convert to wav
    
    with open(file_input, 'rb') as file: # READS AND POSTS THE INPUT FILE TO API 
        files = {'file': (file_input, file, 'audio/wav')}
        response = requests.post("http://127.0.0.1:8000/transcribe", files=files)
    
    os.remove(file_input)

else:
    print("Unsupported file type")

print(response.json())


