"""Blogly application."""

from flask import *
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ redirects to the users page"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """ Shows the users page wich lists the users on it"""
    users = User.query.all()
    return render_template('users_page.html',users=users)

@app.route('/users/new',methods =['GET'])
def new_user_page():
    """ Shows the create user form """
    return render_template('create_user.html')


@app.route('/users/new',methods=['POST'])
def make_new_user():
    """ makes a new user from the form information then gose back to /users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_pic = request.form['pic']
    new_user = None

    if profile_pic:
        new_user = User(first_name=first_name,last_name=last_name,image_url=profile_pic)
    else:
        new_user = User(first_name=first_name,last_name=last_name)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/user/<int:user_id>')
def user_page(user_id):
    """ Shows the user whos id was passed in """
    current_user = User.query.get_or_404(user_id)

    return render_template('user.html',current_user=current_user)


@app.route('/user/<int:user_id>/edit',methods=['GET'])
def edit_user_page(user_id):
    """ Shows the edit user form """
    current_user = User.query.get_or_404(user_id)
    return render_template('edit_user.html',current_user=current_user)


@app.route('/user/<int:user_id>/edit',methods=['POST'])
def edit_user(user_id):
    """edits a user with the information from the form """
    current_user = User.query.get_or_404(user_id)

    current_user.first_name = request.form['first_name'] if request.form['first_name'] else current_user.first_name
    current_user.last_name = request.form['last_name'] if request.form['last_name'] else current_user.last_name
    current_user.image_url = request.form['pic'] if request.form['pic'] else current_user.image_url

    db.session.add(current_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Deletes a user based on user_id """

    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')
