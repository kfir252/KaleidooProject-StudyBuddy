import whisper
import torch

# Check if CUDA is available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)

def SoundToString(path):
    file_name = path.split('\\')[-1]
    if 'א' <= file_name[0] <= 'ת':
        result = model.transcribe(path, language='he', word_timestamps=True)
    elif 'a' <= file_name[0].lower() <= 'z':
        result = model.transcribe(path, language='en', word_timestamps=True)
    else:
        result = model.transcribe(path, language='ar', word_timestamps=True)

    # Access the segments (each segment is like a sentence or a continuous block of speech)
    segments = result['segments']

    # Combine segments into paragraphs, using a threshold for time gaps
    paragraphs = []
    current_paragraph = ""
    gap_threshold = 3  # seconds (this is the time gap used to split paragraphs)

    for i, segment in enumerate(segments):
        current_paragraph += segment['text'].lower() + " "

        # Check if the gap between this segment and the next is larger than the threshold
        if i < len(segments) - 1:
            current_end_time = segment['end']
            next_start_time = segments[i + 1]['start']

            if next_start_time - current_end_time > gap_threshold:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = ""

    # Add any remaining paragraph
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())

    # Return the paragraphs
    return paragraphs
