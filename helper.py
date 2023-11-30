from flask import request
import base64
from moralis import evm_api
from api_key import API_KEY


def upload_image():
    image = request.files['file']

    if image.filename == '':
        return 'empty'

    image_binary=image.read()
    base64_bytes=base64.b64encode(image_binary)
    base64_string = base64_bytes.decode('utf-8')

    return base64_string


def IPFS(filename, base64_file):
    api_key = API_KEY
    body = [{
            "path": filename,
            "content": base64_file,  # we have to provide base64 code for the file which we want to upload
        }]
    return evm_api.ipfs.upload_folder(api_key = api_key, body = body)

