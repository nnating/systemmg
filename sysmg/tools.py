# @Time     :2020/8/14 10:02
# @Author   :dengyuting
# @File     :tools.py


import hashlib

from sysmg.models import Operationlog, User


def hash_code(s, salt='dyttest'):# 加点盐
    """
    密码加密
    :param s:
    :param salt:
    :return:
    """
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def event_log(user_id, opera_type, opera_descrip):
    """
    写日志
    :param opera_descrip:
    :param user_id:
    :param opera_type:
    :return:
    """
    operation_log = Operationlog()
    operation_log.user = User.objects.filter(id=user_id).first()
    operation_log.operationtype = opera_type
    operation_log.descrip = opera_descrip
    operation_log.save()