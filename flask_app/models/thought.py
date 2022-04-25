from flask_app.models.user import User
from flask_app.models.like import Like
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# Create new class
class Thought:
    db="thought"
    def __init__(self,data) -> None:
        self.id=data['id']
        self.content=data['content']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.register_id=data['register_id']
        self.user=None
        self.users_who_liked=[]

    @classmethod
    def save(cls,data):
        query="INSERT INTO thought(content,register_id)VALUES(%(content)s,%(register_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query="SELECT * FROM thought "\
                "LEFT JOIN register ON register.id = thought.register_id "\
                "LEFT JOIN likes ON thought.id = likes.thought_id "\
                "LEFT JOIN register AS register2 ON register2.id = likes.register_id "\
                "ORDER BY thought.created_at DESC"
        results=connectToMySQL(cls.db).query_db(query)
        thoughts=[]

        for result in results:
            new_post = True
            like_user_data = {
                "id" : result["register2.id"],
                "first_name": result["register2.first_name"],
                "last_name": result["register2.last_name"],
                "email": result["register2.email"],
                "password": result["register2.password"],
                "created_at": result["register2.created_at"],
                "updated_at": result["register2.updated_at"]
            }
        
        #If curr row is still for last processed post, there are more users_who_liked the post
            if len(thoughts) >0 and thoughts[len(thoughts) -1].id == result['id']:
                thoughts[len(thoughts)-1].users_who_liked.append(User(like_user_data))
                new_post = False

            if new_post:
                thought=cls(result)
                print(thought)
                user_data = {
                    'id': result['register.id'],
                    'first_name': result['first_name'],
                    'last_name': result['last_name'],
                    'email':result['email'],
                    'password':result['password'],
                    'created_at': result['register.created_at'],
                    'updated_at': result['register.updated_at']
                }
                thought.user=User(user_data)
                print(thought.user)
                if result['register2.id'] is not None:
                    thought.users_who_liked.append(User(like_user_data))
                thoughts.append(thought)
        return thoughts

    @classmethod
    def get_userthought(cls,data):
        query="SELECT * FROM thought where register_id=%(id)s;"
        result=connectToMySQL(cls.db).query_db(query,data)
        thoughts=[]
        for row in result:
            thought=cls(row)
            thought.likers=Like.user_name({"id":row["id"]})
            thoughts.append(thought)
        return thoughts

    @classmethod
    def get_like(cls,data):
        query="SELECT * FROM thought join likes on thought.id=likes.thought_id where thought.id=%(id)s;"
        result=connectToMySQL(cls.db).query_db(query,data)
        thoughts=cls(result[0])
        thoughts.likers=Like.user_name({"id":result[0]["thought_id"]})
        return thoughts

    @classmethod
    def count(cls,data):
        query="SELECT * FROM thought where register_id=%(id)s;"
        result=connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query="DELETE  FROM thought where id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def thought_valid(thought):
        is_valid=True
        if len(thought['content'])<5:
            flash("Invalid ,less than 5 characters","add_thought")
            is_valid=False
        return is_valid

            