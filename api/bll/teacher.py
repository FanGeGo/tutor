#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import traceback
__author__ = 'yinzishao'

from rest_framework.decorators import api_view,authentication_classes
from api.serializers import TeacherSerializer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from tutor.http import JsonResponse,JsonError
from api.models import Teacher,AuthUser,ParentOrder,OrderApply,Message,Config
from wechat_auth.helpers import changeBaseToImg,changeObejct,getParentOrderObj,getTeacherObj,changeTime,changeSingleBaseToImg,defaultChangeTeachShowPhoto, \
    getTeacherResult
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from locations import getUserDistance
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

@login_required()
@api_view(['GET','POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def getTeacherInfo(request):
    """
    获取个人信息
    :param request:
    :return:
    """
    user = AuthUser.objects.get(username=request.user.username)
    format = None
    result = {}
    if request.method == "GET":
        teacher = user.teacher_set.all()
        if len(teacher):
            serializer = TeacherSerializer(teacher[0])
            result = serializer.data
        else:
            return JsonError("not found")
    elif request.method == "POST":
        tea_id = request.data.get('tea_id',None)
        format = request.data.get('format',None)
        if not tea_id:
            teacher = user.teacher_set.all()
            if len(teacher):
                serializer = TeacherSerializer(teacher[0])
                result = serializer.data
        else:
            teas = Teacher.objects.filter(tea_id = tea_id)
            if len(teas):
                serializer = TeacherSerializer(teas[0])
                result = serializer.data
    if format:
        getTeacherObj(result)
    else:
        defaultChangeTeachShowPhoto(result)
        changeTime(result)

    return Response(result)


@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def createTeacher(request):
    """
    创建老师
    :param request:
    :return:
    """
    try:
        user = AuthUser.objects.get(username=request.user.username)
        teachers = user.teacher_set.all()
        if not user.is_superuser and len(teachers) > 0:
            return JsonError("already existed")
        if request.method == 'POST':
            temp = request.data.dict()  if (type(request.data) != type({})) else request.data
            changeObejct(temp)
            photos = temp.get('teach_show_photo',None)
            if photos and photos != "":
                temp['teach_show_photo'] = changeBaseToImg(photos)
            certificate_photo = temp.get('certificate_photo',None)
            if certificate_photo and certificate_photo != "":
                temp['certificate_photo'] = changeSingleBaseToImg(certificate_photo)
            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            temp['create_time']= now
            temp['update_time']= now
            teacher = Teacher(**temp)
            teacher.wechat = user
            teacher.save()
        return JsonResponse({"wechat_id":teacher.wechat_id})
    except Exception,e:
        print 'traceback.print_exc():'; traceback.print_exc()
        return JsonError(e.message)

@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def updateTeacher(request):
    """
    修改老师
    :param request:
    :return:
    """
    try:
        user = AuthUser.objects.get(username=request.user.username)
        teachers = user.teacher_set.all()
        if request.method == 'POST' and len(teachers) > 0:
            temp = request.data.dict()  if (type(request.data) != type({})) else request.data
            changeObejct(temp)
            temp['pass_not'] =1
            photos = temp.get('teach_show_photo',None)
            if photos and photos != "":
                temp['teach_show_photo'] = changeBaseToImg(photos)
            certificate_photo = temp.get('certificate_photo',None)
            if certificate_photo and certificate_photo != "":
                temp['certificate_photo'] = changeSingleBaseToImg(certificate_photo)
            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            temp['update_time']= now
            teacher = user.teacher_set.update(**temp)
            return JsonResponse()
            # 返回更新后的对象
            # serializer = TeacherSerializer(user.teacher_set.all()[0])
            # result = serializer.data
            # getTeacherObj(result)
            # return Response(result)
        return JsonError("not found")
    except Exception,e:
        print 'traceback.print_exc():'; traceback.print_exc()
        return JsonError(e.message)


@login_required()
@api_view(['GET'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def deleteTeacher(request):
    """
    删除
    :param request:
    :return:
    """
    #TODO：删除外键约束
    user = AuthUser.objects.get(username=request.user.username)
    teachers = user.teacher_set.all()
    if len(teachers) > 0:
        teachers[0].delete()
        return JsonResponse()
    return JsonError("not found")

#TODO：为家长推荐老师
@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def getTeachers(request):
    """
        全部老师根据类别获取老师列表
        :param request:
        {
        "size":6,
        "start":0,
        "subject":"语文",
        "grade":1,
        "hot":1,
        }
        :return:
            teacher obejcts
    """
    #TODO:排序与选择
    size = int(request.data.get("size",0))
    start = int(request.data.get("start",0)) * size
    #根据学科排序
    subject = request.data.get("subject", '')
    #根据年级排序
    grade = request.data.get("grade", '')
    keyword = request.data.get("keyword", '')
    #根据最新最热排序,两个参数是最热门和最新，默认为最热门（参数为1），然后是最新（参数为2）
    hot = request.data.get("hot",1)
    where = []
    filter = {}
    order = ['-hot_not','-update_time']
    if hot == 2:
        order = ['-update_time']
    if subject and subject != '':
        where = ['FIND_IN_SET("'+subject+'",subject)']
    #年级,如果里面是字符串，需要加引号
    if grade and grade != '':
        where = ['FIND_IN_SET("'+grade+'",grade)']
    if keyword and keyword != '':
        filter["name__contains"] = keyword
    teachers = Teacher.objects.extra(where=where).filter(**filter).order_by(*order)[start:start + size]
    user = AuthUser.objects.get(username=request.user.username)
    pds = user.parentorder_set.all()
     #管理员调用该该接口,没有isInvited
    if len(pds) > 0 and not user.is_superuser:
        pd = pds[0]
         #获取到老师的数据，需要判断是不是报名或者被邀请
        for t in teachers:
            t.distance = getUserDistance(user,t.wechat)
            t.isInvited = ''
            #家长主动
            orderApply = OrderApply.objects.filter(pd=pd,tea= t)
            if len(orderApply):
                oa = orderApply[0]
                t.isInvited = getTeacherResult(oa)

    elif len(pds) == 0 and not user.is_superuser:
        return JsonError("家长不存在！请重新填问卷")

    serializer = TeacherSerializer(teachers, many=True)
    teachersData = serializer.data
    getTeacherObj(teachersData,many=True)
    return Response(teachersData)
