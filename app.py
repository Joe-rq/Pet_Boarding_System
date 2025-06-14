from flask import Flask, render_template, request, redirect, url_for, flash
from src.models.models import db, Owner, Pet
from src.utils.config import Config
from sqlalchemy import func

def create_app():
    """应用工厂函数"""
    app = Flask(__name__, template_folder='src/templates')
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    return app

app = create_app()

@app.route('/')
def index():
    """首页 - 显示所有功能入口"""
    return render_template('index.html')

@app.route('/pets')
def list_pets():
    """查询宠物列表，支持按寄养状态筛选，并按照体重从轻到重排序"""
    # 获取筛选参数
    status_filter = request.args.get('status', 'all')  # all, boarding, not_boarding
    
    # 根据筛选条件查询
    if status_filter == 'boarding':
        pets = Pet.query.filter_by(is_boarding=True).order_by(Pet.weight.asc()).all()
        filter_text = "寄养中"
    elif status_filter == 'not_boarding':
        pets = Pet.query.filter_by(is_boarding=False).order_by(Pet.weight.asc()).all()
        filter_text = "已离开"
    else:  # all
        pets = Pet.query.order_by(Pet.weight.asc()).all()
        filter_text = "全部"
    
    return render_template('pets.html', pets=pets, status_filter=status_filter, filter_text=filter_text)

@app.route('/owner/<owner_name>')
def owner_pets(owner_name):
    """找出某位主人的宠物信息，支持查看所有宠物或只查看寄养中的"""
    owner = Owner.query.filter_by(name=owner_name).first()
    if not owner:
        flash(f'未找到主人：{owner_name}', 'error')
        return redirect(url_for('index'))
    
    # 获取筛选参数
    status_filter = request.args.get('status', 'boarding')  # boarding, not_boarding, all
    
    # 根据筛选条件查询该主人的宠物
    if status_filter == 'boarding':
        pets = Pet.query.filter_by(owner_id=owner.id, is_boarding=True).all()
        filter_text = "寄养中"
    elif status_filter == 'not_boarding':
        pets = Pet.query.filter_by(owner_id=owner.id, is_boarding=False).all()
        filter_text = "已离开"
    else:  # all
        pets = Pet.query.filter_by(owner_id=owner.id).all()
        filter_text = "全部"
    
    pet_count = len(pets)
    
    return render_template('owner_pets.html', 
                         owner=owner, 
                         pets=pets, 
                         pet_count=pet_count,
                         status_filter=status_filter,
                         filter_text=filter_text)

@app.route('/search_owner', methods=['GET', 'POST'])
def search_owner():
    """搜索主人的宠物 - 支持自定义查询任意主人"""
    if request.method == 'POST':
        owner_name = request.form.get('owner_name', '').strip()
        if not owner_name:
            flash('请输入主人姓名', 'error')
            return render_template('search_owner.html', owners=Owner.query.all())
        
        # 支持模糊搜索
        owners = Owner.query.filter(Owner.name.like(f'%{owner_name}%')).all()
        
        if not owners:
            flash(f'未找到姓名包含"{owner_name}"的主人', 'error')
            return render_template('search_owner.html', owners=Owner.query.all())
        
        # 如果只找到一个主人，直接跳转到详情页
        if len(owners) == 1:
            return redirect(url_for('owner_pets', owner_name=owners[0].name))
        
        # 如果找到多个主人，显示选择列表
        search_results = []
        for owner in owners:
            boarding_pets = Pet.query.filter_by(owner_id=owner.id, is_boarding=True).all()
            search_results.append({
                'owner': owner,
                'pet_count': len(boarding_pets),
                'pets': boarding_pets
            })
        
        return render_template('search_owner.html', 
                             owners=Owner.query.all(),
                             search_results=search_results,
                             search_term=owner_name)
    
    # GET请求，显示搜索页面
    return render_template('search_owner.html', owners=Owner.query.all())

@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    """添加新主人"""
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form.get('phone', '')
        email = request.form.get('email', '')
        
        owner = Owner(name=name, phone=phone, email=email)
        db.session.add(owner)
        db.session.commit()
        
        flash(f'成功添加主人：{name}', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_owner.html')

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    """添加新宠物"""
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        breed = request.form.get('breed', '')
        age = int(request.form['age']) if request.form['age'] else None
        weight = float(request.form['weight'])
        color = request.form.get('color', '')
        owner_id = int(request.form['owner_id'])
        
        pet = Pet(name=name, species=species, breed=breed, 
                 age=age, weight=weight, color=color, owner_id=owner_id)
        db.session.add(pet)
        db.session.commit()
        
        flash(f'成功添加宠物：{name}', 'success')
        return redirect(url_for('index'))
    
    # 获取所有主人供选择
    owners = Owner.query.all()
    return render_template('add_pet.html', owners=owners)

@app.route('/owners')
def list_owners():
    """显示所有主人"""
    owners = Owner.query.all()
    return render_template('owners.html', owners=owners)

@app.route('/edit_owner/<int:owner_id>', methods=['GET', 'POST'])
def edit_owner(owner_id):
    """编辑主人信息"""
    owner = Owner.query.get_or_404(owner_id)
    
    if request.method == 'POST':
        owner.name = request.form['name']
        owner.phone = request.form.get('phone', '')
        owner.email = request.form.get('email', '')
        
        db.session.commit()
        flash(f'成功更新主人信息：{owner.name}', 'success')
        return redirect(url_for('list_owners'))
    
    return render_template('edit_owner.html', owner=owner)

@app.route('/delete_owner/<int:owner_id>', methods=['POST'])
def delete_owner(owner_id):
    """删除主人（会同时删除其所有宠物）"""
    owner = Owner.query.get_or_404(owner_id)
    owner_name = owner.name
    
    db.session.delete(owner)
    db.session.commit()
    
    flash(f'已删除主人：{owner_name} 及其所有宠物', 'success')
    return redirect(url_for('list_owners'))

@app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """编辑宠物信息"""
    pet = Pet.query.get_or_404(pet_id)
    
    if request.method == 'POST':
        pet.name = request.form['name']
        pet.species = request.form['species']
        pet.breed = request.form.get('breed', '')
        pet.age = int(request.form['age']) if request.form['age'] else None
        pet.weight = float(request.form['weight'])
        pet.color = request.form.get('color', '')
        pet.owner_id = int(request.form['owner_id'])
        pet.is_boarding = request.form.get('is_boarding') == 'on'  # 复选框处理
        
        db.session.commit()
        flash(f'成功更新宠物信息：{pet.name}', 'success')
        return redirect(url_for('list_pets'))
    
    # 获取所有主人供选择
    owners = Owner.query.all()
    return render_template('edit_pet.html', pet=pet, owners=owners)

@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    """删除宠物"""
    pet = Pet.query.get_or_404(pet_id)
    pet_name = pet.name
    
    db.session.delete(pet)
    db.session.commit()
    
    flash(f'已删除宠物：{pet_name}', 'success')
    return redirect(url_for('list_pets'))

@app.route('/toggle_boarding/<int:pet_id>', methods=['POST'])
def toggle_boarding(pet_id):
    """快速切换宠物寄养状态"""
    pet = Pet.query.get_or_404(pet_id)
    pet.is_boarding = not pet.is_boarding
    
    db.session.commit()
    
    status = "寄养中" if pet.is_boarding else "已离开"
    flash(f'{pet.name} 的状态已更新为：{status}', 'success')
    
    # 根据来源页面返回
    return redirect(request.referrer or url_for('list_pets'))

@app.route('/init_db')
def init_db():
    """初始化数据库并添加示例数据"""
    # 创建所有表
    db.create_all()
    
    # 检查是否已有数据
    if Owner.query.first():
        flash('数据库已经初始化过了', 'info')
        return redirect(url_for('index'))
    
    # 添加示例主人
    owners_data = [
        {'name': '王小明', 'phone': '13800138001', 'email': 'wang@example.com'},
        {'name': '李小红', 'phone': '13800138002', 'email': 'li@example.com'},
        {'name': '张小强', 'phone': '13800138003', 'email': 'zhang@example.com'},
    ]
    
    for owner_data in owners_data:
        owner = Owner(**owner_data)
        db.session.add(owner)
    
    db.session.commit()
    
    # 添加示例宠物
    pets_data = [
        {'name': '小白', 'species': '狗', 'breed': '金毛', 'age': 3, 'weight': 25.5, 'color': '金色', 'owner_id': 1},
        {'name': '小黑', 'species': '猫', 'breed': '英短', 'age': 2, 'weight': 4.2, 'color': '黑色', 'owner_id': 1},
        {'name': '旺财', 'species': '狗', 'breed': '柴犬', 'age': 1, 'weight': 8.8, 'color': '黄色', 'owner_id': 2},
        {'name': '咪咪', 'species': '猫', 'breed': '波斯猫', 'age': 4, 'weight': 3.5, 'color': '白色', 'owner_id': 2},
        {'name': '大黄', 'species': '狗', 'breed': '拉布拉多', 'age': 5, 'weight': 30.2, 'color': '黄色', 'owner_id': 3},
        {'name': '小花', 'species': '猫', 'breed': '美短', 'age': 1, 'weight': 2.8, 'color': '花色', 'owner_id': 3},
    ]
    
    for pet_data in pets_data:
        pet = Pet(**pet_data)
        db.session.add(pet)
    
    db.session.commit()
    
    flash('数据库初始化成功！已添加示例数据', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 