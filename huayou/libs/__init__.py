from libs.orm import path_orm

# 抢在 setting 加载之前 为Django 的 ORM 执行猴子补丁
path_orm()
