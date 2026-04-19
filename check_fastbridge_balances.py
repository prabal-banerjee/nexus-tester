import json
import os

from web3 import Web3


ADDRESS = os.environ.get("FASTBRIDGE_TEST_ADDRESS", "").strip()

NETWORKS = {
    "ethereum": "https://1rpc.io/eth",
    "arbitrum": "https://1rpc.io/arb",
    "base": "https://1rpc.io/base",
    "optimism": "https://1rpc.io/op",
    "polygon": "https://1rpc.io/matic",
    "avalanche": "https://1rpc.io/avax/c",
    "bnb": "https://1rpc.io/bnb",
    "scroll": "https://1rpc.io/scroll",
}


def main():
    if not ADDRESS:
        raise SystemExit("Set FASTBRIDGE_TEST_ADDRESS to the wallet address you want to inspect.")
    results = []
    for name, rpc_url in NETWORKS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 15}))
            chain_id = w3.eth.chain_id
            balance_wei = w3.eth.get_balance(ADDRESS)
            results.append(
                {
                    "network": name,
                    "rpc": rpc_url,
                    "chainId": chain_id,
                    "balanceWei": str(balance_wei),
                    "balanceEth": str(w3.from_wei(balance_wei, "ether")),
                }
            )
        except Exception as error:
            results.append(
                {
                    "network": name,
                    "rpc": rpc_url,
                    "error": str(error),
                }
            )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
