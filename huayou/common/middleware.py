from django.utils.deprecation import MiddlewareMixin
from common import errors

from libs.http import render_json


class AuthMiddleware(MiddlewareMixin):
    '''登录验证中间件'''
    white_list = [
        '/',
        '/api/user/vcode/fetch',
        '/api/user/vcode/submit',
        '/qiniu/callback',
    ]

    def process_request(self, request):
        # 检查当前路径是否在白名单
        if request.path in self.white_list:
            return

        # 获取并检查 session 中的 uid
        uid = request.session.get('uid')
        if not uid:
            return render_json(data='用户未登录', code=errors.LoginRequired.code)
        else:
            request.uid = uid


class LogicErrMiddleware(MiddlewareMixin):
    '''逻辑异常处理中间件'''

    def process_exception(self, request, exception):
        if isinstance(exception, errors.LogicErr):
            return render_json(exception.data, exception.code)
