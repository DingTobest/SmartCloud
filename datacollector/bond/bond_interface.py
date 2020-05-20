# encoding: utf-8

from .bond_agent import BondAgent

bond_agent = BondAgent()

def get_china_10year_bond_yield_data():
    df, msg = bond_agent.get_china_10year_bond_yield_historical_data()
    return df, msg
