from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View, CreateView, ListView
from backend.account.models import BusinessUser
from backend.account.forms import LoginForm
from users.models import User


class HomePageView(TemplateView):
    """
    Homepage view.
    """
    template_name = 'webapp/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            activities = BusinessUser.objects.all() # TODO da sistemare con object-404?
        except IndexError:
            activities = None
        context['activities'] = activities
        context['login_form'] = LoginForm(auto_id='login_%s')

        return context


class ShowActivityView(TemplateView):
    """
        View to show a activity's webpage.
        """
    template_name = 'webapp/eatery/activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = get_object_or_404(BusinessUser, url=kwargs['businessuser_name'])
        user = get_object_or_404(User, id=activity.owner_id)
        context['viewed_activity'] = activity
        context['business_user'] = user
        context['login_form'] = LoginForm(auto_id='login_%s')
        return context


class NewActivityView(CreateView):         # set the template, upload logo  and image, add each product
    pass


def error404(request, *args):  # status_code = 404
    template_name = 'webapp/error_404.html'
    data = {}
    return render(request, template_name, data)


def error403(request, *args):  # status_code = 403
    template_name = 'webapp/error_403.html'
    data = {}
    return render(request, template_name, data)
