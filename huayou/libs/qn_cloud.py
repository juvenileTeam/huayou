import json
import time

from qiniu import Auth

from huayou import config as cfg


def get_res_url(filename):
    '''获取资源的URL'''
    return f'http://{cfg.QN_DOMAIN}/{filename}'


def gen_token(uid, filename):
    policy = {
        'scope': cfg.QN_BUCKET,
        'deadline': int(time.time() + 600),
        'returnBody': json.dumps({'code': 0, 'data': get_res_url(filename)}),
        'callbackUrl': cfg.QN_CALLBACK_URL,
        'callbackHost': cfg.QN_CALLBACK_DOMAIN,
        'callbackBody': f'key={filename}&uid={uid}',
        'saveKey': filename,
        'forceSaveKey': True,
        'fsizeLimit': 10485760,
        'mimeLimit': 'image/*',
    }
    qn_auth = Auth(cfg.QN_ACCESS_LEY, cfg.QN_SECRET_KEY)

    token = qn_auth.upload_token(cfg.QN_BUCKET, filename, 600, policy)
    return token
