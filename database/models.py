from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, Enum, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class Group(Base):
    """Модель группы/канала"""
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    telegram_chat_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(255))
    username = Column(String(255))
    is_channel = Column(Boolean, default=False)
    is_group = Column(Boolean, default=False)
    members_count = Column(Integer)
    added_at = Column(DateTime, default=datetime.now)
    last_scanned_at = Column(DateTime)
    
    messages = relationship('Message', back_populates='group')
    statistics = relationship('Statistics', back_populates='group')
    
    __table_args__ = (
        Index('idx_telegram_chat_id', 'telegram_chat_id'),
    )


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_bot = Column(Boolean, default=False)
    first_seen_at = Column(DateTime, default=datetime.now)
    last_seen_at = Column(DateTime, default=datetime.now)
    message_count = Column(Integer, default=0)
    
    messages = relationship('Message', back_populates='sender')
    
    __table_args__ = (
        Index('idx_telegram_user_id', 'telegram_user_id'),
        Index('idx_username', 'username'),
    )


class Message(Base):
    """Модель сообщения"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    telegram_message_id = Column(Integer, nullable=False, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'), index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), index=True)
    
    # Информация о группе
    telegram_chat_id = Column(Integer, index=True)
    chat_title = Column(String(255))
    
    # Информация об отправителе
    telegram_sender_id = Column(Integer, index=True)
    sender_username = Column(String(255), index=True)
    sender_first_name = Column(String(255))
    sender_last_name = Column(String(255))
    
    # Контент сообщения
    text = Column(Text, index=True)
    is_edited = Column(Boolean, default=False)
    
    # Медиа
    media_type = Column(String(50))
    media_file_id = Column(String(255))
    
    # Ответы и пересылка
    reply_to_msg_id = Column(Integer)
    forwarded_from = Column(String(255))
    
    # Временные метки
    message_date = Column(DateTime, index=True)
    received_at = Column(DateTime, default=datetime.now, index=True)
    
    group = relationship('Group', back_populates='messages')
    sender = relationship('User', back_populates='messages')
    
    __table_args__ = (
        Index('idx_chat_message_date', 'telegram_chat_id', 'message_date'),
        Index('idx_sender_date', 'telegram_sender_id', 'message_date'),
    )


class Statistics(Base):
    """Кэш статистики для быстрого доступа"""
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), index=True)
    metric_name = Column(String(255))
    metric_value = Column(Integer)
    calculated_at = Column(DateTime, default=datetime.now)
    
    group = relationship('Group', back_populates='statistics')
    
    __table_args__ = (
        Index('idx_chat_metric', 'group_id', 'metric_name'),
    )
