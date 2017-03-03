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
from wechat_auth.helpers import generate_jsapi_signature
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
    return Response(request.session.get("info",None))

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
    :param request:
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

