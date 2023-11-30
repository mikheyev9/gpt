from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render
import threading
import os

from .models import TablesSites, TablesEvent
from .rerating.data_structures import (
     make_structure_django, make_jsonl_with_texts_to_api,
     make_structure_to_write_in_db
)
from .rerating.parallel_requests import process_api_requests_from_file

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, 'rerating', 'files')
path_log = os.path.join(current_dir, 'rerating', 'log', 'log.txt')
# path = '/home/anton/study/GPT/parsing_fwk/gpt/rerating/files/' #путь для записи файлов
# path_log ='/home/anton/study/GPT/parsing_fwk/gpt/rerating/log/log.txt' #лог

def main(request):
    return render(request, 'main.html')

def site_selection(request):
    if request.method == "POST":
        site_id = request.POST.get('site')
        events = TablesEvent.objects.filter(site_id=site_id).values('id', 'name')
        return render(request, 'events_selection.html', {'events': events, 'site_id': site_id})
    else:
        sites = TablesSites.objects.all().order_by('name')
        return render(request, 'site_selection.html', {'sites': sites})


def process_selection(request):
    if request.method == "POST":
        selected_events = request.POST.getlist('event')
        site_id = request.POST.get('site_id')
        events = TablesEvent.objects.filter(
            id__in=selected_events, 
            site_id=site_id).select_related('site').values(
                        'id', 'name', 'about', 'genre', 'site__name')
        all_events, sitename = make_structure_django(events)

        make_jsonl_with_texts_to_api(all_events, path, sitename)
        def run_async_process():
            async_to_sync(process_async_tasks)(path, path_log, sitename)
            box, error_title = make_structure_to_write_in_db(all_events, path, sitename)
            print(box)
            with transaction.atomic():
                try:
                    for event_id, new_about in box:
                        TablesEvent.objects.filter(id=event_id, site_id=site_id).update(about=new_about)
                    print('DB write success')
                except Exception as e:
                    raise e
        threading.Thread(target=run_async_process).start()
        #clear save_filepath
        with open(path_log, "w", encoding='utf-8') as f:
            pass
            
        return render(request, 'confirmation.html', {'events': events})


def get_log_data(request):
    with open(path_log, 'r') as file:
        log_data = file.read()
    
    return JsonResponse({'data': log_data})

#вспомогательный функции
async def process_async_tasks(path, path_log, sitename):
    await process_api_requests_from_file(
        requests_filepath=f'{path}{sitename}_db.jsonl',
        save_filepath=f'{path}{sitename}_gpt.jsonl',
        request_url='https://api.openai.com/v1/chat/completions',
        api_key='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',
        max_requests_per_minute=2,
        max_tokens_per_minute=20000,
        token_encoding_name='cl100k_base',
        max_attempts=3,
        logging_level=10,
        proxy="http://bG6oa7:2KMzZM@163.198.212.98:8000",
        path_to_log=path_log #
    )

async def async_process_selection(path, sitename):
    await process_async_tasks(path, sitename)
