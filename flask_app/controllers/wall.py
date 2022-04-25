from tkinter import N
from flask_app.models.like import Like
from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.thought import Thought
from flask_app.models.like import Like
@app.route('/wall')
def wall():
    if 'user_id' in session:
        data={
            'id':session['user_id']
        } 
    thoughts = Thought.get_all()
    thoughts_user_liked = Like.get_all_user_liked_posts(data)
    return render_template("wall.html",user=User.get_user(data),thoughts=thoughts,thoughts_user_liked=thoughts_user_liked)

@app.route('/add_thought',methods=["POST"])
def new_thought():   
    if Thought.thought_valid(request.form):
        data={
            'content':request.form['content'],
            'register_id':session['user_id']
        }
        thought=Thought.save(data)
        flash("New Thought Added","add_successful")
        return redirect ('/wall')
    else:
        return redirect ('/wall')

@app.route('/user_post/<int:id>/')
def all_thoughts(id):
    data={
        'id':id
    }
   
    if 'user_id' in session:
        session_user_data={
            'id':session['user_id']
        } 
    thoughts=Thought.get_userthought(data)
    user_thought=User.get_user(data)
    return render_template("all_thoughts.html",user=User.get_user(session_user_data),thoughts=thoughts,user_thought=user_thought)

@app.route('/userinfo/<int:id>')
def user_info(id):
    data={
        'id':id
    }
    if 'user_id' in session:
        session_user_data={
            'id':session['user_id']
        } 
    posts=Like.number_ofposts(data)
    info=User.get_user(data)
    totallikes=Like.totallikes(data)
    return render_template("user_info.html",info=info,user=User.get_user(session_user_data),posts=posts,totallikes=totallikes)


@app.route('/like/<int:id>')
def like(id):
    data={
        'thought_id':id,
        'register_id':session['user_id']
    }
    like=Like.save(data)
    return redirect('/wall')

@app.route('/unlike/<int:id>')
def unlike(id):
    data={
        'thought_id':id,
        'register_id':session['user_id']
    }
    like=Like.destroy(data)
    return redirect('/wall')

@app.route('/delete/<int:id>')
def destroy(id):
    data={
        'id':id
    }
    Thought.destroy(data)
    return redirect('/wall')