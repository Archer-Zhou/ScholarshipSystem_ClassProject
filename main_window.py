# -*- coding: utf-8 -*-
import wx
import wx.grid
from mysql_link import Sql
#import database
from pymysql import connect
from random import randint
from pandas import read_excel
from pandas import DataFrame

ID_RES = wx.NewId()
ID_SEL = wx.NewId()
ID_ADD = wx.NewId()
ID_UPD = wx.NewId()
ID_ONE = wx.NewId()
STU_ID = 0
#系统登录界面类
class UserLogin(wx.Frame):
    def __init__(self,*args, **kw):
        super(UserLogin, self).__init__(*args, **kw)
        self.sql = Sql("scholarship")
        self.Center()
        self.pnl = wx.Panel(self)
        self.LoginInterface()
        #菜单栏
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        quit_item = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit')
        reset_item = wx.MenuItem(fileMenu, ID_RES, 'Reset')
        fileMenu.Append(quit_item)
        fileMenu.Append(reset_item)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.exitsys, id = wx.ID_EXIT) 
        self.Bind(wx.EVT_MENU, self.resetdata, id = ID_RES)
    #登录界面
    def LoginInterface(self):
        
		#创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl,label="奖学金管理系统")
        font = logo.GetFont()
        font.PointSize += 30
        font = font.Bold()
        logo.SetFont(font)

        #用户名和密码框
        user_label = wx.StaticText(self.pnl, label = "用户名：")
        password_label = wx.StaticText(self.pnl, label = "密  码：")
        self.user_text = wx.TextCtrl(self.pnl ,size = (200,20))
        self.password_text = wx.TextCtrl(self.pnl ,size = (200,20), style=wx.TE_PASSWORD)
        
        #登录按钮
        login_button = wx.Button(self.pnl, label = "登录", size = (80,20))
        login_button.Bind(wx.EVT_BUTTON, self.LoginButton)
        
        
        #添加到各个horizontal box布局管理器
        hb_sizer_user = wx.BoxSizer(wx.HORIZONTAL)
        hb_sizer_password = wx.BoxSizer(wx.HORIZONTAL)
        hb_sizer_login = wx.BoxSizer(wx.HORIZONTAL)
        
        hb_sizer_user.Add(user_label, 0, wx.EXPAND, wx.BOTTOM, 5)
        hb_sizer_user.Add(self.user_text, 0, wx.EXPAND, wx.BOTTOM, 5)
        
        hb_sizer_password.Add(password_label, 0, wx.EXPAND, wx.BOTTOM, 5)
        hb_sizer_password.Add(self.password_text, 0, wx.EXPAND, wx.BOTTOM, 5)
        
        hb_sizer_login.Add(login_button, 0, wx.EXPAND, wx.BOTTOM, 5)
        
        #添加到vertical box布局管理器
        vb_sizer = wx.BoxSizer(wx.VERTICAL)
        vb_sizer.Add(logo,proportion=0,flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER,border=50)
        vb_sizer.Add(hb_sizer_user, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 10)
        vb_sizer.Add(hb_sizer_password, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 10)
        vb_sizer.Add(hb_sizer_login, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 10)
        #设置面板的布局管理器
        self.pnl.SetSizer(vb_sizer)	
 
    #登录按钮事件
    def LoginButton(self,event):
        #连接数据库
        #op = Sql("scholarship")
        #获取users表中的用户名和密码信息，返回为二维元组
        np = self.sql.SelectAll("users")
        print(np)
        login_sign = 0
        #匹配用户名和密码
        for i in np:
            if (i[1] == self.user_text.GetValue()) and (i[2] == self.password_text.GetValue()):
                login_sign = 1
                break
        if login_sign == 0:
            print("用户名或密码错误！")
        elif login_sign == 1:
            print("登录成功！")			
            operation = UserWindow(None,title="学生奖学金管理系统",size=(1024,668))
            operation.Show()
            self.Close(True)
            
    def resetdata(self,event):
        reset()
        
    def exitsys(self, event):
        self.Close(True)
    
#用户使用界面类        
class UserWindow(wx.Frame):
    def __init__(self,*args,**kw):
        # ensure the parent's __init__ is called
        super(UserWindow,self).__init__(*args, **kw)
        self.Center()
        self.pnl = wx.Panel(self)
        self.sql = Sql("scholarship")
        self.OperationInterface()
        #操作界面
        #菜单栏
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        #self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.exitsys, fileItem)
    def OperationInterface(self):


        #分两个子窗口
        self.sb_button = wx.StaticBox(self.pnl,label="选择操作", size = (200, 500))
        self.sb_show_operation = wx.StaticBox(self.pnl,label="显示/操作窗口",size=(800,500))
        #操作按钮 + 绑定事件
        check_button = wx.Button(self.pnl,id=ID_SEL,label="查看学生信息",size=(150,50))
        add_button = wx.Button(self.pnl,id=ID_ADD,label="添加学生信息",size=(150,50))
        update_button = wx.Button(self.pnl,id=ID_UPD,label="更新学生信息",size=(150,50))
        delete_button = wx.Button(self.pnl,id=wx.ID_DELETE,label="删除学生信息",size=(150,50))
        oneclick_button = wx.Button(self.pnl,id=ID_ONE,label="一键发钱",size=(150,50))
        quit_button = wx.Button(self.pnl,id=wx.ID_EXIT,label="退出系统",size=(150,50))
        
        self.Bind(wx.EVT_BUTTON, self.selectall, id = ID_SEL)
        self.Bind(wx.EVT_BUTTON, self.insert, id = ID_ADD)
        self.Bind(wx.EVT_BUTTON, self.delrow, id = wx.ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self.exitsys, id = wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.update, id = ID_UPD)
        self.Bind(wx.EVT_BUTTON, self.oneclick, id = ID_ONE)
        
        
        #整体 布局管理器
        self.vb_sizer = wx.BoxSizer(wx.VERTICAL)
        hb_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #子窗口 布局管理器
        vb_sizer_button = wx.StaticBoxSizer(self.sb_button, wx.VERTICAL)
        self.vsbox_show_operation = wx.StaticBoxSizer(self.sb_show_operation,wx.VERTICAL)
        
        vb_sizer_button.Add(check_button,0,wx.EXPAND | wx.BOTTOM,40)
        vb_sizer_button.Add(add_button,0,wx.EXPAND | wx.BOTTOM,40)
        vb_sizer_button.Add(update_button,0,wx.EXPAND | wx.BOTTOM,40)
        vb_sizer_button.Add(delete_button,0,wx.EXPAND | wx.BOTTOM,40)
        vb_sizer_button.Add(oneclick_button,0,wx.EXPAND | wx.BOTTOM,40)
        vb_sizer_button.Add(quit_button,0,wx.EXPAND | wx.BOTTOM,40)
        
        
        hb_sizer.Add(vb_sizer_button,0,wx.EXPAND | wx.LEFT | wx.TOP |wx.RIGHT,10)
        hb_sizer.Add(self.vsbox_show_operation,0,wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,10)	
        self.vb_sizer.Add(hb_sizer, 0, wx.CENTER)		
        #调用
        self.pnl.SetSizer(self.vb_sizer)
        #self.SetMenuBar(menubar)
    #事件函数
    def selectall(self, event):
        #调用选择界面
        inquire = SelectOp(None,title="学生奖学金管理系统",size=(1024,668))
        inquire.Show()
        self.Close(True)
    def insert(self, event):
        add_button = AddOp(None,title="学生奖学金管理系统",size=(1024,668))
        add_button.Show()
        self.Close(True)
    def delrow(self, event):
        del_button = DelOp(None,title="学生奖学金管理系统",size=(1024,668))
        del_button.Show()
        self.Close(True)	
    def exitsys(self, event):
        self.Close(True)
    def update(self, event):
        del_button = UpdateOp(None,title="学生奖学金管理系统",size=(1024,668))
        del_button.Show()
        self.Close(True)
        
    def oneclick(self,event):
        self.sql.Oneclick()
        inquire = SelectOp(None,title="学生奖学金管理系统",size=(1024,668))
        inquire.Show()
        self.Close(True)
        
#选择结果界面
class SelectOp(UserWindow):
	def __init__(self,*args,**kw):
		# ensure the parent's __init__ is called
		super(SelectOp,self).__init__(*args, **kw)
		#创建学生信息网格		
		self.stu_grid = self.CreateGrid()			
		
        
        #self.update_buttom = wx.Buttom()wx.Button(self.sb_show_operation,id=21,label="更新",size=(100,30))
		#添加到vsbox_show_operation运行边布局管理器
		self.vsbox_show_operation.Add(self.stu_grid,0,wx.CENTER | wx.FIXED_MINSIZE,30)		

	def CreateGrid(self):
		#连接login_users数据库
		
		#获取stu_information表中的学生信息，返回为二维元组
		np = self.sql.SelectAll("stu_info")
		column_names = ("姓名","专业","班级","银行卡号","有无奖学金","发放情况")
		stu_grid = wx.grid.Grid(self.pnl)
		stu_grid.CreateGrid(len(np),len(np[0])-1)
		for row in range(len(np)):
			stu_grid.SetRowLabelValue(row,str(np[row][0]))#确保网格序列号与数据库id保持一致
			for col in range(1,len(np[row])):
				stu_grid.SetColLabelValue(col-1,column_names[col-1])				
				stu_grid.SetCellValue(row,col-1,str(np[row][col]))				
		stu_grid.AutoSize()
		return stu_grid

        
#添加界面
class AddOp(UserWindow):
	def __init__(self,*args,**kw):
		# ensure the parent's __init__ is called
		super(AddOp,self).__init__(*args, **kw)
		self.stu_id = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_name = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_major = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_class = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_card = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_scholarship = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_status = wx.TextCtrl(self.pnl,size = (210,25))
		self.add_affirm = wx.Button(self.pnl,label="添加",size=(80,25))
		#为添加按钮组件绑定事件处理
		self.add_affirm.Bind(wx.EVT_BUTTON,self.AddAffirm)
		#################################################################################
		sb_id = wx.StaticBox(self.pnl,label="学  号")
		sb_name = wx.StaticBox(self.pnl,label="姓  名")
		sb_major = wx.StaticBox(self.pnl,label="专  业")
		sb_class = wx.StaticBox(self.pnl,label="班  级")
		sb_card = wx.StaticBox(self.pnl,label="银行卡号")
		sb_scholarship = wx.StaticBox(self.pnl,label="有无奖学金")
		sb_stutas = wx.StaticBox(self.pnl,label="发放状态")		
		hsbox_id = wx.StaticBoxSizer(sb_id,wx.HORIZONTAL)
		hsbox_name = wx.StaticBoxSizer(sb_name,wx.HORIZONTAL)
		hsbox_major = wx.StaticBoxSizer(sb_major,wx.HORIZONTAL)
		hsbox_class = wx.StaticBoxSizer(sb_class,wx.HORIZONTAL)
		hsbox_card = wx.StaticBoxSizer(sb_card,wx.HORIZONTAL)
		hsbox_scholarship = wx.StaticBoxSizer(sb_scholarship,wx.HORIZONTAL)
		hsbox_status = wx.StaticBoxSizer(sb_stutas,wx.HORIZONTAL)
		hsbox_id.Add(self.stu_id,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_name.Add(self.stu_name,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_major.Add(self.stu_major,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_class.Add(self.stu_class,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_card.Add(self.stu_card,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_scholarship.Add(self.stu_scholarship,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_status.Add(self.stu_status,0,wx.EXPAND | wx.BOTTOM,5)
		#################################################################################
		self.vsbox_show_operation.Add(hsbox_id,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_name,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_major,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_class,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_card,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_scholarship,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_status,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(self.add_affirm,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)


	def AddAffirm(self,event):
		#连接login_users数据库
		
		stu_id = self.stu_id.GetValue()
		stu_name = self.stu_name.GetValue()
		stu_major = self.stu_major.GetValue()
		stu_class = self.stu_class.GetValue()
		stu_card = self.stu_card.GetValue()
		stu_scholarship = self.stu_scholarship.GetValue()
		stu_status = self.stu_status.GetValue()
		np = self.sql.Insert(stu_id,stu_name,stu_major,stu_class,stu_card,stu_scholarship,stu_status)
		del_button = DelOp(None,title="学生奖学金管理系统",size=(1024,668))	
		del_button.Show()
		self.Close(True)
		#stu_status = self.stu_status.GetValue()
		#print(stu_status)
		#np = self.sql.Insert(stu_id,stu_name,stu_major,stu_class,stu_card,stu_scholarship,stu_status)
class DelOp(SelectOp):
	def __init__(self,*args,**kw):
		# ensure the parent's __init__ is called
		super(DelOp,self).__init__(*args, **kw)
		#创建删除学员信息输入框、删除按钮
		self.del_id = wx.TextCtrl(self.pnl,pos = (407,78),size = (210,25))
		self.del_affirm = wx.Button(self.pnl,label="删除",pos=(625,78),size=(80,25))
		#为删除按钮组件绑定事件处理
		self.del_affirm.Bind(wx.EVT_BUTTON,self.DelAffirm)
		#################################################################################
		#创建静态框
		sb_del = wx.StaticBox(self.pnl,label="请选择需要删除的学生id")
		#创建水平方向box布局管理器
		hsbox_del = wx.StaticBoxSizer(sb_del,wx.HORIZONTAL)
		#添加到hsbox_name布局管理器
		hsbox_del.Add(self.del_id,0,wx.EXPAND | wx.BOTTOM,5)
		#添加到vsbox_show_operation布局管理器
		self.vsbox_show_operation.Add(hsbox_del,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(self.del_affirm,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)


	def DelAffirm(self,event):
		#连接login_users数据库
		#op = Sql("scholarship")
		#向stu_information表添加学生信息
		del_id = self.del_id.GetValue()
		print(del_id)
		np = self.sql.Del(int(del_id))
		
		del_button = DelOp(None,title="学生奖学金管理系统",size=(1024,668))
		del_button.Show()
		self.Close(True)
        



#选择更新id界面
class UpdateOp(SelectOp):
	def __init__(self,*args,**kw):
		# ensure the parent's __init__ is called
		super(UpdateOp,self).__init__(*args, **kw)
		#创建更新信息输入框、按钮
		self.up_id = wx.TextCtrl(self.pnl,pos = (407,78),size = (210,25))
		self.up_affirm = wx.Button(self.pnl,label="更新",pos=(625,78),size=(80,25))
		#为更新按钮组件绑定事件处理
		self.up_affirm.Bind(wx.EVT_BUTTON,self.UpdAffirm)
		#################################################################################
		#创建静态框
		sb_del = wx.StaticBox(self.pnl,label="请选择需要更新信息的学生id")
		#创建水平方向box布局管理器
		hsbox_del = wx.StaticBoxSizer(sb_del,wx.HORIZONTAL)
		#添加到hsbox_name布局管理器
		hsbox_del.Add(self.up_id,0,wx.EXPAND | wx.BOTTOM,5)
		#添加到vsbox_show_operation布局管理器
		self.vsbox_show_operation.Add(hsbox_del,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(self.up_affirm,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)



	def UpdAffirm(self,event):
		#保存
		#需要更新的id
		up_id = self.up_id.GetValue()
		print(up_id)
		
		global STU_ID
		STU_ID = up_id
		up_button = UpdateInputOp(None,title="学生奖学金管理系统",size=(1024,668))
		up_button.Show()
		self.Close(True)
        

#输入更新信息界面
class UpdateInputOp(UserWindow):
	def __init__(self,*args,**kw):
		# ensure the parent's __init__ is called
		super(UpdateInputOp,self).__init__(*args, **kw)
		#self.stu_id = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_name = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_major = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_class = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_card = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_scholarship = wx.TextCtrl(self.pnl,size = (210,25))
		self.stu_status = wx.TextCtrl(self.pnl,size = (210,25))
		self.upd_affirm = wx.Button(self.pnl,label="更新",size=(80,25))
		#为添加按钮组件绑定事件处理
		self.upd_affirm.Bind(wx.EVT_BUTTON,self.UpdAffirm)
		#################################################################################
		#sb_id = wx.StaticBox(self.pnl,label="学  号")
		sb_name = wx.StaticBox(self.pnl,label="姓  名")
		sb_major = wx.StaticBox(self.pnl,label="专  业")
		sb_class = wx.StaticBox(self.pnl,label="班  级")
		sb_card = wx.StaticBox(self.pnl,label="银行卡号")
		sb_scholarship = wx.StaticBox(self.pnl,label="有无奖学金")
		sb_stutas = wx.StaticBox(self.pnl,label="发放状态")		
		#hsbox_id = wx.StaticBoxSizer(sb_id,wx.HORIZONTAL)
		hsbox_name = wx.StaticBoxSizer(sb_name,wx.HORIZONTAL)
		hsbox_major = wx.StaticBoxSizer(sb_major,wx.HORIZONTAL)
		hsbox_class = wx.StaticBoxSizer(sb_class,wx.HORIZONTAL)
		hsbox_card = wx.StaticBoxSizer(sb_card,wx.HORIZONTAL)
		hsbox_scholarship = wx.StaticBoxSizer(sb_scholarship,wx.HORIZONTAL)
		hsbox_status = wx.StaticBoxSizer(sb_stutas,wx.HORIZONTAL)
		#hsbox_id.Add(self.stu_id,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_name.Add(self.stu_name,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_major.Add(self.stu_major,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_class.Add(self.stu_class,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_card.Add(self.stu_card,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_scholarship.Add(self.stu_scholarship,0,wx.EXPAND | wx.BOTTOM,5)
		hsbox_status.Add(self.stu_status,0,wx.EXPAND | wx.BOTTOM,5)
		#################################################################################
		#self.vsbox_show_operation.Add(hsbox_id,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_name,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_major,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_class,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_card,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_scholarship,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(hsbox_status,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)
		self.vsbox_show_operation.Add(self.upd_affirm,0,wx.CENTER | wx.TOP | wx.FIXED_MINSIZE,5)


	def UpdAffirm(self,event):
		global STU_ID
		stu_name = self.stu_name.GetValue()
		stu_major = self.stu_major.GetValue()
		print(stu_major)
		stu_class = self.stu_class.GetValue()
		print(stu_class)
		stu_card = self.stu_card.GetValue()
		print(stu_card)		
		stu_scholarship = self.stu_scholarship.GetValue()
		print(stu_scholarship)
		stu_status = self.stu_status.GetValue()
		print(stu_status)
		np = self.sql.Update(STU_ID,stu_name,stu_major,stu_class,stu_card,stu_scholarship,stu_status)
		up_button = UpdateOp(None,title="学生奖学金管理系统",size=(1024,668))
		up_button.Show()
		self.Close(True)

#重置数据库至初始默认状态
def reset():

    #随机生成银行卡号写入文件
    s='6217'
    card_num =[]
    flag= 20
    while flag:
        s='6217'
        for i in range(19):
            s = s+str(randint(0,10))
        if s not in card_num:
            card_num.append(s)
            flag = flag-1
    
    print(card_num)
    
    df = read_excel('./data.xlsx',sheet_name='Sheet1')
    df['银行卡号'] = card_num
    DataFrame(df).to_excel('data.xlsx', sheet_name='Sheet1', index=False, header=True)
    
    # 打开数据库
    db = connect(host='localhost',port =3306,user='root',passwd='123456',db='scholarship',charset='utf8' )
     
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
    stu_data = read_excel('./data.xlsx',sheet_name='Sheet1')
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
    app = wx.App()
    login = UserLogin(None,title="学生奖学金管理系统",size=(512,334))
    login.Show()
    app.MainLoop()