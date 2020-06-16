# -*- coding: utf-8 -*-

# 导入:import db
# 取带有中文数据的字段时，需注意是否需要对unicode进行编码，可选参数encode('palmos')

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import DECIMAL
from sqlalchemy import desc
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:
Base = declarative_base()


# 定义 BankInfo 对象：
class BankInfo(Base):
    __tablename__ = 'bank_info'

    id = Column(BigInteger, primary_key=True)
    bank_crawl_result_id = Column(BigInteger)
    bank_name = Column(String)
    rmb_gold_customer_sell = Column(DECIMAL)
    rmb_gold_update_beijing_time = Column(DateTime)


# 定义 BuyBankOrder 对象：
class BuyBankOrder(Base):
    __tablename__ = 'buy_bank_order'

    id = Column(BigInteger, primary_key=True)
    bank_name = Column(String)
    product = Column(String)
    price = Column(DECIMAL)
    quantity = Column(BigInteger)
    time = Column(DateTime)


# 定义 SellBankOrder 对象：
class SellBankOrder(Base):
    __tablename__ = 'sell_bank_order'

    id = Column(BigInteger, primary_key=True)
    buy_bank_order_id = Column(BigInteger, ForeignKey('buy_bank_order.id'))
    bank_name = Column(String)
    product = Column(String)
    price = Column(DECIMAL)
    quantity = Column(BigInteger)
    time = Column(DateTime)
    buy_bank_order = relationship('BuyBankOrder', back_populates='sell_bank_order')


BuyBankOrder.sell_bank_order = relationship('SellBankOrder', uselist=False, back_populates='buy_bank_order')


# 定义 FundInfo 对象：
class FundInfo(Base):
    __tablename__ = 'fund_info'

    id = Column(BigInteger, primary_key=True)
    fund_name = Column(String)
    fund_code = Column(String)
    time = Column(Date)
    IOPV = Column(DECIMAL)
    LJJZ = Column(DECIMAL)


# 定义 BuyFundOrder 对象：
class BuyFundOrder(Base):
    __tablename__ = 'buy_fund_order'

    id = Column(BigInteger, primary_key=True)
    fund_name = Column(String)
    fund_code = Column(String)
    total_money = Column(DECIMAL)
    LJJZ = Column(DECIMAL)
    quantity = Column(DECIMAL)
    time = Column(Date)
    charge = Column(DECIMAL)
    redemption_rule = Column(String)


# 初始化数据库连接:
MYSQL_HOST = 'database-1.c7qylssqavie.ap-northeast-1.rds.amazonaws.com'
engine = create_engine('mysql+pymysql://davidblus:davidblus@' + MYSQL_HOST + ':3306/interest?charset=utf8', encoding='utf-8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 从此处开始调试，和gdb调试方法类似
# import pdb
# pdb.set_trace()
