DROP DATABASE IF EXISTS Hospital;
CREATE DATABASE Hospital;
USE Hospital;

CREATE TABLE `patient`(
 `p_id` VARCHAR(20) PRIMARY KEY,
    `name` VARCHAR(15) NOT NULL,
    `age` INT(3) NOT NULL,
    `contact_info` VARCHAR(20) NOT NULL,
    `severity` VARCHAR(20) NOT NULL,
    `life_state` VARCHAR(20) NOT NULL,
    `en_id` VARCHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `patient` VALUES
 ('730980','哈十奇','56','13844444444','轻症','在院治疗','478921'),
    ('715698','可小基','22','18833344444','轻症','在院治疗','478921'),
    ('712298','格里斯','18','18812344444','轻症','在院治疗','478921'),
    ('789018','柴四季','34','18223398744','重症','在院治疗','478921'),
    ('711111','熊宰','78','13333333333','轻症','在院治疗','478921'),
    ('751512','路人甲','51','13843432444','轻症','在院治疗','478921'),
    ('797421','路人乙','25','18253253244','重症','在院治疗','478921'),
    ('724214','路人丁','44','18624211144','重症','在院治疗','478921'),
    ('771895','路人丙','31','18226454354','轻症','在院治疗','478921'),
    ('724487','步晓骅','99','13352352352','重症','在院治疗','478921'),
    ('712411','熊宰','78','13333333333','轻症','在院治疗','478921'),
    ('754512','路人1','51','13843432444','轻症','在院治疗','478921'),
    ('747421','路人2','25','18253253244','轻症','在院治疗','478921'),
    ('725314','路人3','44','18624211144','重症','在院治疗','478921'),
    ('783231','路人4','31','18226454354','危重症','在院治疗','478921'),
    ('794214','路人4','99','13352352352','危重症','在院治疗','478921'),
    ('700000','路人5','199','13352352322','轻症','在院治疗','478921');
SELECT* FROM patient;

CREATE TABLE `doctor`(
 `d_id` VARCHAR(20) PRIMARY KEY,
    `name` VARCHAR(15) NOT NULL,
    `contact_info` VARCHAR(20) NOT NULL,
    `password` VARCHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `doctor` VALUES
 ('109823','景建册','18972890982','000000'),
    ('143690','尹见次','18971111982','000000'),
    ('165690','王莱恩','10971260982','000000');
SELECT* FROM doctor;

CREATE TABLE `head_nurse`(
 `hn_id` VARCHAR(20) PRIMARY KEY,
    `name` VARCHAR(15) NOT NULL,
    `contact_info` VARCHAR(20) NOT NULL,
    `password` VARCHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `head_nurse` VALUES
 ('209823','凯里','16272890982','000000'),
    ('243690','渐次','10111111982','000000'),
    ('273691','茂秋','10222260982','000000');
SELECT* FROM head_nurse;

CREATE TABLE `ward_nurse`(
 `wn_id` VARCHAR(20) PRIMARY KEY,
    `name` VARCHAR(15) NOT NULL,
    `contact_info` VARCHAR(20) NOT NULL,
    `password` VARCHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `ward_nurse` VALUES
 ('309823','泡福','19972891982','000000'),
    ('383634','朵保祝','18098761982','000000'),
    ('350290','王世子','12371260982','000000'),
    ('300003','柴葱妮','18972890982','000000'),
    ('309827','哨笛余','18972890982','000000'),
    ('300000','萧萌萌','18971111982','000000'),
    ('340000','力达','10971260982','000000'),
    ('300023','凑拉拉','18972890982','000000'),
    ('300090','艾交胡','18971111982','000000'),
    ('342290','吴龙察','10971260982','000000');
SELECT* FROM ward_nurse;


CREATE TABLE `emergency_nurse`(
	`en_id` VARCHAR(20) PRIMARY KEY,
    `name` VARCHAR(20) NOT NULL,
    `contact_info` VARCHAR(20) NOT NULL,
    `password` CHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `emergency_nurse` VALUES
    ('478921','Bill Gates','18805321267','000000'),
	('421121','Muhammad','18833267899','000000');
SELECT* FROM emergency_nurse;

CREATE TABLE `location`(
	`area` VARCHAR(10),
    `room_no` VARCHAR(10),
    `bed_no` VARCHAR(10),
    `d_id` VARCHAR(20),
    `hn_id` VARCHAR(20),
    `wn_id` VARCHAR(20),
    `p_id` VARCHAR(20),
    PRIMARY KEY(area,room_no,bed_no),
    FOREIGN KEY (d_id)
    REFERENCES doctor(d_id),
    FOREIGN KEY (hn_id)
    REFERENCES head_nurse(hn_id),
    FOREIGN KEY (wn_id)
    REFERENCES ward_nurse(wn_id),
    FOREIGN KEY (p_id)
    REFERENCES patient(p_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `location` VALUES
	('0','1','1',NULL,NULL,NULL,NULL),
	('0','1','2',NULL,NULL,NULL,NULL),
	('0','1','3',NULL,NULL,NULL,NULL),
	('0','1','4',NULL,NULL,NULL,NULL),
	('0','1','5',NULL,NULL,NULL,NULL),
	('0','1','6',NULL,NULL,NULL,NULL),
	('0','1','7',NULL,NULL,NULL,NULL),
	('0','1','8',NULL,NULL,NULL,NULL),
	('0','1','9',NULL,NULL,NULL,NULL),
	('0','1','10',NULL,NULL,NULL,NULL),
	('0','1','11',NULL,NULL,NULL,NULL),
	('0','1','12',NULL,NULL,NULL,NULL),
	('1','1','1','165690','273691','300090','751512'),
	('1','1','2','165690','273691','309827','711111'),
	('1','1','3','165690','273691','309823','715698'),
	('1','1','4','165690','273691','309827','712298'),
	('1','2','1','165690','273691','300090','771895'),
	('1','2','2','165690','273691','309827','747421'),
	('1','2','3','165690','273691','309827','730980'),
	('1','2','4','165690','273691','350290','700000'),
	('2','1','1','143690','243690','342290','724214'),
	('2','1','2','143690','243690','340000','797421'),
	('2','2','1','143690','243690','340000','789018'),
	('2','2','2','143690','243690','383634','725314'),
	('3','1','1','109823','209823','300000','783231'),
    ('3','2','1','109823','209823','300023','794214');
SELECT* FROM location;
    
CREATE TABLE `covid_test`(
	`t_id` VARCHAR(20) PRIMARY KEY,
    `the_date` DATETIME NOT NULL,
    `result` BOOLEAN NOT NULL,
    `severity` VARCHAR(20) NOT NULL,
    `p_id` VARCHAR(20) NOT NULL,
    `d_id` VARCHAR(20) NOT NULL,
    FOREIGN KEY (p_id)
    REFERENCES patient(p_id),
    FOREIGN KEY (d_id)
    REFERENCES doctor(d_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `covid_test` VALUES
	('100001','2021-01-02 13:14:07',0,'轻症','730980','165690'),
    ('100003','2021-01-04 10:14:07',0,'轻症','730980','165690'),
    ('100002','2021-01-02 13:20:00',1,'轻症','712298','165690'),
    ('100004','2021-01-04 10:20:00',1,'轻症','712298','165690');
SELECT* FROM covid_test;


CREATE TABLE `daily_info`(
	`info_id` VARCHAR(20) PRIMARY KEY,
	`the_date` DATETIME NOT NULL,
	`temperature` VARCHAR(10) NOT NULL,
    `symptom` VARCHAR(50),
    `result` BOOLEAN NOT NULL,
    `life_state` VARCHAR(20) NOT NULL,
    `p_id` VARCHAR(20) NOT NULL,
	`wn_id` VARCHAR(20) NOT NULL,
	FOREIGN KEY (p_id)
    REFERENCES patient(p_id),
    FOREIGN KEY (wn_id)
    REFERENCES ward_nurse(wn_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `daily_info` VALUES
	('000001','2021-01-03','37.0','无',0,'在院治疗','730980','309827'),
    ('000004','2021-01-04','36.8','无',0,'在院治疗','730980','309827'),
    ('000005','2021-01-05','36.9','无',0,'在院治疗','730980','309827'),
    ('000002','2021-01-03','38.0','发烧',1,'在院治疗','712298','309827'),
    ('000003','2021-01-04','38.1','发烧',1,'在院治疗','712298','309827'),
    ('000006','2021-01-05','37.0','无',1,'在院治疗','712298','309827');
SELECT* FROM daily_info;

