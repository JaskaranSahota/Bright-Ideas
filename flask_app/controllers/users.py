from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_bcrypt import Bcrypt   
from flask_app.models.user import User   
bcrypt = Bcrypt(app)   
@app.route('/')
def home():
    return render_template("user.html")

@app.route('/register',methods=["POST"])
def register():
        if User.register_valid(request.form):
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            data= {
                "first_name":request.form['first_name'],
                'last_name':request.form['last_name'],
                'email':request.form['email'],
                'password':pw_hash,
                'password2':pw_hash
            }
            user_id=User.save(data)
            flash("Welcome, You are registered now","register successful")
            return redirect('/')
        else:
            flash("You are not Regsitered","register")
            return redirect('/')

@app.route('/login',methods=["POST"])
def login():
        data = { "email" : request.form["email"] }
        user_in_db = User.get_email(data)
        # user is not registered in the db
        if not user_in_db:
            flash("Invalid Email","login")
            return redirect("/")
        if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            # if we get False after checking the password
            flash("Invalid Password","login")
            return redirect('/')
        # if the passwords matched, we set the user_id into session
        session['user_id'] = user_in_db.id
        # never render on a post!!!
        return redirect('/wall')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
