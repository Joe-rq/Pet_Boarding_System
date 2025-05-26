# 宠物寄养小屋管理系统

一个基于Flask和SQLAlchemy的宠物寄养管理系统，实现了宠物与主人的一对多关系管理。

## 🎯 项目目标

为宠物寄养小屋设计一个小型数据库系统，记录宠物信息和主人信息，实现以下核心功能：

1. **查询所有寄养中的宠物，并按照体重从轻到重排序**
2. **找出某位主人（例如"王小明"）寄养的宠物数量，同时显示这些宠物的名字**

## 🏗️ 技术架构

- **Web框架**: Flask 2.3.3
- **ORM**: SQLAlchemy 2.0.23
- **数据库**: SQLite
- **前端**: Bootstrap 5 + Font Awesome
- **语言**: Python 3.x

## 📊 数据库设计

### 主人表 (owners)
- `id`: 主键
- `name`: 姓名
- `phone`: 电话
- `email`: 邮箱
- `created_at`: 创建时间

### 宠物表 (pets)
- `id`: 主键
- `name`: 宠物名字
- `species`: 物种（狗、猫等）
- `breed`: 品种
- `age`: 年龄
- `weight`: 体重（用于排序）
- `color`: 颜色
- `is_boarding`: 是否正在寄养
- `check_in_date`: 入住日期
- `owner_id`: 外键，关联主人

### 关系设计
- **一对多关系**: 一个主人可以有多只宠物
- **外键约束**: 每只宠物必须属于一个主人

## 🚀 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python app.py
```

### 3. 访问应用
打开浏览器访问: http://127.0.0.1:5000

### 4. 初始化数据库
首次运行时，点击首页的"初始化数据库"按钮，系统会：
- 创建数据库表
- 添加示例主人数据（王小明、李小红、张小强）
- 添加示例宠物数据

## 🎮 功能演示

### 核心功能1: 按体重排序查看宠物
- 访问路径: `/pets`
- 功能: 显示所有寄养中的宠物，按体重从轻到重排序
- 实现: `Pet.query.filter_by(is_boarding=True).order_by(Pet.weight.asc()).all()`

### 核心功能2: 查询指定主人的宠物
- 访问路径: `/owner/王小明`
- 功能: 显示王小明寄养的宠物数量和详情
- 实现: 通过主人姓名查询，统计其寄养中的宠物

## 📁 项目结构

```
Pet_Boarding_System/
├── app.py              # 主应用文件
├── models.py           # 数据库模型
├── config.py           # 配置文件
├── requirements.txt    # 依赖包
├── README.md          # 项目说明
├── templates/         # HTML模板
│   ├── base.html      # 基础模板
│   ├── index.html     # 首页
│   ├── pets.html      # 宠物列表
│   ├── owner_pets.html # 主人宠物详情
│   ├── owners.html    # 主人列表
│   ├── add_owner.html # 添加主人
│   └── add_pet.html   # 添加宠物
├── pet_boarding.db    # SQLite数据库文件
├── 页面展示.png       # 系统界面截图
├── 宠物编辑.png       # 宠物编辑界面截图
├── 宠物列表.png       # 宠物列表界面截图
└── 宠物添加.png       # 宠物添加界面截图
```

## 🔧 主要路由

- `/` - 首页
- `/init_db` - 初始化数据库
- `/pets` - 宠物列表（按体重排序）
- `/owner/<owner_name>` - 查询指定主人的宠物
- `/owners` - 所有主人列表
- `/add_owner` - 添加主人
- `/add_pet` - 添加宠物

## 💡 核心ORM查询

### 1. 按体重排序查询宠物
```python
pets = Pet.query.filter_by(is_boarding=True).order_by(Pet.weight.asc()).all()
```

### 2. 查询指定主人的宠物
```python
owner = Owner.query.filter_by(name=owner_name).first()
boarding_pets = Pet.query.filter_by(owner_id=owner.id, is_boarding=True).all()
```

### 3. 一对多关系查询
```python
# 通过关系属性直接访问
owner.pets  # 获取主人的所有宠物
pet.owner   # 获取宠物的主人
```

## 🎨 界面特色

- 响应式设计，支持移动端
- Bootstrap 5 现代化界面
- Font Awesome 图标
- 卡片式布局
- 颜色编码状态显示
- 悬停动画效果

## 📝 示例数据

系统预置了以下示例数据：

**主人数据:**
- 王小明 (2只宠物: 小白25.5kg, 小黑4.2kg)
- 李小红 (2只宠物: 旺财8.8kg, 咪咪3.5kg)  
- 张小强 (2只宠物: 大黄30.2kg, 小花2.8kg)

**体重排序结果:** 小花(2.8kg) → 咪咪(3.5kg) → 小黑(4.2kg) → 旺财(8.8kg) → 小白(25.5kg) → 大黄(30.2kg)

## 🔍 验证核心功能

1. **体重排序功能**: 访问 `/pets` 查看宠物按体重排序
2. **主人查询功能**: 访问 `/owner/王小明` 查看王小明的2只宠物（小白、小黑）

## 🛠️ 开发说明

- 使用SQLAlchemy ORM，避免直接SQL操作
- 实现了完整的CRUD操作
- 数据库关系通过外键和relationship建立
- 模板继承减少代码重复
- 消息闪现提供用户反馈 