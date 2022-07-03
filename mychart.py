#! /usr/bin/python3
import json
import setup
import test_data

setup.login()
setup.switch_profile()
test_results = test_data.get_test_list()
for test_result in test_results:
    test_data.get_test_result_details(test_result)
print(len(test_results))
f = open('output.json', 'w')
f.write(json.dumps(test_results, indent=4, sort_keys=True))
f.close()
