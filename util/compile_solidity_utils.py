# coding:utf-8
import pickle
from web3 import Web3, WebsocketProvider
from solc import compile_files, link_code
import config
from web3.middleware import geth_poa_middleware
# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# w3 = Web3(Web3.HTTPProvider(config.w3_url_neiwang))
# w3 = Web3(Web3.HTTPProvider(config.w3_url))
# w3 = Web3(WebsocketProvider('ws://127.0.0.1:8546'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)


def separate_main_n_link(file_path, contracts):
    # separate out main file and link files
    # assuming first file is main file.
    main = {}
    link = {}

    all_keys = list(contracts.keys())
    for key in all_keys:
        if file_path[0] in key:
            main = contracts[key]
        else:
            link[key] = contracts[key]
    return main, link


def deploy_contract(contract_interface, account):
    account = w3.toChecksumAddress(account)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # Instantiate and deploy contract
    contract = w3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    # Get transaction hash from deployed contract
    tx_hash = contract.constructor().transact()
    # Get tx receipt to get contract address
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress'], tx_hash.hex(), tx_receipt


def deploy_n_transact(file_path, mappings=[], account=w3.eth.accounts[0]):
    # compile all files
    contracts = compile_files(file_path, import_remappings=mappings)
    link_add = {}
    contract_interface, links = separate_main_n_link(file_path, contracts)
    # first deploy all link libraries
    for link in links:
        link_add[link] = deploy_contract(links[link], account)
    # now link dependent library code to main contract binary 
    # https://solidity.readthedocs.io/en/v0.4.24/using-the-compiler.html?highlight=library
    if link_add:
        contract_interface['bin'] = link_code(contract_interface['bin'], link_add)    
    # return contract receipt and abi(application binary interface)
    return deploy_contract(contract_interface, account), contract_interface['abi']



