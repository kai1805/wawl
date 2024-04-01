from re import template
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .crawler import *

def index(request):
    template = loader.get_template('crawl/index.html')
    print(request)
    return HttpResponse(template.render())

def crawl_render(request, urls):
    print(urls)
    link_urls, file_urls = urls
    context = {'link_urls': link_urls, 'file_urls': file_urls}
    return render(request, 'crawl/index.html', context=context)


@csrf_exempt 
def crawl_submit(request):
    if request.method == "POST":
        print(request.POST)
        url = request.POST['url-name']
        duration = int(request.POST['duration']) * 60 - 10
        urls, file_urls = crawl(url, duration=duration)
        # context = {'urls': urls}
        print("Crawl Done!")
        print(urls)
        return crawl_render(request, urls=(urls, file_urls))
    return redirect('/')

def statistic(request):
    template = loader.get_template('crawl/statistics.html')
    return HttpResponse(template.render())

def about_us(request):
    template = loader.get_template('crawl/about.html')
    return HttpResponse(template.render())

def get_with_param(request, question_id):
    return HttpResponse(question_id)