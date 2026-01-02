from rest_framework import serializers
from .models import Ideas, Comments, Votes


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
