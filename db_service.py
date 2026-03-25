import requests
import streamlit as st

DB_URL = st.secrets["firebase"].get("databaseURL")
print(f"[DB] DB_URL la startup: '{DB_URL}'")

def salveaza_portofoliu(email: str, portfolio_data: dict):
    if not DB_URL or not email:
        st.error("Eroare internă: Link-ul bazei de date sau email-ul lipsește!")
        return

    safe_email = email.replace(".", ",")
    url = f"{DB_URL}/users/{safe_email}/portfolio.json"

    response = requests.put(url, json=portfolio_data)

    if response.status_code != 200:
        st.error(f"Eroare Firebase la SALVARE: {response.text}")
        print(f"Eroare Salvare Firebase: {response.text}")
    else:
        print(f"[DB] Salvat cu succes pentru {safe_email}")


def incarca_portofoliu(email: str) -> dict:
    if not DB_URL or not email:
        print("[DB] EROARE: DB_URL sau email lipsa!")
        return None

    safe_email = email.replace(".", ",")
    url = f"{DB_URL}/users/{safe_email}/portfolio.json"

    print(f"[DB] Incarc portofoliu pentru: {safe_email}")
    print(f"[DB] URL: {url}")

    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        print(f"[DB] EROARE REQUEST: {e}")
        st.warning("Nu s-a putut conecta la baza de date. Reîncearcă.")
        return None

    print(f"[DB] Status: {response.status_code}")
    print(f"[DB] Raspuns: {response.text[:200]}")  # primele 200 caractere

    if response.status_code != 200:
        print(f"[DB] Eroare Citire Firebase: {response.text}")
        return None

    if response.text == "null" or response.text.strip() == "":
        print(f"[DB] Firebase a returnat null - portofoliu gol pentru {safe_email}")
        return None

    try:
        data = response.json()
        print(f"[DB] Date incarcate: {list(data.keys()) if data else 'gol'}")
        return data
    except Exception as e:
        print(f"[DB] EROARE parsare JSON: {e}")
        return None