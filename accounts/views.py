from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import UserLoginForm, UserRegisterForm


# Create your views here.
def login_user(request):
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')

		user = authenticate(username=username, password=password)
		login(request, user)

		if next:
			return redirect(next)
		
		return redirect(reverse('items:index'))

	context = {
		'form': form,
	}

	return render(request, 'accounts/login.html', context)

def logout_user(request):
	logout(request)
	return redirect(reverse('accounts:login'))