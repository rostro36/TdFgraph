import requests
import base64
'''
f = open("vuelta2018.png",
         "rb")  # open our image file as read only in binary mode
image_data = f.read()
b64_image = base64.standard_b64encode(image_data)
url = 'https://api.imgur.com/3/image'
payload = {'image': b64_image}
headers = {'Authorization': 'Client-ID bb79416fdaad09a'}

response = requests.request('POST',
                            url,
                            headers=headers,
                            data=payload,
                            allow_redirects=False)
print(response.text)
'''

import unittest


class MyTest(unittest.TestCase):
    def test_pass(self):
        assert 1 == 1

    def test_fail(self):
        assert 1 == 2


if __name__ == '__main__':
    unittest.main()
