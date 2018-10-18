import django_filters
from post_office.models import EmailTemplate

from mailing.models import EmailTask


class EmailTaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = EmailTask
        fields = ["start_date", "sent"]


class EmailTemplateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = EmailTemplate
        fields = {"subject": ["icontains"], "created": ["exact"]}
