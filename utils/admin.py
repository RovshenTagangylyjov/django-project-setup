import operator
from functools import reduce

from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class BaseContentTypeListFilter(SimpleListFilter):
    title = _("content types")
    parameter_name = "content_type"
    models: list[str] = []

    def lookups(self, request, model_admin):
        queries = []

        for model in self.models:
            app_label, name = model.split(".")
            queries.append(Q(app_label=app_label, model__iexact=name))

        content_types = ContentType.objects.filter(reduce(operator.or_, queries))

        return [(ct.id, ct.app_labeled_name) for ct in content_types]

    def queryset(self, request, queryset):
        if content_type := self.value():
            return queryset.filter(content_type=content_type)

        return queryset
