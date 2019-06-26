# -*- coding: GB2312-80 -*-
import time,os,sched,threading
class 客户:
    """一个简单的客户实例"""
    def __init__(self,客户名字="初始门店",计划消费金额=25,到店=False,新客户=True,消费计划=["汉堡","薯条","可乐"],oth=""):
        self.客户名字 = 客户名字
        self.计划消费金额 = 计划消费金额
        self.到店 = 到店
        self.消费金额=0
        self.新客户=新客户
        self.消费计划=消费计划
        self.oth=oth
    def 消费(self):
        return self.消费金额
    def f(self):
        return 'hello world'
默认客户=客户()

class 员工:
    """一个简单的员工实例"""
    def __init__(self,员工名字="初始门店员工",员工能力=25,员工努力=0,员工工资=5000,员工工作状态=None):
        self.员工名字 = 员工名字
        self.员工能力 = 员工能力
        self.员工努力 = 员工努力
        self.员工工资 = 员工工资
        self.员工工作状态 = 员工工作状态
    def f(self):
        return 'hello world'
默认员工=员工()



class 门店:
    """一个简单的门店实例，静态门店"""
    class 门店报表:
        """一个简单的门店财务报表"""
        堂吃新顾客收入=0
        堂吃老顾客收入=0

        @property
        def 堂吃收入(self): return self.堂吃新顾客收入+self.堂吃老顾客收入

        外卖新顾客收入=0
        外卖老顾客收入=0

        @property
        def 外卖收入(self): return self.外卖新顾客收入+self.外卖老顾客收入

        @property
        def 营业额(self): return self.外卖收入+self.堂吃收入

        房租=0

        @property
        def 固定成本(self): return self.房租

        人工=0

        @property
        def 半固定成本(self): return self.人工

        食品成本=0
        水电煤=0
        外卖手续费=0

        @property
        def 变动成本(self): return self.食品成本+self.水电煤+self.外卖手续费

        食品报废损失=0
        卫生事件损失=0

        @property
        def 损失(self): return self.食品报废损失+self.卫生事件损失

        @property
        def 费用(self): return  0 # self.费用

        @property
        def 成本(self): return self.固定成本+self.半固定成本+self.变动成本+self.损失+self.费用

        @property
        def 利润(self): return self.收入+self.成本

    当前门店报表=门店报表()

    class 设备:
        前台={"收银台":1,
            "座位":1,
            "到店客户体验":1
            ,"前台库存":{"汉堡":{"count":10,"time":30},"薯条":{"count":10,"time":30},"可乐":{"count":9999,"time":9999}}
        } # 1 个汉堡，储存剩余时间30分钟
        后厨={"冰箱":1, #影响库存
        "电炸锅":1, # 影响生产速度
        "烤堡机":1, # 影响汉堡生产速度
        "腌泡机":1,  # 影响腌制速度
        "开水机":1, # 没有不行
        "滤水系统":1, # 没有不行
        "制冰机":1, # 没有不行
        "可乐机":1} # 没有不行

    

    def __init__(self,门店名字="初始门店",初始资金=0,员工=[],客户=[],设备=设备(),菜单={"汉堡":15,"薯条":8,"可乐":6},环境="这一项还在开发中",oth=""):
        self.门店名字 = 门店名字
        self.员工 = 员工
        self.初始资金 = 初始资金
        self.环境 = 环境
        self.设备=设备
        self.oth=oth
        self.顾客满意度_线上_外卖好评=5
        self.顾客满意度_线下_QSC=5
        self.回头客_留存率_线上=0
        self.回头客_留存率_线下=0
        self.菜单=菜单



默认门店=门店()

def 客户来店(来店门店=默认门店,来店客户=默认客户):
    缺货=[]
    for k in 来店客户.消费计划:
        print(k)
        if 来店门店.设备.前台["前台库存"][k]["count"]:
            来店门店.设备.前台["前台库存"][k]["count"] -= 1
            来店客户.消费金额 +=来店门店.菜单[k]
        else:
            缺货.append(k)
    本次收入=来店客户.消费()
    来店门店.当前门店报表.外卖新顾客收入+= (not 来店客户.到店 ) * ( 来店客户.新客户 ) * 本次收入
    来店门店.当前门店报表.外卖老顾客收入+= (not 来店客户.到店 ) * ( not 来店客户.新客户 ) * 本次收入
    来店门店.当前门店报表.堂吃新顾客收入+= (来店客户.到店 ) * ( 来店客户.新客户 ) * 本次收入
    来店门店.当前门店报表.堂吃老顾客收入+= (来店客户.到店 ) * (not 来店客户.新客户 ) * 本次收入
    print("客户消费完毕")
    if 缺货 == []:
        return "客户消费完毕，消费计划：" + str(来店客户.消费计划)
    else:
        return "客户消费完毕，消费计划：" + str(来店客户.消费计划) + "   缺货商品"+str(缺货) 

def 加汉堡(门店=门店):
   for 员工 in 门店.员工:     # 第一个实例
       if 员工.员工工作状态 == None:
           门店.设备.前台["前台库存"]["汉堡"]["count"] += 1
           门店.当前门店报表.食品成本  += 100
           员工.员工工作状态 ={"工作状态":"做汉堡","开始时间":time.strftime("%Y-%m-%d %H:%M:%S")}
           return "汉堡制作中"
   return "所有员工都在忙"

def 加顾客(门店=门店,消费金额=25):
    新客户=客户(计划消费金额=消费金额)
    return 客户来店(来店门店=门店,来店客户=新客户)

def 加员工(门店=门店,员工名字="门店员工"):
    门店.员工.append(员工(员工名字=员工名字))
    return "招聘成功"

if __name__ == '__main__':
    # 实例化类
    员工1=员工()
    员工2=员工()
    客户1=客户()
    客户2=客户()
    x = 门店(门店名字="123初始门店店",初始资金=0,员工=[员工1,员工2],客户=[],环境="这一项还在开发中")
 
    # 访问类的属性和方法
    print("MyClass 类的属性 员工 为：", x.员工)
