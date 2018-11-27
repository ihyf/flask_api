# encoding: utf-8
from flask import render_template
from solc import link_code
from create_app import create_app
from werkzeug.contrib.fixers import ProxyFix
from util.compile_solidity_utils import deploy_n_transact
import os
import sys

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
@app.route('/')
def hello():
    return "hello"


@app.route('/compile_contracts')
def compile_contracts():
    import json
    # Solidity source code
    contract_address, abi = deploy_n_transact(['contracts/user.sol', 'contracts/stringUtils.sol'])
    
    with open('data.json', 'w') as outfile:
        data = {
            "abi": abi,
            "contract_address": contract_address
        }
        json.dump(data, outfile, indent=4, sort_keys=True)
    
    return "ok"


if __name__ == '__main__':
    app.run(host='localhost', port=3000)
