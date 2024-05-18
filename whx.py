import whisperx
import gc

device = "cuda"
batch_size = 16  # reduce if low on GPU mem
compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model(
    "large-v3", device, compute_type=compute_type, language="ru"
)


def speech_to_text(file):
    audio = whisperx.load_audio(file)
    result = model.transcribe(audio, batch_size=batch_size)
    print(result)
    text = [result["segments"][i]["text"] for i in range(len(result["segments"]))]
    return text
