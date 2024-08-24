from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Platform(db.Model):
    __tablename__ = 'platform'
    __table_args__ = {'schema': 'public'}

    platformid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow())


class UserPlatform(db.Model):
    __tablename__ = 'userplatform'
    __table_args__ = {'schema': 'public'}

    userplatformid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('public.User.userid'), nullable=False)
    platformid = db.Column(db.Integer, db.ForeignKey('public.platform.platformid'), nullable=False)
    datejoined = db.Column(db.Date, nullable=False, default=datetime.utcnow())

    user = db.relationship('User', backref=db.backref('userplatforms', lazy=True))
    platform = db.relationship('Platform', backref=db.backref('userplatforms', lazy=True))


class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'public'}

    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False)
    datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    datemodified = db.Column(db.Date, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())


class Blog(db.Model):
    __tablename__ = 'blog'
    __table_args__ = {'schema': 'public'}

    blogid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    authorid = db.Column(db.Integer, db.ForeignKey('public.User.userid'), nullable=False)
    datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    datemodified = db.Column(db.Date, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())
    isdeleted = db.Column(db.Boolean, nullable=False, default=False)

    author = db.relationship('User', backref=db.backref('blogs', lazy=True))


class Comment(db.Model):
    __tablename__ = 'comment'
    __table_args__ = {'schema': 'public'}

    commentid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    authorid = db.Column(db.Integer, db.ForeignKey('public.User.userid'), nullable=False)
    blogid = db.Column(db.Integer, db.ForeignKey('public.blog.blogid'), nullable=False)
    datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    datemodified = db.Column(db.Date, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())
    isdeleted = db.Column(db.Boolean, nullable=False, default=False)

    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    blog = db.relationship('Blog', backref=db.backref('comments', lazy=True))