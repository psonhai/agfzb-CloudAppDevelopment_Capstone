from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import datetime

# REST APIs
from .restapis import get_dealer_reviews_from_cf, get_dealers_from_cf, post_request, get_dealer_by_id_from_cf
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
	if request.method == "GET":
		return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
	if request.method == "GET":
		return render(request, 'djangoapp/contact_us.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
	if request.method == "POST":
		print(request.user.is_authenticated)
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
		return redirect('/djangoapp')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
	if request.method == "POST":
		logout(request)
		return redirect('/djangoapp')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
	if request.method == "GET":
		return render(request, 'djangoapp/registration.html')

	elif request.method == "POST":
		username = request.POST.get('username')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		print(username)
		user = User.objects.create_user(username=username,
																		first_name=first_name,
																		last_name=last_name,
																		password=password)

		login(request, user)
		return render(request, 'djangoapp/index.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
	if request.method == "GET":
		url = "https://us-south.functions.appdomain.cloud/api/v1/web/704fa087-0d6f-4afe-b2d6-2c553f6625d1/dealership-package/get-all-dealership"
		# Get dealers from the URL
		dealerships = get_dealers_from_cf(url)
		# Concat all dealer's short name
		# dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
		# Return a list of dealer short name
		return render(request, 'djangoapp/index.html', {'dealership_list': dealerships})


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
	if request.method == "GET":
		url = "https://us-south.functions.appdomain.cloud/api/v1/web/704fa087-0d6f-4afe-b2d6-2c553f6625d1/review-package/get-reviews-by-dealership"
		reviews = get_dealer_reviews_from_cf(url, dealer_id)

		print(reviews[0].dealership)

	dealer = get_dealer_by_id_from_cf(dealer_id)[0]
	return render(request, 'djangoapp/dealer_details.html', {'reviews': reviews, 'dealer_name': dealer['full_name']})

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
	if request.user.is_authenticated:
		if request.method == "GET":
			dealer = get_dealer_by_id_from_cf(dealer_id)[0]
			dealer_cars_owned = CarModel.objects.all().filter(dealer_id=dealer_id)
			# dealer_cars_owned = list(map(lambda obj: f"{obj.name}-{obj.car_make.name}-{obj.year.year}", dealer_cars_owned))
			return render(request, 'djangoapp/add_review.html', {'dealer_id': dealer_id,'dealer_name': dealer['full_name'], 'cars': dealer_cars_owned})
		# try except
		if request.method == "POST":
			review = {}
			json_payload = {}
			car_id = request.POST.get('car')
			car = CarModel.objects.get(id=car_id)
			review['dealership'] = dealer_id
			review['review'] = request.POST.get('review', None)
			review['name'] = request.POST.get('name', "")
			review['purchase'] = True if request.POST.get('purchase', False) == 'on' else False
			review['purchase_date'] = request.POST.get('purchase_date', None)
			review['car_make'] = car.car_make.name
			review['car_model'] = car.name
			review['car_year'] = car.year.strftime('%Y')
			json_payload = review

			print(review)
			
			response = post_request('https://us-south.functions.appdomain.cloud/api/v1/web/704fa087-0d6f-4afe-b2d6-2c553f6625d1/review-package/post-review', json_payload, dealerId=dealer_id)
			# print(response)
			return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

		


