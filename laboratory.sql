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

 Date: 28/03/2022 23:49:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_addr
-- ----------------------------
DROP TABLE IF EXISTS `t_addr`;
CREATE TABLE `t_addr`  (
  `addrid` int NOT NULL AUTO_INCREMENT,
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`addrid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_addr
-- ----------------------------

-- ----------------------------
-- Table structure for t_admin
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin`  (
  `admid` int NOT NULL AUTO_INCREMENT,
  `admname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`admid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
  `bro_time` datetime NULL DEFAULT NULL,
  `days` int NULL DEFAULT NULL,
  `is_agree` int NULL DEFAULT NULL COMMENT '0为不同意，1为同意',
  PRIMARY KEY (`bid`) USING BTREE,
  INDEX `uid`(`uid`) USING BTREE,
  CONSTRAINT `uid` FOREIGN KEY (`uid`) REFERENCES `t_user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_booking
-- ----------------------------
INSERT INTO `t_booking` VALUES (1, 1, '2022-03-22 11:36:05', 1, NULL);

-- ----------------------------
-- Table structure for t_brodtl
-- ----------------------------
DROP TABLE IF EXISTS `t_brodtl`;
CREATE TABLE `t_brodtl`  (
  `dtlid` int NOT NULL AUTO_INCREMENT,
  `bid` int NULL DEFAULT NULL,
  `eqpid` int NULL DEFAULT NULL,
  `addrid` int NULL DEFAULT NULL,
  `is_addr` int NULL DEFAULT NULL,
  `bro_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`dtlid`) USING BTREE,
  INDEX `eqpid`(`eqpid`) USING BTREE,
  INDEX `dtl_bid`(`bid`) USING BTREE,
  INDEX `addrid`(`addrid`) USING BTREE,
  CONSTRAINT `addrid` FOREIGN KEY (`addrid`) REFERENCES `t_addr` (`addrid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `dtl_bid` FOREIGN KEY (`bid`) REFERENCES `t_booking` (`bid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eqpid` FOREIGN KEY (`eqpid`) REFERENCES `t_equipment` (`eqpid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_brodtl
-- ----------------------------

-- ----------------------------
-- Table structure for t_equipment
-- ----------------------------
DROP TABLE IF EXISTS `t_equipment`;
CREATE TABLE `t_equipment`  (
  `eqpid` int NOT NULL AUTO_INCREMENT,
  `eqp_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `num` int NULL DEFAULT NULL,
  PRIMARY KEY (`eqpid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_equipment
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_notice
-- ----------------------------

-- ----------------------------
-- Table structure for t_record
-- ----------------------------
DROP TABLE IF EXISTS `t_record`;
CREATE TABLE `t_record`  (
  `recd_id` int NOT NULL AUTO_INCREMENT,
  `bid` int NULL DEFAULT NULL,
  `admid` int NULL DEFAULT NULL,
  `rtn_date` datetime NULL DEFAULT NULL,
  `is_return` int NULL DEFAULT NULL COMMENT '0是未归还，1是已归还',
  `remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`recd_id`) USING BTREE,
  INDEX `recd_bid`(`bid`) USING BTREE,
  INDEX `amdid`(`admid`) USING BTREE,
  CONSTRAINT `amdid` FOREIGN KEY (`admid`) REFERENCES `t_admin` (`admid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `recd_bid` FOREIGN KEY (`bid`) REFERENCES `t_booking` (`bid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_record
-- ----------------------------

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `uid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_out` int NULL DEFAULT 1 COMMENT '0为内部人员，1为外部人员',
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_user
-- ----------------------------
INSERT INTO `t_user` VALUES (1, 'user', '698d51a19d8a121ce581499d7b701668', 0);

-- ----------------------------
-- Table structure for t_work
-- ----------------------------
DROP TABLE IF EXISTS `t_work`;
CREATE TABLE `t_work`  (
  `wid` int NOT NULL AUTO_INCREMENT,
  `is_deal` int NULL DEFAULT NULL COMMENT '0为未处理，1为处理',
  `bid` int NULL DEFAULT NULL,
  PRIMARY KEY (`wid`) USING BTREE,
  INDEX `work_bid`(`bid`) USING BTREE,
  CONSTRAINT `work_bid` FOREIGN KEY (`bid`) REFERENCES `t_booking` (`bid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_work
-- ----------------------------
INSERT INTO `t_work` VALUES (1, 0, 1);

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
