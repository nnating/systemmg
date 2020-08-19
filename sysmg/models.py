from django.db import models

# Create your models here.
class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', '女'),
    )

    name =models.CharField(max_length=128 , unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="male")
    c_time = models.DateTimeField(auto_now_add=True)
    admintype = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = '用户表'

class Machinfo(models.Model):
    """    设备信息    """

    # mach_type_choice = (
    #     ('server', '服务器'),
    #     ('networkdevice', '网络设备'),
    #     ('storagedevice', '存储设备'),
    #     ('securitydevice', '安全设备'),
    #     ('software', '软件资产'),
    # )
    #
    mach_status = (
        (0, '未借出'),
        (1, '已借出'),
        (2, '未借出，故障'),
        )

    id = models.AutoField(primary_key=True)
    mach_status = models.SmallIntegerField(choices=mach_status, default='0', verbose_name="设备状态")
    name = models.CharField(max_length=64, unique=True, verbose_name="设备名称")     # 不可重复
    sn = models.CharField(max_length=128, verbose_name="型号")
    mach_num = models.CharField(max_length=128, verbose_name="设备编号", null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='', verbose_name="照片")
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    user = models.CharField(max_length=128, verbose_name="领用人", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    outtime = models.CharField(max_length=128, blank=True, null=True, verbose_name='借出日期')
    djuser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='录入人', blank=True)

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = "设备信息表"
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class Operationlog(models.Model):
    """用户操作日志"""

    log_choice = (
        (1, '新增设备'),
        (2, '编辑设备'),
        (3, '删除设备'),
        (4, '登陆系统'),
        (5, '新增用户'),
        (6, '编辑用户'),
        (7, '删除用户'),
        (8, '用户注册'),
        (9, '导入设备'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='操作人', blank=True)
    operationtype = models.IntegerField(choices=log_choice)
    descrip = models.CharField(null=True, max_length=1024, blank=True)
    createtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_operationtype_display()

    class Meta:
        ordering = ["-createtime"]
        verbose_name = '用户日志'
        verbose_name_plural = '用户日志'
