#!/usr/bin/env bash
zip -ruv0 campobot.zip ./campobot
scp ./campobot.zip mimimi@35.231.210.15:~/
