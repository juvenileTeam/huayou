'''缓存中出现的所有 key'''

VCODE_K = 'Vcode-'  # 验证码缓存，拼接用户的手机号
FIRST_RCMD_Q = 'FirstRcmdQ-'  # 优先推荐队列，拼接用户uid
REWIND_TIMES_K = 'RewindTime-'  # 反悔次数的k,拼接当前日期 和 - 和 uid
