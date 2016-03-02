#!/bin/bash
echo "$(date)   crontab start"
BASE_DIR=$(cd `dirname $0`; pwd)
cd ${BASE_DIR}
FILE_CLASSPATH=$BASE_DIR/lib/DataHandler.py
RUNNING_PIDS=$(pgrep -f "$FILE_CLASSPATH")
echo "$(date)   running_pids: $RUNNING_PIDS "
if [ -n "$RUNNING_PIDS" ];then
   echo "$(date)   Already running"
   NOW=$(date +%Y)
   NOWDATE=$(date +%s)
   PTIME=$(ps -p "$RUNNING_PIDS" -o lstart|grep "$NOW")
   STIME=$(date -d "$PTIME" +%s)
   DIFF=`expr $NOWDATE - $STIME`
   MAX=1200
   echo "$(date)   Running time $DIFF"
   if [ $DIFF -gt $MAX ]
   then
      echo "$(date)   kill -9 $RUNNING_PIDS"
      kill $RUNNING_PIDS
      echo "$(date)   launch $FILE_CLASSPATH"
   else
      echo "$(date)   do nothing"
      exit 1;
   fi
fi
python $FILE_CLASSPATH  &
