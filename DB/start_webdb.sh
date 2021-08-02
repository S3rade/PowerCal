#!/bin/sh

#if not working, remember to " modprobe ip6table_filter " on kali first
ufw allow ssh
ufw allow 8080/tcp
ufw allow 80/tcp
ufw enable
#comment the below line if facing issues accessing the database
#ufw limit 8080/tcp
cd /root/iot_vol/scripts
service mysql start
mysql < init_mysql.sql
#Starts up both docker_app.py and webappreceiving.py
./docker_app.py & ./webappreceiving.py
