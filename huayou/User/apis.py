from django.core.cache import cache
from django.http import JsonResponse


# Create your views here.
from User.logic import send_code
from User.models import User
from django.views.decorators.csrf import csrf_exempt

from libs.sms import send_msg


def fetch_vcode(request):
    '''提交手机号'''
    phonenum = request.GET.get('phonenum')
    if send_code(phonenum):
        return JsonResponse({
            'code': 0,
            'data': '验证码已发送'
        })
    else:
        return JsonResponse({
            'code': 1000,
            'data': '验证码发送失败'
        })


@csrf_exempt
def submit_vcode(request):
    '''提交验证码登录'''
    phonenum = request.POST.get('phonenum')
    u_vcode = request.POST.get('vcode')
    key = f'Vcode-{phonenum}'
    vcode = cache.get(key)
    if vcode and vcode == u_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User()
            user.phonenum = phonenum
            user.nickname = phonenum
            user.save()
        request.session['uid'] = user.id
        return JsonResponse({
            'code':0,
            'data':user.to_dict()
        })
    else:
        return JsonResponse({
            'code':1001,
            'data':'验证码错误'
        })


#  获取配置信息
# def show_profile(request):
#     user_id = request.session.get('uid')
#     if user_id:
#         make_friends_info = MakeFriends.objects.filter(user_id=user_id)[0]
#         if make_friends_info.vibration:
#             vibration = True
#         else:
#             vibration = False
#         if make_friends_info.only_matched:
#             only_matched = True
#         else:
#             only_matched = False
#         if make_friends_info.auto_play:
#             auto_play = True
#         else:
#             auto_play = False
#         data = {
#             'code': 0,
#             'data': {
#                 "dating_gender": make_friends_info.dating_gender,
#                 "dating_location": make_friends_info.dating_location,
#                 "max_distance": make_friends_info.max_distance,
#                 "min_distance": make_friends_info.min_distance,
#                 "max_dating_age": make_friends_info.max_dating_age,
#                 "min_dating_age": make_friends_info.min_dating_age,
#                 "vibration": vibration,
#                 "only_matched": only_matched,
#                 "auto_play": auto_play
#             }
#         }
#
#         return JsonResponse(data=data)
#     else:
#         data = {
#             'code': 1002,
#             'data': None
#         }
#         return JsonResponse(data=data)
#
#
# #  修改资料
# def update_profile(request):
#     uid = request.session.get('uid')
#     if uid:
#         user = User.objects.get(pk=uid)
#         nickname = request.POST.get('nickname')
#         birthday = request.POST.get('birthday')
#         gender = request.POST.get('gender')
#
#         if gender == "male":
#             gender = True
#         elif gender == 'female':
#             gender = False
#         else:
#             data = {
#                 'code': 1003,
#                 'data': None
#             }
#             return JsonResponse(data=data)
#
#         location = request.POST.get('location')
#         dating_gender = request.POST.get('dating_gender')
#         dating_location = request.POST.get('dating_location')
#         max_distance = request.POST.get('max_distance')
#         min_distance = request.POST.get('min_distance')
#         max_dating_age = request.POST.get('max_dating_age')
#         min_dating_age = request.POST.get('min_dating_age')
#
#         vibration = request.POST.get('vibration')
#         if vibration == 'true':
#             vibration = True
#         else:
#             vibration = False
#         only_matched = request.POST.get('only_matched')
#         if only_matched == 'true':
#             only_matched = True
#         else:
#             only_matched = False
#
#         auto_play = request.POST.get('auto_play')
#         if auto_play == 'true':
#             auto_play = True
#         else:
#             auto_play = False
#
#         user.nickname = nickname
#         user.birthday = birthday
#         user.gender = gender
#         user.location = location
#         user.makefriends_set.dating_gender = dating_gender
#         user.makefriends_set.dating_location = dating_location
#         # max_distance
#         # min_distance
#         # max_dating_age
#         # min_dating_age
#         # vibration
#         # only_matched
#         # auto_play
#
#     return JsonResponse(data=data)
