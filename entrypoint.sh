#!/bin/sh
filebeat setup -e ; service filebeat start ; service cron start & tail -f /var/log/cron.log
