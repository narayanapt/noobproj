from django.shortcuts import render
from .models import Profile


# Create your views here.


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from noobproj.apps.core.forms import SignUpForm

def home(request):
    return render(request, 'core/home.html')

def blog(request):
    return render(request, 'core/blog.html')

def qa(request):
    return render(request, 'core/qa.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def verify(request, uid):
    try:
       user =  Profile.objects.get(email_uid = uid,  verified = False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")
    user.verified = True
    user.save()

    return redirect('home')
