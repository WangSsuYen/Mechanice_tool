from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config import DATABASE_URI

# 定義基類
Base = declarative_base()

# 廠商名稱
class Manufacturer(Base):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    manufacturer_name = Column(String(64), nullable=False, info="製造商名稱")

    # 一對多關係
    spindle_motors = relationship('SpindleMotor', back_populates='manufacturer')
    servo_motors = relationship('ServoMotor', back_populates='manufacturer')

# 主軸馬達
class SpindleMotor(Base):
    __tablename__ = 'spindle_motor'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True, info={'chinese_name': '名稱', 'unit': ''})
    rate_output = Column(Integer, nullable=False, info={'chinese_name': '額定功率', 'unit': 'Kw'})
    torgue = Column(Integer, nullable=False, info={'chinese_name': '額定扭矩', 'unit': 'N.m'})
    speed = Column(Integer, nullable=False, info={'chinese_name': '最高轉速', 'unit': 'RPM'})
    max_torgue = Column(Integer, nullable=False, info={'chinese_name': '最大扭矩', 'unit': 'N.m'})
    max_speed = Column(Integer, nullable=False, info={'chinese_name': '最高轉速', 'unit': 'RPM'})
    weight = Column(Integer, info={'chinese_name': '重量', 'unit': 'Kg'})
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False, info={'chinese_name': '製造廠商', 'unit': ''})

    # 反向關係
    manufacturer = relationship('Manufacturer', back_populates='spindle_motors')

# 伺服馬達
class ServoMotor(Base):
    __tablename__ = 'servo_motor'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True, info={'chinese_name': '名稱', 'unit': ''})
    rate_output = Column(Integer, nullable=False, info={'chinese_name': '額定功率', 'unit': 'Kw'})
    torgue = Column(Integer, nullable=False, info={'chinese_name': '額定扭矩', 'unit': 'Nm'})
    speed = Column(Integer, nullable=False, info={'chinese_name': '額定轉速', 'unit': 'RPM'})
    max_torgue = Column(Integer, nullable=False, info={'chinese_name': '最大扭矩', 'unit': 'Nm'})
    max_speed = Column(Integer, nullable=False, info={'chinese_name': '最高轉速', 'unit': 'RPM'})
    weight = Column(Integer, info={'chinese_name': '重量', 'unit': 'Kg'})
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False, info={'chinese_name': '製造廠商', 'unit': ''})

    # 反向關係
    manufacturer = relationship('Manufacturer', back_populates='servo_motors')


# 設置數據庫連接
engine = create_engine(DATABASE_URI)
# 創建所有表
Base.metadata.create_all(engine)

# 創建Session
Session = sessionmaker(bind=engine)
session = Session()
