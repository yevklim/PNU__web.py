from sqlalchemy import Column, Integer, String, DateTime, Enum, Float
from app import db
import enum

class OrderStatusEnum(enum.Enum):
    created = 1
    ready_to_send = 2
    sent = 3
    ready_to_receive = 4
    received = 5
    declined_to_receive = 6
    cancelled = 7


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    status = Column(Enum(OrderStatusEnum), default='created')
    sender_phone = Column(Integer, nullable=False)
    receiver_phone = Column(Integer, nullable=False)
    commodity_name = Column(String(100), nullable=False)
    commodity_total_price = Column(Float, nullable=False)
    sent_date = Column(DateTime(True), nullable=True)
    received_date = Column(DateTime(True), nullable=True)
