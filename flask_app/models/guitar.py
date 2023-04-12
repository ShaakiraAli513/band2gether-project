from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Band:
    DB = "rockband"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.city = data['city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.rockstar = None


    @classmethod
    def create_band(cls, data):
        query = """
        INSERT INTO bands (name, genre, city, user_id) 
        VALUES (%(name)s, %(genre)s, %(city)s, %(user_id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("CREATE BAND QUERY-->", results)
        return results


    @classmethod
    def user_bands(cls, data):
        #get bands with one user
        query = """
                SELECT * FROM bands 
                JOIN users 
                ON users.id = bands.user_id
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("GET ONLY USERS BANDS QUERY--->", results)
        community_bands = []
        
        for one_band in results:
            rocking_out = cls(one_band)
            rocker_data ={
                "id" : one_band['users.id'],
                "first_name" : one_band['first_name'],
                "last_name" :one_band['last_name'],
                "email" : one_band['email'],
                "password" : one_band['password'],
                "created_at" : one_band['created_at'],
                "updated_at" : one_band['updated_at']
            }
            user_obj = user.User(rocker_data)
            rocking_out.rockstar = user_obj
            community_bands.append(rocking_out)
        return community_bands


    @classmethod
    def get_one_band(cls, data):
        # get one tree
        query = "SELECT * FROM bands WHERE id= %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("GET_BAND QUERY -->", results)
        return cls(results[0])


    @classmethod
    def update_band(cls, data):
        
        query = """
        UPDATE bands SET name=%(name)s, genre =  %(genre)s, city = %(city)s WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        print("UPDATE BAND QUERY--->",results)
        return results


    @classmethod
    def delete_band(cls, data):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("DELETED BAND QUERY--->", results)
        return results


    @classmethod
    def band_community(cls):
        #get bands from everyone
        query = """
                SELECT * FROM bands 
                JOIN users 
                ON users.id = bands.user_id;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        print("GET ALL BANDS QUERY--->", results)
        community_rockers = []
        
        for a_band in results:
            rock_on = cls(a_band)
            hugger_data ={
                "id" : a_band['users.id'],
                "first_name" : a_band['first_name'],
                "last_name" :a_band['last_name'],
                "email" : a_band['email'],
                "password" : a_band['password'],
                "created_at" : a_band['created_at'],
                "updated_at" : a_band['updated_at']
            }
            user_obj = user.User(hugger_data)
            rock_on.rockstar = user_obj
            community_rockers.append(rock_on)
        return community_rockers


    @staticmethod
    def validate_band(new_band):
        is_valid = True
        if len(new_band['add_name']) < 2:
            flash("Band Name is too short.")
            is_valid = False
        if len(new_band['add_genre']) < 2:
            flash("Genre is too short.")
            is_valid = False
        if len(new_band['add_city']) < 1:
            flash("city is too short.")
            is_valid = False
        return is_valid