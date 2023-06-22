import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
	print(kwargs)
	print("GET from {} ".format(url))
	response = None
	api_key = kwargs.get("api_key", None)
	try:
		response = {}
		if api_key:
			params = dict()
			params["text"] = kwargs["text"]
			params["version"] = kwargs["version"]
			params["features"] = kwargs["features"]
			params["language"] = "en"
			params["return_analyzed_text"] = kwargs["return_analyzed_text"]
			response = requests.get(url, headers={'Content-Type': 'application/json'},
																	params=params, auth=HTTPBasicAuth('apikey', api_key))
		else:
			# Call get method of requests library with URL and parameters
			response = requests.get(url, headers={'Content-Type': 'application/json'},
																	params=kwargs)

		
									
		status_code = response.status_code
		print("With status {} ".format(status_code))
		json_data = json.loads(response.text)
		return json_data

	except requests.exceptions.RequestException as e:
		# If any error occurs
		print("Network exception occurred")
		print(e)
		return None


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
	try:
		response = requests.post(url, params=kwargs, json=json_payload)
	except requests.exceptions.RequestException as e:
		# If any error occurs
		print("Network exception occurred")
		print(e)
		return None
	return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
	results = []
	# Call get_request with a URL parameter
	json_result = get_request(url)
	if json_result:
		# Get the row list in JSON as dealers
		dealers = json_result
		# For each dealer object
		for dealer in dealers:
			# Create a CarDealer object with values in `doc` object
			dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
									 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
									 short_name=dealer["short_name"],
									 st=dealer["st"], zip=dealer["zip"])
			results.append(dealer_obj)
	return results

def get_dealer_by_id_from_cf(dealer_id):
	json_result = get_request('https://us-south.functions.appdomain.cloud/api/v1/web/704fa087-0d6f-4afe-b2d6-2c553f6625d1/dealership-package/get_dealer_by_id', dealerId=dealer_id)
	if json_result:
		return json_result

def get_dealer_reviews_from_cf(url, dealer_id):
	results = []
	json_result = get_request(url, dealerId=dealer_id)
	if json_result:
		reviews = json_result
		for review in reviews:
			# review_doc = review['doc']
			print(review)
			review_obj = DealerReview(
				dealership=review.get('dealership', None),
				name=review.get('name', None),
				purchase=review.get('purchase', None),
				review=review.get('review', None),
				purchase_date=review.get('purchase_date', None),
				car_make=review.get('car_make', None),
				car_model=review.get('car_model', None),
				car_year=review.get('car_year', None),
				id=review.get('id', None),
			)
			review_obj.sentiment = analyze_review_sentiments(review_obj.review)['sentiment']['document']['label']
			results.append(review_obj)
	print(results)
	return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
	url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/efa226dd-feb5-41a1-97e6-50e668f9be7a/v1/analyze?version"
	api_key = os.environ.get("NLU_IBM_API_KEY", None)
	features = {
		"sentiment": {}
	}
	version="2022-04-07"
	response = get_request(url, api_key=api_key, text=dealer_review, version=version, features=features, return_analyzed_text="")
	print(response)
	return response





