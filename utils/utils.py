import uuid
import os
from django.utils.text import get_valid_filename
from tyf.settings import MEDIA_ROOT


def generate_uuid(length=8, klass=None):
    """Safely generate UUID given length and check if it's unique for the given class."""
    UUID = str(uuid.uuid4())
    length = min(length, len(UUID))
    if klass:
        while klass.objects.filter(identifier=UUID[:length]).exists():
            UUID = str(uuid.uuid4())
    return UUID[:length]


def generate_media_path(instance, filename, key, remove_with_same_key, depth=3, step=1):
    """
    Generate unique directory path for media files.
    'key' is a name of the field of the instance using for generating hash,
    'remove_with_same_key' is a boolean value, if 'True' file with the same key will be deleted,
    'depth' specifies the number of directories in the path,
    'step' specifies the number of characters in first (depth - 1) directories in path.
    """
    UUID = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(getattr(instance, key))))
    path = ""
    for i in range(depth - 1):
        path = os.path.join(path, UUID[(i * step) : ((i + 1) * step)])
    extension = filename.split(".")[-1]
    filename = get_valid_filename(f"{UUID}.{extension}")
    path = os.path.join(path, UUID[(depth - 1) * step :], filename)
    if remove_with_same_key and os.path.exists(os.path.join(str(MEDIA_ROOT), path)):
        os.remove(os.path.join(str(MEDIA_ROOT), path))
    return path
