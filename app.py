from chalice import Chalice, BadRequestError
import pycountry

app = Chalice(app_name='country-data')
app.debug = True


@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/country-list', methods=['GET'], cors=True)
def get_country_list():
    """
    This function returns all countries.
    
    Args: N/A
    
    Returns: List of country in JSON format.
    """
    data = []

    for country in pycountry.countries:
        record = {}
        record["code"] = country.alpha_2
        
        name = country.name
        record["name"] = name
        
        data.append(record)

    return data

@app.route('/currency/{country}', methods=['GET'], cors=True)
def get_currency(country):
    """
    This function returns currency based on country.
    
    Args: country
    
    Returns: Currency name in JSON format
    """
    
    if country is None or len(country) == 0:
        raise BadRequestError("Country is required in this REST APi")
        
    result = pycountry.countries.search_fuzzy(country)
    
    data = []
    
    if result is None or len(result) == 0:
        raise BadRequestError("Country {} is not availalbe".format(country))
    else:
        for country in result:
            currency = {}
            value = pycountry.currencies.get(numeric=country.numeric)
            if value:
                currency['currency'] = value.name
                data.append(currency)
    
    return data