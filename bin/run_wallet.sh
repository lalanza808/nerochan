#!/bin/sh

export RPC_CREDS="${2}"
export DAEMON_ADDRESS="${3}"
export WALLET_FILE=/data/wallet

# Define the network we plan to operate our wallet in
if [[ "${1}" == "stagenet" ]]; then
  export NETWORK=--stagenet
  export PORT=38081
elif [[ "${1}" == "testnet" ]]; then
  export NETWORK=--testnet
  export PORT=28081
else
  export NETWORK=
  export PORT=18089
fi

# Create new wallet if it doesn't exist
if [[ ! -d ${WALLET_FILE} ]]; then
  monero-wallet-cli ${NETWORK} \
    --generate-new-wallet ${WALLET_FILE} \
    --daemon-address ${DAEMON_ADDRESS} \
    --trusted-daemon \
    --use-english-language-names \
    --mnemonic-language English
fi

# Run RPC wallet
monero-wallet-rpc ${NETWORK} \
  --daemon-address ${DAEMON_ADDRESS} \
  --wallet-file ${WALLET_FILE} \
  --password "" \
  --rpc-login ${RPC_CREDS} \
  --rpc-bind-port 8000 \
  --rpc-bind-ip 0.0.0.0 \
  --confirm-external-bind \
  --log-file ${WALLET_FILE}-rpc.log \
  --trusted-daemon
