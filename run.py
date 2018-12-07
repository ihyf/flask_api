# encoding: utf-8
import json
import os
from flask import render_template
from solc import link_code
from werkzeug.utils import secure_filename

from create_app import create_app
from werkzeug.contrib.fixers import ProxyFix
from util.compile_solidity_utils import deploy_n_transact
from util.upload import Upload
from flask import request
from util.ext import db

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
with app.app_context():
    db.init_app(app)
with app.app_context():
    db.create_all()
html = """
    <!DOCTYPE html>
    <title>Contract Upload</title>
    <h1>Contract Upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=upload>
    </form>
    """


@app.route('/')
def hello():
    return "hello"


@app.route('/upload_contract', methods=['GET', 'POST'])
def upload_contract():
    if request.method == 'POST':
        file = request.files.get("file", None)
        if file:
            up = Upload()
            if up.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(up.upload_dir, filename))
                return "upload_contract ok"
            else:
                return "no sol"
        else:
            return "no files"
    return html


@app.route('/compile_contracts')
def compile_contracts_test():
    # Solidity source code
    contract_address, abi = deploy_n_transact(['contracts/user.sol', 'contracts/stringUtils.sol'])
    
    with open('data.json', 'w') as outfile:
        data = {
            "abi": abi,
            "contract_address": contract_address
        }
        json.dump(data, outfile, indent=4, sort_keys=True)
    
    return "ok"


@app.route('/compile/<filename>')
def compile_contract(filename):
    # 根据文件名 编译合约
    contract_address, abi = deploy_n_transact(['contracts/{}'.format(filename)])
    with open('json_files/data_{}.json'.format(filename.split(".")[0]), 'w') as outfile:
        data = {
            "abi": abi,
            "contract_address": contract_address
        }
        json.dump(data, outfile, indent=4, sort_keys=True)

    return "compile {} ok".format(filename)


if __name__ == '__main__':
    app.run(host='localhost', port=3000)
    # app.run(host='0.0.0.0', port=4000)
