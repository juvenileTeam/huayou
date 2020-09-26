from User.forms import UserForm, ProfileForm
from User.logic import send_code
from User.models import User, Profile
from django.views.decorators.csrf import csrf_exempt

from common import errors, keys
from libs.cache import rds
from libs.http import render_json
from libs.qn_cloud import gen_token, get_res_url


def fetch_vcode(request):
    '''提交手机号'''
    phonenum = request.GET.get('phonenum')
    if send_code(phonenum):
        return render_json()
    else:
        return render_json(data='验证码发送失败', code=errors.VCODE_FAILD, )


@csrf_exempt
def submit_vcode(request):
    '''提交验证码登录'''
    phonenum = request.POST.get('phonenum')
    u_vcode = request.POST.get('vcode')
    key = keys.VCODE_K + str(f'{phonenum}')
    vcode = rds.get(key)
    if vcode and vcode == u_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User()
            user.phonenum = phonenum
            user.nickname = phonenum
            user.save()
        request.session['uid'] = user.id
        return render_json()
    else:
        return render_json(data='验证码错误', code=errors.VCODE_ERR)


def show_profile(request):
    '''获取配置信息'''
    uid = request.session.get('uid')
    profile, _ = Profile.objects.get_or_create(id=uid)
    return render_json(data=profile.to_dict())


@csrf_exempt
def update_profile(request):
    '''修改个人资料以及交友资料'''
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session.get('uid')
        User.objects.filter(id=uid).update(**user_form.cleaned_data)
        Profile.objects.update_or_create(id=uid, defaults=profile_form.cleaned_data)
        return render_json()
    else:
        return render_json(data={'usererr': user_form.errors,
                                 'profile': profile_form.errors},
                           code=errors.PROGILE_ERR,
                           )


def qn_token(request):
    '''获取七牛云 token'''
    uid = request.session.get('uid')
    filename = f'Avatar-{uid}'
    token = gen_token(uid, filename)

    return render_json(data={'token': token, 'key': filename})


@csrf_exempt
def qn_callback(request):
    '''七牛云回调接口'''
    uid = request.POST.get('uid')
    key = request.POST.get('key')
    avatar_url = get_res_url(key)
    User.objects.filter(id=uid).update(avatar=avatar_url)
    return render_json(data=avatar_url)
