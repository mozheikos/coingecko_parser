from sqlalchemy.dialects import postgresql
from sqlalchemy import JSON, BigInteger, Index, create_engine,\
     MetaData, Integer, String, Column, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://parser:parser@localhost:5432/analyticsgroupdb")
engine.connect()

metadata = MetaData()
Base = declarative_base()



class Coins(Base):
    __tablename__ = 'coins'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ticker = Column(String, nullable=False)
    coingecko_id = Column(String(100), nullable=False)
    coin_rank = Column(Integer)
    price = Column(Numeric)
    total_volume = Column(postgresql.NUMERIC)
    circulating_supply = Column(postgresql.NUMERIC)
    total_supply = Column(postgresql.NUMERIC)
    links = Column(JSON)

    __table_args__ = (
        Index('ticker_idx', 'ticker'),
    )


class Exchanges(Base):
    __tablename__ = 'exchanges'
    id = Column(Integer, primary_key=True)
    coingecko_id = Column(String(255), nullable=False)
    display_symbol = Column(String(255), nullable=False)
    exchange_name = Column(String(255), nullable=False)

class TradeItems(Base):
    __tablename__ = 'coins_exchanges'
    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coins.id'))
    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    coin_symbol = Column(String(255))
    volume = Column(BigInteger)
    volume_percentage = Column(postgresql.NUMERIC)
    trust_score = Column(String(15))

def create_tables(base_class, engine):
    base_class.metadata.create_all(engine, checkfirst=True)

