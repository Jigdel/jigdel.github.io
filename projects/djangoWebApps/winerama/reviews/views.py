from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Review, Wine

# Create your views here.
# Once we are inside the view function, 
# we normally do some model query, and create a context object with the results.
# Queries are normally performed by using 
# the .objects attribute in the given domain entity class (e.g. Review.objects)
# sorting, filter methods etc. More about query sets: https://docs.djangoproject.com/en/1.8/ref/models/querysets/

# gets a list of the latest 9 reviews and renders it using `reviews/list.html'.
def review_list(request):
	latest_review_list = Review.objects.order_by('-pub_date')[:9]
	context = {'latest_review_list': latest_review_list}
	return render(request, 'reviews/review_list.html', context)

# gets a review given its ID and renders it using review_detail.html.
def review_detail(request, review_id):
	review = get_object_or_404(Review, pk=review_id)
	return render(request, 'reviews/review_detail.html', {'review': review})

# gets all the wines sorted by name and passes it to wine_list.html to be rendered.
def wine_list(request):
	wine_list = Wine.objects.order_by('-name')
	context = {'wine_list': wine_list}
	return render(request, 'reviews/wine_list.html', context)

# gets a wine from the DB given its ID and renders it using wine_detail.html.
def wine_detail(request, wine_id):
	wine = get_object_or_404(Wine, pk=wine_id)
	form = ReviewForm()
	return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

# in charge of validating the form & creating the new review instance
# first thing it does is use the request url winde ID to look for the wine we are going 
# to add the review to.
def add_review(request, wine_id):
	wine = get_object_or_404(Wine, pk=wine_id)
	form = ReviewForm(request.POST)
	if form.is_valid():
		rating = form.cleaned_data['rating']
		comment = form.cleaned_data['comment']
		user_name = form.cleaned_data['user_name']
		review = Review()
		review.wine = wine
		review.user_name = user_name
		review.rating = rating
		review.comment = comment
		review.pub_date = datetime.datetime.now()
		review.save()
		# Always return an HttpResponseRedirect after successfully dealing 
		# with POST data. This prevents data from being posted twice if a 
		# user hits the Back button.
		return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))

	return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})



