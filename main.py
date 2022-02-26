from pycoingecko import CoinGeckoAPI
import json
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from tables_creator import Coins, Exchanges, TradeItems, engine, create_tables, Base

cg = CoinGeckoAPI()

Base.metadata.drop_all(engine)
create_tables(Base, engine)

session = Session(bind=engine)


def get_coin_first_run(cg_coin, coin_id):
    # links = cg.get_coin_by_id(coin_id)['links']
    coin = Coins(
        name = cg_coin['name'],
        ticker = cg_coin['symbol'],
        coingecko_id = cg_coin['id'],
        coin_rank = cg_coin['market_cap_rank'],
        price = cg_coin['current_price'],
        circulating_supply = cg_coin['circulating_supply'],
        total_supply = cg_coin['total_supply'],
        # links = json.dumps(links)
        # homepage = links['homepage'],
        # blockchain_site = links['blockchain_site'],
        # official_forum_url = links['official_forum_url'],
        # chat_url = links['chat_url'],
        # announcement_url = links['announcement_url'],
        # twitter_screen_name = links['twitter_screen_name'],
        # facebook_username = links['facebook_username'],
        # bitcointalk_thread_identifier = links['bitcointalk_thread_identifier'],
        # telegram_channel_identifier = links['telegram_channel_identifier'],
        # subreddit_url = links['subreddit_url'],
        # repos_url = json.dumps(links['repos_url'])
    )
    return coin

coins = cg.get_coins_markets('usd')
for item in coins:
    coin_id = item['id']
    coin = get_coin_first_run(item, coin_id)
    session.add(coin)
session.commit()