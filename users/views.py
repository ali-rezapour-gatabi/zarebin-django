import random
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from .serializers import UserSerializer, OtpSerializer
from .service import UserService

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False, is_active=True)
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"], url_path="send-otp")
    def send_otp(self, request):
        phone = request.data.get("phone_number")
        if not phone:
            return Response(
                {"message": "شماره همراه مورد نیاز است"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            code = f"{random.randint(0, 999999):06d}"
            cache.set(f"otp:{phone}", code, 120)
            # only for test remove them after add otp sms panel
            print(code)
        except ValueError as e:
            return Response(
                {"message": "خطای سمت سرور صورت گرفته لطفا مجدد تلاش کنید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "کد با موفقیت ارسال شد", "success": True},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="verify-otp")
    def verify_otp(self, request):
        serializer = OtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "اطلاعات وارد شده معتبر نمی باشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        phone = serializer.validated_data["phone_number"]  # type: ignore
        first_name = serializer.validated_data["first_name"]  # type: ignore
        last_name = serializer.validated_data["last_name"]  # type: ignore
        code = serializer.validated_data["code"]  # type: ignore

        try:
            user = UserService().verify_otp(phone, first_name, last_name, code)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "data": UserSerializer(user).data,
                "token": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "تایید موفقیت انجام شد",
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="get",
        permission_classes=[IsAuthenticated],
    )
    def get(self, request):
        user = request.user
        user_data = User.objects.filter(
            id=user.id, is_deleted=False, is_active=True
        ).first()
        if not user_data:
            return Response(
                {"message": "کاربر مورد نظر یافت نشد"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"data": UserSerializer(user_data).data, "message": "درخواست انجام شد"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        refresh = request.data.get("refresh") or request.data.get("token")
        if not refresh:
            return Response(
                {"success": False, "message": "دسترسی مجاز نیست"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except ValueError:
            return Response(
                {"success": False, "message": "دسترسی مجاز نیست"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": True, "message": "خروج از سیستم موفقیت انجام شد"},
            status=status.HTTP_205_RESET_CONTENT,
        )
