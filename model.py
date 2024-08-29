from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# 定義基類
Base = declarative_base()

# 廠商名稱
class Manufacturer(Base):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    manufacturer_name = Column(String(64), nullable=False)

    # 一對多關係
    spindle_motors = relationship('SpindleMotor', back_populates='manufacturer')
    servo_motors = relationship('ServoMotor', back_populates='manufacturer')

# 主軸馬達
class SpindleMotor(Base):
    __tablename__ = 'spindle_motor'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    rate_output = Column(Integer, nullable=False)
    torgue = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    max_torgue = Column(Integer, nullable=False)
    max_speed = Column(Integer, nullable=False)
    weight = Column(Integer)
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)

    # 反向關係
    manufacturer = relationship('Manufacturer', back_populates='spindle_motors')

# 伺服馬達
class ServoMotor(Base):
    __tablename__ = 'servo_motor'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    rate_output = Column(Integer, nullable=False)
    torgue = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    max_torgue = Column(Integer, nullable=False)
    max_speed = Column(Integer, nullable=False)
    weight = Column(Integer)
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)

    # 反向關係
    manufacturer = relationship('Manufacturer', back_populates='servo_motors')

# 設置數據庫連接
DATABASE_URI = 'sqlite:///mechanics_tools.db'
engine = create_engine(DATABASE_URI)

# 創建所有表
Base.metadata.create_all(engine)

# 創建Session
Session = sessionmaker(bind=engine)
session = Session()
