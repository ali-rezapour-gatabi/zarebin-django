from rest_framework import serializers
from .models import Ideas, Comments, Votes
from users.serializers import UserSerializer


class IdeasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ideas
        fields = (
            "id",
            "title",
            "description",
            "domain",
            "comments_visibility",
        )


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            "id",
            "idea",
            "author",
            "content",
        )


class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = (
            "id",
            "idea",
            "user",
            "is_like",
        )


class IdeasListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Ideas
        fields = (
            "id",
            "title",
            "description",
            "domain",
            "comments_visibility",
            "author",
            "created_at",
            "like_count",
            "comment_count",
            "author",
        )
