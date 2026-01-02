from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "created_at",
        )

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None


class OtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)
    first_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class Meta:
        fields = (
            "code",
            "first_name",
            "last_name",
            "phone_number",
        )
