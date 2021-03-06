'''程序逻辑配置，及第三方平台配置'''

# Redis 配置
REDIS = {
    'host': '49.235.252.5',
    'port': 6379,
    'db': 2
}

# 滑动积分
SWIPE_SCORE = {
    'like': 5,
    'dislike': -5,
    'superlike': 7
}

# 榜单配置
RANK_NUM = 50

#  塞迪云通信设置
SD_APPID = '54728'
SD_APPKEY = '5473664699497c9be234d615b1f0286b'
SD_PROJECT = 'WwxHr1'
SD_SIGN_TYPE = 'md5'
SD_API = 'https://api.mysubmail.com/message/xsend.json'

#  七牛云配置
QN_DOMAIN = 'qh61eh0uk.hd-bkt.clouddn.com'
QN_BUCKET = 'dback'
QN_ACCESS_LEY = 'UYNX_8zKOZkJAPWOUAev--KLfiJKtisS__wfuIxP'
QN_SECRET_KEY = 'tKSagqakwv80DiTbd261klBKgPnMHFyAGG0a14fA'
QN_CALLBACK_URL = 'http://49.235.252.5/qiniu/callback'
QN_CALLBACK_DOMAIN = '49.235.252.5'

#  反悔功能相关配置
REWIND_TIMES = 3  # 当日最大反悔次数
REWIND_TIMEOUT = 5 * 60  # 反悔超时时间 秒
