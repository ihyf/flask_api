# encoding: utf-8
import json
import os
from flask import render_template
from solc import link_code
from werkzeug.utils import secure_filename
from util.compile_solidity_utils import w3
from create_app import create_app
from util.dbmanager import db_manager
from util.db_redis import redis_store
from util.mysql_db import create_tables
from werkzeug.contrib.fixers import ProxyFix
from util.compile_solidity_utils import deploy_n_transact
from util.upload import Upload
from flask import request
from util.mysql_db import db_manager, DeployContracts
import time

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
with app.app_context():
    db_manager.init_app(app)
    redis_store.init_app(app)
    # create_tables()   # 手动创建数据库表
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
                return "no .sol files"
        else:
            return "no files"
    return html


@app.route('/compile/<filename>')
def compile_contract(filename):
    # 根据文件名 编译合约
    account = w3.eth.accounts[1]
    pay_gas = 1
    contract_address, abi = deploy_n_transact(['contracts/{}'.format(filename)], account=account)
    tx_hash = contract_address[1]
    with open('json_files/data_{}.json'.format(filename.split(".")[0]), 'w') as outfile:
        data = {
            "abi": abi,
            "contract_address": contract_address[0]
        }
        json.dump(data, outfile, indent=4, sort_keys=True)

    session = db_manager.master()
    deploy_time = time.strftime("%Y-%m-%d %X", time.localtime())
    new_dc = DeployContracts(contract_name=filename, address=account, tx_hash=tx_hash,
                             deploy_time=deploy_time, pay_gas=pay_gas, contract_address=contract_address[0])
    session.add(new_dc)
    session.commit()
    session.close()

    return "compile {} ok".format(filename)


if __name__ == '__main__':
    #app.run(host='localhost', port=3000)
    app.run(host='0.0.0.0', port=9000)
