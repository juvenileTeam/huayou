import datetime

from Social.models import Swiped, Friend
from User.models import Profile, User
from common import keys
from libs.cache import rds


def rcmd(uid):
    first_users = rcmd_from_queue(uid)
    remain = 20 - len(first_users)  # 计算需要从db中获取的用户的个数
    if remain:
        second_users = rcmd_from_db(uid, remain)
        return set(first_users) | set(second_users)
    else:
        return first_users


def rcmd_from_queue(uid):
    '''从优先推荐队列里推荐用户'''
    uid_list = rds.lrange(keys.FIRST_RCMD_Q + str(f'{uid}'), 0, 19)  # 从优先推荐队列取出uid
    uid_list = [int(uid) for uid in uid_list]
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num=20):
    '''从数据库中为用户推荐滑动用户'''
    profile = Profile.objects.get(id=uid)

    # 计算出生日期
    today = datetime.date.today()
    earliest_birth = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birth = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    # 获取已经划过的用户 ID
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)
    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        # birthday__gte=earliest_birth,
        # birthday__lte=latest_birth,
        birthday__range=[earliest_birth, latest_birth]
    ).exclude(id__in=sid_list)[:num]
    return users


def like_someone(uid, sid):
    '''喜欢某人(右滑)'''
    # 添加滑动记录
    Swiped.swiped(uid, sid, 'like')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q + str(f'{uid}'), count=0, value=sid)

    # 检查对方是否喜欢过自己
    is_liked = Swiped.objects.filter(uid=sid, sid=uid, stype__in=['like', 'superlike']).exists()
    if is_liked:
        # 将互相喜欢的两个人添加为好友
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢某人(上滑)'''
    # 添加滑动记录
    Swiped.swiped(uid, sid, 'superlike')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q + str(f'{uid}'), count=0, value=sid)

    # 检查对方是否喜欢过自己
    is_liked = Swiped.is_liked(sid, uid)
    if is_liked is True:
        # 将互相喜欢的两个人添加为好友
        Friend.make_friends(uid, sid)
        return True
    elif is_liked is False:
        return False
    else:
        # 对方尚未滑动过自己，将自己优先推荐给对方
        rds.rpush(keys.FIRST_RCMD_Q + str(f'{sid}'), uid)
        return False


def dislike_someone(uid, sid):
    '''不喜欢(左滑)'''
    # 添加滑动记录
    Swiped.swiped(uid, sid, 'dislike')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q + str(f'{uid}'), count=0, value=sid)