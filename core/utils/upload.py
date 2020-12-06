from django.utils import timezone
from django.utils.text import slugify


__all__ = ["generate_upload_path"]


def generate_upload_path(instance, filename):
    model_name = slugify(f"{instance._meta.model_name}")
    return f"{model_name}/{timezone.now().strftime('%Y-%m-%d_%H-%M-%s')}/{filename}"
