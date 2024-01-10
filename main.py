import torchaudio
import speechbrain as sb
from speechbrain.pretrained import EncoderDecoderASR
from fastapi import FastAPI, File, UploadFile 
import os
import time

app = FastAPI() #uvicorn main:app --reload (This runs starts a local instance of the API)

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

        with open(file_path, 'wb') as file_output:
            file_output.write(file.file.read())

        # Transcribe the audio using the ASR model
        asr_model = EncoderDecoderASR.from_hparams(
            source="speechbrain/asr-crdnn-rnnlm-librispeech",
            savedir="pretrained_models/asr-crdnn-rnnlm-librispeech",
        )
        transcription = asr_model.transcribe_file(file_path)

        return {"Transcription": transcription}

    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}