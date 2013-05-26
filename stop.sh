#!/bin/bash

pid=$(<.pid)
kill $pid

echo "Bot was stopped."