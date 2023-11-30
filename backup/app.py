from flask import Flask, render_template, request
from moralis import evm_api
import base64
from api_key import API_KEY


app= Flask(__name__)

uploaded_files = {}
ipfs_hash = {}


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


@app.route('/', methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        encoded_file = upload_image()

        if encoded_file!="empty":
            uploaded_files[request.form.get("filename")] = encoded_file

        if request.form.get("convert_btn")=="submit":
            for key, value in uploaded_files.items():
                result_url = IPFS(key, str(value))
                ipfs_hash[key] = result_url

            print(ipfs_hash)
            uploaded_files.clear()

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True, port = 8000)