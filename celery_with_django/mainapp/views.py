from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from tasks import download_video,extract_audio_task,transcribe_task,generate_subtitle_file_task,add_subtitle_to_video_task
from django.views.decorators.csrf import csrf_exempt
from celery import chain
from src.constant import *

import os
os.makedirs(AUDIOS_PATH, exist_ok=True)
os.makedirs(VIDEOS_PATH, exist_ok=True)
os.makedirs(SUBTITLES, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

@csrf_exempt
@api_view(["POST"])
def download_video_via_url(request):
    if request.method == "POST":
        url = request.data.get("url")
        task = download_video.delay(url)
        print(url)
        return JsonResponse({"message": "Video download task added to the queue", "task_id": task.id})
@csrf_exempt
@api_view(["POST"])
def generate_subtitle(request):
    if request.method == "POST":
        yt_id = request.data.get("yt_id")
        # yt_id = "hPdLgWlA_FU"
        dest = request.data.get("dest")
        print(yt_id,dest)
        task_chain = chain(
            extract_audio_task.s(yt_id),
            transcribe_task.s(dest),
            generate_subtitle_file_task.s(),
            add_subtitle_to_video_task.s()
        )
    result = task_chain.delay()

    return JsonResponse({"message": "Subtitle task added to the queue", "task_id": result.id})
# def task_status(task_id: str):
#     # Kiểm tra trạng thái tác vụ
#     task_result = AsyncResult(task_id)
#     return {"status": task_result.status, "result": task_result.result}
