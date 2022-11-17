# Pulpo Technical Challenge

## Getting your API Key

Before executing this project you must have your own API key. They're available in the IATI site [here](https://developer.iatistandard.org/subscriptions)

Once you have it, then create a file named ".env" inside your just-cloned repo; there, paste the key in the following format:

```
API_KEY = '<your-api-key-goes-here>'
```

## Run backend

```
pip install -r requirements.txt

python -m uvicorn main:app --reload

Open a browser and go to 'localhost:8000'. If you see a _Hello World_ text, everything is fine and running!

Go to 'localhost:8000/docs' to see the endpoints and try them out.
```
## Understanding the API

This API has only one endpoint. Its function is to get the donators from a given country in the last 5 years starting from a fixed date e.g.

"I want all the organizations that made a donation to Sudan from 2017 to 2022"

For more information about the IATI API, find the documentation [here](https://developer.iatistandard.org/apis)

## Calling the API
**Pre-steps: Have the backend running on a local server (see [Run Backend](https://github.com/MrCasco/pulpo-technical-challenge-backend/edit/main/README.md#run-backend) section) and getting your own API Key for IATI site [here](https://developer.iatistandard.org/subscriptions)**

1. Go to **localhost:8000/docs** to see the Fast API menu.
2. Open the 'donatives_by_country_code' tab and click 'Try it out'
3. Enter a valid year in the start_date field
4. Enter a valid country code in the country_code field (check out the available country codes [here](https://countrycode.org/)
5. Click 'Execute' and see the results!
