#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置文件

MIT License
Copyright (c) 2024 Pet Boarding System
"""

import os

class Config:
    """应用配置类"""
    # 数据库配置
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "database", "pet_boarding.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask配置
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True 