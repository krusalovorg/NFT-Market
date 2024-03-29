import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import flask
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from wtforms.validators import DataRequired

import nft.api
from forms.search import SearchForm
from forms.users import RegisterForm, LoginForm
# from forms.settings import RedactForm
from forms.add import AddForm
from forms.pay import PayForm
from data.goods import Goods
from data.nft import NFT
from data.users import User
from data.association import Association
from data import db_session
from nft.api import NFTApi

# from forms.check import ChecksForm  # new


import sqlite3  # new!!!!!!!!!

db = 'db/db.db'  # new !!!!!!!

PASS = "NFTMarket123"
marka = "NFTMarket"

nftapi = NFTApi(PASS)

UPLOAD_FOLDER = 'static/img/'

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secreret123123'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

res = []

DEBUG = True

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_favs():
    favs = []
    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    a = db_sess.query(Association)
    if current_user.is_authenticated:
        for i in goods:
            for j in a:
                if current_user.id == j.user_id:
                    if i.id == j.favs_id:
                        favs.append(i.id)
    return favs


def get_category():
    category = []
    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    if current_user.is_authenticated:
        for item in goods:
            if item.category not in category:
                category.append(item.category)
    return category


def get_ords():
    ords = []
    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    a = db_sess.query(Association)
    if current_user.is_authenticated:
        for i in goods:
            for j in a:
                if current_user.id == j.user_id:
                    if i.id == j.orders_id:
                        ords.append(i.id)
    return ords


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/db.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)


# new
@app.route('/func_run')
def func_run():
    x = request.args.get('par_1')
    y = request.args.get('par_2')
    z = request.args.get('par_3')
    if z == '2':
        if y == 'true':
            db_sess = db_session.create_session()
            product = Association(
                user_id=int(str(current_user).split()[1]),
                favs_id=None,
                orders_id=int(x) - 100,
                o_count=1
            )
            db_sess.add(product)
            db_sess.commit()
        else:
            db_sess = db_session.create_session()
            a = db_sess.query(Association).filter(Association.user_id == int(str(current_user).split()[1]),
                                                  Association.orders_id == int(x) - 100).first()
            db_sess.delete(a)
            db_sess.commit()
    elif z == "remove":
        if current_user.is_authenticated and current_user.role == "admin":
            print("delete", x, y, z)
            db_sess = db_session.create_session()
            item = db_sess.query(NFT).filter(NFT.id == int(x)).first()
            if item:
                db_sess.delete(item)

                db_sess.commit()
    elif z == "remove_user":
        if current_user.is_authenticated and current_user.role == "admin":
            db_sess = db_session.create_session()
            item = db_sess.query(User).filter(User.id == x).first()
            if item:
                db_sess.delete(item)

                db_sess.commit()
    elif z == "get_private_key":
        if current_user.is_authenticated:
            return flask.jsonify(key=current_user.private_key)
    elif z == "get_balance":
        if current_user.is_authenticated:
            return flask.jsonify(balance=nftapi.getBalance(current_user.address))

    elif z.startswith('del_img'):
        if z.split(' ')[-1] == '1':

            con = sqlite3.connect(db)
            cur = con.cursor()
            oldfile = cur.execute("SELECT image FROM users WHERE id = ?", (current_user.id,)).fetchone()[0]
            if oldfile:
                cur.execute("UPDATE users SET image = NULL WHERE nickname = ?", (current_user.nickname,))
                if os.path.exists(f'{oldfile}'):
                    os.remove(oldfile)
            con.commit()

        if z.split(' ')[-1] == '2':

            con = sqlite3.connect(db)
            cur = con.cursor()
            oldfile = cur.execute("SELECT banner FROM users WHERE id = ?", (current_user.id,)).fetchone()[0]
            if oldfile:
                cur.execute("UPDATE users SET banner = NULL WHERE nickname = ?", (current_user.nickname,))
                if os.path.exists(f'{oldfile}'):
                    os.remove(oldfile)
            con.commit()

    elif z.startswith('sale'):
        if current_user.is_authenticated and current_user.role == "admin":
            print("add sale", x, y, z)

            con = sqlite3.connect(db)
            cur = con.cursor()
            if len(z.split(' ')[1]) == 0:
                print('скидка пустая')
            else:
                cur.execute("UPDATE nft SET sale = ? WHERE id = ?", (z.split(' ')[1], int(x)))
                con.commit()

    else:
        if y == 'true':
            db_sess = db_session.create_session()
            product = Association(
                user_id=int(str(current_user).split()[1]),
                favs_id=int(x),
                orders_id=None,
                o_count=None
            )
            db_sess.add(product)
            db_sess.commit()
        else:
            db_sess = db_session.create_session()
            # a = db_sess.query(Association).filter(Association.user_id == int(str(current_user).split()[1]),
            #                                       Association.favs_id == int(x)).first()
            # db_sess.delete(a)
            db_sess.commit()
    return '', 204


@app.route("/", methods=['GET', 'POST'])
def index():
    global res
    categories = get_category()
    res.clear()
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')
    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)

    # form4 = FavsForm()
    # form4 = ChecksForm()  # new
    # if form4.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     assoc = Association(
    #         user_id=current_user.id,
    #         favs_id=form4.favs_id.data,
    #         orders_id=0,
    #         o_count=0
    #     )
    #     db_sess.add(assoc)
    #     db_sess.commit()
    if current_user.is_authenticated:
        return render_template("main.html", title='Главная страница', goods=goods,
                               favs=get_favs(), ords=get_ords(),
                               form2=form, cats=categories, role=current_user.role)
    else:
        return render_template("main.html", title='Главная страница', goods=goods,
                               favs=get_favs(), ords=get_ords(),
                               form2=form, cats=categories, role=False)


@login_required
@app.route("/profile/<r>", methods=['GET', 'POST'])
def profile(r):
    global res
    nfts = []

    # db_sess = db_session.create_session()
    # a = db_sess.query(User)  # .filter(User.nickname == r).first()
    # for i in a:
    #     if i.nickname == r:
    #         print(i)

    con = sqlite3.connect(db)
    cur = con.cursor()
    try:
        db_imgs = cur.execute("SELECT image, banner FROM users WHERE nickname = ?", (r,)).fetchall()[0]
    except IndexError as ie:
        print(ie)
        return redirect('/')

    if not os.path.exists(f'{db_imgs[0]}'):
        cur.execute("UPDATE users SET image = NULL WHERE nickname = ?", (r,))
    if not os.path.exists(f'{db_imgs[1]}'):
        cur.execute("UPDATE users SET banner = NULL WHERE nickname = ?", (r,))

    user = cur.execute("SELECT * FROM users WHERE nickname = ?", (r,)).fetchone()
    con.commit()

    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')
    #
    # db_sess = db_session.create_session()
    # nft = db_sess.query(NFT)
    # for i in nft:
    #     if i.address == current_user.address:
    #         nfts.append()

    return render_template("profile.html", title=r,
                           favs=get_favs(),
                           ords=get_ords(), form2=form, user=user)


@login_required
@app.route("/settings", methods=['GET', 'POST'])
def settings():
    global res

    ################################# форма тут для того, чтобы сохранять дефолтыне значения
    class RedactingForm(FlaskForm):
        nickname = StringField('Никнейм', validators=[DataRequired()], default=current_user.nickname)
        description = StringField('Описание', validators=[DataRequired()], default=current_user.description)
        name = StringField('Имя', validators=[DataRequired()], default=current_user.name)
        surname = StringField('Фамилия', validators=[DataRequired()], default=current_user.surname)
        submit = SubmitField('Применить')

    ##################################
    form = SearchForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    form_redact = RedactingForm()
    if form_redact.validate_on_submit():
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("UPDATE users SET nickname = ?, description = ?, name = ?, surname = ? WHERE id = ?", (
            form_redact.nickname.data, form_redact.description.data, form_redact.name.data, form_redact.surname.data,
            current_user.id))

        file = request.files["file"]
        filename = file.filename
        if filename:
            oldfile = cur.execute("SELECT image FROM users WHERE id = ?", (current_user.id,)).fetchone()[0]
            if oldfile:
                os.remove(oldfile)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cur.execute("UPDATE users SET image = ? WHERE id = ?", (
                os.path.join(app.config['UPLOAD_FOLDER'], filename),
                current_user.id))

        file = request.files["file2"]
        filename = file.filename
        if filename:
            oldfile = cur.execute("SELECT banner FROM users WHERE id = ?", (current_user.id,)).fetchone()[0]
            if oldfile:
                os.remove(oldfile)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cur.execute("UPDATE users SET banner = ? WHERE id = ?", (
                os.path.join(app.config['UPLOAD_FOLDER'], filename),
                current_user.id))

        con.commit()
        return redirect(f"/profile/{current_user.nickname}")

    return render_template("settings.html", title='Настройки',
                           favs=get_favs(),
                           ords=get_ords(), form2=form, form_red=form_redact)


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    global res
    ords = get_ords()
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    summ = 0

    for i in goods:
        if i.id in ords:
            summ += i.cost - i.cost * (i.sale / 100)

    return render_template("basket.html", title='Корзина', goods=goods, favs=get_favs(),
                           ords=ords, summ=summ, form2=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_category_choice():
    category = [('Выберети категорию', 'Выберети категорию')]
    buffer = []
    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    if current_user.is_authenticated:
        for item in goods:
            if item.category not in buffer:
                category.append((item.category, item.category))
                buffer.append(item.category)
    return category


@app.route('/meta/<hash_block>', methods=['GET', 'POST'])
def get_metadata(hash_block):
    return flask.jsonify()


@app.route('/add', methods=['GET', 'POST'])
def add():
    if current_user.is_authenticated and current_user.role == "admin":
        form2 = SearchForm()
        if form2.validate_on_submit():
            db_sess = db_session.create_session()
            goods = db_sess.query(NFT)
            for i in goods:
                if str(form2.ttle.data).lower() in str(i.title).lower():
                    res.append(i.id)
            return redirect('/search_results')
        form3 = AddForm()
        cats = get_category_choice()
        form3.category.choices = cats

        if form3.validate_on_submit() and (
                (form3.category.data == "Выберите категорию" and form3.new_category.data != "") or (
                form3.category.data != "Выберите категорию" and form3.new_category.data == "")):
            caty = ""
            if form3.category.data == "Выберите категорию":
                caty = form3.new_category.data
            else:
                caty = form3.category.data

            file = request.files["file"]
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_hash = nftapi.uploadImageNFT("static/img/" + filename)
            if image_hash:
                if current_user.role == "admin" and form3.createAsMarket == True:
                    NFT_Result = nftapi.CreateMarketNFT(form3.title.data,
                                                        "0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621",
                                                        form3.description.data,
                                                        "https://ipfs.io/ipfs/" + image_hash,
                                                        1,
                                                        form3.cost.data,
                                                        caty)
                    print(NFT_Result)
                    if NFT_Result.get("status") == "true":
                        db_sess = db_session.create_session()

                        nft = NFT(title=form3.title.data,
                                  address="0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621",
                                  description=form3.description.data,
                                  image="https://ipfs.io/ipfs/" + image_hash,
                                  amount=1,
                                  cost=form3.cost.data,
                                  category=caty,
                                  rate=5,
                                  hash_block=NFT_Result.get("hash_block"))

                        db_sess.add(nft)
                        db_sess.commit()

                        return redirect('/add')
                else:
                    NFT_Result = nftapi.CreateNFT(form3.title.data,
                                                  current_user.address,
                                                  form3.description.data,
                                                  "https://ipfs.io/ipfs/" + image_hash,
                                                  1,
                                                  form3.cost.data,
                                                  caty,
                                                  current_user.private_key)
                    print(NFT_Result)
                    if NFT_Result.get("status") == "true":
                        db_sess = db_session.create_session()

                        nft = NFT(title=form3.title.data,
                                  address=current_user.address,
                                  description=form3.description.data,
                                  image="https://ipfs.io/ipfs/" + image_hash,
                                  amount=1,
                                  cost=form3.cost.data,
                                  category=caty,
                                  rate=5,
                                  hash_block=NFT_Result.get("hash_block"))

                        db_sess.add(nft)
                        db_sess.commit()

                        return redirect('/add')

        # if form3.validate_on_submit() and (
        #         (form3.category.data == "Выберети категорию" and form3.new_category.data != "") or (
        #         form3.category.data != "Выберети категорию" and form3.new_category.data == "")):
        #     db_sess = db_session.create_session()
        #
        #     file = request.files["file"]
        #     filename = file.filename
        #
        #     caty = ""
        #     if form3.category.data == "Выберети категорию":
        #         caty = form3.new_category.data
        #     else:
        #         caty = form3.category.data
        #
        #     product = Goods(
        #         title=form3.title.data,
        #         cost=form3.cost.data,
        #         description=form3.description.data,
        #         category=caty,
        #         rate=0,
        #         image="/static/img/" + filename,
        #     )
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #
        #     # img = form3.image
        #     # img.file.save(os.path.join(app.config['UPLOAD_FOLDER'], form3.image.file.filename))
        #
        #     db_sess.add(product)
        #     db_sess.commit()
        #     return redirect('/')
        return render_template('add.html', title='Добавление товара', form2=form2,
                               form3=form3,
                               gas=nftapi.getPriceGas(),
                               role=current_user.role)
    else:
        return redirect('/')


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    global res
    ords = get_ords()
    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    summ = 0
    for i in goods:
        if i.id in ords:
            summ += i.cost

    form2 = SearchForm()
    if form2.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form2.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    form3 = PayForm()
    if form3.validate_on_submit():
        if current_user.balance >= summ:
            new_bal = current_user.balance - summ
            db_sess = db_session.create_session()
            for i in ords:
                a = db_sess.query(Association).filter(Association.user_id == int(current_user.id),
                                                      Association.orders_id == i).first()
                db_sess.delete(a)
                db_sess.commit()

            con = sqlite3.connect(db)
            cur = con.cursor()
            cur.execute("UPDATE users SET balance = ? WHERE id = ?", (new_bal, current_user.id))
            con.commit()

        return redirect('/')

    return render_template("pay.html", title='Оплата', goods=goods,
                           ords=ords, summ=summ, form2=form2, form3=form3, balance=current_user.balance)


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    global res
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    return render_template("favorites.html", title='Избранное', goods=goods,
                           favs=get_favs(), ords=get_ords(), form2=form)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    global res
    categories = get_category()
    form = SearchForm()
    if form.validate_on_submit():
        res.clear()
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    # form.button.data true - false
    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)

    return render_template('search_results.html', title='Результаты поиска',
                           res=res, form2=form,
                           goods=goods,
                           favs=get_favs(), ords=get_ords(), cats=categories)


@app.route("/categories/<int:r>", methods=['GET', 'POST'])
def cat(r):
    global res
    categories = get_category()
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    col = 0
    for i in goods:
        if i.category == categories[r - 1]:
            col += 1
    return render_template("categories.html", title='Поиск по категориям',
                           goods=goods, favs=get_favs(),
                           ords=get_ords(),
                           form2=form, cat=categories[r - 1], col=col, cats=categories)


@app.route("/product/<int:r>", methods=['GET', 'POST'])
def product(r):
    global res
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(NFT)
    for i in goods:
        if i.id == r:
            tl = i.title
    return render_template("product.html", title=f'{tl}', goods=goods,
                           favs=get_favs(),
                           ords=get_ords(),
                           form2=form, i_id=r)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global res

    form2 = SearchForm()
    if form2.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form2.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", form2=form2)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   form2=form2)
        if form.email.data == "adminpanel@adminpanel.adminpanel":
            private, address_ = createEthAccount()

            user = User(
                nickname=form.nickname.data,
                surname=form.surname.data,
                name=form.name.data,
                email=form.email.data,
                role="admin",
                private_key=private,
                address=address_,
                description="NFT художник.. ( изменить описание можно в настройках аккаунта )",
                balance=0
            )
        else:
            private, address_ = createEthAccount()

            user = User(
                nickname=form.nickname.data,
                surname=form.surname.data,
                name=form.name.data,
                email=form.email.data,
                private_key=private,
                address=address_,
                description="NFT художник.. ( изменить описание можно в настройках аккаунта )",
                role="user",
            )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           form2=form2)


@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    if current_user.is_authenticated and current_user.role == "admin":
        global res

        form2 = SearchForm()
        if form2.validate_on_submit():
            db_sess = db_session.create_session()
            goods = db_sess.query(NFT)
            for i in goods:
                if str(form2.ttle.data).lower() in str(i.title).lower():
                    res.append(i.id)
            return redirect('/search_results')

        db_sess = db_session.create_session()
        users = db_sess.query(User)
        return render_template('admin/users.html', title='Пользователи', users=users,
                               form2=form2, role=current_user.role)
    else:
        return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    global res

    form2 = SearchForm()
    if form2.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(NFT)
        for i in goods:
            if str(form2.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form,
                               form2=form2)
    return render_template('login.html', title='Авторизация', form=form,
                           form2=form2)


if __name__ == '__main__':
    main()
