cd /root/cost_vol/scripts
service mysql start
mysql < init_mysql.sql
./powercal.py
