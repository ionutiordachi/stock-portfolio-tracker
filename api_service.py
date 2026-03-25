import requests
import streamlit as st


AVAILABLE_COINS = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Solana (SOL)": "solana",
    "Cardano (ADA)": "cardano",
    "Ripple (XRP)": "ripple",
    "Dogecoin (DOGE)": "dogecoin",
    "Polkadot (DOT)": "polkadot",
    "Polygon (MATIC)": "matic-network",
    "Chainlink (LINK)": "chainlink",
    "Avalanche (AVAX)": "avalanche-2"
}
@st.cache_data(ttl=60)
def get_crypto_prices(coins_to_fetch):
    url="https://api.coingecko.com/api/v3/simple/price"
    coin_ids = ",".join(AVAILABLE_COINS.values())
    params = {
        "ids": coins_to_fetch,
        "vs_currencies": "usd",
        "include_24hr_change":"true"
    }
    try:
        response=requests.get(url,params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Eroare API CoinGecho{e}")
        return None