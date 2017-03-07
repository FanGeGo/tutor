# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage,
    VideoMessage, LinkMessage, LocationMessage, EventMessage
)
from wechat_sdk.context.framework.django import DatabaseContextStore
from django.conf import settings
from api.models import AuthUser

TOKEN=settings.TOKEN
APP_ID=settings.APP_ID
APP_SECRET=settings.APP_SECRET
DOMAIN=settings.DOMAIN

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=TOKEN,
    appid=APP_ID,
    appsecret=APP_SECRET
)

index_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APP_ID + '&redirect_uri='+DOMAIN+'authorization&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=1#wechat_redirect'
index_pic = 'http://www.ziqiangxuetang.com/static/images/newlogo.png'
admin_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APP_ID + '&redirect_uri='+DOMAIN+'adminAuthorization&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=1#wechat_redirect'
admin_pic = 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg'

@csrf_exempt
def index(request):
    """
    微信端接入,跳转主页
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # POST
    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
    # 利用本次请求中的用户OpenID来初始化上下文对话
    context = DatabaseContextStore(openid=message.source)

    response = None

    if isinstance(message, TextMessage):
        # step = context.get('step', 1)  # 当前对话次数，如果没有则返回 1
        # last_text = context.get('last_text')  # 上次对话内容
        content = message.content.strip()  # 当前会话内容

        if message.content == '家教':
            response = wechat_instance.response_news([
                {
                    'title': '家教平台',
                    'picurl': index_pic,
                    'description': '家教平台',
                    'url': index_url,
                }, {
                    'title': '管理后台',
                    'picurl': admin_pic,
                    'url': admin_url,
                }
            ])
            return HttpResponse(response, content_type="application/xml")


        # 文本消息结束

    elif isinstance(message, VoiceMessage):
        reply_text = '语音信息我听不懂/:P-(/:P-(/:P-('
    elif isinstance(message, ImageMessage):
        reply_text = '图片信息我也看不懂/:P-(/:P-(/:P-('
    elif isinstance(message, VideoMessage):
        reply_text = '视频我不会看/:P-('
    elif isinstance(message, LinkMessage):
        reply_text = '链接信息'
    elif isinstance(message, LocationMessage):
        reply_text = '地理位置信息'
    elif isinstance(message, EventMessage):  # 事件信息
        if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            reply_text = 'reply_text'

            # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
            if message.key and message.ticket:
                reply_text += '\n来源：扫描二维码关注'
            else:
                reply_text += '\n来源：搜索名称关注'
        elif message.type == 'unsubscribe':
            reply_text = '取消关注事件'
        elif message.type == 'scan':
            reply_text = '已关注用户扫描二维码！'
        elif message.type == 'location':
            reply_text = '上报地理位置'
        elif message.type == 'click':
            reply_text = '自定义菜单点击'
        elif message.type == 'view':
            reply_text = '自定义菜单跳转链接'
        elif message.type == 'templatesendjobfinish':
            reply_text = '模板消息'

    response = wechat_instance.response_text(content=reply_text)
    return HttpResponse(response, content_type="application/xml")

from weixin.client import WeixinAPI
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def authorization(request):
    """
    获取用户信息，登录,跳转
    :param request:
    :return:
    """
    """
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx6fe7f0568b75d925&redirect_uri=http://www.yinzishao.cn/authorization&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=1#wechat_redirect
    """
    code = request.GET.get('code')
    auth_redirect_uri = DOMAIN + "authorization"
    api = WeixinAPI(appid=APP_ID,
	    app_secret=APP_SECRET,
	    redirect_uri=auth_redirect_uri)
    auth_info = api.exchange_code_for_access_token(code=code)
    api = WeixinAPI(access_token=auth_info['access_token'])
    resp = api.user(openid=auth_info['openid'])
    request.session['info'] = resp
    openid = resp['openid']

    try:
        user = User.objects.get(username=openid)
    except User.DoesNotExist,e:
        print "user not exist"
        user = User.objects.create_user(openid,password=openid)
    if user and user.is_active:
        user = authenticate(username=openid, password=openid)
        login(request,user)
        user = AuthUser.objects.get(username=request.user.username)
    else:
        #返回错误
        return HttpResponse('error')
    #TODO：判断是不是已经填了问卷并在数据库创建了数据
    teacher = user.teacher_set.all()
    parent =  user.parentorder_set.all()
    if not len(teacher) and not len(parent):
        #都不存在，返回填问卷界面
        redirect_uri= DOMAIN + 'tutor_web/view/index.html'

    else:
        if len(teacher):
            #已填问卷返回，主页
            redirect_uri=DOMAIN + 'tutor_web/view/teacherPage.html'
        elif len(parent):
            redirect_uri=DOMAIN + 'tutor_web/view/parentPage.html'
    return redirect(redirect_uri)
@csrf_exempt
def login_from_pwd(request, id=2):
    openid = 'odE4WwK3g05pesjOYGbwcbmOWTnc' + str(id)
    try:
        user = User.objects.get(username=openid)
    except User.DoesNotExist,e:
        print "user not exist"
        user = User.objects.create_user(openid,password=openid)
    if user and user.is_active:
        user = authenticate(username=openid, password=openid)
        login(request,user)
        request.session['info'] = {
            'province': 'Guangdong',
            'openid': 'odE4WwK3g05pesjOYGbwcbmOWTnc',
            'headimgurl': 'http://wx.qlogo.cn/mmopen/fR41VbicrntibxhNY3WfaKgHBTbe1d6Gz0tPjhHpicwJerJiaAictfHiaLiaqCcVIs5EKOzsD4yaiadyUIUHK2Lu07K9EqArtialVJd4b/0',
            'language': 'zh_CN',
            'city': 'Yunfu',
            'country': 'CN',
            'sex': 1,
            'privilege': [],
            'nickname': u'\u5c39\u5b50\u52fa'
        }
    return redirect('/updateTeacher/')

def login_admin(request):
    name = 'yinzishao'
    user = authenticate(username=name, password=name)
    login(request,user)
    request.session['info'] = {
            'province': 'Guangdong',
            'openid': 'odE4WwK3g05pesjOYGbwcbmOWTnc',
            'headimgurl': 'http://wx.qlogo.cn/mmopen/fR41VbicrntibxhNY3WfaKgHBTbe1d6Gz0tPjhHpicwJerJiaAictfHiaLiaqCcVIs5EKOzsD4yaiadyUIUHK2Lu07K9EqArtialVJd4b/0',
            'language': 'zh_CN',
            'city': 'Yunfu',
            'country': 'CN',
            'sex': 1,
            'privilege': [],
            'nickname': u'\u5c39\u5b50\u52fa'
        }
    return redirect('/getNum/')
#KN5BZ-WXX6G-P2CQ6-II5X4-Q3G65-XMF7C
#http://apis.map.qq.com/ws/geocoder/v1/?location=39.984154,116.307490&key=KN5BZ-WXX6G-P2CQ6-II5X4-Q3G65-XMF7C

def testJs(request):
    return render(request, 'testjs.html')

def adminAuthorization(request):
    """
    获取用户信息，登录,跳转
    :param request:
    :return:
    """
    auth_redirect_uri = DOMAIN + "adminAuthorization"
    code = request.GET.get('code')
    api = WeixinAPI(appid=APP_ID,
	    app_secret=APP_SECRET,
	    redirect_uri=auth_redirect_uri)
    auth_info = api.exchange_code_for_access_token(code=code)
    api = WeixinAPI(access_token=auth_info['access_token'])
    resp = api.user(openid=auth_info['openid'])
    request.session['info'] = resp
    return redirect(DOMAIN + 'administor/view/index.html')
