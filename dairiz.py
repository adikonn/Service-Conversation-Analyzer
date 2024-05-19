from io import BytesIO

from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment
import torch
from uuid import uuid1
from whx import speech_to_text
import os
from dotenv import load_dotenv

load_dotenv()

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1", use_auth_token=os.getenv("HF_token")
)
pipeline.to(torch.device("cuda"))

pipeline(r"C:\Users\murka\Desktop\train_RZHD_AnalizatorPeregovorov\24к_875 КВ - 02.05.2024 01_41_25.mp3")

def seconds_to_mins(seconds):
    secs = int(seconds)
    return f"{secs // 60}:{secs % 60}"


def get_diar(file):
    with ProgressHook() as hook:
        diarization = pipeline(file, hook=hook)
    audio_file = AudioSegment.from_mp3(file)
    for i, (turn, _, speaker) in enumerate(diarization.itertracks(yield_label=True), 1):
        filename = f"music/{uuid1()}.wav"
        segment = audio_file[turn.start * 1000 : turn.end * 1000]
        segment.export(filename, format="wav")
        yield f"\n{i}. {seconds_to_mins(turn.start)} - {seconds_to_mins(turn.end)} {speech_to_text(filename)[0]}"
