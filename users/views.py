from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import FormView
from users.forms import CustomUserCreationForm


class RegistrationView(FormView):
    form_class = CustomUserCreationForm

    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)
