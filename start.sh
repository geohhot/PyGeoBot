#!/bin/bash

# start bot
eval "(python ./src/main.py 1> /dev/null) &"
pid=$!

echo "Bot has started"

echo $pid > ".pid"
