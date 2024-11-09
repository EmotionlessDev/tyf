import uuid
import functools
import os
from django.utils.text import get_valid_filename


def create_unique_dir(instance, filename, depth=3, step=1):
    UUID = str(uuid.uuid4())
    path = ""
    for i in range(depth - 1):
        path = os.path.join(path, UUID[(i * step) : ((i + 1) * step)])
    extension = filename.split(".")[-1]
    filename = get_valid_filename(f"{instance.pk}.{extension}")
    path = os.path.join(path, UUID[(depth - 1) * step :], filename)
    return path
