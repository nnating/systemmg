# from django.contrib.auth.models import User
import time
from datetime import datetime

from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
# from django.http import JsonResponse

# Create your views here.

from sysmg.models import User, Machinfo, Operationlog
from sysmg.tools import hash_code, event_log
import xlrd

def login(request):
    """
    登录
    :param request:
    :return:
    """
    # print("1111", request.session.get('is_login'))
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')

    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:  # 确保用户名和密码都不为空
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login.html', {'message': message})
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                event_log(user.id, 4, '用户登陆成功')
                return redirect('/index/')
                # return render(request, 'index.html')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', {'message': message})
        else:
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')


def index(request):
    total = Machinfo.objects.count()
    wjc_count = Machinfo.objects.filter(mach_status=0).count()
    yjc_count = Machinfo.objects.filter(mach_status=1).count()
    gz_count = Machinfo.objects.filter(mach_status=2).count()
    # lyuser = Machinfo.objects.filter(~Q(user=''))
    # a = []
    # for i in lyuser:
    #     lyuser_name = i.user
    #     a.append(lyuser_name)
    # print(a)
    if total != 0:
        wjc_rate = str(round(wjc_count/total*100))+"%"
        yjc_rate = round(yjc_count/total*100)
        gz_rate = round(gz_count/total*100)
    else:
        wjc_rate = 0
        yjc_rate = 0
        gz_rate = 0
    return render(request, 'index.html', {'wjc_rate': wjc_rate, 'yjc_rate':yjc_rate, 'gz_rate': gz_rate,'wjc_count':wjc_count,'yjc_count':yjc_count,"gz_count":gz_count})


def register(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')

    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')

        if password != password1:
            message = '两次输入密码不一致'
            return render(request, 'register.html', {'message': message})
        else:
            same_name_user = User.objects.filter(name = username)
            if same_name_user:
                message = "用户名已存在"
                return render(request, 'register.html', {'message': message})
            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                message = '该邮箱已经被注册了！'
                return render(request, 'register.html', {'message': message})
            new_user = User()
            new_user.name = username
            new_user.password = hash_code(password)
            new_user.email = email
            new_user.admintype = 0
            new_user.save()
            event_log(new_user.id, 8, '用户：{} 注册成功'.format(new_user.name))
            message = '注册成功'

            return render(request, 'register.html', {'message': message})
    return render(request, 'register.html')


def logout(request):
    if not request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/login/')
    request.session.flush()
    return redirect("/login/")


def machlist(request):
    machlist = Machinfo.objects.all()
    if len(machlist) > 0:
        dname = machlist.first().djuser.name
    return render(request, 'machlist.html', {'machlist': machlist})


def machdetail(request, mach_id):
    machdetail = Machinfo.objects.get(id=mach_id )
    return render(request, 'machdetail.html', {'machdetail': machdetail})

def machedit(request, mach_id):
    machedit = Machinfo.objects.get(id=mach_id)

    if request.method == 'POST':
        mach_status = request.POST.get('mach_status')
        name = request.POST.get('name')
        sn = request.POST.get('sn')
        img = request.FILES.get('img')
        mach_num = request.POST.get('mach_num')
        remark = request.POST.get('remark')
        user = request.POST.get('user')
        outtime = request.POST.get('outtime')
        djuser_name = request.POST.get('djuser_name')
        djuser = User.objects.filter(name=djuser_name)

        new_name = Machinfo.objects.exclude(id=mach_id).filter(name=name)
        if new_name:
            message = "设备名称已存在"
            return render(request, 'machedit.html', {'message': message, 'machedit': machedit})
        # Machinfo.objects.filter(id=mach_id).update(name=name, mach_status=mach_status, sn=sn, image=img, mach_num=mach_num, remark=remark, user=user, outtime=outtime)
        edit_mach = Machinfo()
        edit_mach.id = mach_id
        edit_mach.name = name
        edit_mach.mach_status = mach_status
        edit_mach.sn = sn
        edit_mach.image = img
        edit_mach.mach_num = mach_num
        edit_mach.remark = remark
        edit_mach.user = user
        edit_mach.outtime = outtime
        edit_mach.save(force_update=True, update_fields=['name','mach_status','sn','image','mach_num','remark','user','outtime'])
        event_log(request.session['user_id'], 2, '编辑设备：{}'.format(name))
        return redirect('/machlist/')
    return render(request, 'machedit.html', {'machedit': machedit})


def machdel(request, mach_id):
    machdel_name = Machinfo.objects.filter(id=mach_id).first().name
    Machinfo.objects.get(id=mach_id).delete()
    event_log(request.session['user_id'], 3,'删除设备：{}'.format(machdel_name))
    return redirect('/machlist/')


def machadd(request):

    if request.method == 'POST':
        mach_status = request.POST.get('mach_status')
        name = request.POST.get('name')
        sn = request.POST.get('sn')
        img = request.FILES.get('img')
        mach_num = request.POST.get('mach_num')
        remark = request.POST.get('remark')
        user = request.POST.get('user')
        outtime = request.POST.get('outtime')
        # update_time = request.POST.get('update_time')
        djuser_name = request.POST.get('djuser_name')
        djuser = User.objects.filter(name=djuser_name)

        new_name = Machinfo.objects.filter(name=name)
        if new_name:
            message = "设备名称已存在"
            return render(request, 'machadd.html', {'message': message})

        new_mach = Machinfo()
        new_mach.mach_status = mach_status
        new_mach.name = name
        new_mach.sn = sn
        new_mach.image = img
        new_mach.mach_num = mach_num
        new_mach.remark = remark
        new_mach.user = user
        new_mach.outtime = outtime
        new_mach.djuser = djuser.first()
        new_mach.save()
        djuser_id = User.objects.get(name=djuser_name).id
        event_log(request.session['user_id'], 1, '新增设备：{}'.format(new_mach.name))
        return redirect('/machlist/')

    return render(request, 'machadd.html')


def userlist(request):
    userlist = User.objects.all()
    return render(request, 'userlist.html', {'userlist': userlist})


def useredit(request, user_id):
    useredit = User.objects.get(id=user_id )

    if request.method == 'POST':
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        email = request.POST.get('email')

        same_name_user = User.objects.exclude(id=user_id).filter(name = name)
        if same_name_user:
            message = "用户名已存在"
            return render(request, 'useredit.html', {'message': message, 'useredit': useredit})
        same_email_user = User.objects.exclude(id=user_id).filter(email=email)
        if same_email_user:
            message = '该邮箱已经被注册了！'
            return render(request, 'useredit.html', {'message': message, 'useredit': useredit})
        User.objects.filter(id=user_id).update(name=name,sex=sex,email=email)
        event_log(request.session['user_id'], 6, '编辑用户：{}'.format(name))
        return redirect('/userlist/')
    return render(request, 'useredit.html', {'useredit': useredit})


def userdel(request, user_id):
    if User.objects.filter(id=user_id).first().admintype == '1':
        return redirect('/userlist/')
    user_name = User.objects.filter(id=user_id).first().name
    User.objects.get(id=user_id).delete()
    event_log(request.session['user_id'], 7, '删除用户：{}'.format(user_name))
    return redirect('/userlist/')


def useradd(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        email = request.POST.get('email')

        same_name_user = User.objects.filter(name = name)
        if same_name_user:
            message = "用户名已存在"
            return render(request, 'useradd.html', {'message': message})
        same_email_user = User.objects.filter(email=email)
        if same_email_user:
            message = '该邮箱已经被注册了！'
            return render(request, 'useradd.html', {'message': message})
        new_user = User()
        new_user.name = name
        new_user.sex = sex
        new_user.email = email
        new_user.admintype = 0
        new_user.password = hash_code('123456')
        new_user.save()
        # message = '新增成功'
        event_log(request.session['user_id'], 5, '新增用户：{}'.format(new_user.name))
        return redirect('/userlist/')

    return render(request, 'useradd.html')


def operationlog(request):
    operationlog = Operationlog.objects.all()
    return render(request, 'operationlog.html', {'operationlog': operationlog})


def excelin(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('filename')
        excel_type = excel_file.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            # ncols = sheet.ncols
            if nrows > 1:
                try:
                    with transaction.atomic():  # 控制数据库事务交易
                        for i in range(1, nrows):
                            rowVlaues = sheet.row_values(i)
                            same_name = Machinfo.objects.filter(name=rowVlaues[0])
                            if same_name:
                                # message1 = "设备名称已存在"
                                return redirect('/machlist/')
                            if rowVlaues[5] == '未借出，故障':
                                rowVlaues[5] = 2
                            elif rowVlaues[5] == '已借出':
                                rowVlaues[5] = 1
                            else:
                                rowVlaues[5] = 0
                            Machinfo.objects.create(name=rowVlaues[0], sn=rowVlaues[1], mach_num=rowVlaues[2], remark=rowVlaues[3], user=rowVlaues[4], mach_status=rowVlaues[5], outtime=rowVlaues[6], djuser_id=request.session['user_id'])
                            event_log(request.session['user_id'], 9, '导入设备：{}'.format(rowVlaues[0]))
                except:
                    print('解析excel文件或者数据插入错误')
                return redirect('/machlist/')

            else:
                print('空文件')
                return redirect('/machlist/')
        else:
            print('非Excel文件')

    return redirect('/machlist/')
