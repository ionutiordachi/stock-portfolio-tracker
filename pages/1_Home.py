import datetime

import pandas as pd
import streamlit as st
import plotly.express as px
import os


is_firebase_logged = st.session_state.get("logged_in",False)
is_google_logged= getattr(st.user,"is_logged_in",False)


if not ( is_firebase_logged or is_google_logged):
    st.switch_page("../app.py")

if "asset_saved_message" not in st.session_state:
    st.session_state.asset_saved_message = None

if is_google_logged:
    display_name = st.user.name or st.user.email
else:
    display_name = st.session_state.user_email

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(f"#### Welcome, {display_name}")
with col2:
    if st.button("Log out", width="stretch"):

        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.id_token = None

        if st.user.is_logged_in:
            st.logout()
        else:
            st.rerun()



top_col1,top_col2 = st.columns([1.5,1])

with top_col1:
    st.markdown("#### TOTAL PORTFOLIO VALUE")
    st.metric(label="Total Portfolio Value",value="$12.540,50",delta="+2.4% ($285.50)",label_visibility="collapsed")
with top_col2:
    st.markdown("#### ASSET DISTRIBUTION")
    df_donut= pd.DataFrame({
        'Asset':['BTC','ETH','SOL'],
        'Value':[60000,5000,2540]
    })
    fig= px.pie(df_donut, values='Value', names="Asset",hole=0.6)
    fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height= 150,showlegend=True)
    st.plotly_chart(fig,width="stretch")

st.divider()

@st.dialog("➕ ADD ASSET MANUALLY")
def add_asset_modal():
    asset_select = st.selectbox("Select Asset", ["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)"])
    qty_input = st.number_input("Quantity", min_value=0.0000, format="%f", step=0.01)
    number_input = st.number_input("Purchase Price per Unit ($)", value=0.0, format="%.2f", min_value=0.00, step=10.00)
    date_input = st.date_input("Date", max_value="today", min_value=datetime.date(2000, 1, 1))
    if st.button("Save Asset", type="primary", width="stretch"):
        """TODO:To implement Add asset to Portfolio"""
        st.session_state.asset_saved_message = f"Added {qty_input} {asset_select}!"
        st.rerun()

mid_col1,mid_col2 = st.columns([4,1])
with mid_col1:
    st.markdown("##### MY CRYPTO ASSETS")

with mid_col2:
    if st.button("➕ ADD ASSET MANUALLY", width="stretch"):
        add_asset_modal()
if st.session_state.asset_saved_message:
    st.toast(st.session_state.asset_saved_message, duration="short")
    st.session_state.asset_saved_message= None

date_tabel = {
    "Asset": ["Bitcoin BTC", "Ethereum ETH", "Solana SOL", "Cardano ADA"],
    "Quantity": ["0.00001614", "0.00002867", "0.00104130", "0.00002483"],
    "Avg Purchase Price": ["€30.50", "€123.20", "€130.00", "€45.00"],
    "Current Price": ["€1,114.80", "€370.50", "€9.23", "€9.39"]
}

df_assets = pd.DataFrame(date_tabel)
st.dataframe(df_assets,width="stretch", hide_index=True )
