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

# def get_trade_items(item):
#     base_id = session.query(Coins).filter(Coins.coingecko_id == item['coin_id']).one().id
#     target_id = session.query(Coins).filter(Coins.coingecko_id == item['target_coin_id']).one().id
#     exchange_id = session.query(Exchanges).filter(Exchanges.coingecko_id == )

#     oin_id = base_id,
#     target_coin_id = target_id,
#     exchange_id = Column(Integer, ForeignKey('exchanges.id'))
#     coin_symbol = Column(String(40), default=('coin_id.ticker' + '/' + 'target_coin_id.ticker'))


coins = cg.get_coins_markets('usd')
fill_table(coins, get_coin_first_run)

exchanges = cg.get_exchanges_list()
fill_table(exchanges, get_exchanges)