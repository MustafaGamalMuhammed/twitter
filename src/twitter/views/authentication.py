from django.shortcuts import redirect, render, reverse
from django.contrib import auth
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from twitter.forms import SignupForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("signin")
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
    
    context = {'form': SignupForm()}

    return render(request, 'twitter/signup.html', context)


class SigninView(views.LoginView):
    template_name = "twitter/signin.html"
    
    def get_success_url(self):
        return reverse("home")


@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('signin')
