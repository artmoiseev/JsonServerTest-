import requests
import json
import os

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class MakingHttpRequestsTask():

    session = None
    root = 'https://jsonplaceholder.typicode.com/'
    items_count = None

    def __init__(self, items_count):
        self.session = self._requests_retry_session()
        self.items_count = items_count

    def make_and_save_request(self):
        for item in self.items_count:
            requestId = 1
            while True:
                url = str(item) + "/" + str(requestId)
                print(url)
                response = self.session.request('Get', self.root + url)
                if response.status_code == 404:
                    break
                else:
                    self._write_data_to_file(str(item), requestId, response)
                    requestId += 1
            self._validate_number_of_created_files_for_current_item(item)

    def _validate_number_of_created_files_for_current_item(self, item):
        number_of_files = len(os.listdir(os.getcwd() + "//" + str(item)))
        if number_of_files != self.items_count[item]:
            error_message = "Number of files in the folder '%s' must be equal to %s" % (str(item), str(self.items_count[item]))
            raise Exception(error_message)
        print("Number of files in the folder " + str(item) + " " + str(number_of_files))

    def _write_data_to_file(self, item, requestId, response):
        self._create_dir_if_not_exist(item)
        with open(item + "/" + str(requestId) + '.json', 'w') as outfile:
            json.dump(response.json(), outfile, ensure_ascii=False)
        print(response.json())

    def _create_dir_if_not_exist(self, folder_name):
        if not os.path.exists(os.getcwd() + "//" + folder_name):
            os.makedirs(folder_name)

    def _requests_retry_session(
            retries=5,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504)
    ):
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
