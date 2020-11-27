from django import forms
from vitudo.forms import BaseForm
from django.contrib.auth import authenticate, get_user_model 

User = get_user_model()

class UserLoginForm(BaseForm):
	username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}), required=True, label='')
	password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}), required=True, label='')

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError('Užívateľ neexistuje')
			if not user.check_password(password):
				raise forms.ValidationError('Zlé heslo')
			if not user.is_active:
				raise forms.ValidationError('Užívateľ je neaktívny')

		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email')
	email2 = forms.EmailField(label='Confirm email')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]

	def clean_email(self):
		email = self.cleaned_data.get(email)
		email2 = self.cleaned_data.get(email2)
		password = self.cleaned_data.get(password)

		if email != email:
			raise forms.ValidationError('Emails do not match')

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError('Email is already taken')

		return email

