from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
	# <HINT> Create a Car Make model `class CarMake(models.Model)`:
	# - Name
	# - Description
	# - Any other fields you would like to include in car make model
	# - __str__ method to print a car make object
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=30)

	def __str__(self):
		return f"Car Make: {self.name} - {self.description}"

class CarModel(models.Model):
	# <HINT> Create a Car Model model `class CarModel(models.Model):`:
	# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
	# - Name
	# - Dealer id, used to refer a dealer created in cloudant database
	# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
	# - Year (DateField)
	# - Any other fields you would like to include in car model
	# - __str__ method to print a car make object
	car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	dealer_id = models.IntegerField()
	car_type = models.CharField(max_length=30)
	year = models.DateField()
	
	def __str__(self):
		return f"""Car Make:
			Name: {self.name}
			Dealer ID: {self.dealer_id}
			Model: {self.car_make.name}
			Type: {self.car_type}
			Year: {self.year}
		"""

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
	def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
		# Dealer address
		self.address = address
		# Dealer city
		self.city = city
		# Dealer Full Name
		self.full_name = full_name
		# Dealer id
		self.id = id
		# Location lat
		self.lat = lat
		# Location long
		self.long = long
		# Dealer short name
		self.short_name = short_name
		# Dealer state
		self.st = st
		# Dealer zip
		self.zip = zip
		
	def __str__(self):
		return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
	def __init__(self, **kwargs):
		self.dealership = kwargs.get('dealership', None)
		self.name = kwargs.get('name', None)
		self.review = kwargs.get('review', None)
		self.purchase_date = kwargs.get('purchase_date', None)
		self.car_make = kwargs.get('car_make', None)
		self.car_model = kwargs.get('car_model', None)
		self.car_year = kwargs.get('car_year', None)
		self.id = kwargs.get('id', None)
		# self.sentiment = self.get_sentiment(kwargs.get('review', ''))

	def get_sentiment(self):
		return self.sentiment['sentiment']['document']['label']

	def __str__(self):
		return f"""Dealer Review:
			ID: {self.id}
			Dealership: {self.dealership}
			Name: {self.name}
			Review: {self.review}
			Purchase date: {self.purchase_date}
			Car Make: {self.car_make}
			Car Model: {self.car_model}
			Car Year: {self.car_year}
		"""
