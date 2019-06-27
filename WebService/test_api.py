import time

import requests

SERVER_URL = 'http://127.0.0.1:5000'
DATA_ROUTE = '/process-data'

JSON_TYPE = 'json'
FILE_TYPE = 'json_file'


s = requests.Session()


def _post_data(route, data):
    url = SERVER_URL + route
    d = dict(data=data)
    response = s.post(url, json=d)
    print('Uploading data to server at {}, response: {}'.format(url, response))
    return response.content


def _get_data(route):
    url = SERVER_URL + route
    response = s.get(url)
    print('Getting data from server at {}, response: {}'.format(url, response))
    return response.content


def _post_file(route, _type, file_path):
    url = SERVER_URL + route
    file = {_type: open(file_path, 'rb')}
    response = s.post(url, files=file)
    print('Uploading file to server at {}, response: {}'.format(url, response))
    return response.content


def post_data(data):
    return _post_data(DATA_ROUTE, data)


def post_file(file_path):
    return _post_file(DATA_ROUTE, FILE_TYPE, file_path)


def get_data():
    return _get_data(DATA_ROUTE)


if __name__ == '__main__':
    for _ in range(5):
        print('=========> test {} \n'.format(_))
        _post_json_data = 'this is uploading data {}'.format(_)
        print('post data = "{}"'.format(_post_json_data))
        post_data(_post_json_data)
        time.sleep(1)

        print()
        _fetched_data = get_data()
        print('server response ==> ', _fetched_data, '\n')
        time.sleep(1)
