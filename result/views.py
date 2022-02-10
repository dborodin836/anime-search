from django.shortcuts import render, redirect
import requests
import json
from .paginator.paginator import Paginator


# Create your views here.

def search(request):
    if 'keyword' in request.GET:
        if request.GET['keyword']:
            if 'page' in request.GET:
                current_page = int(request.GET['page'])
                keyword = request.GET['keyword']
                page_offset = current_page * 10

                response = requests.get(
                    f'https://kitsu.io/api/edge/anime?filter[text]={keyword}&page[offset]={page_offset}')
                raw_data = json.loads(response.text)
                results = raw_data['meta']['count']  # Amount of the found results

                paginator = Paginator(current_page, results, limit=10)

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
