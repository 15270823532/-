from libs.orm import db


class Weibo(db.Model):
    __tablename__ = 'weibo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime)