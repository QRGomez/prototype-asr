import torchaudio
import speechbrain as sb
from speechbrain.pretrained import EncoderDecoderASR
from fastapi import FastAPI, File, UploadFile 
import os
from preprocess import MP32Wav, Video2Wav

app = FastAPI() #uvicorn main:app --reload (This runs starts a local instance of the API)

AUDIODIR = 'audios/' #Directory of audio uploads / extractions.

@app.get('/')
async def root():
    return {
        'ASR API': 'Active'
    }

@app.post(f'/transcribe')
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to the audios directory
        file_path = file.filename
        temp_filepath = file_path

        with open(file_path, 'wb') as file_output:
            file_output.write(file.file.read())

        file_name, file_extension = os.path.splitext(file_path)
        if file_extension == ".mp3":
            file_path = MP32Wav(file_path, "audios", f"{file_name}.wav")
        elif file_extension ==".mp4":
            file_path = Video2Wav(file_path, "audios", f"{file_name}.wav")
        else:
            return {"error": "Unsupported file type"}

        # Transcribe the audio using the ASR model
        asr_model = EncoderDecoderASR.from_hparams(
            source="speechbrain/asr-crdnn-rnnlm-librispeech",
            savedir="pretrained_models/asr-crdnn-rnnlm-librispeech",
        )
        transcripted_text = asr_model.transcribe_file(file_path)

        # Remove the temporary file
        os.remove(temp_filepath)
        os.remove(file_path)
        
        return {"Transcription": transcripted_text}

    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}