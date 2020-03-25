from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View, CreateView, ListView
from users.models import User
from backend.account.forms import LoginForm, UserForm, CustomerUserForm, BusinessUserForm
from backend.account.models import BusinessUser


class SignupView(View):
    """
    This class will create a new user with its associated profile if requested via POST, or it will show a sign up
    form if GET.
    This class will use ``get()`` or ``post()`` depending on the HTTP request.The method that will "decide" what to do
    is dispatch(), that has not been overridden.
    """
    user_form_prefix = 'user_signup'
    profile_form_prefix = 'profile_signup'

    form_context = {
        user_form_prefix: UserForm(prefix=user_form_prefix),
        profile_form_prefix: CustomerUserForm(prefix=profile_form_prefix),
    }
    template_name = 'account/signup.html'

    def get(self, request):
        context = self.form_context
        context['login_form'] = LoginForm(auto_id='login_%s')
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserForm(request.POST, prefix=self.user_form_prefix)
        profile_form = CustomerUserForm(request.POST, prefix=self.profile_form_prefix)

        if all((user_form.is_valid(), profile_form.is_valid())):
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.base_user_id = user.pk
            profile.save()
            messages.success(request, message=_('User successfully created. Now login!'))
            return redirect('webapp:homepage')
        else:
            return render(request, self.template_name, context={
                self.user_form_prefix: user_form,
                self.profile_form_prefix: profile_form
            })


class BusinessSignupView(View):
    """
    This class will create a new user with its associated profile if requested via POST, or it will show a sign up
    form if GET.
    This class will use ``get()`` or ``post()`` depending on the HTTP request.The method that will "decide" what to do
    is dispatch(), that has not been overridden.
    """
    user_form_prefix = 'user_signup'
    business_profile_form_prefix = 'business_profile_signup'

    form_context = {
        user_form_prefix: UserForm(prefix=user_form_prefix),
        business_profile_form_prefix: BusinessUserForm(prefix=business_profile_form_prefix),
    }
    template_name = 'account/business_signup.html'

    def get(self, request):
        context = self.form_context
        context['login_form'] = LoginForm(auto_id='login_%s')
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserForm(request.POST, prefix=self.user_form_prefix)
        business_profile_form = BusinessUserForm(request.POST, prefix=self.business_profile_form_prefix)

        if all((user_form.is_valid(), business_profile_form.is_valid())):
            user = user_form.save()
            business_profile = business_profile_form.save(commit=False)
            business_profile.owner_id = user.pk
            business_profile.url = BusinessUser.get_url(self, business_profile.activity_name)
            business_profile.save()
            messages.success(request, message=_('Business User successfully created. Now login!'))
            return redirect('webapp:homepage')
        else:
            return render(request, self.template_name, context={
                self.user_form_prefix: user_form,
                self.business_profile_form_prefix: business_profile_form
            })


class UserProfileView(TemplateView):
    """
    View to show a user's profile.
    """
    template_name = 'account/userprofile.html'    # todo ????

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs['user_id'] == self.request.user.pk:
            usr = get_object_or_404(User, pk=kwargs['user_id'])
            context['viewed_user'] = usr
            return context
