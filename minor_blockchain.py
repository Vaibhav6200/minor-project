from flask import Flask, jsonify, request, render_template, session
from blockchain import Blockchain
from helper import *
from urllib.parse import urlparse


uploaded_files = {}


blockchain = Blockchain()

app = Flask(__name__, template_folder='C:\\Users\\Vaibhav\\Desktop\\minor\\templates')
app.config['SECRET_KEY'] = 'vaibhav_paliwal_secret_key'


def mineBlock():
    if session['ipfs_hash']:
        previous_block = blockchain.getPrevBlock()
        prev_block_proof = previous_block['proof']
        new_mined_proof = blockchain.proof_of_work(prev_block_proof)
        prev_hash = blockchain.hash(previous_block)

        ipfs_hashes = session['ipfs_hash']
        block = blockchain.createBlock(proof=new_mined_proof, previous_hash=prev_hash, ipfs_hash_data=ipfs_hashes)
        response = {
            "message": "Congratulations! You just mined a block",
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'curr_mined_block_hash': blockchain.hash(block),
            'ipfs_hashes': ipfs_hashes,
        }
        session.pop('ipfs_hash')
        return jsonify(response), 200       # json response and status code
    else:
        print("ERROR: NO Hashes Available to put into Block !!!")


@app.route('/get_chain', methods=['GET'])
def getChain():
    response = {
        'chain': blockchain.chain,
        'chain_length': len(blockchain.chain),
        'root_url': "https://ipfs.moralis.io:2053/ipfs/"
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
        session['ipfs_hash'] = {}
        encoded_file = upload_image()

        if encoded_file != "empty":
            uploaded_files[request.form.get("filename")] = encoded_file

        if request.form.get("convert_and_mine_btn")=="submit":
            for key, value in uploaded_files.items():
                result = IPFS(key, str(value))
                result_url = result[0]['path']
                file_hash = urlparse(result_url).path.split('/')[2]
                session['ipfs_hash'][key] = file_hash

            uploaded_files.clear()

            mineBlock()

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True, port = 8000)