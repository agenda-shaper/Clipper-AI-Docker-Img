import os
import subprocess
import random
import requests
from faster_whisper import WhisperModel


def transcribe_whisper(model, audio_file_path) -> list:
    segments, info = model.transcribe(
        audio_file_path, word_timestamps=True, vad_filter=True
    )

    subtitles = []
    for segment in segments:
        for word in segment.words:
            start_time = word.start
            end_time = word.end
            subtitle = word.word
            subtitle_dict = {
                "start_time": start_time,
                "end_time": end_time,
                "text": subtitle,
            }
            subtitles.append(subtitle_dict)

    return subtitles


def send_webhook_error(message):
    # send payload to webhook
    webhook_url = "https://discord.com/api/webhooks/1107384471495397416/nIf_g-biCs7AFOtkH4lyptuqDo-uDJrYhE_WCdF2Qm9QCJ5EVnVf5fzxWLoIScmUsPlq"

    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {"content": message}

    result = requests.post(webhook_url, json=data)


def download_yt_audio(url, start_time, end_time, audio_file):
    if os.path.exists(audio_file):
        os.remove(audio_file)

    start_time_parts = str(start_time).split(":")
    end_time_parts = str(end_time).split(":")

    start_seconds = (
        (int(start_time_parts[0]) * 3600)
        + (int(start_time_parts[1]) * 60)
        + int(start_time_parts[2])
    )
    end_seconds = (
        (int(end_time_parts[0]) * 3600)
        + (int(end_time_parts[1]) * 60)
        + int(end_time_parts[2])
    )

    audio_cmd = f'yt-dlp -f "bestaudio[ext=m4a]" --get-url "{url}"'
    audio_url = subprocess.check_output(audio_cmd, shell=True).decode().strip()

    duration = end_seconds - start_seconds

    audio_ffmpeg_cmd = f'ffmpeg -ss {start_seconds} -i "{audio_url}" -t {duration} -vn -c:a copy {audio_file}'
    subprocess.call(audio_ffmpeg_cmd, shell=True)  # download audio


# Inference is ran for every server call
# Reference your preloaded global model variable here.
def generate(whisper_model, model_inputs) -> dict:
    print("kk")
    try:
        print("try")
        # Access URL from model_inputs dictionary
        url = model_inputs["url"]

        # Access start time from model_inputs dictionary
        start_time = model_inputs["start_time"]

        # Access end time from model_inputs dictionary
        end_time = model_inputs["end_time"]
        print("lol")
        audio_file = f"input{random.randint(1000, 9999)}.m4a"
        print(audio_file)
        download_yt_audio(url, start_time, end_time, audio_file)
        print(audio_file)
        output = transcribe_whisper(whisper_model, audio_file)
        print(output)
        return output

    except Exception as e:
        message = f"Error:\n```\n{e}```"
        send_webhook_error(message)
        return e
