from django.views.decorators.csrf import csrf_exempt

from Social import logics
from libs.http import render_json


def rcmd_users(request):
    '''获取推荐用户'''
    users = logics.rcmd(request.uid)
    user_data = [user.to_dict() for user in users]
    return render_json(user_data)


@csrf_exempt
def like(request):
    '''喜欢(右滑)'''
    sid = request.POST.get('sid')
    is_matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched':is_matched})


@csrf_exempt
def superlike(request):
    '''超级喜欢(上滑)'''
    sid = request.POST.get('sid')
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


@csrf_exempt
def dislike(request):
    '''不喜欢(左滑)'''
    sid = request.POST.get('sid')
    logics.dislike_someone(request.uid, sid)
    return render_json()


def rewind(request):
    '''反悔'''
    return render_json()


def show_fans(request):
    '''查看喜欢我的人'''
    return render_json()


def show_friends(request):
    '''查看我的好友'''
    return render_json()
