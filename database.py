# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///basadan.db')
Session = sessionmaker(bind=engine)

class Пользователь(Base):
    __tablename__ = 'Пользователь'

    uuid = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    available_lessons = relationship("Доступные_Уроки", back_populates="пользователь")

class Админ(Base):
    __tablename__ = 'Админ'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

class Урок(Base):
    __tablename__ = 'Урок'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    subtitle = Column(Text)
    stages = relationship("Этап", back_populates="урок")

class Этап(Base):
    __tablename__ = 'Этап'

    id = Column(Integer, primary_key=True, autoincrement=True)
    урок_id = Column(Integer, ForeignKey('Урок.id'))
    index = Column(Integer, nullable=False)
    images = Column(Text)
    lesson_text = Column(Text, nullable=False)
    lesson_speech = Column(Text)
    урок = relationship("Урок", back_populates="stages")

class Тариф(Base):
    __tablename__ = 'Тариф'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class Доступные_Уроки(Base):
    __tablename__ = 'Доступные_Уроки'

    пользователь_uuid = Column(String, ForeignKey('Пользователь.uuid'), primary_key=True)
    урок_id = Column(Integer, ForeignKey('Урок.id'), primary_key=True)
    пользователь = relationship("Пользователь", back_populates="available_lessons")
    урок = relationship("Урок")

def init_db():
    Base.metadata.create_all(engine)

# Функция для добавления тестовых тарифов
def add_test_tarif(name, price):
    add_tariff(name="SMM-Мастер", price=499)
    add_tariff(name="SMM-Старт", price=2000)
    add_tariff(name="SMM-Профи", price=3500)


def add_user(uuid, username):
    session = Session()
    new_user = Пользователь(uuid=uuid, username=username)
    session.add(new_user)
    session.commit()
    session.close()

def get_user(uuid):
    session = Session()
    user = session.query(Пользователь).filter_by(uuid=uuid).first()
    session.close()
    return user
def get_admin(uuid):
    session = Session()
    admin = session.query(Админ).filter_by(id=uuid).first()
    session.close()
    if admin is None:
        return False
    else:
        return True
def get_tarif(id_):
    session = Session()
    tar = session.query(Тариф).filter_by(id=id_).first()
    session.close()
    return tar
# Другие функции для добавления, удаления и редактирования записей...

# Создаем подключение к базе данных SQLite
#engine = create_engine('sqlite:///example.db')
#Base.metadata.create_all(engine)
#Session = sessionmaker(bind=engine)

def add_user(uuid, username):
    session = Session()
    new_user = Пользователь(uuid=uuid, username=username)
    session.add(new_user)
    session.commit()
    session.close()

def add_admin(uuid, username):
    session = Session()
    new_admin = Админ(id=uuid, username=username)
    session.add(new_admin)
    session.commit()
    session.close()
def add_stage(урок_id, index, images, lesson_text, lesson_speech):
    session = Session()
    new_stage = Этап(урок_id=урок_id, index=index, images=images, lesson_text=lesson_text, lesson_speech=lesson_speech)
    session.add(new_stage)
    session.commit()
    session.close()
def add_lesson(title, subtitle):
    session = Session()
    new_lesson = Урок(title=title, subtitle=subtitle)
    session.add(new_lesson)
    session.commit()
    lesson_id = new_lesson.id
    session.close()
    return lesson_id


# Функция для добавления тестовых уроков
def add_test_lessons():
    lesson1_id = add_lesson("Урок 1", "Описание урока 1")
    add_stage(lesson1_id, 1, "image1.png", "Текст урока 1 этап 1", "speech1.mp3")
    add_stage(lesson1_id, 2, "image2.png", "Текст урока 1 этап 2", None)

    lesson2_id = add_lesson("Урок 2", "Описание урока 2")
    add_stage(lesson2_id, 1, None, "Текст урока 2 этап 1", "speech2.mp3")
    add_stage(lesson2_id, 2, "image3.png", "Текст урока 2 этап 2", "speech3.mp3")
    add_stage(lesson2_id, 3, None, "Текст урока 2 этап 3", None)

def get_aLL_lesson():
    session = Session()
    lesson = session.query(Урок)

    return lesson
    session.close()

def get_aLL_tarifs():
    session = Session()
    les = session.query(Тариф)
    return les
    session.close()
# ... остальная часть вашего database.py ...


def add_tariff(name, price):
    session = Session()
    new_tariff = Тариф(name=name, price=price)
    session.add(new_tariff)
    session.commit()
    session.close()

def add_available_lesson(пользователь_uuid, урок_id):
    session = Session()
    new_available_lesson = Доступные_Уроки(пользователь_uuid=пользователь_uuid, урок_id=урок_id)
    session.add(new_available_lesson)
    session.commit()
    session.close()

def delete_user(uuid):
    session = Session()
    user = session.query(Пользователь).filter_by(uuid=uuid).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()

def delete_admin(admin_id):
    session = Session()
    admin = session.query(Админ).filter_by(id=admin_id).first()
    if admin:
        session.delete(admin)
        session.commit()
    session.close()

def delete_lesson(lesson_id):
    session = Session()
    lesson = session.query(Урок).filter_by(id=lesson_id).first()
    if lesson:
        session.delete(lesson)
        session.commit()
    session.close()

def get_user(uuid):
    session = Session()
    user = session.query(Пользователь).filter_by(uuid=uuid).first()

    if user:
        session.close()
        return True
    else:
        session.close()
        return False


def update_user(uuid, new_username):
    session = Session()
    user = session.query(Пользователь).filter_by(uuid=uuid).first()
    if user:
        user.username = new_username
        session.commit()
    session.close()

def update_admin(admin_id, new_username):
    session = Session()
    admin = session.query(Админ).filter_by(id=admin_id).first()
    if admin:
        admin.username = new_username
        session.commit()
    session.close()

def update_lesson(lesson_id, new_title, new_subtitle):
    session = Session()
    lesson = session.query(Урок).filter_by(id=lesson_id).first()
    if lesson:
        lesson.title = new_title
        lesson.subtitle = new_subtitle
        session.commit()
    session.close()


def upadate_tariff(tariff_id,new_name, new_price):
    session = Session()
    tariff = session.query(Тариф).filter_by(id = tariff_id).first()
    if tariff:
        tariff.name = new_name
        tariff.price = new_price
        session.commit()
    session.close()
