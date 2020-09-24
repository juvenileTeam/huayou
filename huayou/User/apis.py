from django.core.cache import cache
from django.http import JsonResponse

from User.forms import UserForm, ProfileForm
from User.logic import send_code
from User.models import User, Profile
from django.views.decorators.csrf import csrf_exempt




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
            'code': 0,
            'data': user.to_dict()
        })
    else:
        return JsonResponse({
            'code': 1001,
            'data': '验证码错误'
        })


def show_profile(request):
    '''获取配置信息'''
    uid = request.session.get('uid')
    profile, _ = Profile.objects.get_or_create(id=uid)
    return JsonResponse({'code': 0, 'data': profile.to_dict()})


@csrf_exempt
def update_profile(request):
    '''修改个人资料以及交友资料'''
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session.get('uid')
        User.objects.filter(id=uid).update(**user_form)
        User.objects.filter(id=uid).update_or_create(profile_form)
        return JsonResponse({
            'code': 0,
            'data': '修改成功'
        })
    else:
        return JsonResponse({'code': 1003,'data': '用户资料表单数据错误'})