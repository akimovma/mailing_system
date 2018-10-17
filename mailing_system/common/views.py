from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView
from django.core.exceptions import ImproperlyConfigured


class LoginRequired(LoginRequiredMixin):
    login_url = '/accounts/login/'


class LoginRequiredDetailView(LoginRequired, DetailView):
    pass


class LoginRequiredListView(LoginRequired, ListView):
    pass


class LoginRequiredCreateView(LoginRequired, CreateView):
    pass


class FilteredMixin:
    filterset_class = None

    def get_filterset_class(self):
        if not self.filterset_class:
            raise ImproperlyConfigured("Need to add 'filter_class' when used"
                                       "FilteredMixin")
        return self.filterset_class

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        filterset_class = self.get_filtesetr_class()
        filterset = filterset_class(self.request.GET,
                                    queryset=self.get_queryset())
        context['filter'] = filterset
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        filterset = self.get_filterset_class()
        qs = filterset(self.request.GET, queryset=queryset).qs
        return qs
