drop user if exists 'cost'@'localhost';
create user 'cost'@'localhost' IDENTIFIED BY 'CostGroupA';
create database if not exists cost;
grant all privileges on cost.* TO 'cost'@'localhost';
use cost;
drop table if exists sensors;
create table sensors(ID int not null auto_increment,Appliance_Name varchar(100),Status tinyint(1) not null,Start_Time timestamp,primary key(id));
