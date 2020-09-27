import json
import time
from hashlib import md5

import requests

from huayou import config


def send_msg(phonenum, vcode):
    '''  发送短信  '''

    args = {
        'appid': config.SD_APPID,
        'to': phonenum,
        'project': config.SD_PROJECT,
        'vars': json.dumps({'vcode': vcode}),
        'timestamp': int(time.time()),
        'sign_type': 'md5',
    }

    # 计算参数的签名
    sorted_args = sorted(args.items())
    args_str = '&'.join([f'{key}={value}' for key, value in sorted_args])
    sign_str = f'{config.SD_APPID}{config.SD_APPKEY}{args_str}{config.SD_APPID}{config.SD_APPKEY}'.encode('utf8')
    signature = md5(sign_str).hexdigest()
    args['signature'] = signature

    response = requests.post(config.SD_API, data=args)
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            return True
    return False
