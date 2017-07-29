#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

__author__ = 'yinzishao'
from django.shortcuts import render

# Create your views here.
from api.bll.teacher import *
from api.bll.parent import *
from api.bll.order import *
from api.bll.message import *
from api.bll.admin import *
from api.bll.locations import *
from rest_framework.decorators import api_view,authentication_classes
from api.serializers import TeacherSerializer,ParentOrderSerializer,MessageSerializer,OrderApplySerializer
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from tutor.http import JsonResponse,JsonError
from api.models import Teacher,AuthUser,ParentOrder,OrderApply,Message,Config,Locations
from django.db import transaction
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from wechat_auth.helpers import generate_jsapi_signature,sendTemplateMessage, downloadImg


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

@login_required()
@api_view(['GET'])
def loginSuc(request):

    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)


@login_required()
@api_view(['GET'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def getWechatInfo(request):
    """
    获取微信个人信息
    :param request:
    :return:
    """
    result = request.session.get("info", {})
    user = AuthUser.objects.get(username=request.user.username)
    teacher = user.teacher_set.all()
    parent = user.parentorder_set.all()
    if not len(teacher) and not len(parent):
        return JsonError("no user")
    else:

        if len(teacher):
            obj = teacher[0]
        else:
            obj = parent[0]
        massage_warn = obj.massage_warn
        result['message_warn'] = massage_warn
    return Response(result)

@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def getText(request):
    """
    获取系统一些配置信息
    :param request:
    :return:
    """
    key = request.data.get('key',None)
    result = {}
    try:
        for k in key:
            if k == "getImg":
                value = []
                image = Config.objects.filter(key='image')[0].value
                url = Config.objects.filter(key='url')[0].value
                imgs = image.split(',') if image != "" else []
                urls = url.split(',') if image != "" else []
                for i,v in enumerate(imgs):
                    value.append({"img":v,"url":urls[i]})
            else:
                value = Config.objects.get(key=k).value
            result[k] = value
        return JsonResponse(result)
    except Exception,e:
        return JsonError(e.message)

@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def generate_signature(request):
    """
    生成jssdk所需的_signature
    :param request: {"timestamp":"1482652615","nonceStr":"yinzishao","url":"http://www.yinzishao.cn/testjs"}
    :return:
    """
    timestamp = request.data.get('timestamp',None)
    nonceStr = request.data.get('nonceStr',None)
    url = request.data.get('url',None)

    if not url:
        url = request.META['HTTP_REFERER']
    return JsonResponse({
        "signature":generate_jsapi_signature(timestamp,nonceStr,url)
    })

@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def uploadImgServerId(request):
    """
    上传微信端的serverId，然后下载照片存放在本地
    :param request:
    :return:
    """
    serverId = request.data.get('serverId',None)
    print downloadImg(serverId)
    print 'serverId ==================='
    print serverId
    return JsonResponse()


@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def setMessageWarn(request):
    """
    改变消息通知状态
    :param request:
    :return:
    """
    user = AuthUser.objects.get(username=request.user.username)
    status = request.data.get('status', 1)
    teacher = user.teacher_set.all()
    parent = user.parentorder_set.all()
    if not len(teacher) and not len(parent):
        return JsonError("no user")
    else:

        if len(teacher):
            obj = teacher[0]
        else:
            obj = parent[0]
        obj.massage_warn = status
        obj.save()
        return JsonResponse()
