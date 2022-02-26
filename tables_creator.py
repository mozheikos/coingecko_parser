from sqlalchemy.orm import relationship, session
from sqlalchemy import BigInteger, Index, UniqueConstraint, create_engine,\
     MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://parser:parser@localhost:5432/analyticsgroupdb")
engine.connect()

metadata = MetaData()
Base = declarative_base()



class Coins(Base):
    __tablename__ = 'coins'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ticker = Column(String(10), nullable=False)
    coingecko_id = Column(String(100), nullable=False)
    coin_rank = Column(Integer)
    price = Column(Numeric)
    circulating_supply = Column(BigInteger)
    total_supply = Column(BigInteger)
    # homepage = Column(String(255))
    # blockchain_site = Column(String(1000))
    # official_forum_url = Column(String(1000))
    # chat_url = Column(String(1000))
    # announcement_url = Column(String(1000))
    # twitter_screen_name = Column(String(30))
    # facebook_username = Column(String(30))
    # bitcointalk_thread_identifier = Column(String(30))
    # telegram_channel_identifier = Column(String(30))
    # subreddit_url = Column(String(255))
    # links = Column(JSON(1000))

    __table_args__ = (
        UniqueConstraint('name'),
        UniqueConstraint('ticker'),
        Index('ticker_idx', 'ticker'),
    )


class Exchanges(Base):
    __tablename__ = 'exchanges'
    id = Column(Integer, primary_key=True)
    coingecko_id = Column(String(30))
    display_symbol = Column(String(30))
    exchange_name = Column(String(255))
    trust_score = Column(Boolean)

class TradeItems(Base):
    __tablename__ = 'coins_exchanges'
    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coins.id'))
    target_coin_id = Column(Integer, ForeignKey('coins.id'))
    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    coin_symbol = Column(String(40), default=('coin_id.ticker' + '/' + 'target_coin_id.ticker'))

def create_tables(base_class, engine):
    base_class.metadata.create_all(engine, checkfirst=True)
