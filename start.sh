#!/bin/bash

# start bot
eval "(python ./src/main.py 1> /dev/null 2> .error_log) &"
pid=$!

echo "Bot has started"

echo $pid > ".pid"
