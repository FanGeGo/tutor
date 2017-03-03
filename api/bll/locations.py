#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from django.utils import timezone
import traceback
__author__ = 'yinzishao'

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from api.serializers import OrderApplySerializer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from tutor.http import JsonResponse,JsonError
from api.models import Teacher,AuthUser,ParentOrder,OrderApply,Message,Locations
from django.db import transaction
from wechat_auth.helpers import changeSingleBaseToImg, getTeacherResult, getParentResult,getAddress
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def setLocations(request):
    """
    用户设置locations
    :param request:
        {
            "longitude":39.984154,
            "latitude":116.307490
        }
    :return:
    """
    try:
        longitude = float(request.data.get("longitude", -1))
        latitude = float(request.data.get("latitude", -1))
        user = AuthUser.objects.get(username=request.user.username)
        address = getAddress(longitude,latitude)
        locations = user.locations_set.all()
        if len(locations) > 0:
            l=locations[0]
            l.longitude=longitude
            l.latitude=latitude
            l.address=address
        else:
            l = Locations(longitude=longitude,latitude=latitude,wechat=user,address=address)
        l.save()
        return JsonResponse()
    except Exception,e:
        print 'traceback.print_exc():'; traceback.print_exc()
        return JsonError(e.message)

@login_required()
@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication))
def getUserAddress(request):
    """

    :param request:
    :return:
    """
    longitude = float(request.data.get("longitude", -1))
    latitude = float(request.data.get("latitude", -1))
    address = getAddress(longitude,latitude)
    return JsonResponse({'address':address})
