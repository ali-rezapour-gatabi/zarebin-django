import os


def expert_document_upload_to(expert, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    return f"users/{expert.user.id}/experts/{filename}{ext}"


def avatar_upload_to(expert, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    return f"users/{expert.user.id}/{filename}{ext}"
