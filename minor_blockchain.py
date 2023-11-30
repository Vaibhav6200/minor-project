from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain
from helper import *
import requests


uploaded_files = {}
ipfs_hash = {}

blockchain = Blockchain()

app = Flask(__name__, template_folder='C:\\Users\\Vaibhav\\Desktop\\minor\\templates')

@app.route('/mine_block', methods=['GET'])
def mineBlock():
    previous_block = blockchain.getPrevBlock()
    prev_block_proof = previous_block['proof']
    new_mined_proof = blockchain.proof_of_work(prev_block_proof)
    prev_hash = blockchain.hash(previous_block)
    block = blockchain.createBlock(proof=new_mined_proof, previous_hash=prev_hash, ipfs_hash=ipfs_hash)
    response = {
        "message": "Congratulations! You just mined a block",
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'curr_mined_block_hash': blockchain.hash(block),
        'ipfs_hash': ipfs_hash,
    }
    return jsonify(response), 200       # json response and status code


@app.route('/get_chain', methods=['GET'])
def getChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def checkBlockchainValidity():
    valid = blockchain.isChainValid(blockchain.chain)
    if valid:
        response = {"message": "All Good, Blockchain is Valid"}
    else:
        response = {"message": "We have a Problem!!!, Blockchain is inValid"}
    return jsonify(response), 200


@app.route('/', methods=['POST','GET'])
def convert_and_mine():
    if request.method=='POST':
        encoded_file = upload_image()

        if encoded_file!="empty":
            uploaded_files[request.form.get("filename")] = encoded_file

        if request.form.get("convert_and_mine_btn")=="submit":
            for key, value in uploaded_files.items():
                result_url = IPFS(key, str(value))
                ipfs_hash[key] = result_url[0]['path']
            uploaded_files.clear()

            response = requests.get(f'http://127.0.0.1:8000/mine_block')
            ipfs_hash.clear()       # clearing hash dictionary after uploading all files
            print(response.json())

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True, port = 8000)