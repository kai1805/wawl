from django.urls import path

from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('statistics', views.statistic, name='statistic'),
#     path('about-us', views.about_us, name='about_us'),
#     path('crawl_submit', views.crawl_submit, name='crawl_submit'),
#     path('<int:question_id>', views.get_with_param,'get_with_param'),
# ]
urlpatterns = [
    path('', views.index),
    path('statistics', views.statistic),
    path('about-us', views.about_us),
    path('crawl', views.crawl_render),
    path('crawl_submit', views.crawl_submit),
    path('<int:question_id>', views.get_with_param)
]