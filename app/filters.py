from django_filters import rest_framework as filters

from .models import PurchaseOrder


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """
    For more Information check BaseInFilter in `django-filter` package
    """


class PurchaseOrderFilter(filters.FilterSet):

    vendor = NumberInFilter(field_name="vendor", lookup_expr="in")

    class Meta:
        model = PurchaseOrder
        fields = ("vendor",)
