from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Click, UserPreference
from .forms import UserPreferenceForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Create a UserPreference instance for the new user
            UserPreference.objects.get_or_create(user=user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                UserPreference.objects.get_or_create(user=user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def index(request):
    try:
        click = Click.objects.get(user=request.user)
    except Click.DoesNotExist:
        click = Click.objects.create(user=request.user)
    return render(request, 'index.html', {'click_count': click.count})

@login_required
def increment_click_count(request):
    if request.method == 'POST':
        click, created = Click.objects.get_or_create(user=request.user)
        click.count += 1
        click.save()
        return JsonResponse({'click_count': click.count})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def leaderboard(request):
    leaderboard_data = Click.objects.all().order_by('-count')
    return render(request, 'leaderboard.html', {'leaderboard_data': leaderboard_data})




@login_required
def update_btext(request):
    # Ensure the UserPreference instance exists
    user_preference, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=user_preference)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = UserPreferenceForm(instance=user_preference)

    return render(request, 'update_btext.html', {'form': form, 'preference': user_preference})


@login_required
def delete_preference(request):
    preference = get_object_or_404(UserPreference, user=request.user)
    if preference.user == request.user:  # Ensure users can only delete their own preferences
        preference.delete()
    return redirect('index')  # Redirect to the index page

