import json
import os

from web3 import Web3


ADDRESS = os.environ.get("FASTBRIDGE_TEST_ADDRESS", "").strip()

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

NETWORKS = {
    "ethereum": {
        "rpc": "https://1rpc.io/eth",
        "tokens": {
            "USDC": "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        },
    },
    "arbitrum": {
        "rpc": "https://1rpc.io/arb",
        "tokens": {
            "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "USDT": "0xFd086bC7CD5C481DCC9C85ebe478A1C0b69FCbb9",
            "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
            "WETH": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
            "WBTC": "0x2f2a2543b76a4166549f7aaab2e75bef0aefc5b0",
        },
    },
    "base": {
        "rpc": "https://1rpc.io/base",
        "tokens": {
            "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
            "WETH": "0x4200000000000000000000000000000000000006",
            "cbBTC": "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf",
        },
    },
    "optimism": {
        "rpc": "https://1rpc.io/op",
        "tokens": {
            "USDC": "0x0b2C639c533813f4Aa9D7837CaF62653d097Ff85",
            "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
            "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
            "WETH": "0x4200000000000000000000000000000000000006",
            "WBTC": "0x68f180fcce6836688e9084f035309e29bf0a2095",
        },
    },
    "polygon": {
        "rpc": "https://1rpc.io/matic",
        "tokens": {
            "USDC": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
            "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
            "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
            "WBTC": "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6",
        },
    },
    "avalanche": {
        "rpc": "https://1rpc.io/avax/c",
        "tokens": {
            "USDC": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
            "USDT": "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7",
            "DAI": "0xd586E7F844cEa2F87f50152665BCbc2C279D8d70",
            "WETH.e": "0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB",
            "WBTC.e": "0x50b7545627a5162F82A992c33b87aDc75187B218",
        },
    },
    "bnb": {
        "rpc": "https://1rpc.io/bnb",
        "tokens": {
            "USDC": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
            "USDT": "0x55d398326f99059fF775485246999027B3197955",
            "DAI": "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
            "ETH": "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
            "BTCB": "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
        },
    },
}


def token_result(w3: Web3, owner: str, symbol_hint: str, token_address: str):
    contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    raw_balance = contract.functions.balanceOf(owner).call()
    decimals = contract.functions.decimals().call()
    try:
        symbol = contract.functions.symbol().call()
    except Exception:
        symbol = symbol_hint
    human_balance = raw_balance / (10 ** decimals)
    return {
        "symbol": symbol,
        "tokenAddress": token_address,
        "rawBalance": str(raw_balance),
        "decimals": decimals,
        "balance": str(human_balance),
        "hasBalance": raw_balance > 0,
    }


def main():
    if not ADDRESS:
        raise SystemExit("Set FASTBRIDGE_TEST_ADDRESS to the wallet address you want to inspect.")
    results = []
    for network_name, config in NETWORKS.items():
        rpc_url = config["rpc"]
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 20}))
            chain_id = w3.eth.chain_id
            token_results = []
            for symbol_hint, token_address in config["tokens"].items():
                try:
                    token_results.append(token_result(w3, ADDRESS, symbol_hint, token_address))
                except Exception as error:
                    token_results.append(
                        {
                            "symbol": symbol_hint,
                            "tokenAddress": token_address,
                            "error": str(error),
                        }
                    )
            results.append(
                {
                    "network": network_name,
                    "chainId": chain_id,
                    "rpc": rpc_url,
                    "tokens": token_results,
                }
            )
        except Exception as error:
            results.append(
                {
                    "network": network_name,
                    "rpc": rpc_url,
                    "error": str(error),
                }
            )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
