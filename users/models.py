from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .utils import expert_document_upload_to, avatar_upload_to
from .manage import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "users"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.phone_number} ({self.first_name} {self.last_name})"


class Domain(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "domains"
        verbose_name_plural = "domains"


class Experts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    subdomain = models.JSONField(null=False, blank=False)
    skills = models.JSONField(null=False, blank=False)
    province = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    contract_link = models.JSONField(null=True, blank=True)
    contract_number = models.JSONField(null=True, blank=True)
    years_of_experience = models.CharField(max_length=100, null=True, blank=True)
    sample_job = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    activation = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "experts"
        verbose_name_plural = "experts"


class ExpertsDocument(models.Model):
    user = models.ForeignKey(
        Experts,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    file = models.FileField(upload_to=expert_document_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "experts_documents"
        verbose_name_plural = "experts_documents"
