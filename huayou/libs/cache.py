import pickle

from redis import Redis as _Redis
from huayou.config import REDIS


class Redis(_Redis):
    def set(self, name, value,
            ex=None, px=None, nx=False, xx=False, keepttl=False):
        '''带序列化处理的 set 方法'''
        pickled_data = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        return super().set(name, pickled_data, ex, px, nx, xx, keepttl)

    def get(self, name, default=None):
        pickled_data = super().get(name)

        if pickled_data is None:
            return default
        try:
            value = pickle.loads(pickled_data)
            return value
        except (KeyError, EOFError, pickle.UnpicklingError):
            return pickled_data


rds = Redis(**REDIS)
