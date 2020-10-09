import datetime

from django.db.transaction import atomic

from Social.models import Swiped, Friend
from User.models import Profile, User
from common import keys, errors
from huayou import config
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


@atomic
def like_someone(uid, sid):
    '''喜欢某人(右滑)'''
    # 添加滑动记录
    Swiped.swiped(uid, sid, 'like')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q + str(f'{uid}'), count=0, value=sid)

    # 增加对方的滑动积分
    rds.zincrby(keys.HOT_RANK, config.SWIPE_SCORE['like'], sid)

    # 检查对方是否喜欢过自己
    is_liked = Swiped.objects.filter(uid=sid, sid=uid, stype__in=['like', 'superlike']).exists()
    if is_liked:
        # 将互相喜欢的两个人添加为好友
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


@atomic
def superlike_someone(uid, sid):
    '''超级喜欢某人(上滑)'''
    # 添加滑动记录
    Swiped.swiped(uid, sid, 'superlike')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q + str(f'{uid}'), count=0, value=sid)

    # 增加对方的滑动积分
    rds.zincrby(keys.HOT_RANK, config.SWIPE_SCORE['superlike'], sid)

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

    # 增加对方的滑动积分
    rds.zincrby(keys.HOT_RANK, config.SWIPE_SCORE['dislike'], sid)


def rewind_last_swiped(uid):
    '''反悔上一次滑动 (每天允许反悔参数)'''
    now = datetime.datetime.now()

    # 检查今天是否已经反悔 3 次
    rewind_key = keys.REWIND_TIMES_K + str(f'{now.date()}' + '-' + str(f'{uid}'))
    rewind_times = rds.get(rewind_key, 0)
    if rewind_times >= config.REWIND_TIMES:
        raise errors.RewindLimit

    # 找到最后一次滑动
    last_swipe = Swiped.objects.filter(uid=uid).latest('stime')

    # 检查最后一次滑动是否在 5 分钟内
    time_past = (now - last_swipe.stime).total_seconds()
    if time_past >= config.REWIND_TIMEOUT:
        raise errors.RewindTimeout

    with atomic():  # 将多次数据修改在事务中执行
        # 如果之前是好友，删除好友关系
        if last_swipe.stype in ['like', 'superlike']:
            Friend.breakoff(uid1=uid, uid2=last_swipe.sid)

            # 如果是超级喜欢，删除对方优先队列里面的数据
            if last_swipe.stype == 'superlike':
                rds.lrem(keys.FIRST_RCMD_Q + str(f'{last_swipe}'), 0, uid)

        # 增加对方的滑动积分
        score = config.SWIPE_SCORE[last_swipe.stype]
        rds.zincrby(keys.HOT_RANK, -score, last_swipe.sid)

        # 删除最后一次滑动
        last_swipe.delete()

        # 今日反悔次数加一
        rds.set(rewind_key, rewind_times + 1, 86460)  # 设置缓存过期时间 一天零一分


def find__my_fans(uid):
    '''查找自己的粉丝'''
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)  # 自己已经滑过的用户的id -> sid

    fans_id_list = Swiped.objects.filter(sid=uid, stype__in=['like', 'superlike']) \
                                 .exclude(uid__in=sid_list) \
                                 .values_list('uid', flat=True)
    users = User.objects.filter(id__in=fans_id_list)
    return users


