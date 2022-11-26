import streamlit as st
from web3 import Web3

from ABI import *
import json

web3 = Web3(Web3.HTTPProvider('https://polygon-mainnet.infura.io/v3/496529dab76f4d8d981bcab8f10df625'))
address = '0x86935F11C86623deC8a25696E1C19a8659CbF95d'

contract = web3.eth.contract(address=address, abi=abi)



def render_image(svg):
    ratio = svg.props.em / svg.props.dpi_x
    svg.set_dpi(160 / ratio)

    dim = svg.get_dimensions()
    # create the cairo context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, dim.width, dim.height)
    context = cairo.Context(surface)
    svg.render_cairo(context)


contract2 = web3.eth.contract(address=address, abi=abi2)
contract3 = web3.eth.contract(address=address, abi=abi3)

user_address = st.text_input('Input Address', placeholder='0x...')
try:
    IDS = (contract3.caller.tokenIdsOfOwner(user_address))
    col1, col2 = st.columns(2)
    with col1:
        for gotchis in IDS[:5]:
            st.image(contract.caller.getAavegotchiSvg(gotchis))
    with col2:
        for gotchis in IDS[5:]:
            st.image(contract.caller.getAavegotchiSvg(gotchis))


except:
    st.warning('Insert valid address')

