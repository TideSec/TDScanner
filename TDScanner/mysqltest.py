from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):

    __tablename__ = 'target_baseinfo'


    id = Column(String(50), primary_key=True)
    url = Column(String(50))


engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/TDScan')

DBSession = sessionmaker(bind=engine)
session = DBSession()
user = session.query(User).filter(User.id=='e31258c2c3dd45d4256a577fc7d5b55a').one()
print 'type:', type(user)
print 'name:', user.url
session.close()