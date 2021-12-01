from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
from grocery_app import bcrypt

# Import app and db from events_app package so that we can run app
from grocery_app import db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)


@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()
    form_valid = form.validate_on_submit()

    if form_valid:
        store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user
        )
        db.session.add(store)
        db.session.commit()
        flash('Store successfully created!')
        return redirect(url_for('main.store_detail', store_id=store.id))

    return render_template('new_store.html', form=form)


@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()
    form_valid = form.validate_on_submit()

    if form_valid:
        item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user
        )
        db.session.add(item)
        db.session.commit()
        flash('Item successfully created!')
        return redirect(url_for('main.item_detail', item_id=item.id))

    return render_template('new_item.html', form=form)


@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)
    form_valid = form.validate_on_submit()

    if form_valid:
        store.title = form.title.data
        store.address = form.address.data
        db.session.add(store)
        db.session.commit()
        flash('Store successfully updated!')
        return redirect(url_for('main.store_detail', store_id=store.id, store=store))

    store = GroceryStore.query.get(store_id)
    return render_template('store_detail.html', store=store, form=form)


@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)
    form_valid = form.validate_on_submit()

    if form_valid:
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.add(item)
        db.session.commit()

        flash('Item was successfully updated!')
        return redirect(url_for('main.item_detail', item_id=item.id, item=item))

    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item, form = form)


@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.append(item)

    db.session.add(current_user)
    db.session.commit()

    flash('Item was added to cart successfully!')
    return redirect(url_for('main.shopping_list'))


@main.route('/shopping_list')
@login_required
def shopping_list():
    return render_template('shopping_list.html', items=current_user.shopping_list_items)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
