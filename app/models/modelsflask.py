from app import db, ma


# Configurações
class Config(db.Model):
    __tablename__ = 'configs'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    chave = db.Column(db.String(255))
    valor = db.Column(db.String(255))
    

class ConfigSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'chave','valor')
        

config = ConfigSchema()
configs = ConfigSchema(many=True)


# Menus
class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255))

class MenuSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'nome')
        

menu = MenuSchema()
menus = MenuSchema(many=True)


# Itens do menu
class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    icon = db.Column(db.String(255))
    menus_id = db.Column(db.ForeignKey('menus.id'), nullable=False, index=True)

    menus = db.relationship('Menu', primaryjoin='MenuItem.menus_id == Menu.id', backref='menu_items')


class MenuItemSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name','url', 'icon','menus_id')
        

menuItem = MenuItemSchema()
menuItems = MenuItemSchema(many=True)



# Acessos do sistema
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

class RoleSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name','description')

role = RoleSchema()
roles = RoleSchema(many=True)

# Usuarios
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    user_name = db.Column(db.String(255), primary_key=True, nullable=False)
    active = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    token = db.Column(db.String(255))
    first_login = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime)
    waiting_fo__approval = db.Column('waiting_fo_ approval', db.Integer, nullable=False, server_default=db.FetchedValue())

class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name','email','user_name', 'active','token','first_login', 'created_at','updated_at')

user = UserSchema()
users = UserSchema(many=True)

# Senha dos usuarios
class UsersPassword(db.Model):
    __tablename__ = 'users_passwords'
    __table_args__ = (
        db.ForeignKeyConstraint(['users_id', 'users_email', 'users_user_name'], ['users.id', 'users.email', 'users.user_name']),
        db.Index('fk_users_passwords_users_idx', 'users_id', 'users_email', 'users_user_name')
    )

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    users_id = db.Column(db.Integer, nullable=False)
    users_email = db.Column(db.String(255), nullable=False)
    users_user_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    users = db.relationship('User', primaryjoin='and_(UsersPassword.users_id == User.id, UsersPassword.users_email == User.email, UsersPassword.users_user_name == User.user_name)', backref='users_passwords')

class UsersPasswordSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'users_id','users_email', 'users_user_name', 'password','active','created_at')

userPassword = UsersPasswordSchema()
userPasswords = UsersPasswordSchema(many=True)

# Acessos dos usuarios
class UsersRole(db.Model):
    __tablename__ = 'users_roles'
    __table_args__ = (
        db.ForeignKeyConstraint(['users_id', 'users_email', 'users_user_name'], ['users.id', 'users.email', 'users.user_name']),
        db.Index('fk_users_roles_users1_idx', 'users_id', 'users_email', 'users_user_name')
    )

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    users_id = db.Column(db.Integer, nullable=False)
    users_email = db.Column(db.String(255), nullable=False)
    users_user_name = db.Column(db.String(255), nullable=False)
    roles_id = db.Column(db.ForeignKey('roles.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime)

    roles = db.relationship('Role', primaryjoin='UsersRole.roles_id == Role.id', backref='users_roles')
    users = db.relationship('User', primaryjoin='and_(UsersRole.users_id == User.id, UsersRole.users_email == User.email, UsersRole.users_user_name == User.user_name)', backref='users_roles')

class UsersRoleSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'users_id','users_email','users_user_name', 'roles_id','created_at','updated_at')

userRole = UsersRoleSchema()
userRoles = UsersRoleSchema(many=True)