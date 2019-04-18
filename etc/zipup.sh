#!/usr/bin/env bash

cd ~/PycharmProjects/
zip -ruv0 campobot.zip ./campobot
scp ./campobot.zip mimimi@35.231.210.15:~/

