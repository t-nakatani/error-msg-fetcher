import warnings

import streamlit
from eth_defi.revert_reason import fetch_transaction_revert_reason
from web3 import Web3

# SyntaxWarningを無視する
warnings.filterwarnings("ignore", category=SyntaxWarning)

# RPC URLのオプション
RPC_URLS = {
    "zkCRO": "https://mainnet.zkevm.cronos.org",
    "IOTA": "https://json-rpc.evm.iotaledger.net",
}


class ErrorMsgFetcher:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url

    def fetch(self, tx_hash: str) -> str:
        w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        return fetch_transaction_revert_reason(w3, tx_hash)


class StreamlitApp:
    def __init__(self, error_msg_fetcher: ErrorMsgFetcher):
        self.error_msg_fetcher = error_msg_fetcher
        self.title = "Tx Error Message Fetcher"

    def _print_error_msg(self, msg: str):
        streamlit.write(rf"\>\> **{msg}**")

    def run(self, **kwargs):
        streamlit.title(self.title)

        # RPC URLの選択
        selected_rpc_name = streamlit.selectbox("Select RPC URL", options=list(RPC_URLS.keys()))
        selected_rpc_url = RPC_URLS[selected_rpc_name]

        # ErrorMsgFetcherを選択されたRPC URLで更新
        self.error_msg_fetcher = ErrorMsgFetcher(rpc_url=selected_rpc_url)

        tx_hash = streamlit.text_input("Tx Hash", "")

        if not tx_hash:
            self._print_error_msg("Please input tx hash.")
            return

        result = self.error_msg_fetcher.fetch(tx_hash)
        self._print_error_msg(result)


if __name__ == "__main__":
    error_msg_fetcher = ErrorMsgFetcher(rpc_url=RPC_URLS["zkCRO"])
    app = StreamlitApp(error_msg_fetcher)
    app.run()
