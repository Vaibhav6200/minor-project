import datetime
import hashlib
import json


class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, previous_hash='0', ipfs_hash_data={})      # creating genesis block

    def createBlock(self, proof, previous_hash, ipfs_hash_data):
        block = {
            'index': str(len(self.chain) + 1),
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'ipfs_hashes': ipfs_hash_data
        }
        self.chain.append(block)
        return block

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof=False
        while check_proof == False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def getPrevBlock(self):
        return self.chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # Two things we have to check:
    # (i) current_block[prev_hash] === previous_block_hash
    # (ii) proof of work is valid for each block
    def isChainValid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(prev_block):
                return False
            previous_proof = prev_block['proof']
            curr_block_proof = block['proof']
            hash_operation = hashlib.sha256(str(curr_block_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True
