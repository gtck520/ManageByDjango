# 序列化
from django.contrib.auth.models import User,Group
from users.models import UserProfile
from  rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserProfile
        fields = "__all__"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = "__all__"
class UserPostSerializer(serializers.HyperlinkedModelSerializer):

    #自定义一个tellphone序列化字段
    telephone = serializers.CharField(required=True, write_only=True, max_length=11, min_length=11,
                                 error_messages={
                                        "blank": "请输入电话号码",
                                        "required": "请输入电话号码",
                                        "max_length": "电话号码格式错误",
                                        "min_length": "电话号码格式错误"
                                 },
                                help_text="电话号码",validators=[UniqueValidator(queryset=User.objects.all(), message="电话号码已经存在")])
    #User中没有code字段，这里需要自定义一个code序列化字段
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,
                                 error_messages={
                                        "blank": "请输入验证码",
                                        "required": "请输入验证码",
                                        "max_length": "验证码格式错误",
                                        "min_length": "验证码格式错误"
                                 },
                                help_text="验证码")
    #验证用户名是否存在
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    #验证code
    def validate_code(self, code):
        # 用户注册，已post方式提交注册信息，post的数据都保存在initial_data里面
        #username就是用户注册的手机号，验证码按添加时间倒序排序，为了后面验证过期，错误等
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        if verify_records:
            # 最近的一个验证码
            last_record = verify_records[0]
            # 有效期为五分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")
    # profile = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='telephone'
    #  )
    class Meta:
        model = User
        fields = ("username","telephone","password","code")
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =Group
        fields = "__all__"