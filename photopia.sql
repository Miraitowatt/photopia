/*
 Navicat Premium Data Transfer

 Source Server         : artverse
 Source Server Type    : MySQL
 Source Server Version : 50739 (5.7.39-log)
 Source Host           : localhost:3306
 Source Schema         : photopia

 Target Server Type    : MySQL
 Target Server Version : 50739 (5.7.39-log)
 File Encoding         : 65001

 Date: 09/06/2024 12:32:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for collects
-- ----------------------------
DROP TABLE IF EXISTS `collects`;
CREATE TABLE `collects`  (
  `collect_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '收藏记录ID',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '收藏用户ID',
  `collected_id` int(11) NULL DEFAULT NULL COMMENT '被赞作品ID',
  `collect_time` datetime NULL DEFAULT NULL COMMENT '收藏时间',
  PRIMARY KEY (`collect_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '收藏记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of collects
-- ----------------------------
INSERT INTO `collects` VALUES (1, 2, 26, '2024-06-07 08:11:44');
INSERT INTO `collects` VALUES (2, 2, 24, '2024-06-07 08:12:20');
INSERT INTO `collects` VALUES (3, 1, 12, '2024-06-07 08:49:44');

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`  (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户ID',
  `commented_id` int(11) NULL DEFAULT NULL COMMENT '被评论的对象ID',
  `comment_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '评论内容',
  `comment_time` datetime NULL DEFAULT NULL COMMENT '评论时间',
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '评论记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comments
-- ----------------------------
INSERT INTO `comments` VALUES (1, 1, 12, '太棒了！！！', '2024-06-07 08:05:22');
INSERT INTO `comments` VALUES (2, 1, 12, 'good', '2024-06-07 08:05:29');
INSERT INTO `comments` VALUES (3, 3, 23, '光影好绝', '2024-06-07 08:09:58');
INSERT INTO `comments` VALUES (4, 2, 19, '好棒的图片', '2024-06-07 08:10:33');
INSERT INTO `comments` VALUES (5, 2, 26, '唯美而清新~', '2024-06-07 08:11:24');
INSERT INTO `comments` VALUES (6, 2, 26, '感谢你的分享，很美的画面', '2024-06-07 08:11:57');
INSERT INTO `comments` VALUES (7, 3, 26, '喜欢日系的感觉！', '2024-06-07 08:15:03');
INSERT INTO `comments` VALUES (8, 3, 19, '富有诗意....', '2024-06-07 08:16:02');
INSERT INTO `comments` VALUES (9, 3, 27, '令人眼前一亮的色彩～', '2024-06-07 08:16:32');
INSERT INTO `comments` VALUES (10, 3, 26, '好美', '2024-06-07 08:49:18');
INSERT INTO `comments` VALUES (11, 3, 26, '好美', '2024-06-07 08:49:18');
INSERT INTO `comments` VALUES (12, 1, 12, '123456', '2024-06-07 08:49:38');

-- ----------------------------
-- Table structure for devices
-- ----------------------------
DROP TABLE IF EXISTS `devices`;
CREATE TABLE `devices`  (
  `device_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '设备ID',
  `device_name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '设备名称',
  `device_brand` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '设备品牌',
  `device_score` int(11) NULL DEFAULT NULL COMMENT '设备评分',
  `device_dr` float NULL DEFAULT NULL COMMENT '动态范围',
  `device_iso` float NULL DEFAULT NULL COMMENT '最大ISO',
  `device_type` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '设备类型',
  `device_picture` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备图片的URL',
  `device_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备购买的URL',
  PRIMARY KEY (`device_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 48 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '设备信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of devices
-- ----------------------------
INSERT INTO `devices` VALUES (1, 'A7R V', 'Sony', 100, 14.8, 3187, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Sony1.png', 'https://www.dxomark.cn/Cameras/Sony/A7RV');
INSERT INTO `devices` VALUES (2, 'A7R IV', 'Sony', 97, 14.7, 3379, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Sony2.png', 'https://www.dxomark.cn/Cameras/Sony/A7RIV');
INSERT INTO `devices` VALUES (3, 'A1', 'Sony', 98, 14.5, 3163, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Sony3.png', 'https://www.dxomark.cn/Cameras/Sony/A1');
INSERT INTO `devices` VALUES (4, 'A7C', 'Sony', 95, 14.7, 3407, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Sony4.png', 'https://www.dxomark.cn/Cameras/Sony/A7C');
INSERT INTO `devices` VALUES (5, 'A7SIII', 'Sony', 86, 13.9, 2520, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Sony5.png', 'https://www.dxomark.cn/Cameras/Sony/A7SIII');
INSERT INTO `devices` VALUES (6, 'A9 II', 'Sony', 93, 14, 3434, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Sony6.png', 'https://www.dxomark.cn/Cameras/Sony/a9-II');
INSERT INTO `devices` VALUES (7, 'EOS R3', 'Canon', 96, 14.7, 4086, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Canon1.png', 'https://www.dxomark.cn/cn/Cameras/Canon/EOS-R3');
INSERT INTO `devices` VALUES (8, 'EOS R5', 'Canon', 95, 14.6, 3042, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Canon2.png', 'https://www.dxomark.cn/cn/Cameras/Canon/EOS-R5');
INSERT INTO `devices` VALUES (9, 'EOS R8', 'Canon', 93, 14.7, 3295, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Canon3.png', 'https://www.dxomark.cn/cn/Cameras/Canon/EOS-R8');
INSERT INTO `devices` VALUES (10, 'EOS-1D X Mark III', 'Canon', 91, 14.5, 3248, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Canon4.png', 'https://www.dxomark.cn/cn/Cameras/Canon/EOS-1D-X-Mark-III');
INSERT INTO `devices` VALUES (11, 'EOS 5D Mark IV', 'Canon', 91, 13.6, 2995, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Canon5.png', 'https://www.dxomark.cn/cn/Cameras/Canon/EOS-5D-Mark-IV');
INSERT INTO `devices` VALUES (12, 'EOS R6', 'Canon', 90, 14.3, 3394, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Canon6.png', 'https://www.dxomark.cn/cn/Cameras/Canon/EOS-R6');
INSERT INTO `devices` VALUES (13, 'D850', 'Nikon', 100, 14.8, 2660, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Nikon1.png', 'https://www.dxomark.cn/cn/Cameras/Nikon/D850');
INSERT INTO `devices` VALUES (14, 'Z7II', 'Nikon', 100, 14.7, 2841, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Nikon2.png', 'https://www.dxomark.cn/cn/Cameras/Nikon/Z7II');
INSERT INTO `devices` VALUES (15, 'Z7', 'Nikon', 99, 14.6, 2668, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Nikon3.png', 'https://www.dxomark.cn/cn/Cameras/Nikon/Z7II');
INSERT INTO `devices` VALUES (16, 'Z8', 'Nikon', 98, 14.2, 2548, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Nikon4.png', 'https://www.dxomark.cn/cn/Cameras/Nikon/Z8');
INSERT INTO `devices` VALUES (17, 'Z9', 'Nikon', 98, 14.4, 2451, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Nikon5.png', 'https://www.dxomark.cn/cn/Cameras/Nikon/Z9');
INSERT INTO `devices` VALUES (18, 'D810', 'Nikon', 97, 14.8, 2853, '相机', 'http://sdxa2uyxf.bkt.gdipper.com/Nikon6.png', 'https://www.dxomark.cn/cn/Cameras/Nikon/D810');

-- ----------------------------
-- Table structure for follows
-- ----------------------------
DROP TABLE IF EXISTS `follows`;
CREATE TABLE `follows`  (
  `follow_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '关注记录ID',
  `follower_id` int(11) NULL DEFAULT NULL COMMENT '关注者的用户ID',
  `followed_id` int(11) NULL DEFAULT NULL COMMENT '被关注者的用户ID',
  `follow_time` datetime NULL DEFAULT NULL COMMENT '关注时间',
  PRIMARY KEY (`follow_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '关注记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of follows
-- ----------------------------
INSERT INTO `follows` VALUES (3, 3, 1, '2024-06-07 08:15:08');

-- ----------------------------
-- Table structure for likes
-- ----------------------------
DROP TABLE IF EXISTS `likes`;
CREATE TABLE `likes`  (
  `like_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '点赞记录ID',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '点赞用户ID',
  `liked_id` int(11) NULL DEFAULT NULL COMMENT '被赞作品ID',
  `like_time` datetime NULL DEFAULT NULL COMMENT '点赞时间',
  `like_type` int(11) NULL DEFAULT NULL COMMENT '点赞类型:1-作品点赞,2-评论点赞',
  PRIMARY KEY (`like_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of likes
-- ----------------------------
INSERT INTO `likes` VALUES (2, 3, 12, '2024-06-07 08:09:23', 1);
INSERT INTO `likes` VALUES (3, 3, 13, '2024-06-07 08:09:25', 1);
INSERT INTO `likes` VALUES (7, 3, 23, '2024-06-07 08:09:32', 1);
INSERT INTO `likes` VALUES (8, 3, 18, '2024-06-07 08:09:35', 1);
INSERT INTO `likes` VALUES (9, 2, 26, '2024-06-07 08:11:42', 1);
INSERT INTO `likes` VALUES (10, 2, 24, '2024-06-07 08:12:21', 1);
INSERT INTO `likes` VALUES (11, 3, 26, '2024-06-07 08:15:43', 1);
INSERT INTO `likes` VALUES (13, 3, 24, '2024-06-07 08:15:47', 1);
INSERT INTO `likes` VALUES (15, 3, 20, '2024-06-07 08:15:50', 1);
INSERT INTO `likes` VALUES (16, 3, 19, '2024-06-07 08:15:53', 1);
INSERT INTO `likes` VALUES (18, 3, 27, '2024-06-07 08:16:37', 1);
INSERT INTO `likes` VALUES (19, 3, 36, '2024-06-07 08:20:17', 1);
INSERT INTO `likes` VALUES (20, 3, 33, '2024-06-07 08:20:19', 1);
INSERT INTO `likes` VALUES (21, 3, 35, '2024-06-07 08:20:22', 1);
INSERT INTO `likes` VALUES (22, 1, 12, '2024-06-07 08:49:43', 1);

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `notice_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '发布公告的用户ID',
  `notice_name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '公告标题',
  `notice_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '公告内容',
  `notice_time` datetime NULL DEFAULT NULL COMMENT '公告发布时间',
  `notice_picture` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图片的URL',
  PRIMARY KEY (`notice_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '公告信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------

-- ----------------------------
-- Table structure for places
-- ----------------------------
DROP TABLE IF EXISTS `places`;
CREATE TABLE `places`  (
  `place_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '地点ID',
  `place_name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '具体地点',
  `place_x` float NULL DEFAULT NULL COMMENT '经度',
  `place_y` float NULL DEFAULT NULL COMMENT '维度',
  `place_img` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图片的URL',
  PRIMARY KEY (`place_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '地点信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of places
-- ----------------------------
INSERT INTO `places` VALUES (1, '中国人民大学公共教学1楼', 116.316, 39.9686, 'http://sdxa2uyxf.bkt.gdipper.com/%E4%BA%BA%E5%A4%A7%E5%85%AC%E6%95%99%E4%B8%80%E6%A5%BC1.jpg');
INSERT INTO `places` VALUES (2, '中国人民大学明德广场', 116.308, 39.9714, 'http://sdxa2uyxf.bkt.gdipper.com/%E4%BA%BA%E5%A4%A7%E6%98%8E%E5%BE%B7%E6%A5%BC1.jpg');
INSERT INTO `places` VALUES (3, '中国人民大学明德广场', 116.308, 39.9716, 'http://sdxa2uyxf.bkt.gdipper.com/%E4%BA%BA%E5%A4%A7%E6%98%8E%E5%BE%B7%E6%A5%BC2.jpg');
INSERT INTO `places` VALUES (4, '中国人民大学逸夫会堂', 116.316, 39.9701, 'http://sdxa2uyxf.bkt.gdipper.com/%E6%98%9F%E8%BD%AC%E9%80%B8%E5%A4%AB%E5%A0%821.jpg');
INSERT INTO `places` VALUES (5, '中国人民大学图书馆', 116.316, 39.972, 'http://sdxa2uyxf.bkt.gdipper.com/%E5%9B%BE%E4%B9%A6%E9%A6%86%E6%98%9F%E8%BD%A81.jpg');
INSERT INTO `places` VALUES (6, '中国人民大学博物馆', 116.314, 39.9699, 'http://sdxa2uyxf.bkt.gdipper.com/%E4%BA%BA%E5%A4%A7%E5%8D%9A%E7%89%A9%E9%A6%861.jpg');
INSERT INTO `places` VALUES (7, '中国人民大学藏书馆', 116.313, 39.9708, 'http://sdxa2uyxf.bkt.gdipper.com/%E4%BA%BA%E5%A4%A7%E8%97%8F%E4%B9%A6%E9%A6%861.jpg');
INSERT INTO `places` VALUES (8, '故宫博物院-午门', 116.397, 39.9133, 'https://rmrbcmsonline.peopleapp.com/rb_recsys/img/2019/1230/311515_396251089827000320.jpeg');
INSERT INTO `places` VALUES (9, '天安门城楼', 116.397, 39.9087, 'https://img0.baidu.com/it/u=2591868193,482476247&fm=253&fmt=auto&app=120&f=JPEG?w=889&h=500');
INSERT INTO `places` VALUES (10, '故宫太和殿', 116.397, 39.9172, 'https://img0.baidu.com/it/u=3546216388,2844115986&fm=253&fmt=auto&app=138&f=JPEG?w=889&h=500');
INSERT INTO `places` VALUES (11, NULL, NULL, 39.9253, NULL);
INSERT INTO `places` VALUES (12, NULL, NULL, 39.9257, NULL);
INSERT INTO `places` VALUES (13, NULL, NULL, 39.9037, NULL);
INSERT INTO `places` VALUES (14, NULL, NULL, 39.905, NULL);
INSERT INTO `places` VALUES (16, NULL, NULL, 39.9034, NULL);

-- ----------------------------
-- Table structure for resetpasswd
-- ----------------------------
DROP TABLE IF EXISTS `resetpasswd`;
CREATE TABLE `resetpasswd`  (
  `reset_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '重置密码请求ID',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户ID',
  `reset_date` datetime NULL DEFAULT NULL COMMENT '请求重置密码的日期时间',
  `old_passwd` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户原密码',
  `new_passwd` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户新密码',
  PRIMARY KEY (`reset_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '重置密码表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resetpasswd
-- ----------------------------
INSERT INTO `resetpasswd` VALUES (1, 1, '2024-06-07 04:52:40', '', '');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `user_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户登录名',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户密码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户昵称',
  `birthday` datetime NULL DEFAULT NULL COMMENT '用户生日',
  `gender` tinyint(1) NULL DEFAULT NULL COMMENT '用户性别，True为男性，False为女性',
  `photo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户头像URL',
  `power` int(11) NULL DEFAULT NULL COMMENT '用户权限等级',
  `self_description` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '用户自我描述',
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户邮箱',
  `register_time` datetime NULL DEFAULT NULL COMMENT '用户注册时间',
  `last_login` datetime NULL DEFAULT NULL COMMENT '用户最后登录时间',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'WannWindy', '50a11ccc74764d73faa2918773d2eb78', 'iiiii', NULL, 1, 'https://ts1.cn.mm.bing.net/th/id/R-C.232904c2ee9450d3afabd2c553477793?rik=Wrs6xV46pcnU%2fg&riu=http%3a%2f%2fwww.sucaijishi.com%2fuploadfile%2f2016%2f0203%2f20160203022635285.png&ehk=qK8HIsKsLMdhbBUdvvlQJnmEw7K%2fpbcfFp5ZrHO2F9w%3d&risl=&pid=ImgRaw&r=0', 2, NULL, 'wann2333@ruc.edu.cn', '2024-06-07 03:10:39', '2024-06-07 08:48:17');
INSERT INTO `users` VALUES (2, 'Harvey', 'e964284b6dc4b66e5abd85f32ac01209', 'Harvey', NULL, 1, 'https://ts1.cn.mm.bing.net/th/id/R-C.232904c2ee9450d3afabd2c553477793?rik=Wrs6xV46pcnU%2fg&riu=http%3a%2f%2fwww.sucaijishi.com%2fuploadfile%2f2016%2f0203%2f20160203022635285.png&ehk=qK8HIsKsLMdhbBUdvvlQJnmEw7K%2fpbcfFp5ZrHO2F9w%3d&risl=&pid=ImgRaw&r=0', 1, NULL, 'runharvey@163.com', '2024-06-07 07:37:39', '2024-06-07 08:48:18');
INSERT INTO `users` VALUES (3, 'Mira', '08f80b1a7d0a2867d68060da61e3e27b', 'Mira', NULL, 1, 'https://ts1.cn.mm.bing.net/th/id/R-C.232904c2ee9450d3afabd2c553477793?rik=Wrs6xV46pcnU%2fg&riu=http%3a%2f%2fwww.sucaijishi.com%2fuploadfile%2f2016%2f0203%2f20160203022635285.png&ehk=qK8HIsKsLMdhbBUdvvlQJnmEw7K%2fpbcfFp5ZrHO2F9w%3d&risl=&pid=ImgRaw&r=0', 1, NULL, '657735312@qq.com', '2024-06-07 08:03:17', '2024-06-07 08:48:34');

-- ----------------------------
-- Table structure for works
-- ----------------------------
DROP TABLE IF EXISTS `works`;
CREATE TABLE `works`  (
  `artwork_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '作品ID',
  `artwork_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '作品名称',
  `artwork_description` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '作品描述',
  `artwork_time` datetime NULL DEFAULT NULL COMMENT '作品发布时间',
  `artwork_type` int(11) NULL DEFAULT NULL COMMENT '摄影类型:1-风光,2-人文,3-人像,4-静物,5-其他',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '发布用户ID',
  `artwork_picture` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图片的URL',
  `keyword1` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '关键词1',
  `keyword2` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '关键词2',
  `keyword3` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '关键词3',
  `keyword4` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '关键词4',
  `keyword5` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '关键词5',
  PRIMARY KEY (`artwork_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '图片作品信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of works
-- ----------------------------
INSERT INTO `works` VALUES (12, '春江水暖谁先知', '', '2024-06-07 07:41:29', 1, 2, 'http://sdxa2uyxf.bkt.gdipper.com/3-NEF_DxO_DeepPRIME.jpg', '野鸭', '绿头鸭', '盆栽植物', '自行车', '鸟类');
INSERT INTO `works` VALUES (13, '人大信管院庆晚会', '七十周年院庆晚会', '2024-06-07 07:43:15', 5, 2, 'http://sdxa2uyxf.bkt.gdipper.com/IMG_0855.jpg', '工作总结表彰大会', '预备会议', '总结表彰大会', '多功能报告厅', '总结大会');
INSERT INTO `works` VALUES (15, '美丽的他', '美丽的他', '2024-06-07 07:44:19', 4, 2, 'http://sdxa2uyxf.bkt.gdipper.com/20221103145019.jpg', '头发', '美女', '秀发', '钢笔画', '时装T台');
INSERT INTO `works` VALUES (18, '春风正好', '花色满堂', '2024-06-07 07:51:29', 4, 2, 'http://sdxa2uyxf.bkt.gdipper.com/20230326115652.jpg', '花朵', '春天', '风景', '树', '湖泊');
INSERT INTO `works` VALUES (19, '好似山水画', '空山新雨后，天气晚来秋。 明月松间照，清泉石上流。', '2024-06-07 07:52:17', 1, 1, 'http://sdxa2uyxf.bkt.gdipper.com/7b8c48f0.jpg', '绘画', '云雾', '江河', '山峦', '湖泊');
INSERT INTO `works` VALUES (20, '风景照', '11111', '2024-06-07 07:52:40', 1, 1, 'http://sdxa2uyxf.bkt.gdipper.com/9288c1c22.jpg', '风景', '天空', '草原', '瑞士', '树');
INSERT INTO `works` VALUES (21, '激烈的篮球赛', '热血拼搏！', '2024-06-07 07:52:52', 4, 2, 'http://sdxa2uyxf.bkt.gdipper.com/DSC_3196.jpg', '美女', '合照', '篮球赛', '女孩', '情侣');
INSERT INTO `works` VALUES (23, '光影', '', '2024-06-07 07:54:40', 2, 1, 'http://sdxa2uyxf.bkt.gdipper.com/gy27b035d679.jpg', '巷道', '屏幕截图', '城市街道', '民居', '地下通道');
INSERT INTO `works` VALUES (24, '新春', '', '2024-06-07 07:55:09', 2, 1, 'http://sdxa2uyxf.bkt.gdipper.com/xc91b147.jpg', '街道', '楹联', '商场', '建筑', '门');
INSERT INTO `works` VALUES (25, '雪地打猎', '亚瑟摩根', '2024-06-07 07:55:52', 2, 2, 'http://sdxa2uyxf.bkt.gdipper.com/7.png', '卡通动漫人物', '工艺品', '天空', '图画', '屏幕截图');
INSERT INTO `works` VALUES (26, '日本的地铁站', '', '2024-06-07 07:56:51', 2, 1, 'http://sdxa2uyxf.bkt.gdipper.com/jpbe35f.jpg', '卡通动漫人物', '屏幕截图', '桌式足球', '羽毛球赛', '羽毛球俱乐部');
INSERT INTO `works` VALUES (27, '欧洲街头', '', '2024-06-07 07:58:38', 2, 1, 'http://sdxa2uyxf.bkt.gdipper.com/jtf79aad.jpg', '民俗活动', '婚车', '短号', '济州岛泰迪熊博物馆', '拖把');
INSERT INTO `works` VALUES (28, '退潮后的扑克牌', '', '2024-06-07 07:59:58', 3, 2, 'http://sdxa2uyxf.bkt.gdipper.com/q1.jpg', '扑克', '打火机', '村道', '中式传统建筑', '钱包');
INSERT INTO `works` VALUES (29, '蜡烛 | 静物摄影', '', '2024-06-07 08:00:14', 3, 1, 'http://sdxa2uyxf.bkt.gdipper.com/lzb799d.jpg', '蜡烛', '蜡烛芯', '打火机', '火柴杆', '比赛');
INSERT INTO `works` VALUES (30, '陶瓷', '', '2024-06-07 08:01:19', 3, 1, 'http://sdxa2uyxf.bkt.gdipper.com/tcf3fe.jpg', '瓷器', '工艺品', '花瓶', '瓶子', '瓷瓶');
INSERT INTO `works` VALUES (31, '花瓶', '', '2024-06-07 08:02:47', 3, 1, 'http://sdxa2uyxf.bkt.gdipper.com/hhh5341.jpg', '仿真花', '仿真花卉', '花束', '艺术插花', '油画');
INSERT INTO `works` VALUES (33, '春天的明德楼～', '太美啦', '2024-06-07 08:08:54', 3, 3, 'http://sdxa2uyxf.bkt.gdipper.com/7.jpg', '花卉', '植物', '文字图片', '庙会', '婚礼');
INSERT INTO `works` VALUES (34, '秋', '', '2024-06-07 08:10:46', 3, 3, 'http://sdxa2uyxf.bkt.gdipper.com/4.jpg', '油画', '湖泊', '江河', '峡谷', '生态林');
INSERT INTO `works` VALUES (35, '好喜欢这样的生命力！！', '', '2024-06-07 08:12:07', 4, 3, 'http://sdxa2uyxf.bkt.gdipper.com/1_TheAehT_.jpg', '婚纱写真', '42式太极拳', '对练', '太极拳', '合气道');
INSERT INTO `works` VALUES (36, '我眼中的香港', '', '2024-06-07 08:13:01', 2, 3, 'http://sdxa2uyxf.bkt.gdipper.com/1_TommyTian_.jpg', '街道', '现代建筑', '都市夜景', '建筑', '居民楼');
INSERT INTO `works` VALUES (37, '夜晚街拍的光影艺术', '', '2024-06-07 08:14:19', 2, 3, 'http://sdxa2uyxf.bkt.gdipper.com/55_4___.jpg', '街道', '检票口', '灯', '门', '显示器屏幕');
INSERT INTO `works` VALUES (38, '和树影晃来晃去的初夏', '似乎每个夏天\r\n都是窗外近乎弥烂的绿', '2024-06-07 08:17:40', 2, 3, 'http://sdxa2uyxf.bkt.gdipper.com/1_hey.juice_.jpg', '树', '自然公园', '城市街道', '寺塔', '巷道');
INSERT INTO `works` VALUES (39, '相濡以沫', '在路上偶遇了爱情❤️', '2024-06-07 08:18:50', 4, 3, 'http://sdxa2uyxf.bkt.gdipper.com/GuoSy__.jpg', '人物特写', '植物', '街道', '树', '长城');
INSERT INTO `works` VALUES (40, '相濡以沫', '在路上偶遇了爱情❤️', '2024-06-07 08:18:50', 4, 3, 'http://sdxa2uyxf.bkt.gdipper.com/GuoSy__.jpg', '人物特写', '植物', '街道', '树', '长城');
INSERT INTO `works` VALUES (41, '相濡以沫', '在路上偶遇了爱情❤️', '2024-06-07 08:18:50', 4, 3, 'http://sdxa2uyxf.bkt.gdipper.com/GuoSy__.jpg', '人物特写', '植物', '街道', '树', '长城');
INSERT INTO `works` VALUES (42, '123', '123455', '2024-06-07 08:45:24', 2, 4, 'http://sdxa2uyxf.bkt.gdipper.com/12755.jpg', '城楼', '北京天安门', '钢笔画', '大阅兵', '卡通动漫人物');

SET FOREIGN_KEY_CHECKS = 1;
