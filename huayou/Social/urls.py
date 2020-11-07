from django.urls import path

from Social import apis

urlpatterns = [
    path('rcmd', apis.rcmd_users),
    path('like', apis.like),
    path('superlike', apis.superlike),
    path('dislike', apis.dislike),
    path('rewind', apis.rewind),
    path('fans', apis.show_fans),
    path('friends', apis.show_friends),
    path('rank', apis.hot_rank),
]