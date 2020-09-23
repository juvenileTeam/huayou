from django.db import models


# Create your models here.
class User(models.Model):
    GENDER = (
        ('male','男性'),
        ('female','女性')
    )
    LOCATION = (
        ('北京','北京'),
        ('上海','上海'),
        ('深圳','深圳'),
        ('成都','成都'),
        ('西安','西安'),
        ('武汉','武汉'),
        ('沈阳','沈阳')
    )
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, db_index=True, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=GENDER, verbose_name='性别')
    birthday = models.DateField(default='2000-1-1', verbose_name='生日')
    avatar = models.CharField(max_length=256, verbose_name='头像')
    location = models.CharField(max_length=32, choices=LOCATION, verbose_name='常居地')

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

#
#
# class MakeFriends(models.Model):
#     user = models.ForeignKey(User)
#     dating_gender = models.CharField(max_length=32,default='male')
#     dating_location = models.CharField(max_length=32,default='北京')
#     max_distance = models.FloatField(default=100)
#     min_distance = models.FloatField(default=0)
#     max_dating_age = models.IntegerField(default=40)
#     min_dating_age = models.IntegerField(default=18)
#     vibration = models.BooleanField(default=True)
#     only_matched = models.BooleanField(default=True)
#     auto_play = models.BooleanField(default=True)
#
#     class Meta:
#         db_table = 'make_friends'
