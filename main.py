import json
from pycoingecko import CoinGeckoAPI
from math import ceil
from time import sleep
from sqlalchemy.orm import Session
from tables_creator import Coins, Exchanges, TradeItems, engine, create_tables, Base

cg = CoinGeckoAPI()

Base.metadata.drop_all(engine)
create_tables(Base, engine)

session = Session(bind=engine)

def fill_table(iter_item, function):
    ids = []
    for item in iter_item:
        row, item_id = function(item)
        if item_id:
            ids.append(item_id)
        if row:
            session.add(row)
    session.commit()
    return ids

def get_coin_first_run(cg_coin):
    rank = cg_coin['market_cap_rank']
    links = json.dumps(cg.get_coin_by_id(cg_coin['id'])['links'])
    if not rank:
        return None
    coin = Coins(
        name = cg_coin['name'],
        ticker = cg_coin['symbol'],
        coingecko_id = cg_coin['id'],
        coin_rank = rank,
        price = cg_coin['current_price'],
        total_volume = cg_coin['total_volume'],
        circulating_supply = cg_coin['circulating_supply'],
        total_supply = cg_coin['total_supply'],
        links = links,
    )
    return coin, coin.coingecko_id

def get_exchange(exch):
    trust = exch['trust_score']
    if not trust:
        return None
    exchange = Exchanges(
        coingecko_id = exch['id'],
        display_symbol = exch['id'],
        exchange_name = exch['name'],
    )
    return exchange, exchange.coingecko_id

def get_trade_items(item):
    coin = session.query(Coins).filter(Coins.coingecko_id == item['coin_id']).one_or_none()
    exchange = session.query(Exchanges).filter(Exchanges.coingecko_id == item['market']['identifier']).one_or_none()
    volume_percentage = round(item['converted_volume']['usd'] / float(coin.total_volume) * 100, 2)
    if not coin:
        return None, None
    trust = item['trust_score']
    if not trust:
        return None, None
    tradeitem = TradeItems(
        coin_id = coin.id,
        exchange_id = exchange.id,
        coin_symbol = f"{item['base']}/{item['target']}",
        volume = item['converted_volume']['usd'],
        volume_percentage = volume_percentage,
        trust_score = trust,
    )
    return tradeitem, None

coins = cg.get_coins_markets('usd', per_page=40)
coins_ids = fill_table(coins, get_coin_first_run)

exchanges = cg.get_exchanges_list()[:40]
exchanges_ids = fill_table(exchanges, get_exchange)

tickers_ids = []
for item in exchanges_ids:
    tickers_list = cg.get_exchanges_tickers_by_id(item, coin_ids=coins_ids)['tickers']
    tickers_ids += fill_table(tickers_list, get_trade_items)
