from bs4 import BeautifulSoup as bs
import requests
import json
import re
from datetime import datetime
from app_globals import base_url, s


def get_test_list(serialized_index='', result_list=[]):
    token_url = base_url + "/Home/CSRFToken"
    page = s.get(token_url)
    soup = bs(page.content, 'html.parser')
    request_verfication_token = soup.findAll(
        attrs={'name': '__RequestVerificationToken'})[0]['value']
    test_results_url = base_url + '/Clinical/TestResults/GetPageSet?filterIPURL=0&searchString=&serializedIndex=' + \
        serialized_index + '&oldestRenderedDate=2022-03-11T03:45:04.297Z&ComponentNumber=4'
    page = s.post(
        test_results_url, headers={
            "__RequestVerificationToken": request_verfication_token})
    print('result status code:')
    print(page.status_code)
    result = json.loads(page.content)
    weird_key = next(iter(result['List']))
    for key in result['List'][weird_key]['List']:
        item = {
            'test_name': key['Name'],
            'provider_name': key['ProviderName'],
            'provider_title': ','.join(key['ProviderName'].split(',')[1:]),
            'result_date_time': key['ResultDateTime'],
            'details_link': key['DetailsLink']
        }
        result_list.append(item)
    if len(result['List'][weird_key]['List']) == 100:
        get_test_list(result['SerializedIndex'], result_list)
    return result_list

def get_test_result_details(test_result):
    page = s.get(base_url + test_result['details_link'])
    components = parse_test_details_page(page, test_result['test_name'])
    test_result['components'] = components


def parse_test_details_page(page, test_name):
    soup = bs(page.content, 'html.parser')
    try:
        find_result = soup.find(id='results').table.tbody.find_all('tr')
        result = []
        for r_index, row in enumerate(find_result):
            columns = row.find_all('td')
            for c_index, column in enumerate(columns):
                if c_index == 0:
                    component_name = column.text 
                elif c_index == 1:
                    numeric_value = parse_component_numeric_value(column)
                    if numeric_value is not None:
                        numeric_data= {}
                        numeric_data['name'] = component_name
                        numeric_data['numeric_value'] = numeric_value
                        numeric_data['unit'] = parse_component_unit_value(column)
                        result.append(numeric_data)
        return result
    except Exception as e:
        print(str(e))
        print("Incorrectly formatted: " + test_name)

def parse_component_numeric_value(column):
    if(column.span):
        column.span.decompose()
    value = column.text
    numeric_value = re.search('-?[0-9+\\.?[0-9]*', value).group()
    if len(numeric_value) > 0:
        return float(numeric_value)
    else:
        return None
 

def parse_component_unit_value(column):
    value = column.text
    if(len(value) > 0):
        if(is_number(value.split()[-1])):
            unit = 'unitless'
        else:
            unit = value.split()[-1]
        return unit
    else:
        return None
     

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
