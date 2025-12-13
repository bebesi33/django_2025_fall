from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import logging
from django.views import View
from users.perm_decorators import anonymous_required


logger = logging.getLogger(__file__)


@anonymous_required("/")
def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            # Csak sikeres authentication után engedjük a következő lépésre a usert-t
            # (None ha nem jön össze...)
            logger.warning(f"User : {str(user)}.")
            if user:
                login(request, user)
                messages.success(request, "Successful login!", extra_tags="login")
            else:
                messages.warning(
                    request, "Invalid username or password", extra_tags="login"
                )
        else:
            messages.warning(
                request, "Invalid username or password", extra_tags="login"
            )
    return redirect("index")


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, f"You have been logged out.", extra_tags="login")
    return redirect("index")


@anonymous_required("/")
def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Successful Sign up!", extra_tags="registration")
            return render(request, "registration.html")
        else:
            # logger.warning("Not ok... :'(")
            messages.warning(
                request, f"Invalid form submission!", extra_tags="registration"
            )
            return render(request, "registration.html", {"form": form})
    elif request.method == "GET":
        form = UserCreationForm()
        return render(request, "registration.html", {"form": form})


class RegisterView(View):
    template_name = "registration.html"

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Successful Sign up!", extra_tags="registration")
            return render(request, self.template_name)
        else:
            # logger.warning("Not ok... :'(")
            messages.warning(
                request, f"Invalid form submission!", extra_tags="registration"
            )
            return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {"form": form})
