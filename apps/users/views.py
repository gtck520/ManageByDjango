# _*_ encoding:utf-8 _*_
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler, jwt_decode_handler

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer, CaptchaSerializer, \
    CaptchaCheckSerializer, UserUpdateSerializer
from ManageByDjango.settings import APIKEY
from common.yunpian import YunPian
from .models import VerifyCode
from common.views import captcha, jarge_captcha

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except Exception as e:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class CaptchaViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    图片验证码生成
    """
    serializer_class = CaptchaSerializer

    def list(self, request, *args, **kwargs):
        captchajson = captcha()
        if captchajson:
            host = 'http://' + request.get_host()
            sms_status = captchajson
            sms_status['image_url'] = host + captchajson['image_url']
            return Response(sms_status, status=status.HTTP_200_OK)
        else:
            return Response({"error": "获取图片码错误"}, status=status.HTTP_400_BAD_REQUEST)


class CaptchaCheckViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    图片验证码验证
    """
    serializer_class = CaptchaCheckSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        imagecode = serializer.validated_data["imagecode"]
        hashkey = serializer.validated_data["hashkey"]
        checkstatus = jarge_captcha(imagecode, hashkey)
        if checkstatus:
            sms_status = checkstatus
            return Response({'status': sms_status}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "图片码错误"}, status=status.HTTP_400_BAD_REQUEST)


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        sms_status["code"] = 0 # 测试开启 不论服务商是否发送成功均当作成功处理，正式需去掉
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        elif self.action == "update":
            return UserUpdateSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve" or self.action == "update":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class UserInfoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    根据token获得用户详细信息
    """

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 原来自己写的验证jwt
    # def list(self, request, *args, **kwargs):
    #     token = request.META.get("HTTP_JWT")
    #     if token:
    #         user_dict = jwt_decode_handler(token=token)
    #         user = User.objects.get(id=user_dict['user_id'])
    #         serializer = self.get_serializer(user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)


