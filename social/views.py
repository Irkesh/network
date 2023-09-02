from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import logout


def room(request, room_name):
    return render(request, 'social/room.html', {'room_name': room_name })


def list_friends(request):
    
    return HttpResponseRedirect('../')

def search_friends(request):
    
    return HttpResponseRedirect('../')


#if used loggin in - he will have a possiblity to log out
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../')

#handling form that receives username and password
def user_login(request):
    master_genes = Gene.objects.all()

    #if getting HTTP POST - handle form, if not - return login form
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        #check that username and passwosrd are matching
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'social/login.html', {'master_genes': master_genes})


def register(request):
    
    #flag that indicates whether or not the user is registered
    registered = False
    #user has sent us done registr data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'organisation' in user_form.cleaned_data:
                profile.organisation = request.DATA['organisation']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    
    #if it is not POST - blank form for registration
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'social/register.html',
                  { 'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered })
    

def SPA(request):
    return render(request, 'social/spa.html')


def index(request):
    # Get the currently logged-in user
    user = request.user
    # Query the Image model for images with user_id matching the current user's pk
    user_images = Image.objects.filter(user_id=user.pk)
    return render(request, 'social/index.html', {'user_images': user_images})



class AppUserDetail(DetailView):
    model = AppUser
    context_object_name = 'appuser'
    template_name = 'social/basic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appuser'] = AppUser.objects.all()
        return context


def appUserList(request):
    appUsers = AppUser.objects.all()    
    return render(request, 'social/search_friends.html', {'appusers': appUsers, 'type': 'appUserList'})



def appFriendsList(request):
    appUsers = AppUser.objects.all()    
    return render(request, 'social/list_friends.html', {'appusers': appUsers, 'type': 'appUserList'})



def poslist(request):
    genes = Gene.objects.filter(entity__exact='Chromosome').filter(sense__startswith='+')
    master_genes = Gene.objects.all()
    return render(request, 'social/list.html', {'genes': genes, 'type': 'PosList'})


def user_images(request):
    # Get the currently logged-in user
    user = request.user

    # Query the Image model for images with user_id matching the current user's pk
    user_images = Image.objects.filter(user=user)

    # Pass the user_images queryset to the template for rendering
    return render(request, '../', {'user_images': user_images})

def user_upload_media(request):

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.custom_name = form.save(commit=False)
            new_image.user = AppUser.objects.get(user=request.user)            
            new_image.save()
            return HttpResponseRedirect('../')
    else:
        form = ImageUploadForm()

    return render(request, 'social/upload_image.html')

def create_status_update(request):
    if request.method == 'POST':
        form = StatusUpdate(request.POST, request.FILES)
        if form.is_valid():
            new_status = form.save(commit=False)
            new_status.user = AppUser.objects.get(user=request.user)            
            new_status.save()
            return HttpResponseRedirect('../')
    else:
        form = ImageUploadForm()

    return render(request, 'social/upload_image.html')