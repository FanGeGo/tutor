#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

__author__ = 'yinzishao'

from rest_framework.decorators import api_view,authentication_classes
from api.serializers import ParentOrderSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from tutor.http import JsonResponse,JsonError
from api.models import AuthUser,ParentOrder,OrderApply
from wechat_auth.helpers import changeBaseToImg,changeObejct,getParentOrderObj,getTeacherObj,changeTime, getParentResult
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from locations import getUserDistance
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

@login_required()
@api_view(['GET','POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def getParentInfo(request):
    """
    获取个人信息
    :param request:
    :return:
    """
    user = AuthUser.objects.get(username=request.user.username)
    format = None
    if request.method == "GET":
        parents = user.parentorder_set.all()
        if len(parents):
            serializer = ParentOrderSerializer(parents[0])
            result = serializer.data
        else:
            return JsonError("not found")
    elif request.method == "POST":
        pd_id = request.data.get('pd_id',None)
        format = request.data.get('format',None)
        if not pd_id:
            parents =  user.parentorder_set.all()
            if len(parents):
                serializer = ParentOrderSerializer(parents[0])
                result = serializer.data
            else:
                return JsonError("not found")
        else:
            pds = ParentOrder.objects.filter(pd_id = pd_id)
            if len(pds):
                serializer = ParentOrderSerializer(pds[0])
                result = serializer.data
            else:
                return JsonError("not found")
    if format:
        getParentOrderObj(result)
    else:
        changeTime(result)
    return Response(result)


@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def createParentOrder(request):
    """
    创建家长订单
    :param request:
    :return:
    """
    user = AuthUser.objects.get(username=request.user.username)
    parentorder = user.parentorder_set.all()
    #TODO：管理员创建多个会有什么连锁反应
    #TODO:这个以后会加个限制，不让同时创建老师和家长
    if not user.is_superuser and len(parentorder) > 0:
        return JsonError("already existed")
    if request.method == 'POST':
        temp = request.data.dict()  if (type(request.data) != type({})) else request.data
        changeObejct(temp)
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        temp['create_time']= now
        temp['update_time']= now
        po = ParentOrder(**temp)
        po.wechat = user
        po.save()
    return JsonResponse({"wechat_id":po.wechat_id})

@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def updateParentOrder(request):
    """
    更新家长订单
    :param request:
    :return:
    """
    user = AuthUser.objects.get(username=request.user.username)
    parentorder = user.parentorder_set.all()
    if request.method == 'POST' and len(parentorder) > 0:
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        temp = request.data.dict()  if (type(request.data) != type({})) else request.data
        changeObejct(temp)
        temp['update_time']= now
        temp['pass_not'] =1
        po = user.parentorder_set.update(**temp)
        return JsonResponse()
        # serializer = ParentOrderSerializer(user.parentorder_set.all()[0])
        # result = serializer.data
        # getParentOrderObj(result)
        # return Response(result)
    return JsonError("not found")

@login_required()
@api_view(['GET'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def deleteParent(request):
    """
    删除
    :param request:
    :return:
    """
    #TODO：删除外键约束
    user = AuthUser.objects.get(username=request.user.username)
    parentorder = user.parentorder_set.all()
    if len(parentorder) > 0:
        parentorder[0].delete()
        return JsonResponse()
    return JsonError("not found")

@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def getParentOrder(request):
    """
    获取家长列表。家长对于老师的申请处理
    :param request:
    {"start":0,"size":6}
    :return:
    """
    size = int(request.data.get("size",0))
    start = int(request.data.get("start",0)) * size
    keyword = request.data.get("keyword", '')
    filter = {}
    if keyword and keyword != '':
        filter["name__contains"] = keyword
    user = AuthUser.objects.get(username=request.user.username)
    parentOrders = ParentOrder.objects.filter(**filter).order_by('-update_time')[start:start + size]
    teas = user.teacher_set.all()
    if len(teas) > 0 and not user.is_superuser:
        tea = teas[0]
        for po in parentOrders:
            #计算距离
            po.distance = getUserDistance(user,po.wechat)
            #替换微信端的地址
            po.address = ''
            locations = po.wechat.locations_set.all()
            if len(locations) > 0:
                po.address = locations[0].address

            po.isInvited = ''
            #老师主动报名
            orderApply = OrderApply.objects.filter(pd=po,tea= tea)
            if len(orderApply):
                oa = orderApply[0]
                po.isInvited = getParentResult(oa)
    elif len(teas) == 0 and not user.is_superuser:
        return JsonError(u"您不是老师！请重新填问卷")

    serializer = ParentOrderSerializer(parentOrders, many=True)
    result = serializer.data
    getParentOrderObj(result, many=True)
    return Response(result)
