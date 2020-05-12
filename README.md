# SmartCloud
智云未来-个人金融投资数据计算服务

## Dev开发分支

更新计划
- 集成Tushare获取更多数据
- 通过爬虫程序获取每日中证提供的指数成分股（弥补JQDATA不足）

基于Django与Mysql的金融数据计算服务

通过聚宽JQDataSDK获取指数与相关成分股数据，计算指数估值数据。

搭配Jenkins，每日计算数据，生成html文件，推送邮件至个人邮箱，方便每日进行查看。

相关依赖：

Python 3.6.1(Anaconda)

Django 3.0

Mysql 5.7

JQDataSDK
