from django.db import models

# Create your models here.
# 修改了models.py文件需要
# 1、先执行python manage.py makemigrations sign 表示在这个app(sign)下建立 migrations目录，并记录下你所有的关于modes.py的改动，比如0001_initial.py， 但是这个改动还没有作用到数据库文件
# 2、再执行python manage.py migrate 将该改动作用到数据库文件，比如产生table之类的


# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)                 # 发布会标题
    limit = models.IntegerField()                       # 参加人数
    status = models.BooleanField()                      # 发布会状态
    address = models.CharField(max_length=200)          # 发布会地址
    start_time = models.DateTimeField('event_time')                 # 发布会时间
    create_time = models.DateTimeField(auto_now=True)                # 创建时间，自动获取当前时间

    def __str__(self):                          # 重写__str__方法，返回name，也就是发布会标题
        return self.name



# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event,on_delete=models.PROTECT)                    # 嘉宾关联的发布会id
    '''
    在设置外键时，需要通过on_delete选项指明主表删除数据时，对于外键引用表数据如何处理，在django.db.models中包含了可选常量：

    CASCADE级联，删除主表数据时连通一起删除外键表中数据，
    
    PROTECT保护，通过抛出ProtectedError异常，来阻止删除主表中被外键应用的数据，
    
    SET_NULL设置为NULL，仅在该字段null=True允许为null时可用，
    
    SET_DEFAULT设置为默认值，仅在该字段设置了默认值时可用，
    
    SET()设置为特定值或者调用特定方法，
    
    DO_NOTHING不做任何操作，如果数据库前置指明级联性，此选项会抛出IntegrityError异常。
    '''
    realname = models.CharField(max_length=100)         # 嘉宾姓名
    phone = models.CharField(max_length=16)             # 嘉宾手机号
    sign = models.BooleanField()                        # 嘉宾签到状态
    email = models.EmailField()                         # 嘉宾邮件
    create_time = models.DateTimeField(auto_now=True)

    class Meta:                             # django模型类的一个内部类，用于定义一些django模型类的行为特性
        unique_together = ('event','phone')             # unique_together用于设置两个字段的联合主键

    def __str__(self):
        return self.realname
