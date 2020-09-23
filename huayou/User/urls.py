from django.urls import path

from User import apis

urlpatterns = [
    path('vcode/fetch/', apis.fetch_vcode),
    path('vcode/submit/', apis.submit_vcode),
    path('profile/show/', apis.show_profile),
    path('profile/update/', apis.update_profile),
]