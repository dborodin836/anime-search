from django.shortcuts import render, redirect
import requests
import json
from math import ceil


# Create your views here.

def search(request):
    if 'keyword' in request.GET:
        if request.GET['keyword']:

            if 'page' in request.GET:
                current_page = request.GET['page']
                current_page = int(current_page)
            else:
                current_page = 0

            # If user sends request with negative page number
            # I shouldn't do it, this bug can be fixed in JS
            if current_page < 0:
                current_page = 0
            
            # Compensate that loops starts from 0
            current_page -= 1
            
            # Request vars
            page_offset = current_page * 10
            keyword = request.GET['keyword']
            
            response = requests.get(
                f'https://kitsu.io/api/edge/anime?filter[text]={keyword}&page[offset]={page_offset}')
            
            raw_data = json.loads(response.text)
            
            results = raw_data['meta']['count']  # Amount of the found results
            last_page = ceil(results / 10) - 1
            
            # Last clickable page
            current_last_page = current_page + 5
            if current_last_page > last_page:
                current_last_page = last_page

            #  Depends which page is current
            if current_page > 5:
                current_first_page = current_page - 5
            else:
                current_first_page = 1
            
            # Generates list of possible links to pages
            pages_list = [x for x in range(current_first_page + 2 if current_first_page > 3 else current_first_page, current_page + 1)]
            pages_list.extend([x + 1 for x in range(current_page, current_last_page)])

            paginator = {
                'has_other_pages': True if results > 10 else False,
                'current': current_page + 1,
                'pages_list': pages_list,
                'last': last_page,
            }

            data = {
                'data': raw_data['data'],
                'paginator': paginator,
            }

            return render(request, 'result/search.html', data)

    return redirect('home')


def detail(request, anime_id):
    response = requests.get(f'https://kitsu.io/api/edge/anime?filter[id]={anime_id}')
    raw_data = json.loads(response.text)
    episodes_response = requests.get(f'https://kitsu.io/api/edge/anime/{anime_id}/episodes')
    raw_ep_data = json.loads(episodes_response.text)

    data = {
        'data': raw_data['data'][0],
        'ep_data': raw_ep_data['data'],
    }
    return render(request, 'result/detail.html', data)


def random(request):
    response = requests.get('https://animechan.vercel.app/api/random')
    raw_data = json.loads(response.text)
    anime_name = raw_data['anime']
    response = requests.get(f'https://kitsu.io/api/edge/anime?filter[text]={anime_name}')
    anime_id = json.loads(response.text)['data'][0]['id']
    return redirect('detail', anime_id)
