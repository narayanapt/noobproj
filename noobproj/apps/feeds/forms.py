from django import forms
from .models import Feed

class CreateFeedForm(forms.ModelForm):
	
	class Meta:
		model = Feed
		fields = ['post']
			