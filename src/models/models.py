#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模型定义

MIT License
Copyright (c) 2024 Pet Boarding System
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Owner(db.Model):
    """主人模型 - 一个主人可以有多只宠物"""
    __tablename__ = 'owners'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 一对多关系：一个主人可以有多只宠物
    pets = db.relationship('Pet', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Owner {self.name}>'

class Pet(db.Model):
    """宠物模型 - 每只宠物只属于一个主人"""
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)  # 物种：狗、猫等
    breed = db.Column(db.String(100))  # 品种
    age = db.Column(db.Integer)  # 年龄
    weight = db.Column(db.Float, nullable=False)  # 体重（kg）
    color = db.Column(db.String(50))  # 颜色
    is_boarding = db.Column(db.Boolean, default=True)  # 是否正在寄养
    check_in_date = db.Column(db.DateTime, default=datetime.utcnow)  # 入住日期
    
    # 外键关联到主人
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    
    def __repr__(self):
        return f'<Pet {self.name} ({self.species})>' 