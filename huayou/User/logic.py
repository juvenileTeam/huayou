import random
import re

from django.core.cache import cache
from libs.cache import rds
from common import keys
from libs.sms import send_msg


def is_phonenum(phonenum):
    '''判断是否是一个手机号'''
    if re.match(r'1[3-9]\d{9}$', phonenum):
        return True
    else:
        return False


def make_code(length=6):
    '''生成验证码'''
    codes = [str(random.randint(0, 9)) for i in range(length)]
    vcode = ''.join(codes)
    return vcode


def send_code(phonenum):
    '''给用户发送验证码'''
    if not is_phonenum(phonenum):
        return False
    key = keys.VCODE_K + str(f'{phonenum}')

    if rds.get(key):
        return True
    vcode = make_code()
    rds.set(key, vcode, 600)
    return send_msg(phonenum, vcode)
