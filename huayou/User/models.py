import datetime

from django.db import models

# Create your models here.
from Vip.models import Vip


class User(models.Model):
    GENDER = (
        ('male', '男性'),
        ('female', '女性')
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('成都', '成都'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('沈阳', '沈阳')
    )
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, db_index=True, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=GENDER, default='male', verbose_name='性别')
    birthday = models.DateField(default='2000-1-1', verbose_name='生日')
    avatar = models.CharField(max_length=256, verbose_name='头像')
    location = models.CharField(max_length=32, choices=LOCATION, default='上海', verbose_name='常居地')

    vip_id = models.IntegerField(default=1, verbose_name='用户购买的VIP的ID')
    vip_expire = models.DateTimeField(default='3000-12-31', verbose_name='会员过期时间')

    @property
    def profile(self):
        '''当前用户对应的 Profile'''
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        '''当前用户对应的 VIP'''
        #  检查当前会员是否过期
        now = datetime.datetime.now()
        if now >= self.vip_expire:
            self.set_vip(1)  # 强制设置成非会员

        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def set_vip(self, vip_id):
        '''设置当前用户的 ID'''
        vip = Vip.objects.get(id=vip_id)
        self.vip_id = vip_id
        self.vip_expire = datetime.datetime.now() + datetime.timedelta(vip.duration)
        self._vip = vip
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "phonenum": self.phonenum,
            "birthday": str(self.birthday),
            "gender": self.gender,
            "location": self.location,
            "avatar": self.avatar,
        }

    class Meta:
        db_table = 'user'


class Profile(models.Model):
    dating_gender = models.CharField(max_length=10, choices=User.GENDER, default='female')
    dating_location = models.CharField(max_length=32, choices=User.LOCATION, default='北京')
    min_distance = models.FloatField(default=1)
    max_distance = models.FloatField(default=100)
    min_dating_age = models.IntegerField(default=18)
    max_dating_age = models.IntegerField(default=40)
    vibration = models.BooleanField(default=True)
    only_matched = models.BooleanField(default=True)
    auto_play = models.BooleanField(default=True)

    class Meta:
        db_table = 'profile'

    def to_dict(self):
        return {
            'id': self.id,
            'dating_gender': self.dating_gender,
            'dating_location': self.dating_location,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_dating_age': self.min_dating_age,
            'max_dating_age': self.max_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play
        }
