# tasks.py
import pytube
from pytube.innertube import _default_clients
from pytube import cipher
from src.constant import VIDEOS_PATH
from src.utils.utils import extract_audio, transcribe, generate_subtitle_file, add_subtitle_to_video, get_throttling_function_name
from django_celery_project.celery import app
# config
_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

cipher.get_throttling_function_name = get_throttling_function_name

@app.task(queue='add_queue')
def add(a,b):
    print(a+b)
    result = a + b
    return {"title": "Phep cong", "result": result, "status": "completed"}

@app.task(queue='download_queue')
def download_video(url):
    yt = pytube.YouTube(url)
    yt_id = yt.video_id
    yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().download(output_path="media/videos", filename=yt_id)
    return {"VideoCode": yt_id, "VideoTitle": yt.title, "OriginVideoLink": url, "status": "completed"}
@app.task(queue='audio_queue')
def extract_audio_task(yt_id):
    audio_extract = extract_audio(yt_id)
    return audio_extract, yt_id


@app.task(queue='transcribe_queue')
def transcribe_task(args, dest='en'):
    audio_extract, yt_id = args
    language, segments,translated_text_list = transcribe(audio_extract, dest)
    serializable_segments = []
    for segment in segments:
        serializable_segments.append({
            'start': segment.start,
            'end': segment.end,
            'text': segment.text,
            'translated_text_list': translated_text_list
        })
    return language, serializable_segments, yt_id


@app.task(queue='generate_subtitle_queue')
def generate_subtitle_file_task(args):
    language, segments_data, yt_id = args
    subtitle_file = generate_subtitle_file(yt_id, language, segments_data)
    return subtitle_file, language, yt_id

@app.task(queue='add_subtitle_queue')
def add_subtitle_to_video_task(args):
    subtitle_file, language, yt_id = args
    add_subtitle_to_video(yt_id, subtitle_file, language)
    return f"""
        VideoCode: {yt_id},
        VideoTitle: Title here, 
        OriginVideoLink: https://www.youtube.com/watch?v={yt_id},  
        ResultVideoPath: https://www.youtube.com/watch?v={yt_id},  
        VideoContent: 
            timeLine: {subtitle_file}
        ,
        IsPublic: True,  
        username: Username  
    """

