import requests
import json

from django.shortcuts import render, redirect
from django.views.generic import RedirectView, TemplateView
from django.urls import reverse

from .paginator.paginator import Paginator


class SearchView(TemplateView):
    template_name = 'result/search.html'

    # Should probably rewrite this
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(request.GET['keyword'], request.GET['page'], **kwargs))

    def get_context_data(self, keyword, page, **kwargs):
        # keyword = self.kwargs['keyword']
        # page = self.kwargs['page']
        page = int(page)
        page_offset = page * 10

        response = requests.get(
            f'https://kitsu.io/api/edge/anime?filter[text]={keyword}&page[offset]={page_offset}')
        raw_data = json.loads(response.text)
        results = raw_data['meta']['count']  # Amount of the found results

        paginator = Paginator(page, results, limit=10)

        context = {
            'data': raw_data['data'],
            'paginator': paginator,
        }
        return context


class DetailView(TemplateView):
    template_name = 'result/detail.html'

    def get_context_data(self, **kwargs):
        anime_id = kwargs['anime_id']
        response = requests.get(f'https://kitsu.io/api/edge/anime?filter[id]={anime_id}')
        raw_data = json.loads(response.text)
        episodes_response = requests.get(f'https://kitsu.io/api/edge/anime/{anime_id}/episodes')
        raw_ep_data = json.loads(episodes_response.text)

        context = {
            'data': raw_data['data'][0],
            'ep_data': raw_ep_data['data'],
        }
        return context


class RandomAnimeRedirect(RedirectView):

    @staticmethod
    def __get_random_anime_id():
        """This thing works awfully slow. Gotta fix this ASAP."""
        response = requests.get('https://animechan.vercel.app/api/random')
        response_text = json.loads(response.text)
        anime_name = response_text['anime']
        response = requests.get(f'https://kitsu.io/api/edge/anime?filter[text]={anime_name}')
        anime_id = json.loads(response.text)['data'][0]['id']
        return anime_id

    def get_redirect_url(self, *args, **kwargs):
        anime_id = self.__class__.__get_random_anime_id()
        return f"{reverse('detail', args=[anime_id])}"
