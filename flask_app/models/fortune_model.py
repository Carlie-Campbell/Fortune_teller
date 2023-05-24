
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask_app import DATABASE
from flask import flash
import random
import time, sys

class Fortune:
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.f_response = data['f_response']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.asker_id = data['asker_id']
        self.creator = None
        # self.likes = likes_model.Likes.get_for_one_fortune({'id':id})
        # self.comments = comments_model.Comments.get_for_one_fortune({'id':id})

    @classmethod
    def save(cls, data):
        # makes insert into table with the *FIELDS listed ORDER IMPORTANT----
        query = """
        INSERT INTO fortunes(content, f_response, asker_id)
        # ---inserts data given by these field ids------
        VALUES (%(content)s,%(f_response)s,%(asker_id)s);"""
        # ---runs query through DB--------------
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    @classmethod
    def get_all_fortunes( cls):
        query = "SELECT * FROM fortunes LEFT JOIN users ON users.id = fortunes.user_id;"
        results = connectToMySQL(DATABASE).query_db( query )
        fortunes = []
        if results:
            for row_from_db in results:
                fortune = cls(row_from_db)
                user_data = {
                    ** row_from_db,
                    "id" : row_from_db["users.id"],
                    "created_at" : row_from_db["users.created_at"],
                    "updated_at" : row_from_db["users.updated_at"]
                }
                fortune.creator = user_model.User( user_data )
                fortunes.append( fortune )
        return fortunes
    
    @staticmethod
    def fortune_response():
        response = random.randint(0,20)
    
        if response == 1:
            f_response = ("MMMM, no, just, no")
        elif response == 2:
            f_response = ("Sure thing")
        elif response == 3:
            f_response = ("Don't count on it")
        elif response == 4:
            f_response = ("Definitely not")
        elif response == 5:
            f_response = ("Bet on it")
        elif response == 6:
            f_response = ("The Universe says perhaps")
        elif response == 7:
            f_response = ("I don't see why not")
        elif response == 8:
            f_response = ("The future looks good for you")
        elif response == 9:
            f_response = ("That's for sure")
        elif response == 10:
            f_response = ("Maybe")
        elif response == 11:
            f_response = ("There's a chance")
        elif response == 12:
            f_response = ("Certainly!")
        elif response == 13:
            f_response = ("Keep doing what you're doing and it'll happen")
        elif response == 14:
            f_response = ("Not ever")
        elif response == 15:
            f_response = ("No.")
        elif response == 16:
            f_response = ("Yes")
        elif response == 17:
            f_response = ("All depends on if you've been good for Santa this year")
        elif response == 18:
            f_response = ("Not in this lifetime")
        elif response == 19:
            f_response = ("Someday, but not today")
        elif response == 20:
            f_response = ("Right after you hit the lottery")
        else:
            f_response = ("Not a valid question!")
        return f_response
    
    @staticmethod
    def validator(data):
        is_valid = True
        if len(data['query']) < 3:
            is_valid = False
            flash('Query has to be larger than 3 characters','reg')
        return is_valid