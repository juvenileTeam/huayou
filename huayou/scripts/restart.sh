echo '正在重启服务器'

PROJECT_DIR='/opt/swiper'
PID_FILE="$PROJECT_DIR/logs/gunicorn.pid"

if [ -f $PID_FILE ]; then
  PID=`cat $PID_FILE`
  kill -HUP $PID
  echo '程序已重启完毕'
else
  echo '程序尚未启动，直接调用启动脚本'
  $PROJECT_DIR/scripts/start.sh
fi