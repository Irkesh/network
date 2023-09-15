from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse  
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
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

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
        return render(request, 'social/login.html')


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
    app_user = AppUser.objects.get(id=request.user.id)
    # Query the Image model for images with user_id matching the current user's pk
    user_images = Image.objects.filter(user_id=user.pk)
    status_updates = Status.objects.filter(user_id = user.pk).order_by('-created_at')[:3]
    return render(request, 'social/index.html', {'user_images': user_images, 'status_updates': status_updates, 'app_user': app_user})



class AppUserDetail(DetailView):
    model = AppUser
    context_object_name = 'appuser'
    template_name = 'social/basic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appuser'] = AppUser.objects.all()
        return context


def appUserList(request):
    current_user_id = request.user.id

    #Use Q objects to create a complex OR condition
    friendships = Friendship.objects.filter(
        Q(sender_id=current_user_id, status__iexact="accepted") |
        Q(receiver_id=current_user_id, status__iexact="accepted")
    )

     # Extract the IDs of users who are not the current user
    other_user_ids = []
    for friendship in friendships:
        if friendship.sender_id != current_user_id:
            other_user_ids.append(friendship.sender_id)
        if friendship.receiver_id != current_user_id:
            other_user_ids.append(friendship.receiver_id)
    
    # Remove duplicates from the list of IDs
    other_user_ids = list(set(other_user_ids))

    # Retrieve the relevant AppUser objects
    appUsers = AppUser.objects.exclude(id__in=other_user_ids)[:12]

    #appUsers = AppUser.objects.exclude(id=current_user_id).filter()    
    return render(request, 'social/search_friends.html', {'appusers': appUsers, 'type': 'appUserList'})



def appFriendsList(request):

    current_user_id = request.user.id
    #Use Q objects to create a complex OR condition
    friendships = Friendship.objects.filter(
        Q(sender_id=current_user_id, status__iexact="accepted") |
        Q(receiver_id=current_user_id, status__iexact="accepted")
    )
    
    #established friendshipts
    accepted_other_user_ids = []
    for friendship in friendships:
        if friendship.sender_id != current_user_id:
            accepted_other_user_ids.append(friendship.sender_id)
        if friendship.receiver_id != current_user_id:
            accepted_other_user_ids.append(friendship.receiver_id)
    # Remove duplicates from the list of IDs
    accepted_other_user_ids = list(set(accepted_other_user_ids))


    #recieved friendship invitations
    pending_friendship_invitations = Friendship.objects.filter(
        Q(receiver_id=current_user_id, status__iexact="pending")
    )

    #pending friendship invitations to the current user
    pending_recieved_from_other_user_ids = []
    for pending_friendship_invitation in pending_friendship_invitations:        
        pending_recieved_from_other_user_ids.append(pending_friendship_invitation.sender_id)
        
    # Remove duplicates from the pending friendshoips list of IDs
    pending_recieved_from_other_user_ids = list(set(pending_recieved_from_other_user_ids))


    #reqested friendship invitations
    pending_friendship_requests = Friendship.objects.filter(
        Q(sender_id=current_user_id, status__iexact="pending")
    )

    pending_requested_to_other_user_ids = []
    for pending_friendship_request in pending_friendship_requests:           
        pending_requested_to_other_user_ids.append(pending_friendship_request.receiver_id)
    # Remove duplicates from the pending friendshoips list of IDs
    pending_requested_to_other_user_ids = list(set(pending_requested_to_other_user_ids))


    # Retrieve the relevant AppUser objects
    fiends_appUsers = AppUser.objects.filter(id__in=accepted_other_user_ids)
    current_user_id = request.user.id
    pending_friend_requests = AppUser.objects.filter(id__in=pending_requested_to_other_user_ids)
    pending_friend_invitations = AppUser.objects.filter(id__in=pending_recieved_from_other_user_ids)
    return render(request, 'social/list_friends.html', {'friends': fiends_appUsers, 'pending_friend_requests': pending_friend_requests, 'pending_friend_invitations': pending_friend_invitations})



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
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            new_status = form.save(commit=False)
            new_status.user = AppUser.objects.get(user=request.user)            
            new_status.save()
            return HttpResponseRedirect('../')
    else:
        form = StatusUpdateForm()

    return render(request, 'social/update_status.html')



def send_friend_request(request, receiver_id):

    # Retrieve the receiver user based on receiver_id
    receiver = get_object_or_404(AppUser, id=receiver_id)
    sender = AppUser.objects.get(user=request.user.id)
    # Check if a friendship request already exists
    existing_request = Friendship.objects.filter(sender=request.user.id, receiver=receiver_id, status='pending').exists()

    if not existing_request:
        # Create a new Friendship object representing the friend request
        friendship = Friendship(receiver=receiver, sender=sender, status='pending')
        #receiver=friend_id, sender=current_user_id, status__iexact="pending"
        friendship.save()

    # Redirect to the 'list_friends' page
    return HttpResponseRedirect(reverse('search_friends'))


def accept_friend_request(request, sender_id):
    # Retrieve Friendship object 
    current_user_id = request.user.id
    try:
        friendship = Friendship.objects.filter(
            Q(receiver=current_user_id, sender=sender_id, status__iexact="pending")
        )
        friendship.update(status='accepted')
    except Friendship.DoesNotExist:
        # Handle the case where the Friendship object does not exist
        # You can redirect to an error page or display a message
        return redirect('error_page')
    # Redirect to the 'list_friends' page
    return HttpResponseRedirect(reverse('list_friends'))

def decline_friend_request(request, friend_id):
    current_user_id = request.user.id
    try:
        friendship = Friendship.objects.filter(
            Q(receiver=current_user_id, sender=friend_id, status__iexact="pending")
        )
        friendship.delete()
    except Friendship.DoesNotExist:
        return redirect('error_page')
    # Redirect to the 'list_friends' page
    return HttpResponseRedirect(reverse('list_friends'))

def cancel_friend_request(request, friend_id):
    current_user_id = request.user.id
    try:
        friendship = Friendship.objects.filter(
            Q(receiver=friend_id, sender=current_user_id, status__iexact="pending")
        )
        friendship.delete()
    except Friendship.DoesNotExist:
        return redirect('error_page')
    # Redirect to the 'list_friends' page
    return HttpResponseRedirect(reverse('list_friends'))