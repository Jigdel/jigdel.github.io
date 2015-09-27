from django.forms import ModelForm, Textarea
from reviews.models import reviews

class ReviewForm(ModelForm):
	class Meta:
		model = Review
		fields = ['user_name', 'rating', 'comment']
		widgets = {
			'comment': Textarea(attrs={'cols': 40, 'rows': 15})
		}