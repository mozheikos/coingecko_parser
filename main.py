from pycoingecko import CoinGeckoAPI
import json
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from tables_creator import Coins, Exchanges, TradeItems, engine, create_tables, Base

cg = CoinGeckoAPI()

Base.metadata.drop_all(engine)
create_tables(Base, engine)

session = Session(bind=engine)

def fill_table(iter_item, function):
    for item in iter_item:
        row = function(item)
        session.add(row)
    session.commit()

def get_coin_first_run(cg_coin):
    coin = Coins(
        name = cg_coin['name'],
        ticker = cg_coin['symbol'],
        coingecko_id = cg_coin['id'],
        coin_rank = cg_coin['market_cap_rank'],
        price = cg_coin['current_price'],
        circulating_supply = cg_coin['circulating_supply'],
        total_supply = cg_coin['total_supply'],
    )
    return coin

def get_exchanges(exch):
    exchange = Exchanges(
        coingecko_id = exch['id'],
        display_symbol = exch['id'],
        exchange_name = exch['name'],
        trust_score = exch['trust_score'],
    )
    return exchange

coins = cg.get_coins_markets('usd')
fill_table(coins, get_coin_first_run)

exchanges = cg.get_exchanges_list()
fill_table(exchanges, get_exchanges)