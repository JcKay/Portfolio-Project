# IMPORT BLOCKs
# FLASK AND SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
# AUTHENTICATION
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
# OTHER
import secrets
import os
from random import choice
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from functools import wraps

# FLASK INIT
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# python decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if not current_user.user_admin:
            return render_template('admin-dashboard.html', auth_req=True)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# APIs DOCUMENTATION
api_documentation = "https://documenter.getpostman.com/view/21057768/UzBgvVeg"

# CONTACT
context = ssl.create_default_context()
gmail = os.getenv('gmail')
passcode = os.getenv('passcode')


# CREATE DATABASE
## USER DATABASE
class User(UserMixin, db.Model):
    __tablename__ = "user_api_db"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_api = db.Column(db.String(100))
    user_admin = db.Column(db.Boolean)

    # relationship with cafe-database
    cafes_rel = relationship("Cafe", back_populates="user")


## CAFE DATABASE
class Cafe(db.Model):
    __tablename__ = 'cafes_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    township = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    wifi = db.Column(db.String(100), nullable=False)
    sockets = db.Column(db.String(100), nullable=False)
    can_take_calls = db.Column(db.String(100), nullable=False)
    restroom = db.Column(db.String(100), nullable=False)
    cards = db.Column(db.String(100), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # relationship with user-database
    user_id = db.Column(db.Integer, db.ForeignKey("user_api_db.id"))
    user = relationship("User", back_populates="cafes_rel")

    # For APIs
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


db.create_all()


# ROUTE MAPS
@app.route('/')
def home():
    return render_template('index.html')


########     ########  AUTHENTICATION START  ########    ############
##                  REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    # IF POST
    if request.method == 'POST':
        # CHECK 2 PASSWORD
        if request.form['password'] == request.form['repeat_password']:
            # MAKE PASSWORD TO HASHED_PASSWORD
            hashed_password = generate_password_hash(
                request.form['password'],
                method="pbkdf2:sha256",
                salt_length=8
            )
            # MAKE NEW USER
            new_user = User(
                name=request.form['name'],
                username=request.form['username'],
                email=request.form['email'],
                password=hashed_password,
                user_api=secrets.token_hex(16),
                user_admin=False
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('user_profile', username=new_user.username))
        return redirect(url_for('register'))
    return render_template('register.html')


##                  LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        take_email = request.form['email']
        user = User.query.filter_by(email=take_email).first()

        # IF THERE IS NO USER
        if not user:
            flash('Email does not exist, try again!')
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, request.form['password']):
            flash('Incorrect Password, Try Again')
            return redirect(url_for('login'))

        else:
            login_user(user)
            return redirect(url_for('user_profile', username=user.username))

    return render_template('login.html')


##                  LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


########             AUTHENTICATION END        ############

########     ########  CAFE ROUTE START  ########    ############
@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.all()
    return render_template('cafes-table.html', cafes=all_cafes)


@app.route('/random-cafe')
def get_random():
    all_cafes = Cafe.query.all()
    one_cafe = choice(all_cafes)
    return render_template('random-cafe.html', cafe=one_cafe)


@app.route('/township-search', methods=['GET', 'POST'])
def tsp_search():
    tsp = request.form['csearch'].title()
    all_cafes = Cafe.query.filter_by(township=tsp).all()
    return render_template('cafes-table.html', cafes=all_cafes)


@app.route('/cities')
def cities():
    return render_template('get_all_cities.html')


@app.route('/cities/<city_name>')
def get_city(city_name):
    cafes = Cafe.query.filter_by(city=city_name).all()
    return render_template('cafes-table.html', cafes=cafes)


#       ADD CAFE
@app.route('/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    if not current_user.is_authenticated:
        flash('Login or Register to Suggest Cafe.')
        return redirect(url_for('get_login'))

    elif request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get('name'),
            map_url=request.form.get('map_url'),
            address=request.form.get('address'),
            township=request.form.get('township').title(),
            city=request.form.get('city').title(),
            seats=request.form.get('seats'),
            wifi=request.form.get('wifi'),
            sockets=request.form.get('sockets'),
            can_take_calls=request.form.get('can_take_calls'),
            restroom=request.form.get('restroom'),
            cards=request.form.get('cards'),
            coffee_price=request.form.get('coffee_price'),
            user=current_user
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add_cafe.html')


#       EDIT CAFE
@app.route('/edit-cafe/<int:cafe_id>', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if not current_user.is_authenticated:
        flash('Login or Register to Edit Cafe.')
        return redirect(url_for('get_login'))

    elif current_user.user_admin or current_user.id == cafe.user_id:
        cafe.name = request.form['name']
        cafe.map_url = request.form['map_url']
        cafe.address = request.form['address']
        cafe.township = request.form['township'].title()
        cafe.city = request.form['city'].title()
        cafe.seats = request.form['seats']
        cafe.wifi = request.form['wifi']
        cafe.sockets = request.form['sockets']
        cafe.can_take_calls = request.form['can_take_calls']
        cafe.restroom = request.form['restroom']
        cafe.cards = request.form['cards']
        cafe.coffee_price = request.form['coffee_price']
        db.session.commit()
        return redirect(url_for("cafes"))

    elif not current_user.id == cafe.user_id:
        return render_template('edit_cafe.html', auth_req=True), 403

    return render_template('edit_cafe.html', data=cafe)


#       CONTACT ME
@app.route('/contactme', methods=['GET', 'POST'])
def contactme():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        detail = request.form['body']
        flash('Send Successfully')

        # send email smtp module
        msg = MIMEMultipart()
        msg['Subject'] = f"{subject}"
        msg['From'] = gmail
        msg['To'] = gmail
        text = f"""
            Name: {name}
            Email: {email}
            About: {detail}
        """
        body_text = MIMEText(text, 'plain')
        msg.attach(body_text)

        # send mail
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo()  # check connection
                server.starttls(context=context)  # secure the connection
                server.ehlo()  # check connection
                server.login(user=gmail, password=passcode)
                server.sendmail(
                    gmail,
                    gmail,
                    msg.as_string()
                )

        except Exception as e:
            print(e)

        return redirect(url_for('contactme'))

    return render_template('contact.html')


########     ########  PROFILE ROUTE START  ########    ############
# # #           PROFILE ROUTE
@app.route('/profile/<username>')
@login_required
def user_profile(username):
    cafes = Cafe.query.filter_by(user_id=current_user.id).all()
    return render_template('user-profile.html', cafes=cafes, is_profile=True)


# # #           DELETE CAFE
@app.route('/delete-cafe/<int:cafe_id>')
def delete_cafe(cafe_id, username):
    cafe = Cafe.query.get(cafe_id)
    if not current_user.is_authenticated:
        flash('Login or Register to Delete Cafe.')
        return redirect(url_for('login'))

    elif current_user.user_admin or current_user.id == cafe.user_id:
        db.session.delete(cafe)
        db.session.commit()
        return redirect(url_for('user_detail', user_id=cafe.user_id) )

    else:
        return render_template('edit_cafe.html', no_delete=True)


# # #           ADMIN DASHBOARD
@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    users = User.query.all()
    if not current_user.user_admin:
        return render_template('admin-dashboard.html', auth_req=True)

    return render_template('admin-dashboard.html', users=users)


# # #           ADMIN ACCESS CAFEs
@app.route('/admin-dashboard/access-cafes')
@login_required
@admin_only
def admin_access_cafes():
    all_cafes = Cafe.query.all()
    return render_template("admin-access-cafes.html", cafes=all_cafes)


# # #           USER DETAIL
@app.route('/admin-dashboard/<user_id>')
@login_required
@admin_only
def user_detail(user_id):
    user = User.query.get(user_id)
    cafes = Cafe.query.filter_by(user_id=user_id).all()
    return render_template('user-detail.html', user=user, cafes=cafes)


# # #           DELETE USER
@app.route('/delete-user/<int:user_id>')
@admin_only
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


# # #           UPGRADE USER TO ADMIN ROLE
@app.route('/upgrade-user/<int:user_id>')
@admin_only
def upgrade_user(user_id):
    user = User.query.get(user_id)
    user.user_admin = True
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


# # #           DOWNGRADE USER TO ADMIN ROLE
@app.route('/downgrade-user/<int:user_id>')
@admin_only
def downgrade_user(user_id):
    user = User.query.get(user_id)
    user.user_admin = False
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


# # #           SEARCH USERNAME
@app.route('/admin-dashboard/')
@admin_only
def user_search():
    # get data from url
    search_name = request.args.get('Username').lower()
    # get all users from database
    users = User.query.all()
    # if search word are inside user.username , get that user
    filter_users = [user for user in users if search_name in user.username.lower()]
    # show that user
    return render_template('admin-dashboard.html', users=filter_users)


# # # PROFILE ROUTE END # # #


########     ########  PROFILE ROUTE END  ########    ############

########     ########  RESTful APIs START  ########    ############
@app.route('/api')
def get_api():
    return redirect(f'{api_documentation}')


@app.route('/api/cafes')
def _cafes():
    user = User.query.filter_by(user_api=request.args.get('api_key')).first()
    if user:
        cafes = Cafe.query.all()
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes]), 200
    else:
        return jsonify(error={"Forbidden": "Invalid API KEY."}), 403


@app.route('/api/random')
def _random():
    user = User.query.filter_by(user_api=request.args.get('api_key')).first()
    if user:
        cafes = Cafe.query.all()
        cafe = choice(cafes)
        return jsonify(cafe=cafe.to_dict()), 200
    else:
        return jsonify(error={"Forbidden": "Invalid API KEY."}), 403


@app.route('/api/city-search')
def city_search():
    user = User.query.filter_by(user_api=request.args.get('api_key')).first()
    if user:
        city = request.args.get('city').title()
        cafes = Cafe.query.filter_by(city=city).all()
        if cafes:
            return jsonify(cafe=[cafe.to_dict() for cafe in cafes]), 200
        else:
            return jsonify(error={"Not Found": f"Sorry no coffee shop in {city}"}), 404

    else:
        return jsonify(error={"Forbidden": "Invalid API KEY."}), 403


@app.route('/api/township-search')
def township_search():
    user = User.query.filter_by(user_api=request.args.get('api_key')).first()
    if user:
        township = request.args.get('township').title()
        cafes = Cafe.query.filter_by(township=township).all()
        if cafes:
            return jsonify(cafe=[cafe.to_dict() for cafe in cafes]), 200
        else:
            return jsonify(error={"Not Found": f"Sorry no coffee shop in {township}"}), 404

    else:
        return jsonify(error={"Forbidden": "Invalid API KEY."}), 403


@app.route('/api/add', methods=['POST'])
def _add():
    user = User.query.filter_by(user_api=request.args.get('api_key')).first()
    if user:
        print(user.name)
        new_cafe = Cafe(
            name=request.form.get('name'),
            map_url=request.form.get('map_url'),
            address=request.form.get('address'),
            township=request.form.get('township'),
            city=request.form.get('city'),
            seats=request.form.get('seats'),
            wifi=request.form.get('wifi'),
            sockets=request.form.get('sockets'),
            can_take_calls=request.form.get('can_take_calls'),
            restroom=request.form.get('restroom'),
            cards=request.form.get('cards'),
            coffee_price=request.form.get('coffee_price'),
            user=user,

        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new cafe."}), 200
    else:
        return jsonify(error={"Forbidden": "Invalid API KEY."}), 403


@app.route('/api/update-cafe/<cafe_id>', methods=['PATCH'])
def _update(cafe_id):
    user = User.query.filter_by(user_api=request.args.get('api_key')).first()
    cafe = Cafe.query.get(cafe_id)
    new_price = request.args.get('new_price')
    if user:
        if cafe:
            if user.id == cafe.user_id or user.user_admin:
                cafe.coffee_price = new_price
                db.session.commit()
                return jsonify({"Success": "Successfully updated the price."}), 200

            else:
                return jsonify(error={
                    "Not Found": "You can only edit cafe that you suggested."}), 403
        else:
            return jsonify(error={
                "Not Found": "Sorry a cafe with that id was not found in the database."
            }), 404
    else:
        return jsonify(error={"Forbidden": "Invalid API KEY."}), 403


@app.route('/api/delete/<cafe_id>', methods=['DELETE'])
def _delete(cafe_id):
    user = User.query.filter_by(user_api=request.args.get('api_key')).first()
    cafe = Cafe.query.get(cafe_id)
    if user:
        if cafe:
            # cafe's user_id equal user's id or user is admin
            if user.id == cafe.user_id or user.user_admin:
                db.session.delete(cafe)
                db.session.commit()
                return jsonify(response={"Success": "Successfully deleted the cafe from the database."}), 200

            # cafe id wasn't in db
            else:
                return jsonify(error={
                    "Not Found": "You can only delete cafe that you suggested."}), 403
        else:
            return jsonify(error={
                "Not Found": "Cafe with that id was not found in the database."
            }), 404
    # APIKEY not true:
    else:
        return jsonify(error={"Forbidden": "Invalid API KEY."}), 403


# # # APIs END # # #


if __name__ == '__main__':
    app.run(debug=True)
