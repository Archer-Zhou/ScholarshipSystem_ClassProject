import pymysql
import random 
import pandas as pd

def reset():

    #随机生成银行卡号写入文件
    s='6217'
    card_num =[]
    flag= 20
    while flag:
        s='6217'
        for i in range(19):
            s = s+str(random.randint(0,10))
        if s not in card_num:
            card_num.append(s)
            flag = flag-1
    
    print(card_num)
    
    df = pd.read_excel('./data.xlsx',sheet_name='Sheet1')
    df['银行卡号'] = card_num
    pd.DataFrame(df).to_excel('data.xlsx', sheet_name='Sheet1', index=False, header=True)
    
    # 打开数据库
    db = pymysql.connect(host='localhost',port =3306,user='root',passwd='123456',db='scholarship',charset='utf8' )
     
    #使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    SQL = """CREATE DATABASE `scholarship`"""
    
    SQL1 = """DROP TABLE IF EXISTS `stu_info`"""
    SQL2 = """CREATE TABLE `stu_info` (
      `stu_id` varchar(32) NOT NULL COMMENT '学号',
      `stu_name` varchar(32) NOT NULL COMMENT '姓名',
      `stu_major` varchar(32) NOT NULL COMMENT '专业',
      `stu_class` varchar(32) NOT NULL COMMENT '班级',
      `card_num` varchar(32) NOT NULL COMMENT '银行卡号',
      `stu_scholarship` enum('是','否') NOT NULL COMMENT '奖学金有无',
      `stu_scholarship_status` enum('是','否') NOT NULL COMMENT '奖学金发放情况',
      PRIMARY KEY (`stu_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
    """
    cursor.execute(SQL1)
    cursor.execute(SQL2)
    #使用innodb引擎，数据库默认编码为utf-8
    # 创建插入SQL语句
    insert_sql = "insert into stu_info values (%s, %s, %s, %s, %s, %s, %s);"
    stu_data = pd.read_excel('./data.xlsx',sheet_name='Sheet1')
    # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题
    for i in range(len(stu_data)):
          stu_id   = str(stu_data.iloc[i,0])
          stu_name = str(stu_data.iloc[i,1])
          stu_major  = str(stu_data.iloc[i,2])
          stu_class =str(stu_data.iloc[i,3])
          card_num  = str(stu_data.iloc[i,4])
          stu_scholarship = str(stu_data.iloc[i,5])
          stu_scholarship_status = str(stu_data.iloc[i,6])
          values = (stu_id, stu_name, stu_major, stu_class, card_num, stu_scholarship, stu_scholarship_status)
          cursor.execute(insert_sql, values)
    cursor.connection.commit()      
    
    SQL8 = """DROP TABLE IF EXISTS `users`;"""
    SQL9 = """CREATE TABLE `users` (
      `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户id',
      `user_name` varchar(32) NOT NULL COMMENT '用户名',
      `user_password` varchar(23) NOT NULL COMMENT '登录密码',
      PRIMARY KEY (`id`),
      UNIQUE KEY `user_name` (`user_name`)
    ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
    """
    cursor.execute(SQL8)
    cursor.execute(SQL9)
    
    #SQL10 = """LOCK TABLES `users` WRITE;"""
    
    SQL11 = """INSERT INTO `users` VALUES (1,'admin','123456'),(2,'momobaba','123456');"""
    cursor.execute(SQL11)
    cursor.connection.commit()  
    
    #SQL12 = """UNLOCK TABLES;"""
    
    db.close()
    
if __name__ == '__main__':
    reset()