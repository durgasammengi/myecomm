from mailbox import Message
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import ChangePasswordForm, ForgetPasswordForm, ProductForm, ProfileForm, RegistrationForm, LoginForm, OTPForm, ResetPasswordForm
from app.models import Cart, User, Product
from twilio.rest import Client
import random
import smtplib
import pyotp

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)
#Implement registration and login routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    print("in registration")
    if current_user.is_authenticated:
        print("iin authenicated")
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        # user.cart = Cart()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         # login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("In authentication1")
    form = LoginForm()
    if form.validate_on_submit():
        print("success authentication2")
        user = User.query.filter_by(username=form.username.data).first()
        print("success authentication3")
        if user and user.check_password(form.password.data):
            print("success authentication")
            if user.phone_number:
                # Generate OTP and send it via SMS using Twilio
                otp = generate_otp()
                send_otp_sms(user.email, otp)

                # Store the user and OTP for verification
                session['otp_user'] = user.id
                session['otp_code'] = otp

                return redirect(url_for('otp_verification'))

    return render_template('login.html', title='Login', form=form)
def generate_otp():
    # Generate a 6-digit OTP (you can customize the length)
    return ''.join(random.choice('0123456789') for _ in range(6))
def send_otp_sms(phone_number, otp):
    # Initialize Twilio client
    client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

    # Send OTP via SMS
    # message = client.messages.create(
    #     body=f'Your OTP for login is: {otp}',
    #     from_=app.config['TWILIO_PHONE_NUMBER'],
    #     to=phone_number

    # message = client.messages \
    # .create(
    #      from_= '+18447591414'
    #      body='Your OTP for login is: {otp}',
    #      messaging_service_sid='MG9752274e9e519418a7406176694466fa',
    #      to=phone_number
    # )
    #message = client.messages.create(from_='+18447591414',body=f'Your OTP for login is: {otp}',to=phone_number)
    message = send_email_otp(phone_number, otp)
@app.route('/otp-verification', methods=['GET', 'POST'])
def otp_verification():
    user_id = session.get('otp_user')
    otp_code = session.get('otp_code')
    print("otp - "+otp_code)
    if not user_id:
        flash('Invalid access to OTP verification.', 'danger')
        return redirect(url_for('login'))
    elif not otp_code:
        flash('Invalid access to OTP verification.', 'danger')
        return redirect(url_for('otp_verification'))


    form = OTPForm()

    if form.validate_on_submit():
        user = User.query.get(user_id)
        # totp = pyotp.TOTP(user.otp_secret)
        print("otp 1- "+otp_code)
        # if totp.verify(form.otp.data) and form.otp.data == otp_code:
        if form.otp.data == otp_code:
            login_user(user)
            flash('Login successful!', 'success')
            session.pop('otp_user', None)
            session.pop('otp_code', None)
            session['cart'] = []
            print("otp 2- uid{user_id}")
            print(user_id)
            if user.username=="Administrator":
                return redirect(url_for('adminpage'))
            
            return redirect(url_for('index')) 
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('otp_verification.html', title='OTP Verification', form=form)
def send_email_otp(mail, otp):
    
    msg=otp+"your otp"
    s=smtplib.SMTP_SSL("smtp.gmail.com",465)
    Email_id="prasadsammengi@gmail.com"
    s.login(Email_id,"vgbshturkhmsnzyb")
    send_to=mail
    s.sendmail(Email_id,send_to,msg)
#Create a api with name dashboard and return the dashboard page
@app.route('/dashboard')   
@login_required
def dashboard():
    return render_template('dashboard.html')
@app.route('/adminpage')
@login_required
def adminpage():
    products = Product.query.all()
    return render_template('adminpage.html', products=products)

from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = ''  # Set the path where you want to store images
NEW_PATH = '../static/images/products/'

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    UPLOAD_FOLDER = app.root_path+"/static/images/products"
    form = ProductForm()
    print("in add product pages")
    if request.method == 'POST' and form.validate_on_submit():
        # Create a new Product object and populate it with form data
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            product_type=form.product_type.data,
            image_path=''  # Initialize image path as empty
        )

        # Check if an image was uploaded
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            form.image.data.save(image_path)
            new_product.image_path = NEW_PATH+filename

        # Add the new product to the database
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect('/adminpage')  # Redirect to the product listing page (modify URL as needed)
    
    print("in add product pages sedning to html page")
    return render_template('add_product.html', form=form)
@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()    
    return redirect(url_for('index'))
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        print("in add to cart %s"% id)
        if 'cart' not in session:
            print("creating new cart")
            session['cart'] = []
        print("in add to cart, appending ")
        session['cart'].append(product_id)
    except Exception as e:
        print(e)
    # return redirect(url_for('index'),200, cart_count=len(session.get('cart', [])))
    return jsonify({'cart_count':len(session.get('cart', []))})

@app.route('/get_cart_count' , methods=['GET'])
def get_cart_count():
    print("3333333333333333333333333333")
    cart_count = len(session.get('cart', []))  # Assuming the cart is stored in the session
    return jsonify({'count': cart_count})

#create a method show products in a cart
@login_required
@app.route('/show_cart', methods=['GET'])
def show_cart():
    cart = session.get('cart', [])
    products = []
    total = 0
    for id in cart:
        product = Product.query.get(id)
        total += product.price
        products.append(product)
    print("lent of products in cart is %s"%len(products))
    return render_template('show_cart.html', products=products, total=total)
#Create a method for payment page and create a html page for it
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    cart = session.get('cart', [])
    products = []
    total = 0
    for id in cart:
        product = Product.query.get(id)
        total += product.price
        products.append(product)
    print("lent of products in cart is %s"%len(products))
    return render_template('payment.html', products=products, total=total)
#create a method to create a qr code image based on total amount
@app.route('/qr_payment', methods=['GET', 'POST'])
@login_required
def qr_payment():
    cart = session.get('cart', [])
    products = []
    total = 0
    for id in cart:
        product = Product.query.get(id)
        total += product.price
        products.append(product)
    print("lent of products in cart is %s"%len(products))
    return render_template('qr_payment.html', products=products, total=total)

#write a method to fetch current logged in user details

@app.route('/get_user_details', methods=['GET'])
def get_user_details():
    # check user_id exist in session else return status unsuccessful
    user_id = session.get('_user_id')
    print(session.items())
    print("printing user details")
    print(user_id)
    if not user_id:
        return jsonify({'status': 'unsuccessful'})
    user = User.query.get(user_id)
    return jsonify({'name': user.username, 'email': user.email, 'status':'success'})  
#create a method to remove a product from cart
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart.remove(product_id)
    session['cart'] = cart
    return redirect(url_for('show_cart'))

#create a method to remove a product from products
@app.route('/remove_product/<int:product_id>', methods=['GET'])
@login_required
def remove_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('adminpage'))

#create a function to send otp based on email

@app.route('/send_otp/<string:mail>', methods=['GET'])
def send_otp(mail):
    otp = random.randint(100000, 999999)
    msg = Message('OTP for registration', sender='XXXXXXXXXXXXXXXXXXX', recipients=[mail])
    msg.body = 'Your OTP is ' + str(otp)
    mail.send(msg)
    return jsonify({'otp':otp})
# /verifyEmail

@app.route('/verifyEmail', methods=['GET', 'POST'])
def verifyEmail():
    form = ForgetPasswordForm()
    if request.method == 'GET':
        email = request.args.get('email')
        if check_email(email):
            otp = generate_otp()
            send_otp_sms(email, otp)
            # Store the user and OTP for verification
            session['otp_user'] = email
            session['otp_code'] = otp
            print("before post "+otp)
        else:
            flash('Email does not exist.', 'error')
            return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session.get('otp_user')   
        otp_code = session.get('otp_code')
        print("otp email 1- "+otp_code)
        if form.otp.data == otp_code:
            flash('reset password here', 'success')
            session.pop('otp_code', None)
            return redirect(url_for('resetpassword')) 
        else:
            print("not valid otp")
            flash('Invalid OTP. Please try again.', 'error')
    else:
        print("invalid form")
    
    return render_template('forgotpassword.html', title='email Verification', form=form, email=session.get('otp_user'))
#create a function to reset password
@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print("otp email 2- "+session.get('otp_user'))
        user = User.query.filter_by(email= session.get('otp_user')).first()        
        user.set_password(form.password.data)
        db.session.commit()
        flash('password reset successful!', 'success')
        session.pop('otp_user', None)
        session.pop('otp_code', None)
        return redirect(url_for('login'))
    return render_template('resetpassword.html', title='Reset Password', form=form)
#create a method to check email exists or not 
def check_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return True
    else:
        return False    
#create a method to change password and add a condition to check existing password

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('showProfile'))
        else:
            flash('Old password is incorrect.', 'error')
    return render_template('changepassword.html', title='Change Password', form=form)
    
#create a method to show profile

@app.route('/showProfile', methods=['GET', 'POST'])
@login_required
def showProfile():
    form = ProfileForm()
    print("from Post showprofile")
    if request.method == 'POST':
        print("from validated, showprofile")
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data 
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('showProfile'))
    elif request.method == 'GET':
        print("from get showprofile")
        user = User.query.filter_by(username=current_user.username).first()
    return render_template('user_profile.html', title='Profile', form=form,user=current_user)
