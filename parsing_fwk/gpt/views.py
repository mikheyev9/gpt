import threading
import os

from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.utils import timezone


from .models import TablesSites, TablesEvent
from .rerating.data_structures import (
     make_structure_django, make_jsonl_with_texts_to_api,
     make_structure_to_write_in_db
)
from .rerating.parallel_requests import process_api_requests_from_file

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, 'rerating', 'files/')
#GPT/parsing_fwk/gpt/rerating/files/' #путь для записи файлов
path_log = os.path.join(current_dir, 'rerating', 'log', 'log.txt')
# GPT/parsing_fwk/gpt/rerating/log/log.txt' лог

def main(request):
    return render(request, 'main.html')

def site_selection(request):
    if request.method == "POST":
        site_from = request.POST.get('site_from')
        site_to = request.POST.get('site_to')

        events_from = TablesEvent.objects.filter(site_id=site_from,
                                                date__gte=timezone.now()).order_by('date').values('id',
                                                                                                'name',
                                                                                                'date',
                                                                                                'about')
        return render(request, 'events_selection.html', {'events_from': events_from,
                                                          'site_id_from': site_from,
                                                          'site_id_to': site_to})
    else:
        sites = TablesSites.objects.all().order_by('name')
        return render(request, 'site_selection.html', {'sites': sites})

def gpt_options(request):
    if request.method == 'POST':
        request.session['selected_events'] = request.POST.getlist('event')
        request.session['site_id_from'] = request.POST.get('site_id_from')
        request.session['site_id_to'] = request.POST.get('site_id_to')

        api_keys =['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',]
        proxies= ["http://mikheyev9:aXUbosImHR@185.155.233.1:50100",
                   "http://mikheyev90MuzM:i6DdTP6oDC@185.120.79.28:49155"]
        models = [
            'gpt-4',
            'gpt-4-turbo-preview',
            'gpt-4-vision-preview',
            'gpt-4-32k',
            'gpt-3.5-turbo-16k',
            'gpt-3.5-turbo',
            'gpt-3.5-turbo-instruct',
            'babbage-002',
            'davinci-002'
            ]
        return render(request, 'gpt_options.html', context={
                                'api_keys': api_keys,
                                'proxies': proxies,
                                'models': models,})
    else:
        return redirect('site_selection')

def process_selection(request):
    ''''''
    
    process_key = 'process_running'

    if request.method == "POST":
        if cache.get(process_key):
            # Перенаправляем на страницу с логами, если процесс уже запущен
            return redirect(main)
        else:
            cache.set(process_key, True)
        api_key = request.POST.get('api_key')
        proxy = request.POST.get('proxy')
        model = request.POST.get('model')
        content = request.POST.get('content')
        temperature = float(request.POST.get('temperature'))
        top_p = float(request.POST.get('top_p'))
        frequency_penalty = float(request.POST.get('frequency_penalty'))
        presence_penalty = float(request.POST.get('presence_penalty'))
        max_requests_per_minute = int(request.POST.get('max_requests_per_minute'))
        max_tokens_per_minute = int(request.POST.get('max_tokens_per_minute'))
        max_attempts = int(request.POST.get('max_attempts'))
        logging_level = int(request.POST.get('logging_level'))
        

        selected_events = request.session.get('selected_events')
        site_id_from = request.session.get('site_id_from')
        site_id_to = request.session.get('site_id_to')
        
        events = TablesEvent.objects.filter(id__in=selected_events, 
                                            site_id=site_id_from).select_related('site').values(
                                                        'id', 'name', 'about', 'genre', 'site__name')
        all_events, sitename = make_structure_django(events)

        if site_id_from != site_id_to:
            events_to_wtire = merge_to_sites_events(selected_events, site_id_from, site_id_to)#копируем выбранные ивенты
            events_to_wtire, sitename = make_structure_django(events_to_wtire)
        else:
            events_to_wtire = all_events

        make_jsonl_with_texts_to_api(events_to_wtire, path, sitename,
                                     model = model,content = content,
                                    temperature=temperature, top_p=top_p, 
                                    frequency_penalty=frequency_penalty,
                                    presence_penalty=presence_penalty)
        def run_async_process():
            try:
                async_to_sync(process_async_tasks)(path, path_log, sitename,
                                                api_key=api_key,
                                max_requests_per_minute=max_requests_per_minute,
                                max_tokens_per_minute=max_tokens_per_minute,
                                max_attempts=max_attempts,
                                logging_level=logging_level,
                                proxy=proxy)
            except Exception as ex:
                print(ex, 'exception')
            finally:
                box, error_title = make_structure_to_write_in_db(events_to_wtire, path, sitename)
                event_ids = [event_id for event_id, _ in box]
                events_to_update = list(TablesEvent.objects.filter(id__in=event_ids, site_id=site_id_to))
                new_about_dict = dict(box)
                for event in events_to_update:
                    event.about = new_about_dict.get(event.id, event.about)
                TablesEvent.objects.bulk_update(events_to_update, ['about'])
                print('DB write success')
                # Удаляем флаг из кэша после завершения процесса
                cache.delete(process_key)

               
        threading.Thread(target=run_async_process).start()
        #clear save_filepath
        with open(path_log, "w", encoding='utf-8') as f:
            pass
            
        return render(request, 'confirmation.html', {'events_len': len(events_to_wtire)})


def get_log_data(request):
    with open(path_log, 'r') as file:
        log_data = file.read()
    
    return JsonResponse({'data': log_data})

#вспомогательный функции
async def process_async_tasks(path, path_log, sitename, 
                              api_key='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',
                              max_requests_per_minute=2,
                              max_tokens_per_minute=20000,
                              max_attempts=3,
                              logging_level=10,
                              proxy="http://bG6oa7:2KMzZM@163.198.212.98:8000"):
    await process_api_requests_from_file(
        requests_filepath=f'{path}{sitename}_db.jsonl',
        save_filepath=f'{path}{sitename}_gpt.jsonl',
        request_url='https://api.openai.com/v1/chat/completions',
        api_key=api_key,
        max_requests_per_minute=max_requests_per_minute,
        max_tokens_per_minute=max_tokens_per_minute,
        token_encoding_name='cl100k_base',
        max_attempts=max_attempts,
        logging_level=logging_level,
        proxy=proxy,
        path_to_log=path_log #
    )

def merge_to_sites_events(selected_events, site_id_from, site_id_to):
    '''Создаем копии всех ивентов с site_id_from на site_id_to
    и возвращаем массив созданных ивентов'''

    events_first_site = TablesEvent.objects.filter(id__in=selected_events, 
                                             site_id=site_id_from)
    selected_names  = [event.name for event in events_first_site]

    new_events_for_second_site = []
    for event in events_first_site:
        # Проверяем, существует ли событие с таким же именем и датой на втором сайте
        exists_on_second_site = TablesEvent.objects.filter(
            site_id=site_id_to, name=event.name, date=event.date
        ).exists()
        # Если события нет на втором сайте, создаём его копию
        if not exists_on_second_site:
            new_event = TablesEvent(
                # Копируем все необходимые поля
                name=event.name,
                team1_name=event.team1_name,
                team2_name=event.team2_name,
                place=event.place,
                first_image=event.first_image,
                second_image=event.second_image,
                about=event.about,
                header_image=event.header_image,
                top_event=event.top_event,
                margin=event.margin,
                scheme=event.scheme,
                age=event.age,
                date=event.date,
                genre=event.genre,
                image=event.image,
                scene=event.scene,
                site_id=site_id_to,  # Устанавливаем ID второго сайта
                slug=event.slug,
                parsed_url=event.parsed_url,
                fan_id=event.fan_id,
                hidden=event.hidden,
                decrement=event.decrement
            )
            new_events_for_second_site.append(new_event)
    # Сохраняем все новые события для второго сайта
    TablesEvent.objects.bulk_create(new_events_for_second_site)
    # Получаем и возвращаем список всех событий со второго сайта
    return TablesEvent.objects.filter(
            name__in=selected_names, 
            site_id=site_id_to).select_related('site').values(
                        'id', 'name', 'about', 'genre', 'site__name')
