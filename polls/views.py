from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Poll, Choice, Vote
from .forms import SignUpForm, PollForm

from django.contrib.auth import authenticate, login,logout

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print("Signup request here:...")
        if form.is_valid():
            print(form)
            form.save()
            return redirect('login')
        else:
            # form validation failed return message to same page
            # also state the error message in the text
            messages.error(request, form.errors)
            return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("request here in login", email,password)

        user = authenticate(username=email, password=password)
        print("request here in login")
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('poll_list')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('poll_list')



def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
def poll_create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            
            # Create choices
            choice_texts = request.POST.getlist('choice_text')
            for text in choice_texts:
                if text.strip():
                    Choice.objects.create(poll=poll, text=text)
            
            return redirect('poll_list')
    else:
        form = PollForm()
    return render(request, 'polls/poll_form.html', {'form': form})

@login_required
def poll_edit(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.user != poll.created_by:
        messages.error(request, "You can't edit this poll.")
        return redirect('poll_list')
    
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('poll_list')
    else:
        form = PollForm(instance=poll)
    return render(request, 'polls/poll_form.html', {'form': form, 'poll': poll})

@login_required
def poll_delete(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.user != poll.created_by:
        messages.error(request, "You can't delete this poll.")
        return redirect('poll_list')
    poll.delete()
    return redirect('poll_list')


def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    # Calculate the total votes for all choices in the poll
    total_votes = sum(choice.votes for choice in poll.choices.all())

    user_can_vote = True
    if request.user.is_authenticated:
        user_can_vote = not Vote.objects.filter(poll=poll, user=request.user).exists()
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'user_can_vote': user_can_vote,
        'total_votes': total_votes
    })

@login_required
def poll_vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if Vote.objects.filter(poll=poll, user=request.user).exists():
        messages.error(request, "You've already voted on this poll.")
        return redirect('poll_results', pk=pk)
    
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, pk=choice_id)
            Vote.objects.create(poll=poll, choice=choice, user=request.user)
            choice.votes += 1
            choice.save()
            return redirect('poll_results', pk=pk)
    
    return redirect('poll_detail', pk=pk)

def poll_results(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    return render(request, 'polls/poll_results.html', {'poll': poll})