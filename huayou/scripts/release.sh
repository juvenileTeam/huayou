#!/usr/bin/env bash
# 代码发布脚本

USER='Dback'
HOST='49.235.252.5'
LOCAL_DIR='./'
REMOTE_DIR='/opt/swiper'

# 第 1 步：切换指定版本
if [[ "$#" == "1" ]]; then
  git checkout $1
fi

# 第 2 步：将代码上传到服务器
rsync -crvP --exclude={.git,venv,logs,__pycache__,.idea} $LOCAL_DIR $USER@$HOST:$REMOTE_DIR/

# 第 3 步：重启远程服务器

read -p '是否重启服务器？[y/n]  ' result

if [[ $result == 'y' ]]; then
  ssh $USER@$HOST "$REMOTE_DIR/scripts/restart.sh"
fi