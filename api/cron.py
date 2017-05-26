#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

from django.db import transaction
from django.conf import settings
from api.models import Teacher,AuthUser,ParentOrder,OrderApply,Message,Config
from wechat_auth.helpers import sendTemplateMessage
import time
__author__ = 'yinzishao'


def my_scheduled_job():
    now = datetime.datetime.now()
    start = now - datetime.timedelta(minutes=5)
    #半个小时之外,并且没有完成上传截图这步骤的订单
    oas = OrderApply.objects.filter(update_time__lte=start,finished=0,teacher_willing=1,parent_willing=2)
    print oas
    for oa in oas:
        try:
            with transaction.atomic():
                #没有上传截图，当做老师拒绝操作
                oa.finished =1
                oa.teacher_willing = 0
                oa.save()
                #给老师发送消息，老师过期
                message_title = u"你的订单已过期，没有在相应的时间内上传截图！"
                message_content = u"你的订单已过期，没有在相应的时间内上传截图！"
                #应该是管理员发送
                message = Message(sender=oa.tea.wechat, receiver=oa.tea.wechat, message_title=message_title, message_content=message_content,status=0)
                message.save()
                #老家长发送消息，审核不通过
                message_title = u"订单审核不通过！"
                message_content = u"订单审核不通过！"
                message = Message(sender=oa.tea.wechat, receiver=oa.pd.wechat, message_title=message_title, message_content=message_content,status=0)
                message.save()
                #推送到微信端
        except Exception,e:
            print e.message
def checkUpload():
    """
    检查上传截图是否过期
    :return:
    """
    now = datetime.datetime.now()
    start = now - datetime.timedelta(minutes=30)
    #半个小时之外,并且到上传截图这步骤
    oas = OrderApply.objects.filter(update_time__lte=start,finished=0,teacher_willing=2,parent_willing=2)
    for oa in oas:
        try:
            with transaction.atomic():
                #没有上传截图，当做老师拒绝操作
                oa.finished =1
                oa.teacher_willing = 0
                oa.save()
                #给老师发送消息，老师过期
                message_title = u"截图审核未通过，请留意其他家教信息！"
                message_content = u"截图审核未通过，请留意其他家教信息！"
                #应该是管理员发送
                message = Message(sender=oa.tea.wechat, receiver=oa.tea.wechat, message_title=message_title, message_content=message_content,status=0)
                message.save()
                now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                #发送推送给老师
                sendTemplateMessage(
                    oa.tea,
                    settings.DOMAIN+'tutor_web/view/teacherPage.html',
                    message_title,
                    message_content,
                    u"好学吧家教平台",
                    now
                )

                #家长发送消息，审核不通过
                message_title = u"通知老师失败，请重新选择其他老师联系试课！"
                message_content = u"通知老师失败，请重新选择其他老师联系试课！"
                message = Message(sender=oa.tea.wechat, receiver=oa.pd.wechat, message_title=message_title, message_content=message_content,status=0)
                message.save()
                #推送到微信端

                #发送推送给家长
                sendTemplateMessage(
                    oa.pd,
                    settings.DOMAIN+'tutor_web/view/parentPage.html',
                    message_title,
                    message_content,
                    u"好学吧家教平台",
                    now
                )

        except Exception,e:
            print e.message
