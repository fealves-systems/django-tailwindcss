from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetView
import logging
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import CustomUser, CustomUserManager
from datetime import datetime
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

def accounts_login(request):
    print("User: ", request.user)
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("user is ok...")
            login(request, user)
            messages.info(request, f"Hello, {user.username}! Welcome to FEA_Project.")
            # SaveLoginHistory(user, "Login")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")

    now = datetime.now()
    timestamp_str = now.strftime('%Hh%Mm%S.%f')[:-3]
    context = {
        'timestamp': timestamp_str
    }

    return render(request, "accounts/login.html")

@login_required
def accounts_logout(request):
    logout(request)
    return redirect("login")

def accounts_register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower() if 'email' in form.cleaned_data else None  
            user.save()
            # SaveLoginHistory(user, "Registration")
            messages.success(request, "Your user account has been created.")
            login(request, user)
            return redirect("index")
        # else:
            # add_form_errors_as_messages(request, form)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"page_title": "User Registration", "form": form})

def accounts_forgot_password(request):
    if request.user.is_authenticated:
        return redirect("index")

    return render(request, "accounts/forgot_password.html")

class accounts_password_reset(PasswordResetView):
    template_name = 'accounts/password_reset_confirm.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = '/accounts/password_reset_done/'

class accounts_password_reset_done(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class accounts_password_reset_confirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete') 

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # add_form_errors_as_messages(self.request, form, 1)
        return super().form_invalid(form)

class accounts_password_reset_complete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
