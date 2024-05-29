from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile


from PIL import Image
from .forms import UserRegistrationForm, UserLoginForm

# Create your views here.

def logout_page(request):
    logout(request)
    return redirect('login_page')


def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_page')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})



def register_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user=user,
                created_by = user,
                updated_by = user,
                )

            profile.save()
            login(request, user)
            return redirect('dashboard_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def update_profile_picture(request):
    queryset = Profile.objects.filter(user=request.user.id).first()
    if request.method == 'POST':
        profile_picture: UploadedFile = request.FILES.get('profile_picture')
        
        if profile_picture:
            # Check if the file size is more than 1MB
            if profile_picture.size > 1048576:
                messages.warning(request, 'Profile picture size should not exceed 1 MB.')
            else:

                try:
                    img = Image.open(profile_picture)
                    if img.format not in ['JPEG', 'PNG']:
                        messages.warning(request, 'Profile picture must be a JPG or PNG file.')
                    else:
                        queryset.profile_picture = profile_picture
                        queryset.save()
                        messages.success(request, 'Profile Picture updated successfully.')
                except (IOError, ValueError):
                    messages.warning(request, 'Invalid image file type.')

    return redirect('/accounts/edit_profile/')


@login_required
def  update_profile_details(request):
    queryset_user = User.objects.filter(username=request.user).first()
    queryset_profile = Profile.objects.filter(user=request.user.id).first()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email =  request.POST.get('email')
        bio =  request.POST.get('bio')

        # Check if the new email is already taken by another user
        if email != queryset_user.email and User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already taken.')
            return redirect('/accounts/edit_profile/')
        

    queryset_user.first_name = first_name
    queryset_user.last_name = last_name
    queryset_user.email = email
    queryset_profile.bio = bio

    queryset_profile.save()
    queryset_user.save()
    messages.success(request, 'Profile details updated successfully.')

    return redirect('/accounts/edit_profile/')
    



@login_required
def edit_profile(request):
    profile = Profile.objects.filter(user=request.user.id).first()
    context = {
        'profile': profile
    }

    return render(request, 'accounts/edit_profile.html', context)