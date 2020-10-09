import datetime

from django.db.models import query
from django.db import models

from common.keys import MODEL_K
from libs.cache import rds


def get(self, *args, **kwargs):
    """
        Perform the query and return a single object matching the given
        keyword arguments.
        """
    cls_name = self.model.__name__
    pk = kwargs.get('pk') or kwargs.get('id')

    if pk is not None:
        # 先从缓存中获取数据
        key = MODEL_K % (cls_name, pk)
        model_obj = rds.get(key)
        # 验证缓存中的数据
        if isinstance(model_obj, self.model):
            return model_obj
    # 缓存中没有数据，从数据库取出数据
    model_obj = self._get(*args, **kwargs)
    # 将数据写入缓存
    key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(key, model_obj)
    return model_obj


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
        Save the current instance. Override this in a subclass if you want to
        control the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        """
    # 调用 源 save 将数据保存到数据库
    self._save(force_insert, force_update, using, update_fields)

    # 将对象保存到缓存
    key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(key, self)


def to_dict(self, exclude=()):
    '''将用户属性转换成一个字典'''
    # 找到对象身上所有的字段名称
    attr_dict = {}
    for field in self._meta.fields:
        if field.attname in exclude:
            continue
        # 找到字段名对应的值
        value = getattr(self, field.attname)
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = str(value)
        # 组装字典（排除 exclude 中的字段）
        attr_dict[field.attname] = value
    return attr_dict


def path_orm():
    '''通过Monkey Patch 的方式为 ORM 增加缓存处理'''
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model._save = models.Model.save
    models.Model.save = save
    models.Model.to_dict = to_dict
