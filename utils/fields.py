import PIL
from django.db import models
from django.db.models.fields.files import FieldFile
from imagekit import ImageSpec

from .files import upload_file


class CompressedImageSpec(ImageSpec):
    format = "webp"
    options = {"quality": 75}


class CompressedImageFile(FieldFile):
    def save(self, name, content, save=True):
        try:
            with open(content.temporary_file_path(), "rb") as file:
                if not file.name.endswith(".gif"):
                    source_file = CompressedImageSpec(source=file)
                    return super().save(name, source_file.generate(), save)
        except PIL.UnidentifiedImageError:
            pass

        return super().save(name, content, save)


class CompressedMixin:
    attr_class = CompressedImageFile

    def __init__(self, upload_to=upload_file, **kwargs):
        super().__init__(upload_to=upload_to, **kwargs)


class CompressedImageField(CompressedMixin, models.ImageField):
    pass


class CompressedMediaField(CompressedMixin, models.FileField):
    pass


class PriceField(models.DecimalField):
    def __init__(self, verbose_name=None, name=None, max_digits=8, decimal_places=2, **kwargs):
        super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)
