# coding:utf-8
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, JSON, DATETIME, ForeignKey, PickleType
from util.dbmanager import db_manager
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    # __bind_key__ = 'users_write'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Apps(Base):
    __tablename__ = 'apps'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    appid = Column(String(200), primary_key=True, nullable=False, unique=True)
    desc = Column(String(200), nullable=False)
    ip = Column(JSON, nullable=False)
    ns = Column(JSON, nullable=False)
    cli_publickey = Column(Text, nullable=False)
    cli_privatekey = Column(Text, nullable=False)
    srv_publickey = Column(Text, nullable=False)
    srv_privatekey = Column(Text, nullable=False)
    srv = Column(JSON, nullable=False)
    master_contract_address = Column(JSON, nullable=False, default=[])
    status = Column(Integer, nullable=False)


class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(Integer, autoincrement=True, primary_key=True)
    address = Column(String(100), primary_key=True)
    balance = Column(String(20))
    create_time = Column(String(20))
    type = Column(String(10))
    

class TransactionRecord(Base):
    __tablename__ = "transaction_record"
    id = Column(Integer, autoincrement=True, primary_key=True)
    from_address = Column(String(50))
    to_address = Column(String(50))
    value = Column(String(20))
    transaction_time = Column(String(20))
    tx_hash = Column(String(100))
    type = Column(String(10))
    

class DeployContracts(Base):
    __tablename__ = "deploy_contracts"
    id = Column(Integer, autoincrement=True, primary_key=True)
    contract_name = Column(String(200), primary_key=True)
    address = Column(String(200))
    tx_hash = Column(String(100))
    deploy_time = Column(String(20))
    pay_gas = Column(String(20))
    contract_address = Column(String(100))
    master_mark = Column(String(20))
    # service_id = Column(Integer, ForeignKey('deploy_contracts.id'), nullable=True)
    

class Contracts(Base):
    __tablename__ = "contracts"
    contract_id = Column(Integer, autoincrement=True, primary_key=True)
    contract_address = Column(String(100), primary_key=True)
    contract_version = Column(String(20))
    contract_text = Column(Text)
    

class Tokens(Base):
    __tablename__ = "tokens"
    token_id = Column(Integer, autoincrement=True, primary_key=True)
    token_full_name = Column(String(20), primary_key=True)
    token_nick_name = Column(String(10), primary_key=True)


# class Services(Base):
#     __tablename__ = "services"
#     service_id = Column(Integer, autoincrement=True, primary_key=True)
#     service_name = Column(String(20), primary_key=True)
#     service_description = Column(String(1000))
#     contracts = relationship('DeployContracts')
    

class ContractOp(Base):
    __tablename__ = "contract_op_table"
    op_id = Column(Integer, autoincrement=True, primary_key=True)
    contract_name = Column(String(200), primary_key=True)
    contract_address = Column(String(100), primary_key=True)
    op_info = Column(PickleType)
    op_time = Column(String(20))
    tx_hash = Column(String(100))
    
    
def create_tables():
    engine = db_manager.get_engine_master()
    Base.metadata.create_all(engine)


