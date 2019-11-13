from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created{username}")
            login(request, user)
            return redirect("index")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = NewUserForm
    context = {"form": form}
    return render(request, 'users/register.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfull")
    return redirect('index')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged in as {username}")
                return redirect('index')

            else:
                messages.error(request, "Invalid username or password")

        else:
            messages.error(request, "Invalid username or password")


    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def dash(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {'message': None})
    context = {
        "user": request.user
    }
    return render(request, 'users/dash.html', context)