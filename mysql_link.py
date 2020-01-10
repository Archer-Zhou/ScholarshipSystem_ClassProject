import pymysql

class Sql(object):
    """数据库操作"""
    def __init__(self,dbname):
        self.dbname = dbname
        self.db = pymysql.connect(host = 'localhost', user = 'root', password \
                                  = '123456', db = self.dbname, charset = "utf8")
        #游标
        self.cursor = self.db.cursor()
        
    def SelectAll(self,tablename):
        self.tablename = tablename
        
        sql = "select * from %s"%(self.tablename)
        try:
            #执行数据库操作
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data			
        except Exception as err:
            print("SQL执行错误，原因：",err)
        
    def Insert(self, stu_id, stu_name, stu_major, stu_class, card_num, stu_scholarship, \
               stu_scholarship_status):
        self.stu_id = stu_id
        self.stu_name = stu_name
        self.stu_major = stu_major
        self.stu_class = stu_class
        self.card_num = card_num
        self.stu_scholarship = stu_scholarship
        self.stu_scholarship_status = stu_scholarship_status
        sql = "insert into stu_info values('%s','%s','%s','%s','%s','%s','%s')"%(self.stu_id,self.stu_name,\
                                          self.stu_major,self.stu_class,self.card_num,self.stu_scholarship,self.stu_scholarship_status)
        self.Tryit(sql)
            
        
    def Update(self,stu_id, stu_name, stu_major, stu_class, card_num, stu_scholarship, stu_scholarship_status):
        self.stu_id = stu_id
        print (self.stu_id)
        self.stu_name = stu_name
        self.stu_major = stu_major
        self.stu_class = stu_class
        self.card_num = card_num
        self.stu_scholarship = stu_scholarship
        self.stu_scholarship_status = stu_scholarship_status
        sql = "update stu_info set stu_name='%s',stu_major='%s',stu_class='%s',card_num='%s',stu_scholarship='%s',stu_scholarship_status='%s' where stu_id = '%s'"%(self.stu_name,self.stu_major,self.stu_class,self.card_num,self.stu_scholarship,self.stu_scholarship_status,self.stu_id)
        self.Tryit(sql)
            
    def Oneclick(self):
        sql = "update stu_info set stu_scholarship_status = '是' where stu_scholarship = '是'"
        self.Tryit(sql)
        
    def Del(self, stu_id):
        self.stu_id = stu_id
        sql = "delete from stu_info where stu_id=%d"%(self.stu_id)
        self.Tryit(sql)
        
    def Tryit(self,sql):
        print(sql)
        try:
            #执行数据库操作
            self.cursor.execute(sql)
            #事务提交
            self.db.commit()
        except Exception as err:
            #事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：",err)
    
    def __del__(self):
        self.db.close()