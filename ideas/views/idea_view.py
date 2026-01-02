from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import IdeasSerializer
from ..models import Ideas


class IdeasViewSet(viewsets.ModelViewSet):
    queryset = Ideas.objects.filter(is_deleted=False, is_verified=True)
    serializer_class = IdeasSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="create",
        permission_classes=[IsAuthenticated],
    )
    def create_idea(self, request):
        serializer = IdeasSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "اطلاعات وارد شده معتبر نمی باشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        domain = serializer.validated_data["domain"]
        title = serializer.validated_data["title"]
        description = serializer.validated_data["description"]
        comments_visibility = serializer.validated_data["comments_visibility"]

        try:
            idea = Ideas.objects.create(
                author=request.user,
                domain=domain,
                title=title,
                description=description,
                comments_visibility=comments_visibility,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "data": IdeasSerializer(idea).data,
                "message": "ایده مورد نظر با موفقیت ذخیره شد",
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="update",
        permission_classes=[IsAuthenticated],
    )
    def update_idea(self, request, pk=None):
        serializer = IdeasSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "اطلاعات وارد شده معتبر نمی باشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        domain = serializer.validated_data["domain"]
        title = serializer.validated_data["title"]
        description = serializer.validated_data["description"]
        comments_visibility = serializer.validated_data["comments_visibility"]

        try:
            idea = Ideas.objects.get(id=pk)
            idea.domain = domain
            idea.title = title
            idea.description = description
            idea.comments_visibility = comments_visibility
            idea.save()
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "data": IdeasSerializer(idea).data,
                "message": "ذخیره تغییرات با موفقیت انجام شده",
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="delete",
        permission_classes=[IsAuthenticated],
    )
    def delete(self, request, pk=None):
        try:
            idea = Ideas.objects.get(id=pk)
            idea.is_deleted = True
            idea.save()
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "data": IdeasSerializer(idea).data,
                "message": "ایده با موفقیت حذف شد",
            },
            status=status.HTTP_200_OK,
        )
