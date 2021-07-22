drop user if exists 'cost'@'localhost';
create user 'cost'@'localhost' IDENTIFIED BY 'CostGroupA';
create database if not exists cost;
grant all privileges on cost.* TO 'cost'@'localhost';
use cost;
drop table if exists sensors;
create table sensors(ID int not null auto_increment,Appliance_Name varchar(100),Status tinyint(1) not null,Start_Time timestamp,primary key(id));
insert into `sensors` (`ID`,`Appliance_Name`,`Status`,`Start_Time`) VALUES (1,'Aircon','0', current_timestamp()), (2,'TV',1,current_timestamp());

