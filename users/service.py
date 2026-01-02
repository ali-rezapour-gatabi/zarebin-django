from django.core.cache import cache
from .models import User


class UserService:
    def verify_otp(
        self, phone: str, first_name: str | None, last_name: str | None, code: str
    ):
        if not phone or not code:
            raise ValueError("شماره همراه و کد تایید الزامی است")

        otp = cache.get(f"otp:{phone}")
        if not otp:
            raise ValueError("کد تایید منقضی شده است")

        if str(otp) != str(code):
            raise ValueError("کد اشتباه می‌باشد")

        user, created = User.objects.get_or_create(
            phone_number=phone,
            defaults={"first_name": first_name, "last_name": last_name},
        )

        if not created:
            changed = False
            if first_name and not user.first_name:
                user.first_name = first_name
                changed = True
            if last_name and not user.last_name:
                user.last_name = last_name
                changed = True
            if changed:
                user.save(update_fields=["first_name", "last_name"])

        if not user.is_active:
            raise ValueError("دسترسی کاربر محدود شده، لطفاً با پشتیبانی تماس بگیرید")

        cache.delete(f"otp:{phone}")

        return user
