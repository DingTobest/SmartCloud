-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.7.29


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema sc_stock
--

CREATE DATABASE IF NOT EXISTS sc_stock;
USE sc_stock;

--
-- Definition of table `index_info`
--

DROP TABLE IF EXISTS `index_info`;
CREATE TABLE `index_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index_code` varchar(16) NOT NULL,
  `index_name` varchar(32) NOT NULL,
  `index_data_table` varchar(32) NOT NULL,
  `index_data_fund` varchar(32) NOT NULL,
  `start_date` date NOT NULL,
  `last_update_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_info_index_code_11c56675` (`index_code`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `index_info`
--

/*!40000 ALTER TABLE `index_info` DISABLE KEYS */;
INSERT INTO `index_info` (`id`,`index_code`,`index_name`,`index_data_table`,`index_data_fund`,`start_date`,`last_update_date`) VALUES 
 (1,'399106.XSHE','中证全指','QZZS.SC','','2005-01-04','2020-03-20'),
 (2,'000016.XSHG','上证50指数','000016.XSHG','','2005-01-04','2005-01-04'),
 (3,'000300.XSHG','沪深300','000300.XSHG','','2005-04-08','2020-03-28'),
 (4,'000905.XSHG','中证500指数','000905.XSHG','','2007-01-15','2020-02-08'),
 (5,'000852.XSHG','中证1000','000852.XSHG','','2014-10-17','2020-03-28'),
 (6,'399006.XSHE','创业板指','399006.XSHE','','2010-06-01','2020-03-28'),
 (7,'000992.XSHG','全指金融','000992.XSHG','','2011-08-02','2020-03-28'),
 (8,'000993.XSHG','全指信息','000993.XSHG','','2011-08-02','2020-03-28'),
 (9,'000991.XSHG','全指医药','000991.XSHG','','2011-08-02','2020-03-28'),
 (10,'000990.XSHG','全指消费','000990.XSHG','','2011-08-02','2020-03-28'),
 (11,'000922.XSHG','中证红利','000922.XSHG','','2008-05-26','2020-03-28'),
 (12,'399812.XSHE','中证养老','399812.XSHE','','2014-06-06','2020-03-28'),
 (14,'399967.XSHE','中证军工','399967.XSHE','','2013-12-26','2020-03-28');
INSERT INTO `index_info` (`id`,`index_code`,`index_name`,`index_data_table`,`index_data_fund`,`start_date`,`last_update_date`) VALUES 
 (15,'399610.XSHE','TMT50','399610.XSHE','','2010-11-08','2020-03-28'),
 (16,'399550.XSHE','央视50','399550.XSHE','','2012-06-06','2020-03-28'),
 (17,'399673.XSHE','创业板50','399673.XSHE','','2014-06-18','2020-03-28'),
 (18,'000807.XSHG','食品饮料','000807.XSHG','','2012-02-17','2020-03-28'),
 (19,'399417.XSHE','国证新能源汽车指数','399417.XSHE','','2014-09-24','2020-03-28');
/*!40000 ALTER TABLE `index_info` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
