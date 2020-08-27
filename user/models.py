import random

from libs.utils import random_hz_str
from libs.orm import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'unknow'), default='unknow')
    city = db.Column(db.String(10), default='上海')

    @classmethod
    def fake_users(cls, num):
        users_list = []
        for i in range(num):
            username=random_hz_str(random.choice([2,3,4]))
            password='1008611'
            gender=random.choice(['male', 'female', 'unknow'])
            city=random.choice(['旧金山','北京','纽约','东京'])
            user=cls(username=username,password=password,gender=gender,city=city)
            users_list.append(user)
        db.session.add_all(users_list)
        db.session.commit()
        return users_list