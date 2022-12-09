import streamlit as st
from web3 import Web3
import pandas as pd
import ast

from ABI import *
wear_df = pd.read_csv('TestingWEAR.csv')
df_merged = pd.read_csv('RealWear.csv')
df_merged['Wearables'] = df_merged['Wearables'].apply(lambda x : ast.literal_eval(x))
df_ghst = pd.read_csv('GHST.csv')
wear_id = pd.read_csv('WearID.csv')
import graphviz
st.title('Gotchi sells Tracker')
st.subheader('Only works for single addresses, USD prices are calculated daily mean USD price of GHST on the sell day')


web3 = Web3(Web3.HTTPProvider(st.secrets['api']))
address = '0x86935F11C86623deC8a25696E1C19a8659CbF95d'

contract = web3.eth.contract(address=address, abi=abi)





contract2 = web3.eth.contract(address=address, abi=abi2)
contract3 = web3.eth.contract(address=address, abi=abi3)
try:
    user_address = st.text_input('Input Address', placeholder='0x...').lower()
except:
    st.warning('Input a valid Polygon Address')
ls_IDS = list(df_merged[df_merged['Seller'] == user_address.lower()]['ID'].values)

Gotchid = st.selectbox('Select a Gotcher ID', (ls_IDS))

if Gotchid != None:
    try:
        cost_ghst = \
            df_merged[df_merged['Buyer'] == user_address][
                df_merged[df_merged['Buyer'] == user_address]['ID'] == Gotchid][
                'precio'].values[0]
        Cost_dollar = \
            df_merged[df_merged['Buyer'] == user_address][
                df_merged[df_merged['Buyer'] == user_address]['ID'] == Gotchid][
                'precio'].values[0] * (
                df_merged[df_merged['Buyer'] == user_address][
                    df_merged[df_merged['Buyer'] == user_address]['ID'] == Gotchid][
                    'Price'].values[0])
        date = \
            df_merged[df_merged['Buyer'] == user_address][
                df_merged[df_merged['Buyer'] == user_address]['ID'] == Gotchid][
                'Date'].values[0]

        st.markdown(f'Gotchi Buy Price {round(cost_ghst, 2)}GHST, {round(Cost_dollar, 2)}($) \n Purchase Day: {date}')
    except:
        st.warning('No buys found for this GotchiID!')
    try:
        sell_ghst = \
            df_merged[df_merged['Seller'] == user_address][
                df_merged[df_merged['Seller'] == user_address]['ID'] == Gotchid][
                'precio'].values[0]
        sell_dollar = \
            df_merged[df_merged['Seller'] == user_address][
                df_merged[df_merged['Seller'] == user_address]['ID'] == Gotchid][
                'precio'].values[0] * (
                df_merged[df_merged['Seller'] == user_address][
                    df_merged[df_merged['Seller'] == user_address]['ID'] == Gotchid][
                    'Price'].values[0])
        sell_date = \
            df_merged[df_merged['Seller'] == user_address][
                df_merged[df_merged['Seller'] == user_address]['ID'] == Gotchid][
                'Date'].values[0]

        st.markdown(f'Gotchi sell price {round(sell_ghst, 2)}GHST, {round(sell_dollar, 2)}($) \n Sell Day: {sell_date}')
    except:
        st.warning('No sells found for this GotchiID!')
try:
    gotchi_wears = \
        df_merged[df_merged['Buyer'] == user_address][df_merged[df_merged['Buyer'] == user_address]['ID'] == Gotchid][
            'Wearables']
    gotchi_wears = gotchi_wears.iloc[0]

    total = 0
    total2 = 0
    wear_d = {}
except:
    st.warning('No Wearable sales found for this gotchi')
for ids in gotchi_wears:

    try:
        sell_date = \
            wear_df[wear_df['Seller'] == user_address][wear_df[wear_df['Seller'] == user_address]['WearID'] == ids][
                'Date'].values[0]
        wear_sell = \
            wear_df[wear_df['Seller'] == user_address][wear_df[wear_df['Seller'] == user_address]['WearID'] == ids][
                'precio'].values[0]
        wear_sell_usd = \
            wear_df[wear_df['Seller'] == user_address][wear_df[wear_df['Seller'] == user_address]['WearID'] == ids][
                'precio'].values[0] * \
            wear_df[wear_df['Seller'] == user_address][wear_df[wear_df['Seller'] == user_address]['WearID'] == ids][
                'Price'].values[0]
        wear_d[ids] = [wear_sell, round(wear_sell_usd, 2), sell_date]
        total += wear_sell
        total2 += wear_sell_usd
    except:
        ''

st.title('Found Wearable sales')
try:
    if len(wear_d) > 4:
        col1, col2 = st.columns(2)



        with col1:

            for k, v in dict(list(wear_d.items())[0:int((len(wear_d) / 2))]).items():
                graph = graphviz.Digraph()
                graph.attr(rankdir="LR", size="8,5")
                graph.edge(wear_id[wear_id['ID'] == k]['Name'].values[0], str(v[0]) + '$GHST')
                graph.edge(wear_id[wear_id['ID'] == k]['Name'].values[0], str(v[1]) + '$USD')
                graph.edge(wear_id[wear_id['ID'] == k]['Name'].values[0], str(v[2]))
                st.graphviz_chart(graph)
        with col2:
            for k2, v2 in dict(list(wear_d.items())[int((len(wear_d)/2)):]).items():
                graph2 = graphviz.Digraph()
                graph2.attr(rankdir="LR", size="10,7")
                graph2.edge(wear_id[wear_id['ID'] == k2]['Name'].values[0], str(v2[0]) + '$GHST')
                graph2.edge(wear_id[wear_id['ID'] == k2]['Name'].values[0], str(v2[1]) + '$USD')
                graph2.edge(wear_id[wear_id['ID'] == k2]['Name'].values[0], str(v2[2]))
                st.graphviz_chart(graph2)





    else:
        for k, v in wear_d.items():
            graph = graphviz.Digraph()
            graph.edge(wear_id[wear_id['ID'] == k]['Name'].values[0], str(v[0]) + '$GHST')
            graph.edge(wear_id[wear_id['ID'] == k]['Name'].values[0], str(v[1]) + '$USD')
            graph.edge(wear_id[wear_id['ID'] == k]['Name'].values[0], str(v[2]))
            st.graphviz_chart(graph)
    st.write('Total Profit/Loss on Gotchi : ', round(((sell_ghst + total) - cost_ghst), 2), '$GHST',
             round(((sell_dollar + total2) - Cost_dollar), 2), 'USD')

except:
    st.warning('Try another gotchi ID')
