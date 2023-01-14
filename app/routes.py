from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, AddAddressForm
from app.models import User, Address

@app.route('/')
def index():
    addresses = Address.query.all()
    return render_template('index.html', addresses=addresses) 

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # Query our user table to see if there are any users with either username or email from form
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        # If the query comes back with any results
        if check_user:
            # Flash message saying that a user with email/username already exists
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        # If check_user is empty, create a new record in the user table
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        # Flash a success message
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        # Redirect back to Home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the username and password from the form
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Query the user table to see if there is a user with that username
        user = User.query.filter_by(username=username).first()
        # Check if there is a user and that the password is correct
        if user is not None and user.check_password(password):
            # log the user in
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))


@app.route('/add-address', methods=["GET", "POST"])
@login_required
def add_address():
    form = AddAddressForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        new_address = Address(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id=current_user.id)
        flash(f"{new_address.first_name} {new_address.last_name} has been added to the book!", "success")
        return redirect(url_for('index'))
    
    return render_template('add-address.html', form=form)

@app.route('/addresses/<int:address_id>')
def get_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"An address with id {address_id} does not exists", "danger")
        return redirect(url_for('index'))
    return render_template('addresses.html', address=address)

@app.route('/addresses/address_id/edit<int:address_id>', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"An address with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    if address.author != current_user:
        flash("You do not have permissiont to edit this address", "danger")
        return redirect(url_for('index'))
    form = AddAddressForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        addressdata = form.address.data
        address.update(first_name=first_name, last_name=last_name, phone_number=phone_number, address=addressdata)
        flash(f"{address.first_name} {address.last_name} has been updated!", "success")
        return redirect(url_for('index'))
    if request.method == 'GET':
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
    return render_template('edit_address.html', address=address, form=form)

@app.route('/addresses/<int:address_id>/delete')
@login_required
def delete_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"An andress with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    if address.author != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))
    address.delete()
    flash(f"{address} has been deleted", "info")
    return redirect(url_for('index'))

    
    
