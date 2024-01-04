create database HE;
use HE;

	create table if not exists account(
		usr varchar(33) primary key,
		pwd varchar(33) not null
	);

	create table if not exists launch(
		id int auto_increment primary key,
		usr varchar(33) not null,
		title varchar(33) not null,
		captcha varchar(33) unique not null,
		votelimit int not null,
		total text not null
	);

	create table if not exists votedata(
			id int auto_increment primary key,
			captcha varchar(33) not null,
			choice varchar(12) not null,
			tag int not null,
			foreign key(captcha) references launch(captcha) on delete cascade
	);

	create table if not exists voterecords(
		captcha varchar(33) not null,
		usr varchar(33) not null,
		votenum int not null,
		primary key(captcha, usr),
		foreign key(captcha) references launch(captcha) on delete cascade,
		foreign key(usr) references account(usr) on delete cascade
	);

-- 创建用户
CREATE USER 'HEAdmin'@'%' IDENTIFIED BY '7JTEwsh!CFhkqR9R';
-- 赋予数据库权限
GRANT ALL PRIVILEGES ON HE.* TO 'HEAdmin'@'%';
-- 刷新权限
FLUSH PRIVILEGES;
