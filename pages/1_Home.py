import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
from api_service import get_crypto_prices, AVAILABLE_COINS
from db_service import incarca_portofoliu, salveaza_portofoliu
is_firebase_logged = st.session_state.get("logged_in", False)
is_google_logged = getattr(st.user, "is_logged_in", False)

if not (is_firebase_logged or is_google_logged):
    st.switch_page("app.py")

if is_google_logged:
    db_email = st.user.email
    display_name = st.user.name or st.user.email
else:
    display_name = st.session_state.user_email
    db_email = st.session_state.user_email
if "asset_saved_message" not in st.session_state:
    st.session_state.asset_saved_message = None

if "portfolio" not in st.session_state:
    date_salvate = incarca_portofoliu(db_email)
    if date_salvate:
        st.session_state.portfolio=date_salvate
    else:
        st.session_state.portfolio={}
        for coin_name in AVAILABLE_COINS.keys():
            st.session_state.portfolio[coin_name] = {"qty": 0.0, "avg_price": 0.0}


@st.dialog("➕ ADD ASSET MANUALLY")
def add_asset_modal():
    asset_select = st.selectbox("Select Asset", list(AVAILABLE_COINS.keys()))
    qty_input = st.number_input("Quantity", min_value=0.0000, format="%f", step=0.01)
    price_input = st.number_input("Purchase Price per Unit ($)", value=0.0, format="%.2f", min_value=0.00, step=10.00)
    date_input = st.date_input("Date", max_value="today", min_value=datetime.date(2000, 1, 1))

    if st.button("Save Asset", type="primary", use_container_width=True):
        current_qty = st.session_state.portfolio[asset_select]["qty"]
        current_avg = st.session_state.portfolio[asset_select]["avg_price"]

        new_qty = current_qty + qty_input
        if new_qty > 0:
            new_avg = ((current_qty * current_avg) + (qty_input * price_input)) / new_qty
        else:
            new_avg = 0.0

        st.session_state.portfolio[asset_select]["qty"] = new_qty
        st.session_state.portfolio[asset_select]["avg_price"] = new_avg

        salveaza_portofoliu(db_email,st.session_state.portfolio)

        st.session_state.asset_saved_message = f"Added {qty_input} {asset_select}"
        st.rerun()


col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(f"#### Welcome, {display_name}")
with col2:
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.id_token = None
        if st.user.is_logged_in:
            st.logout()
        else:
            st.rerun()

coin_ids_string = ",".join(AVAILABLE_COINS.values())
live_prices = get_crypto_prices(coin_ids_string)

total_portfolio_value = 0.0
total_invested = 0.0
donut_data = []

if live_prices:
    for asset, stats in st.session_state.portfolio.items():
        qty = stats["qty"]
        avg_price = stats["avg_price"]
        coin_id = AVAILABLE_COINS[asset]
        current_price = live_prices.get(coin_id, {}).get('usd', 0.0)

        current_value = qty * current_price
        invested_value = qty * avg_price

        total_portfolio_value += current_value
        total_invested += invested_value

        if current_value > 0:
            donut_data.append({"Asset": asset, "Value": current_value, "Qty": qty})

if total_invested > 0:
    profit_loss_abs = total_portfolio_value - total_invested
    profit_loss_pct = (profit_loss_abs / total_invested) * 100
    sign = "+" if profit_loss_pct >= 0 else ""
    delta_text = f"{sign}{profit_loss_pct:.2f}% ({sign}${profit_loss_abs:,.2f})"
else:
    delta_text = None

top_col1, top_col2 = st.columns([1.5, 1])

with top_col1:
    st.markdown("#### TOTAL PORTFOLIO VALUE")
    st.metric(
        label="Total Portfolio Value",
        value=f"${total_portfolio_value:,.2f}",
        delta=delta_text,
        label_visibility="collapsed"
    )

with top_col2:
    st.markdown("#### ASSET DISTRIBUTION")
    if donut_data:
        df_donut = pd.DataFrame(donut_data)
        fig = px.pie(df_donut, values="Value", names="Asset", hole=0.6, hover_data=['Qty'])
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Valoare: $%{value:,.2f}<br>Cantitate: %{customdata[0]:.4f}<extra></extra>"
        )
        arata_legenda = True
    else:
        df_donut = pd.DataFrame([{"Asset": "Empty", "Value": 1}])
        fig = px.pie(df_donut, values='Value', names="Asset", hole=0.6, color_discrete_sequence=['#e5e5e5'])
        fig.update_traces(hovertemplate="Portofoliu Gol<extra></extra>", textinfo='none')
        arata_legenda = False

    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280, showlegend=arata_legenda)
    st.plotly_chart(fig, use_container_width=True, key="donut_chart")

st.divider()

mid_col1, mid_col2 = st.columns([4, 1])
with mid_col1:
    st.markdown("##### MY CRYPTO ASSETS")

with mid_col2:
    if st.button("➕ ADD ASSET MANUALLY", use_container_width=True):
        add_asset_modal()

if st.session_state.asset_saved_message:
    st.toast(st.session_state.asset_saved_message, icon="✅")
    st.session_state.asset_saved_message = None

if live_prices:
    assets_list = []
    qty_list = []
    avg_price_list = []
    current_price_list = []

    for asset in AVAILABLE_COINS.keys():
        stats = st.session_state.portfolio[asset]
        assets_list.append(asset)
        qty_list.append(stats["qty"])
        avg_price_list.append(stats["avg_price"])

        coin_id = AVAILABLE_COINS[asset]
        current_price_list.append(live_prices.get(coin_id, {}).get('usd', 0.0))

    date_tabel = {
        "Asset": assets_list,
        "Quantity": qty_list,
        "Avg Purchase Price": avg_price_list,
        "Current Price": current_price_list
    }

    df_assets = pd.DataFrame(date_tabel)
    df_assets["Total Value"] = df_assets["Quantity"] * df_assets["Current Price"]

    st.dataframe(
        df_assets,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Avg Purchase Price": st.column_config.NumberColumn("Avg Purchase Price", format="$%.2f"),
            "Current Price": st.column_config.NumberColumn("Current Price", format="$%.2f"),
            "Total Value": st.column_config.NumberColumn("Total Value", format="$%.2f")
        }
    )