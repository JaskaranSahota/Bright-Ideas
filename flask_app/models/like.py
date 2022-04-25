import re
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL

# Create new class
class Like:
    db="thought"
    def __init__(self,data) -> None:
        self.id=data['id']
        self.register_id=data['register_id']
        self.thought_id=data['thought_id']
        
    @classmethod
    def save(cls,data):
        query="INSERT INTO likes(register_id,thought_id)VALUES(%(register_id)s,%(thought_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_user_liked_posts(cls, data):
        posts_liked = []
        query = "SELECT thought_id FROM likes JOIN register ON register.id=register_id WHERE register_id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        for result in results:
            posts_liked.append(result['thought_id'])
        return posts_liked

    @classmethod
    def count(cls,data):
        query="SELECT COUNT(id) as likes from likes where thought_id=%(thought_id)s;"
        result=connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def destroy(cls,data):
        query="Delete  from likes where thought_id=%(thought_id)s and register_id=%(register_id)s order by id desc limit 1;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    #new
    @classmethod
    def user_name(cls,data):
        user_liked=[]
        query="SELECT register.* FROM REGISTER JOIN likes on register.id=likes.register_id join thought on likes.thought_id=thought.id where thought_id=%(id)s;"
        results= connectToMySQL(cls.db).query_db(query,data)
        for result in results:
            user_liked.append(User(result))
        return user_liked

    @classmethod
    def number_ofposts(cls,data):
        total=[]
        query="SELECT COUNT(id) as posts from thought where register_id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        for result in results:
            total.append(result['posts'])
        return total
      

    @classmethod
    def totallikes(cls,data):
        total=[]
        query="select count(likes.id) as likes from likes join thought on likes.thought_id=thought.id left join register on thought.register_id=register.id where register.id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        for result in results:
            total.append(result['likes'])
        return total
    


    
        

 #SELECT first_name from register join likes on register.id =likes.register_id join thought where thought_id=6;