#!/bin/bash
/usr/bin/mysqld_safe --skip-grant-tables &
sleep 5
mysql -u root -e "CREATE DATABASE People"
mysql -u root mydb < /db/people.sql