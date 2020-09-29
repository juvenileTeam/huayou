from django.views.decorators.csrf import csrf_exempt

from Social import logics
from Social.models import Friend
from User.models import User
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


@csrf_exempt
def rewind(request):
    '''反悔'''
    logics.rewind_last_swiped(request.uid)
    return render_json()


def show_fans(request):
    '''查看喜欢我的人'''
    fans = logics.find__my_fans(request.uid)
    fans = [fan.to_dict() for fan in fans]
    return render_json(fans)


def show_friends(request):
    '''查看我的好友'''
    friend_id_list = Friend.find_ids(request.uid)
    friends = User.objects.filter(id__in=friend_id_list)
    friends_list = [friend.to_dict() for friend in friends]
    return render_json(friends_list)
