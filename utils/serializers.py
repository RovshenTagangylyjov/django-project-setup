from rest_framework import serializers


class MediaFileField(serializers.ImageField):
    def to_representation(self, value):
        request = self.context.get("request", None)

        url = value
        if hasattr(value, "url"):
            url = value.url

        if request:
            url = request.build_absolute_uri(url)
        else:
            url = f"http://host{url}"

        return url
