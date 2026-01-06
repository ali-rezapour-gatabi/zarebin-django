from django.db import models


class Ideas(models.Model):

    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField()
    domain = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True)
    comments_visibility = models.BooleanField(default=True)

    class Meta:
        verbose_name = "ideas"
        verbose_name_plural = "ideas"

    def __str__(self):
        return f"{self.title}"


class Comments(models.Model):
    idea = models.ForeignKey(Ideas, on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    verified_at = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "comments"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"{self.content}"


class Votes(models.Model):
    idea = models.ForeignKey(Ideas, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "votes"
        verbose_name_plural = "votes"

    def __str__(self):
        return f"{self.user}"
