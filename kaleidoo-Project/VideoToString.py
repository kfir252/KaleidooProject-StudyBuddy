import subprocess
import os
from PIL import Image
import torch
from torchvision.models import resnet50
from transformers import BlipProcessor, BlipForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
import hashlib
from pathlib import Path

warnings.filterwarnings("ignore", category=UserWarning, module="torchvision")
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

class VideoHandler:
    @staticmethod
    def get_file_name_without_suffix(file_path):
        return Path(file_path).stem

    @staticmethod
    def get_file_hash(file_path, hash_algo='sha256'):
        hash = hashlib.new(hash_algo)
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash.update(chunk)
        return hash.hexdigest()

    @staticmethod
    def pick_evenly_spaced_elements(lst, max_size=100):
        size = len(lst)
        if size <= max_size:
            return lst
        step = size // max_size
        selected_elements = lst[::step]
        return selected_elements[:max_size]

    @staticmethod
    def extract_frames_ffmpeg(video_path, output_directory, frame_rate=1, width=224, height=224):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            return
        command = [
            'ffmpeg',
            '-loglevel', 'quiet',
            '-i', video_path,
            '-vf', f'fps={frame_rate},scale={width}:{height}',
            f'{output_directory}/frame_%04d.png'
        ]
        process = subprocess.run(command)
        if process.returncode != 0:
            os.removedirs(output_directory)
            raise RuntimeError("Frame extraction failed.")

    @staticmethod
    def generate_description_for_frame(frame_file, blip_model, blip_processor, pu):
        image = Image.open(frame_file).convert('RGB')
        inputs = blip_processor(image, return_tensors="pt").to(pu)
        description = blip_model.generate(**inputs, max_new_tokens=20)
        return blip_processor.decode(description[0], skip_special_tokens=True)

    @staticmethod
    def generate_description_for_frames(frames_directory, description_directory, max_workers=4):
        file = 'desc.txt'
        if not os.path.exists(description_directory):
            os.makedirs(description_directory)
        elif os.path.exists(description_directory + "\\" + file):
            return VideoHandler.read_text(description_directory, file)
        model = resnet50(pretrained=True)
        model = torch.nn.Sequential(*list(model.children())[:-1])
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        pu = "cuda" if (torch.cuda.is_available()) else "cpu"
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(pu) 
        frame_files = sorted([os.path.join(frames_directory, f) for f in os.listdir(frames_directory) if f.endswith('.png')])
        frame_files = VideoHandler.pick_evenly_spaced_elements(frame_files, 100)
        descriptions = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(VideoHandler.generate_description_for_frame, frame_file, blip_model, blip_processor, pu): frame_file for frame_file in frame_files}
            for future in as_completed(futures):
                try:
                    descriptions.append(future.result())
                except Exception as e:
                    print(f"Error processing {futures[future]}: {e}")
        return ". ".join(descriptions)

    @staticmethod
    def extract_audio(video_file, output_directory, output_file):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            return
        command = [
            'ffmpeg',
            '-loglevel', 'quiet',
            '-y',
            '-i', video_file,
            '-vn',
            '-acodec','pcm_s16le',
            '-ar', '44100',
            '-ac', '2',
            output_directory + "\\" + output_file + ".wav"
        ]
        process = subprocess.run(command)
        if process.returncode != 0:
            os.removedirs(output_directory)
            raise RuntimeError("Audio extraction failed.")

    @staticmethod
    def write_text(text, directory, file):
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, file)
        with open(file_path, 'w') as file:
            file.write(text)

    @staticmethod
    def read_text(directory, file):
        file_path = os.path.join(directory, file)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as file:
            content = file.read()
        return content


def video_to_string(video_path):
    hash = VideoHandler.get_file_hash(video_path)
    video_directory = f'temp\\{hash}'
    audio_directory = f'{video_directory}\\vid_audio'
    base_file = VideoHandler.get_file_name_without_suffix(video_path);
    frames_directory = f'{video_directory}\\vid_frames'
    description_directory = f'{video_directory}\\vid_desc'
    VideoHandler.extract_audio(video_path, audio_directory, base_file)
    VideoHandler.extract_frames_ffmpeg(video_path, frames_directory, frame_rate=1, width=224, height=224)
    captions = VideoHandler.generate_description_for_frames(frames_directory, description_directory)
    VideoHandler.write_text(captions, description_directory, 'desc.txt')
    return (captions, audio_directory + "\\" + base_file + ".wav")


if __name__ == "__main__":
    print(video_to_string("C:\\Users\\Elad\\Downloads\\x.mp4"))
