from django.shortcuts import render, redirect
import requests
import json


# Create your views here.

def search(request):
    if 'keyword' in request.GET:
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            response = requests.get(f'https://kitsu.io/api/edge/anime?filter[text]={keyword}')
            raw_data = json.loads(response.text)

            data = {
                'no_of_results': raw_data['meta'],
                'links': raw_data['links'],
                'data': raw_data['data']
            }

            return render(request, 'result/search.html', data)

    return redirect('home')


def detail(request, anime_id):
    response = requests.get(f'https://kitsu.io/api/edge/anime?filter[id]={anime_id}')
    raw_data = json.loads(response.text)
    episodes_responce = requests.get(f'https://kitsu.io/api/edge/anime/{anime_id}/episodes')
    raw_ep_data = json.loads(episodes_responce.text)

    data = {
        'data': raw_data['data'][0],
        'ep_data': raw_ep_data['data'],
    }
    return render(request, 'result/detail.html', data)
