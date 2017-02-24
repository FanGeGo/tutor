-- MySQL dump 10.13  Distrib 5.7.16, for Linux (x86_64)
--
-- Host: 119.29.115.117    Database: tutor
-- ------------------------------------------------------
-- Server version	5.7.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `banner`
--

DROP TABLE IF EXISTS `banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banner` (
  `url` text NOT NULL COMMENT '链接',
  `image_path` text NOT NULL COMMENT '广告图片'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='广告banner';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `config`
--

DROP TABLE IF EXISTS `config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(45) DEFAULT NULL,
  `value` text COMMENT '配置相关信息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `corsheaders_corsmodel`
--

DROP TABLE IF EXISTS `corsheaders_corsmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `corsheaders_corsmodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cors` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wechat` int(11) DEFAULT NULL,
  `tutorService` text,
  `appService` text,
  `rate` float NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_feedback_1_idx` (`wechat`),
  CONSTRAINT `fk_feedback_1` FOREIGN KEY (`wechat`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message` (
  `msg_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` int(11) DEFAULT NULL,
  `message_content` text,
  `message_title` text,
  `status` tinyint(4) DEFAULT NULL,
  `receiver` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`msg_id`),
  KEY `fk_message_1_idx` (`sender`),
  KEY `fk_message_2_idx` (`receiver`),
  CONSTRAINT `fk_message_1` FOREIGN KEY (`sender`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_message_2` FOREIGN KEY (`receiver`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_apply`
--

DROP TABLE IF EXISTS `order_apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_apply` (
  `oa_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增编号',
  `apply_type` tinyint(4) NOT NULL COMMENT '申请的方式(1-老师主动申请 2-家长或管理员主动邀请)',
  `pd_id` int(11) NOT NULL COMMENT '家教需求的id',
  `tea_id` int(11) NOT NULL COMMENT '申请或被邀请的老师id',
  `teacher_willing` tinyint(4) NOT NULL COMMENT '老师的意愿:2-愿意 1-待处理 0-拒绝 (老师主动申请的默认为愿意，被邀请的默认为待处理)',
  `parent_willing` tinyint(4) NOT NULL COMMENT '家长的意愿:2-愿意 1-待处理 0-拒绝 (老师主动申请的默认为待处理，邀请老师的默认为愿意)',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `screenshot_path` text COMMENT '付费截图存储路径',
  `pass_not` tinyint(4) NOT NULL DEFAULT '1' COMMENT '管理员通过与否: 2-是 1-待处理 0-否 (如果管理员选择为否,订单重新置为确认双方willing,本申请不再有效)',
  `expectation` text,
  `finished` tinyint(1) NOT NULL DEFAULT '0',
  `tel` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`oa_id`),
  KEY `fk_order_apply_parent_order_idx` (`pd_id`),
  KEY `fk_order_apply_teacher1_idx` (`tea_id`),
  CONSTRAINT `fk_order_apply_parent_order` FOREIGN KEY (`pd_id`) REFERENCES `parent_order` (`pd_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_apply_teacher1` FOREIGN KEY (`tea_id`) REFERENCES `teacher` (`tea_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8 COMMENT='教师对家教需求申请';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parent_order`
--

DROP TABLE IF EXISTS `parent_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parent_order` (
  `pd_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `wechat_id` int(11) DEFAULT NULL COMMENT '家长从微信发过来的标识(如果是管理员发布的需求就填''admin''值)',
  `subject` text COMMENT '孩子要提高的科目(英文,隔开)',
  `subject_other` text,
  `aim` text COMMENT '找老师的目的(英文,隔开)',
  `mon_begin` tinyint(4) DEFAULT NULL COMMENT '周一可安排学习的开始时间',
  `mon_end` tinyint(4) DEFAULT NULL COMMENT '周一可安排的学习结束时间',
  `tues_begin` tinyint(4) DEFAULT NULL,
  `tues_end` tinyint(4) DEFAULT NULL,
  `wed_begin` tinyint(4) DEFAULT NULL,
  `wed_end` tinyint(4) DEFAULT NULL,
  `thur_begin` tinyint(4) DEFAULT NULL,
  `thur_end` tinyint(4) DEFAULT NULL,
  `fri_begin` tinyint(4) DEFAULT NULL,
  `fri_end` tinyint(4) DEFAULT NULL,
  `sat_morning` tinyint(4) DEFAULT '0',
  `sat_afternoon` tinyint(4) DEFAULT '0',
  `sat_evening` tinyint(4) DEFAULT '0',
  `sun_morning` tinyint(4) DEFAULT '0',
  `sun_afternoon` tinyint(4) DEFAULT '0',
  `sun_evening` tinyint(4) DEFAULT '0',
  `weekend_tutor_length` tinyint(4) DEFAULT '0' COMMENT '周末每次辅导的时长(默认为0)',
  `teacher_sex` tinyint(4) DEFAULT NULL COMMENT '老师性别:0-不限 1-男 2-女',
  `teacher_method` text COMMENT '老师特色(用$隔开)',
  `teacher_method_other` text,
  `bonus` text,
  `learning_phase` tinyint(4) DEFAULT NULL COMMENT '学习阶段(0-其他 1-幼升小 2-小学 3-初中 4-高中)',
  `class` tinyint(4) DEFAULT NULL COMMENT '班级排名(1-较为靠后 2-中等偏下 3-中等水平 4-中上水平 5-名列前茅)',
  `grade` text COMMENT '年级(0-无 1-一年级 以此类推)',
  `require` text COMMENT '对老师的要求',
  `salary` decimal(20,2) DEFAULT NULL COMMENT '时薪',
  `allowance_not` tinyint(4) DEFAULT '0' COMMENT '是否补贴(1-是 0-否)',
  `deadline` datetime DEFAULT NULL COMMENT '需求最后期限时间',
  `name` text COMMENT '联系人姓名',
  `tel` text COMMENT '联系电话',
  `address` text COMMENT '住址',
  `pass_not` tinyint(4) DEFAULT '1' COMMENT '审核是否通过(1-待审核 0-不通过 2-通过)',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `status` tinyint(4) DEFAULT '1' COMMENT '需求状态(1-正常显示欢迎预约 2-已经有心仪的老师等待确认 3-完成结束显示)默认为1',
  PRIMARY KEY (`pd_id`),
  KEY `fk_parent_order_1_idx` (`wechat_id`),
  CONSTRAINT `fk_parent_order_1` FOREIGN KEY (`wechat_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='家长发布的订单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_text`
--

DROP TABLE IF EXISTS `sys_text`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_text` (
  `salary_standard` text NOT NULL COMMENT '时薪标准',
  `require_explain` text NOT NULL COMMENT '需求说明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统文本';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `tea_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `wechat_id` int(11) DEFAULT NULL COMMENT '微信传送过来的id号',
  `name` text COMMENT '姓名',
  `qualification` tinyint(4) DEFAULT NULL COMMENT '学历状态: 1-本科生 2-研究生 3-毕业生',
  `sex` tinyint(4) DEFAULT NULL COMMENT '性别: 1-男 2-女',
  `native_place` text COMMENT '籍贯',
  `campus_major` text COMMENT '学院专业',
  `tel` text COMMENT '联系电话',
  `subject` text COMMENT '可辅导的科目(用英文,隔开)',
  `subject_other` text,
  `place` text COMMENT '可辅导的地区(用英文,隔开)',
  `teacher_method` text COMMENT '教学方法(用$隔开)',
  `teacher_method_other` text,
  `score` text COMMENT '相关成绩:大学中学获得的成绩、奖项',
  `self_comment` text COMMENT '自我评价',
  `salary_bottom` decimal(20,2) DEFAULT NULL COMMENT '时薪下限',
  `salary_top` decimal(20,2) DEFAULT NULL COMMENT '时薪上限',
  `certificate_photo` text COMMENT '证件照路径(大图就帮它转小到100k以下)',
  `teach_show_photo` text COMMENT '家教show图片路径(用;号隔开)大图要求压缩为100k以下',
  `massage_warn` tinyint(4) DEFAULT '1' COMMENT '是否有消息提醒 1-提醒 0-不提醒(默认是1)',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL,
  `pass_not` tinyint(4) DEFAULT '1' COMMENT '简历是否审核通过(默认为1) 1-待审核 0-不通过 2-通过 ',
  `mon_begin` tinyint(4) DEFAULT NULL COMMENT '周一可辅导的开始时间(为空即周一没空)',
  `mon_end` tinyint(4) DEFAULT NULL COMMENT '周一可辅导的结束时间',
  `tues_begin` tinyint(4) DEFAULT NULL COMMENT '同周一',
  `tues_end` tinyint(4) DEFAULT NULL COMMENT '同周一',
  `wed_begin` tinyint(4) DEFAULT NULL,
  `wed_end` tinyint(4) DEFAULT NULL,
  `thur_begin` tinyint(4) DEFAULT NULL,
  `thur_end` tinyint(4) DEFAULT NULL,
  `fri_begin` tinyint(4) DEFAULT NULL,
  `fri_end` tinyint(4) DEFAULT NULL,
  `sat_morning` tinyint(4) DEFAULT '1' COMMENT '周六上午 1-有空 0-没空 默认为1',
  `sat_afternoon` tinyint(4) DEFAULT '1' COMMENT '同周六上午',
  `sat_evening` tinyint(4) DEFAULT '1' COMMENT '同周六上午',
  `sun_morning` tinyint(4) DEFAULT '1' COMMENT '同周六上午',
  `sun_afternoon` tinyint(4) DEFAULT '1' COMMENT '同周六上午',
  `sun_evening` tinyint(4) DEFAULT '1' COMMENT '同周六上午',
  `hot_not` tinyint(4) DEFAULT '0' COMMENT '是否设置为热门教师:1-是 0-否(默认为0)',
  `grade` text,
  `number` varchar(45) DEFAULT NULL COMMENT '学号',
  PRIMARY KEY (`tea_id`),
  KEY `fk_teacher_1_idx` (`wechat_id`),
  CONSTRAINT `fk_teacher_1` FOREIGN KEY (`wechat_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'tutor'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-23 20:29:22
