from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import CommentsSerializer, VotesSerializer
from ..models import Comments, Votes


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.filter(is_deleted=False, is_verified=True)
    serializer_class = CommentsSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="create",
        permission_classes=[IsAuthenticated],
    )
    def create_comment(self, request):
        serializer = CommentsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "اطلاعات وارد شده معتبر نمی باشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        idea = serializer.validated_data["idea"]
        content = serializer.validated_data["content"]

        try:
            comment = Comments.objects.create(
                author=request.user, idea=idea, content=content
            )

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "data": CommentsSerializer(comment).data,
                "message": "نظر شما با موفقیت ذخیره شد",
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="update",
        permission_classes=[IsAuthenticated],
    )
    def update_comment(self, request, pk=None):
        serializer = CommentsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "اطلاعات وارد شده معتبر نمی باشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        idea = serializer.validated_data["idea"]
        content = serializer.validated_data["content"]

        try:
            comment = self.queryset.get(id=pk)  # type: ignore
            comment.idea = idea
            comment.content = content
            comment.save()
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "data": CommentsSerializer(comment).data,
                "message": "ذخیره تغییرات با موفقیت انجام شده",
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="list",
        permission_classes=[IsAuthenticated],
    )
    def list_comments(self, pk=None):
        try:
            comments = self.queryset.filter(idea=pk)  # type: ignore
            return Response(
                {
                    "data": CommentsSerializer(comments, many=True).data,
                    "message": "درخواست انجام شد",
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        url_path="delete",
        permission_classes=[IsAuthenticated],
    )
    def delete(self, pk=None):
        try:
            comment = self.queryset.get(id=pk)  # type: ignore
            comment.is_deleted = True
            comment.save()
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "data": CommentsSerializer(comment).data,
                "message": "ایده با موفقیت حذف شد",
            },
            status=status.HTTP_200_OK,
        )


class VotesViewSet(viewsets.ModelViewSet):
    queryset = Votes.objects.filter()
    serializer_class = VotesSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="is_like",
        permission_classes=[IsAuthenticated],
    )
    def create_vote(self, request):
        serializer = VotesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "اطلاعات وارد شده معتبر نمی باشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        idea = serializer.validated_data["idea"]
        is_like = serializer.validated_data["is_like"]

        try:
            vote = Votes.objects.update_or_create(
                idea=idea, user=request.user, is_like=is_like
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "data": VotesSerializer(vote).data,
                "message": "نظر شما با موفقیت ذخیره شد",
            },
            status=status.HTTP_201_CREATED,
        )
