#!/bin/sh

# -- usage ------------
# start.sh <python-interpreter>
# 
# eg. start.sh /usr/bin/python3


if [[ "$1" == "" ]]; then
    echo "No interpreter supplied. Usage: 'start.sh /usr/bin/python3'"
    exit 1
fi

rm -f ./nohup.out
echo "Starting server ..."
nohup $1 ./start.py &

PID=$!
echo "Server running under PID:$PID"
echo "<here comes the test> ..."
$1 ~/kasi/test/client.py

echo "Killing server $PID ..."
kill -9 $PID

echo "Server log"
echo "----------------"
cat ./nohup.out
