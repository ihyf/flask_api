import aiohttp
from util.compile_solidity_utils import w3


async def get_data(url):
    async with aiohttp.request('GET', url) as r:
        data = await r.json()
    return data


async def wait_transactio_confirm(tx_hash):
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt)
    return receipt
