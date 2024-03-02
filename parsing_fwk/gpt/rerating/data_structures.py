import json

def make_structure_django(queryset: list):
    '''Создаем структуру для удобного отображения ивентов,
    возвращаем эту структуру-box и sitename-доменное имя сайта
    '''

    sitename = queryset[0]['site__name'].replace('.', '_')
    box = {}
    for event in queryset:
        #event={'id': 19575,'name':'Салават Юлаев - Трактор','about':'Hello...', 'genre':'КХЛ', 'site__name': 'arena-ufa.ru'}
        if event['name'] in box:
            box[event['name']]['ids'].append(event['id'])
        else:
            box[event['name']] = {
                'text': event['about'],
                'ids': [event['id'],],
                'genre': event['genre'],
            }
    return box, sitename
    '''box = {
            'title': {
                    'text': 'В Москве...',
                    'ids': [8699, 14446, ...], #all ids with this title
                    'genre': 'Драма'
                    },
            }
        ''' 


def make_structure(records: list):
    sitename = records[0][4].replace('.', '_')
    box = {}
    for event in records:
        #event ilike list(int(id), str(title), str(text_about), str(genre))
        if event[1] in box:
            box[event[1]]['ids'].append(event[0])
        else:
            box[event[1]] = {
                'text': event[2],
                'ids': [event[0],],
                'genre': event[3],
            }
    return box, sitename
    ''' {
        'title': {
                'text': 'В Москве...',
                'ids': [8699, 14446, ...], #all ids with this title
                'genre': 'Драма'
                },
        }
    ''' 

def make_jsonl_with_texts_to_api(box: dict, path: str, sitename: str, 
                                 model = "gpt-3.5-turbo",content = "cделай рерайтинг текста" ,
                                temperature=1, top_p=1, frequency_penalty=0.5,
                                 presence_penalty=0.5 ):
    '''Создаем файл.Он нужен для parallel_requests.py, он читает из него построчно
    и отсылает запросы исходя из имеющихся данных в этом файле (path: str(путь к файлу))'''

    with open(f'{path}{sitename}_db.jsonl', 'w', encoding='utf-8') as file:
        for key, val in box.items():
            сontent_send = f"{content},Title:{key},Genre:{val['genre']}"
            x = {"id": key,
                "data": {
                    "model": model,
                    "messages": [
                            {"role": "system", "content": сontent_send},
                            {"role": "user", "content": val['text']}
                        ],
                    "temperature": temperature,
                    "top_p": top_p,
                    "frequency_penalty": frequency_penalty,
                    "presence_penalty": presence_penalty}
                }
            json.dump(x, file, ensure_ascii=False)
            file.write('\n')

def make_structure_to_write_in_db(box_from_db: dict, path: str, sitename: str):
    '''Структура для записи в базу данных
    вернем список [ (id, text_about),  (id, text_about),...]   '''

    with open(f'{path}{sitename}_gpt.jsonl', 'r') as file:
        box_from_gpt = {}
        for i in file:
            try:
                x = json.loads(i)
                title = x[0]
                answer = x[1]['choices'][0]['message']['content']
            except Exception as ex:
                print(ex)
            else:
                box_from_gpt[title] = answer

    box = [] # [ (id, text_about),  (id, text_about),...]   
    error_titles = [] # [ title, title, ...]        
    for title, text_about in box_from_gpt.items():
        if title in box_from_db:
            for id in box_from_db[title]['ids']:
                box.append((id, text_about))
        else:
            error_titles.append(title)
    return box, error_titles