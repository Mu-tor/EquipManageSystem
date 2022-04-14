/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3306
 Source Schema         : laboratory

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 14/04/2022 17:15:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_addr
-- ----------------------------
DROP TABLE IF EXISTS `t_addr`;
CREATE TABLE `t_addr`  (
  `addrid` int NOT NULL AUTO_INCREMENT,
  `addr_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '场地名（类型，如：羽毛球场）',
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '场地位置',
  PRIMARY KEY (`addrid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_addr
-- ----------------------------
INSERT INTO `t_addr` VALUES (1, '自习室', 'A2-201');
INSERT INTO `t_addr` VALUES (2, '自习室', 'A2-202');
INSERT INTO `t_addr` VALUES (3, '自习室', 'A2-203');
INSERT INTO `t_addr` VALUES (4, '化学实验室', 'D2-201');
INSERT INTO `t_addr` VALUES (5, '化学实验室', 'D2-202');
INSERT INTO `t_addr` VALUES (6, '摄影共享室', 'D3-203');
INSERT INTO `t_addr` VALUES (7, '生物实验室', 'D2-301');
INSERT INTO `t_addr` VALUES (8, '生物实验室', 'D2-302');
INSERT INTO `t_addr` VALUES (9, '物理实验室', 'D2-303');

-- ----------------------------
-- Table structure for t_admin
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin`  (
  `admid` int NOT NULL AUTO_INCREMENT,
  `admname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`admid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO `t_admin` VALUES (1, 'admin', '698d51a19d8a121ce581499d7b701668');

-- ----------------------------
-- Table structure for t_booking
-- ----------------------------
DROP TABLE IF EXISTS `t_booking`;
CREATE TABLE `t_booking`  (
  `bid` int NOT NULL AUTO_INCREMENT,
  `uid` int NULL DEFAULT NULL,
  `bro_time` date NULL DEFAULT NULL,
  `days` int NULL DEFAULT NULL,
  `is_agree` int NULL DEFAULT NULL COMMENT '0为不同意，1为同意，-1为未审核，-2为用户取消',
  PRIMARY KEY (`bid`) USING BTREE,
  INDEX `uid`(`uid`) USING BTREE,
  CONSTRAINT `uid` FOREIGN KEY (`uid`) REFERENCES `t_user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_booking
-- ----------------------------
INSERT INTO `t_booking` VALUES (1, 1, '2022-03-22', 1, 1);
INSERT INTO `t_booking` VALUES (2, 1, '2022-04-04', 1, 1);
INSERT INTO `t_booking` VALUES (3, 1, '2022-04-03', 2, 0);
INSERT INTO `t_booking` VALUES (4, 1, '2022-04-30', 1, 1);
INSERT INTO `t_booking` VALUES (5, 1, '2022-01-07', 2, -2);
INSERT INTO `t_booking` VALUES (6, 1, '2022-04-07', 1, -1);
INSERT INTO `t_booking` VALUES (7, 1, '2022-03-30', 1, -1);
INSERT INTO `t_booking` VALUES (8, 1, '2022-03-30', 1, 1);
INSERT INTO `t_booking` VALUES (9, 1, '2022-04-14', 1, -1);
INSERT INTO `t_booking` VALUES (10, 1, '2022-04-14', 1, -1);
INSERT INTO `t_booking` VALUES (11, 1, '2022-04-14', 1, 1);
INSERT INTO `t_booking` VALUES (12, 1, '2022-04-14', 1, -1);
INSERT INTO `t_booking` VALUES (13, 1, '2022-04-15', 1, -1);
INSERT INTO `t_booking` VALUES (14, 1, '2022-04-14', 1, -1);
INSERT INTO `t_booking` VALUES (15, 1, '2022-03-29', 1, -1);
INSERT INTO `t_booking` VALUES (16, 1, '2022-04-27', 1, -1);
INSERT INTO `t_booking` VALUES (17, 1, '2022-02-28', 1, -1);

-- ----------------------------
-- Table structure for t_brodtl
-- ----------------------------
DROP TABLE IF EXISTS `t_brodtl`;
CREATE TABLE `t_brodtl`  (
  `dtlid` int NOT NULL AUTO_INCREMENT COMMENT '借用详情表id',
  `bid` int NULL DEFAULT NULL COMMENT '预约表id',
  `eqpid` int NULL DEFAULT NULL COMMENT '器材id',
  `addrid` int NULL DEFAULT NULL COMMENT '场地id',
  `is_addr` int NULL DEFAULT NULL COMMENT '场地标记1为场地',
  `bro_num` int NULL DEFAULT NULL COMMENT '借用数量',
  PRIMARY KEY (`dtlid`) USING BTREE,
  INDEX `eqpid`(`eqpid`) USING BTREE,
  INDEX `dtl_bid`(`bid`) USING BTREE,
  INDEX `addrid`(`addrid`) USING BTREE,
  CONSTRAINT `addrid` FOREIGN KEY (`addrid`) REFERENCES `t_addr` (`addrid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `dtl_bid` FOREIGN KEY (`bid`) REFERENCES `t_booking` (`bid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eqpid` FOREIGN KEY (`eqpid`) REFERENCES `t_equipment` (`eqpid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_brodtl
-- ----------------------------
INSERT INTO `t_brodtl` VALUES (1, 1, 1, NULL, 0, 2);
INSERT INTO `t_brodtl` VALUES (2, 2, NULL, 7, 1, 1);
INSERT INTO `t_brodtl` VALUES (3, 3, NULL, 8, 1, 1);
INSERT INTO `t_brodtl` VALUES (5, 4, 7, NULL, 0, 5);
INSERT INTO `t_brodtl` VALUES (6, 5, 8, NULL, 0, 3);
INSERT INTO `t_brodtl` VALUES (7, 6, NULL, 7, 1, 1);
INSERT INTO `t_brodtl` VALUES (8, 7, NULL, 7, 1, 1);
INSERT INTO `t_brodtl` VALUES (9, 8, NULL, 7, 1, 1);
INSERT INTO `t_brodtl` VALUES (10, 9, 1, NULL, 0, 1);
INSERT INTO `t_brodtl` VALUES (11, 10, 1, NULL, 0, 3);
INSERT INTO `t_brodtl` VALUES (12, 11, 1, NULL, 0, 2);
INSERT INTO `t_brodtl` VALUES (13, 12, 1, NULL, 0, 5);
INSERT INTO `t_brodtl` VALUES (14, 13, NULL, 7, 1, 1);
INSERT INTO `t_brodtl` VALUES (15, 14, 1, NULL, 0, 10);
INSERT INTO `t_brodtl` VALUES (16, 15, NULL, 3, 1, 1);
INSERT INTO `t_brodtl` VALUES (17, 16, NULL, 7, 1, 1);
INSERT INTO `t_brodtl` VALUES (18, 17, NULL, 7, 1, 1);

-- ----------------------------
-- Table structure for t_equipment
-- ----------------------------
DROP TABLE IF EXISTS `t_equipment`;
CREATE TABLE `t_equipment`  (
  `eqpid` int NOT NULL AUTO_INCREMENT,
  `eqp_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `num` int NULL DEFAULT NULL,
  PRIMARY KEY (`eqpid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_equipment
-- ----------------------------
INSERT INTO `t_equipment` VALUES (1, '哑铃', 0);
INSERT INTO `t_equipment` VALUES (2, '高精度探测仪', 10);
INSERT INTO `t_equipment` VALUES (3, '诺辉 F1-1', 10);
INSERT INTO `t_equipment` VALUES (4, '自动钻孔机', 10);
INSERT INTO `t_equipment` VALUES (5, '数码相机', 5);
INSERT INTO `t_equipment` VALUES (6, '拍照平衡器', 15);
INSERT INTO `t_equipment` VALUES (7, '光波探测仪', 2);
INSERT INTO `t_equipment` VALUES (8, '游标卡尺', 50);
INSERT INTO `t_equipment` VALUES (9, '托盘天平', 50);
INSERT INTO `t_equipment` VALUES (10, '烧杯', 100);
INSERT INTO `t_equipment` VALUES (12, '打点计时器', 200);

-- ----------------------------
-- Table structure for t_faceconfig
-- ----------------------------
DROP TABLE IF EXISTS `t_faceconfig`;
CREATE TABLE `t_faceconfig`  (
  `faceid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `encode` blob NULL COMMENT '人脸数据',
  `is_adm` int NULL DEFAULT NULL COMMENT '0是用户，1是管理员',
  PRIMARY KEY (`faceid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_faceconfig
-- ----------------------------
INSERT INTO `t_faceconfig` VALUES (1, 'admin', 0x00000000B5FBB9BF00000060F7FABE3F000000E01201863F000000E0CFC89CBF000000C07BE5BBBF000000C0A4EDB5BF00000040F6A699BF00000060D257B7BF000000C00DCFC13F000000C042E0ABBF000000809501CB3F0000000094B6BFBF00000020EE8CCBBF000000E027CCAEBF000000A0DCB1B2BF00000040AD95C93F000000C04106C8BF000000C04B4CC3BF000000003BBEB3BF000000006E509D3F000000E09A71C43F00000060D5BCAE3F000000E0D68591BF000000405B66993F000000C07BBEA2BF000000004766D8BF00000000BE10B0BF000000C0978EAABF000000C06EC1B63F00000000AAAB90BF0000002013DFB1BF000000400D3DA83F000000A062BDCABF000000A07732BDBF0000006085C0B13F000000E03C31B13F000000A073F987BF000000C0FAD5B1BF000000C013B6C73F00000040C83A8BBF000000A0C3EDD1BF0000004041E8973F000000C0899EB83F000000C0F4BECC3F000000405BA8C73F00000060F685B13F00000040F7C69E3F000000003430BBBF00000080B630B93F000000007735C1BF00000040F7D696BF000000E0C85EC33F000000408535C43F000000203169B33F000000000C776F3F00000080D33EC5BF0000002099739C3F00000040205CB83F00000060A352C3BF00000060D5BD94BF000000000F93BB3F000000E0FC69BCBF000000207458A13F000000005E56B3BF000000805B1ACB3F000000204C19ABBF00000080E21DB5BF00000060F126C6BF000000009906BE3F000000A0F158C4BF00000040C5E9AABF000000C09469B23F00000080394AC1BF00000080AE23C2BF000000C0716ED4BF00000000C00291BF000000200AEFD73F00000040D548B13F00000060F1A1C2BF000000004CB6B33F0000004093156BBF00000000B52071BF0000006057DFB83F000000808E93C13F000000C0DAEB95BF000000E05E87AD3F000000805E77C2BF000000E0820A9BBF000000202078CE3F000000C031CBB6BF000000C0562A81BF00000080912DC83F00000000563887BF000000A03CE1B23F000000C042CC823F000000E084C7903F00000040E309B2BF000000C0A414953F00000000F81CAFBF000000A078698E3F00000000B791653F00000000DDD3AABF000000E0678498BF00000000D327BC3F00000000A505C0BF000000C0AAC8AB3F000000607906AABF00000040B703B23F000000005609AFBF00000000B68998BF000000A00EA0A6BF000000A0C797B2BF000000A0C8F1B53F000000C090F3C5BF00000080B6F9C63F000000C0D8B1C73F00000040C140973F000000C0A4ABBA3F00000040BB3FB63F000000C0A232AB3F00000040885D81BF00000000C2F96C3F000000C0C290CCBF00000040831DB0BF00000000C10EBA3F000000C0719D9BBF000000005863B93F000000401B248B3F, 1);

-- ----------------------------
-- Table structure for t_notice
-- ----------------------------
DROP TABLE IF EXISTS `t_notice`;
CREATE TABLE `t_notice`  (
  `notid` int NOT NULL AUTO_INCREMENT,
  `admid` int NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`notid`) USING BTREE,
  INDEX `admid`(`admid`) USING BTREE,
  CONSTRAINT `admid` FOREIGN KEY (`admid`) REFERENCES `t_admin` (`admid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_notice
-- ----------------------------
INSERT INTO `t_notice` VALUES (1, 1, '清明假期维护');
INSERT INTO `t_notice` VALUES (2, 1, '微量精密天平一套招标');
INSERT INTO `t_notice` VALUES (3, 1, '仪器设备(档案管理系统、档案馆数字化)招标\n');
INSERT INTO `t_notice` VALUES (4, 1, '仪器设备(玻切超乳一体机一套、532nm眼底激光机一套、台式计算机一批)招标\n');
INSERT INTO `t_notice` VALUES (5, 1, '五一假期维护');

-- ----------------------------
-- Table structure for t_record
-- ----------------------------
DROP TABLE IF EXISTS `t_record`;
CREATE TABLE `t_record`  (
  `recd_id` int NOT NULL AUTO_INCREMENT,
  `bid` int NULL DEFAULT NULL,
  `admid` int NULL DEFAULT NULL,
  `rtn_date` datetime NULL DEFAULT NULL,
  `is_return` int NULL DEFAULT NULL COMMENT '0是未归还，1是已归还，-1是驳回',
  `remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`recd_id`) USING BTREE,
  INDEX `recd_bid`(`bid`) USING BTREE,
  INDEX `amdid`(`admid`) USING BTREE,
  CONSTRAINT `amdid` FOREIGN KEY (`admid`) REFERENCES `t_admin` (`admid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `recd_bid` FOREIGN KEY (`bid`) REFERENCES `t_booking` (`bid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_record
-- ----------------------------
INSERT INTO `t_record` VALUES (1, 1, 1, '2022-03-23 09:53:56', 1, '保持整洁');
INSERT INTO `t_record` VALUES (2, 2, 1, '2022-04-03 09:53:56', 0, '未还');
INSERT INTO `t_record` VALUES (7, 3, 1, NULL, -1, '驳回');
INSERT INTO `t_record` VALUES (8, 4, 1, '2022-04-13 18:30:41', 1, '归还');
INSERT INTO `t_record` VALUES (9, 5, 1, NULL, -1, '驳回');
INSERT INTO `t_record` VALUES (10, 8, 1, NULL, 0, '同意');
INSERT INTO `t_record` VALUES (11, 11, 1, NULL, 0, '同意');

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `uid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `tel` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '电话号码',
  `is_out` int NULL DEFAULT 1 COMMENT '0为内部人员，1为外部人员',
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_user
-- ----------------------------
INSERT INTO `t_user` VALUES (1, 'user', '698d51a19d8a121ce581499d7b701668', NULL, 0);
INSERT INTO `t_user` VALUES (2, 'xiaofu', '5dc705b55e159c9e131e12ea10d5d80c', '18888888888', 0);

-- ----------------------------
-- Table structure for t_work
-- ----------------------------
DROP TABLE IF EXISTS `t_work`;
CREATE TABLE `t_work`  (
  `wid` int NOT NULL AUTO_INCREMENT,
  `bid` int NULL DEFAULT NULL,
  `is_deal` int NULL DEFAULT NULL COMMENT '0为未处理，1为处理',
  PRIMARY KEY (`wid`) USING BTREE,
  INDEX `work_bid`(`bid`) USING BTREE,
  CONSTRAINT `work_bid` FOREIGN KEY (`bid`) REFERENCES `t_booking` (`bid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_work
-- ----------------------------
INSERT INTO `t_work` VALUES (1, 1, 0);
INSERT INTO `t_work` VALUES (2, 2, 0);
INSERT INTO `t_work` VALUES (3, 3, 1);
INSERT INTO `t_work` VALUES (4, 4, 1);
INSERT INTO `t_work` VALUES (5, 4, 0);
INSERT INTO `t_work` VALUES (6, 5, 1);
INSERT INTO `t_work` VALUES (7, 6, 0);
INSERT INTO `t_work` VALUES (8, 7, 0);
INSERT INTO `t_work` VALUES (9, 8, 1);
INSERT INTO `t_work` VALUES (10, 9, 0);
INSERT INTO `t_work` VALUES (11, 10, 0);
INSERT INTO `t_work` VALUES (12, 11, 1);
INSERT INTO `t_work` VALUES (13, 12, 0);
INSERT INTO `t_work` VALUES (14, 13, 0);
INSERT INTO `t_work` VALUES (15, 14, 0);
INSERT INTO `t_work` VALUES (16, 15, 0);
INSERT INTO `t_work` VALUES (17, 16, 0);
INSERT INTO `t_work` VALUES (18, 17, 0);

-- ----------------------------
-- Triggers structure for table t_booking
-- ----------------------------
DROP TRIGGER IF EXISTS `after_i_work_trig`;
delimiter ;;
CREATE TRIGGER `after_i_work_trig` AFTER INSERT ON `t_booking` FOR EACH ROW insert into t_work(is_deal,bid) values (0,NEW.bid)
;
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
