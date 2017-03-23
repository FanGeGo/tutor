#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
import requests
import json
from django.conf import settings
TOKEN=settings.TOKEN
APP_ID=settings.APP_ID
APP_SECRET=settings.APP_SECRET
DOMAIN=settings.DOMAIN
TEMPLATE_ID=settings.TEMPLATE_ID
ADDRESS_KEY=settings.ADDRESS_KEY

__author__ = 'yinzishao'

admin_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APP_ID + '&redirect_uri='+DOMAIN+'adminAuthorization&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=1#wechat_redirect'


week = ["mon_begin","mon_end","tues_begin","tues_end",
            "wed_begin","wed_end","thur_begin","thur_end","fri_begin","fri_end"]
weekend = ["sat_morning","sat_afternoon","sat_evening",
               "sun_morning","sun_afternoon","sun_evening"]
token_path = settings.BASE_DIR + '/wechat_auth/access_token.json'
def get_access_token_function():
    """ 注意返回值为一个 Tuple，第一个元素为 access_token 的值，第二个元素为 access_token_expires_at 的值 """
    with open(token_path, 'r') as f:
        data = json.loads(f.read())
        return (data['access_token'],data['access_token_expires_at'])


def set_access_token_function(access_token=None, access_token_expires_at=None):
    with open(token_path, 'r+') as f :
        data = f.read()
        d = json.loads(data)
        d["access_token"] = access_token
        d["access_token_expires_at"] = access_token_expires_at
        f.seek(0)
        f.write(json.dumps(d))
        f.truncate()


def get_jsapi_ticket_function():
    with open(token_path, 'r') as f:
        data = json.loads(f.read())
        return (data['jsapi_ticket'],data['jsapi_ticket_expires_at'])

def set_jsapi_ticket_function(jsapi_ticket=None, jsapi_ticket_expires_at=None):
    with open(token_path, 'r+') as f :
        data = f.read()
        d = json.loads(data)
        d["jsapi_ticket"] = jsapi_ticket
        d["jsapi_ticket_expires_at"] = jsapi_ticket_expires_at
        f.seek(0)
        f.write(json.dumps(d))
        f.truncate()

def sendTemplateMessage(receiver="odE4WwK3g05pesjOYGbwcbmOWTnc",
                        redir_url="http://www.yinzishao.cn/login",
                        abstarct="你的报名有最新消息！ＸＸ接受／拒绝了你的报名！",
                        content= 'message_content',
                        name= "黄先生",
                        date= "2016/12/22"):
    #获取用户，判断是否是管理员，如果是管理员则first_name是openId
    user = receiver.wechat
    if user.is_superuser:
        openid = user.first_name
        remark = "管理员的消息通知"
        redir_url = admin_url
    else:
        openid = user.username
        remark = "谢谢关注家教平台"
    token = conf.get_access_token()['access_token']
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % token
    TEMPLATE_ID = "LUdCxE5cvGT1GI-NX8UpNFq1Ywde8H2VN_NV-AjpZCg"
    post_data = {
        "touser":openid,
        "template_id":TEMPLATE_ID,
        "url":redir_url,
        "topcolor":"#FF0000",
        "data":{
            "first": {
                "value":abstarct,
                "color":"#173177"
            },
            "keyword1":{
                "value":name,
                "color":"#173177"
            },
            "keyword2": {
                "value":'',
                "color":"#173177"
            },
            "keyword3":{
                "value":date,
                "color":"#173177"
            },
            "keyword4":{
                "value":content,
                "color":"#173177"
            },
            "remark":{
                "value":content,
                "color":"#173177"
            }
        }
    }
    import requests
    requests.post(url,json=post_data)

conf = WechatConf(
    token=TOKEN,
    appid=APP_ID,
    appsecret=APP_SECRET,
    access_token_getfunc=get_access_token_function,
    access_token_setfunc=set_access_token_function,
    jsapi_ticket_getfunc=get_jsapi_ticket_function,
    jsapi_ticket_setfunc=set_jsapi_ticket_function
)

def generate_jsapi_signature(timestamp,nonceStr,url):
    jt = conf.get_jsapi_ticket()
    return WechatBasic().generate_jsapi_signature(timestamp,nonceStr,url,jt['jsapi_ticket'])
# import time
# jt = conf.get_jsapi_ticket()
# print WechatBasic().generate_jsapi_signature(1482652615,"yinzishao","http://www.yinzishao.cn:8000/testjs",jt['jsapi_ticket'])
# # sendTemplateMessage()
dir = settings.BASE_DIR + '/api/static/'

import base64
import re
import time
def changeBaseToImg(data):
    result = []
    for imgData in data:
        pic_data = imgData["img"]
        name = changeSingleBaseToImg(pic_data)
        result.append(name)
    return ','.join(result)

def changeSingleBaseToImg(pic_data):
    """
    serverId下载单个照片
    :param pic_data: 可能是serverId 或者是文件路径
    :return:
    """
    if pic_data == '':
        return ''
    try:
        pic_data.index("static")
        return pic_data
    except Exception,e:
        return downloadImg(pic_data)

def changeObejct(obj):
    """
    兼容接受到的对象
    :param obj:
    :return:
    """
    changeWeek(obj,week)
    changeWeekend(obj,weekend)
    if obj.has_key('salary'):
        obj['salary'] = float('%.2f' % float(obj['salary'])) if obj['salary'] != "" else 0.00
    if obj.has_key('deadline') and obj['deadline'] == "":
        del obj['deadline']
    #禁止自己设置为热门老师
    if obj.has_key('hot_not'):
        del obj['hot_not']
    #禁止自己审核
    if obj.has_key('pass_not'):
        del obj['pass_not']
    if obj.has_key('tea_id'):
        del obj['tea_id']
    if obj.has_key('pd_id'):
        del obj['pd_id']
    return obj


def getParentOrderObj(objs,many=False):

    """
    将parentOrder对象转换为前端所需对象
    :param obj:
    :return:
    """
    if many:
        for obj in objs:
            changeParentOrderObj(obj)
    else:
        changeParentOrderObj(objs)

def getTeacherObj(objs, many=False):
    """
    将teacher对象转换为前端所需对象
    :param objs:
    :param many:
    :return:
    """
    if many:
        for obj in objs:
            changeTeacherObj(obj)
    else:
        changeTeacherObj(objs)

def changeParentOrderObj(obj):
    """
    改变单个parentOrderObj对象
    :param obj:
    :return:
    """
    # changeParentWilling(obj)
    changeTeacherSex(obj)
    changeWeekToRange(obj, week)
    changeWeekEndToRange(obj, weekend)
    changeTime(obj)
    changeLearningPhase(obj)
def changeTeacherObj(obj):
    """
    改变单个teacher对象
    :param obj:
    :return:
    """
    changeQualification(obj)
    changeSex(obj)
    changeWeekToRange(obj, week)
    changeWeekEndToRange(obj, weekend)
    changeTime(obj)
    changeTeachShowPhoto(obj)

def changeTeachShowPhoto(obj):
    teach_show_photo = obj.get('teach_show_photo',None)
    if teach_show_photo:
        if teach_show_photo !='':
            result = teach_show_photo.split(',')
            res = [ i for i in result if i != '']
            obj['teach_show_photo'] = res
        else:
            obj['teach_show_photo'] = []
def defaultChangeTeachShowPhoto(obj):
    """
    {"teach_show_photo": [
          {"img":""},
          {"img":""},
          {"img":""}
       ]}
    :param obj:
    :return:
    """
    teach_show_photo = obj.get('teach_show_photo',None)
    img = []
    if teach_show_photo and teach_show_photo !='':
        for t in teach_show_photo.split(','):
            img.append({"img":t})
    obj['teach_show_photo'] = img
def changeLearningPhase(obj):
    """
    学习阶段(0-其他 1-幼升小 2-小学 3-初中 4-高中)
    :param obj:
    :return:
    """
    learning_phase = obj.get('learning_phase', None)
    obj["learning_phase"] = u''
    if learning_phase == 0 :
        obj["learning_phase"] = u'其他'
    if learning_phase == 1:
        obj["learning_phase"] = u'幼升小'
    if learning_phase == 2:
        obj["learning_phase"] = u'小学'
    if learning_phase == 3:
        obj["learning_phase"] = u'初中'
    if learning_phase == 4:
        obj["learning_phase"] = u'高中'

def changeTime(obj):
    """
    将时间格式转换为前端所需，2017-01-18T10:58:11改成2017-01-18这
    :param obj:
    :return:
    """
    update_time = obj.get('update_time', None)
    create_time = obj.get('create_time', None)
    deadline = obj.get('deadline', None)
    if update_time:
        obj["update_time"] = update_time[:10]
    if create_time:
        obj["create_time"] = create_time[:10]
    if deadline:
        obj["deadline"] = deadline[:10]

def changeTeacherSex(obj):
    #性别
    teacher_sex = obj.get('teacher_sex', 0)
    if teacher_sex == 0 or teacher_sex == None:
        obj["teacher_sex"] = u"不限"
    elif teacher_sex == 1:
        obj["teacher_sex"] = u"男"
    elif teacher_sex == 2:
        obj["teacher_sex"] = u"女"

def changeSex(obj):
    sex = obj.get('sex', 0)
    if sex == 0 or sex == None:
        obj["sex"] = u"不限"
    elif sex == 1:
        obj["sex"] = u"男"
    elif sex == 2:
        obj["sex"] = u"女"

def changeQualification(obj):
    #学历状态: 1-本科生 2-研究生 3-毕业生
    qualification = obj.get('qualification', None)
    if qualification:
        if qualification == 1:
            obj["qualification"] = u"本科生"
        elif qualification == 2:
            obj["qualification"] = u"研究生"
        if qualification == 3:
            obj["qualification"] = u"毕业生"
    else:
        obj["qualification"] = u""
def changeParentWilling(obj):
    #家长的意愿:2-愿意 1-待处理 0-拒绝 (老师主动申请的默认为待处理，邀请老师的默认为愿意)
    pw = obj.get('parent_willing', None)
    obj["isInvited"] = ''
    if pw:
        if pw == 1:
            obj["isInvited"] = u"已报名"
        elif pw == 2:
            obj["isInvited"] = u"已接受"
        elif pw == 0:
            obj["isInvited"] = u"已拒绝"

def changeWeek(obj, times):
    """
    兼容接受到的对象如果为空的字符串则删除
    :param obj:
    :param times:
    :return:
    """
    for time in times:
        if obj.has_key(time):
            m = obj.get(time, None)
            if m != "" and m:
                obj[time] = int(m)
            else:
                del obj[time]

def changeWeekend(obj, weekend):
    """
    兼容接受到的对象, weekend true/false change 1/0
    :param obj:
    :param weekend:
    :return:
    """
    for time in weekend:
        if obj.has_key(time):
            m = obj.get(time, False)
            if m and m != "":
                obj[time] = 1
            else:
                obj[time] = 0

def changeWeekToRange(obj, time):
    """
    将星期一到星期五的字段返回前端所要求的数就
    :param obj:
    :param time:
    :return:
    """
    obj["time"]  = ""
    for index in range(0, len(time),2):
        field_name = time[index]
        if obj[field_name]:
            if field_name.startswith("mon"):
                date = u"一"
            if field_name.startswith("tues"):
                date = u"二"
            if field_name.startswith("wed"):
                date = u"三"
            if field_name.startswith("thur"):
                date = u"四"
            if field_name.startswith("fri"):
                date = u"五"
            start = obj.get(field_name, None)
            end = obj.get(time[index+1], None)
            obj["time"] = obj["time"] + u"星期" + date + str(start) + u"点到" + str(end) + u"点 "

def changeWeekEndToRange(obj, time):
    """
    将周末的字段返回前端所要求的数就
    :param obj:
    :param time:
    :return:
    """
    obj["time"] = obj.get("time", "")
    for field_name in time:
        if obj[field_name]:
            if field_name == "sat_morning":
                date = u"星期六早上 "
            if field_name == "sat_afternoon":
                date = u"星期六下午 "
            if field_name == "sat_evening":
                date = u"星期六晚上 "
            if field_name == "sun_morning":
                date = u"星期日早上 "
            if field_name == "sun_afternoon":
                date = u"星期日下午 "
            if field_name == "sun_evening":
                date = u"星期日晚上 "
            obj["time"] = obj["time"] + date

def changePassnot(obj):
    if obj.has_key("pass_not"):
        pass_not = obj["pass_not"]
        if pass_not == 0:
            obj["pass_not"] = u"未通过"
        if pass_not == 1:
            obj["pass_not"] = u""
        if pass_not == 2:
            obj["pass_not"] = u"已通过"

def getTeacherResult(oa):
    """
    家长端获取老师的订单详情结果
    :param oa: 订单
    :return:
    """
    isInvited = ''
    if oa.apply_type == 2:
        #家长主动，finished为0
        #1.老师意愿为1，家长端订单显示为“已邀请”
        #2.老师意愿为2，老师正在上传截图
        #finished为1
        #1. 老师意愿为0，家长意愿为2，老师拒绝
        #2. 老师意愿为2，已成交
        #意愿第一判断可以更简洁
        #finished为2
        #1. 老师意愿为2,管理员审核中
        #2. 老师意愿为0,管理员不通过（暂无）
        if oa.finished == 0:
            if oa.teacher_willing == 1:
                isInvited = u"您已邀请"
            elif oa.teacher_willing == 2:
                isInvited = u"管理员审核中"
        if oa.finished == 1:
            if oa.teacher_willing == 0:
                isInvited = u"老师已拒绝"
            if oa.teacher_willing == 2:
                isInvited = u"已成交"
        if oa.finished == 2:
            isInvited = u"管理员审核中"
    elif oa.apply_type == 1:
        #教师主动，finished为0
        #家长意愿为1，老师向其报名
        #家长意愿为2，老师意愿为1，家长同意
        #家长意愿为2，老师意愿为2，老师正在上传截图
        #finished为1
        #家长意愿为2，老师意愿为2，已成交
        #家长意愿为0，已拒绝
        #finished为2
        #1. 老师意愿为2,管理员审核中
        #2. 老师意愿为0,管理员不通过（暂无）
        if oa.finished == 0:
            if oa.parent_willing == 1:
                isInvited = u"向您报名"
            elif oa.parent_willing == 2 and oa.teacher_willing == 1:
                isInvited = u"您已同意"
            elif oa.parent_willing == 2 and oa.teacher_willing == 2:
                isInvited = u"管理员审核中"
        if oa.finished == 1:
            if oa.parent_willing == 0:
                isInvited = u"您已拒绝"
            elif oa.parent_willing == 2 and oa.teacher_willing == 2:
                isInvited = u"已成交"
        if oa.finished == 2:
            isInvited = u"管理员审核中"
    return isInvited

def getParentResult(oa):
    """
    老师端获取家长的订单详情结果
    :param oa:
    :return:
    """
    result= ''

    if oa.apply_type == 1:
        #教师主动,finished为0
        #1. 家长意愿为1，老师端订单显示为“已报名”
        #2. 家长意愿为2和老师意愿为1，家长同意
        #3. 家长意愿为2和老师意愿为2，老师正在上传截图
        #finished为1
        #1. 家长意愿为0，老师意愿为1，家长拒绝
        #2. 家长意愿为2，老师意愿为2，老师上传截图，完成订单
        #3. 家长意愿为2，老师意愿为0，代表未按时上传截图
        #finished为2
        #1. 老师意愿为2,管理员审核中
        #2. 老师意愿为0,管理员不通过（暂无）
        if oa.finished == 0:
            if oa.parent_willing == 1:
                result = u"您已报名"
            elif oa.parent_willing == 2 and oa.teacher_willing == 1:
                result = u"对方已同意"
            elif oa.parent_willing == 2 and oa.teacher_willing ==2:
                result = u"请上传截图"
        if oa.finished == 1:
            if oa.parent_willing == 0:
                result = u"家长已拒绝"
            elif oa.parent_willing == 2 and oa.teacher_willing == 0:
                result = u"您未按时上传截图"
            elif oa.parent_willing == 2 and oa.teacher_willing == 2:
                result = u"已成交"
        if oa.finished == 2:
            result = u"管理员审核中"
    elif oa.apply_type == 2:
        #家长主动,finished为0
            #1. 老师意愿为1，老师端订单显示为“已邀请”
            #2. 老师意愿为2，老师正在上传截图
            #finished为1
            #1. 老师意愿为0，老师拒绝/老师未按时上传截图
            #2. 老师意愿为2，老师上传截图，管理员通过，完成订单
            #finished为2
            #1. 老师意愿为2,管理员审核中
            #2. 老师意愿为0,管理员不通过（暂无）
        if oa.finished == 0:
            if oa.teacher_willing == 1:
                result = u"对方已邀请"
            elif oa.teacher_willing == 2:
                result = u"请上传截图"
        if oa.finished ==1:
            if oa.teacher_willing == 0:
                result = u"您已拒绝"
            if oa.teacher_willing == 2:
                result = u"已成交"
        if oa.finished == 2:
            result = u"管理员审核中"

    return result

def getAddress(latitude,longitude):
    """
    根据经纬度获取位置信息
    :return:
    """
    url = 'http://apis.map.qq.com/ws/geocoder/v1/?location=' + str(latitude) +','+ str(longitude) +'&key='+ADDRESS_KEY
    import requests
    try:
        res = requests.get(url)
        result = res.json()
        return result['result']['address_component']['city'] + result['result']['address_component']['district']
    except Exception,e:
        print '获取用户位置失败！'
        print 'traceback.print_exc():'; traceback.print_exc()
        return ''
import math

def rad(d):
    return d*math.pi/180.0


def distance(lat1,lng1,lat2,lng2):
    """
    根据经纬度获取距离
    :param lat1:
    :param lng1:
    :param lat2:
    :param lng2:
    :return:
    """
    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius
    if s<0:
        return -s
    else:
        return s

def downloadImg(serverId):
    token = conf.get_access_token()['access_token']
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=' + token +'&media_id=' + serverId
    res = requests.get(url)
    data = res.content
    name = str(int(time.time() * 1000000)) + '.jpg'
    path = dir+name
    with open(path, "wb") as fh:
        fh.write(data)
    return '/static/' + name
