
from pathlib import PurePosixPath
from urllib.parse import quote

from django import template
from django.conf import settings

register = template.Library()


def get_filename(file_path):
    return PurePosixPath(str(file_path).replace("\\", "/")).name


@register.filter
def cloudinary_image(image_path):
    if not image_path:
        return ""

    base_url = settings.CLOUDINARY_IMAGE_URL.rstrip("/")
    return f"{base_url}/{quote(get_filename(image_path))}"


@register.filter
def cloudinary_video(video_path):
    if not video_path:
        return ""

    base_url = settings.CLOUDINARY_IMAGE_URL.rstrip("/")
    video_url = base_url.replace("/image/upload", "/video/upload")

    return f"{video_url}/{quote(get_filename(video_path))}"
