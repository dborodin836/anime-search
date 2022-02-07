from django.shortcuts import render, redirect
import requests
import json
from math import ceil


# Create your views here.

def search(request):
    if 'keyword' in request.GET:
        if request.GET['keyword']:

            if 'page' in request.GET:
                page = request.GET['page']
                page = int(page)
            else:
                page = 0

            page_offset = page * 10
            keyword = request.GET['keyword']
            response = requests.get(
                f'https://kitsu.io/api/edge/anime?filter[text]={keyword}&page[offset]={page_offset}')
            raw_data = json.loads(response.text)

            results = raw_data['meta']['count']
            last_page = ceil(results / 10) - 1

            current_last_page = page + 5
            if current_last_page > last_page:
                current_last_page = last_page
            pages_list = [x for x in range(1, page)]
            pages_list.extend([x + 1 for x in range(page, current_last_page)])

            paginator = {
                'has_other_pages': True if results > 10 else False,
                'current': page,
                'no_of_pages': [x + 1 for x in range(page, current_last_page)],  # Pages that are available
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
