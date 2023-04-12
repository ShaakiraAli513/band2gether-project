from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.guitar import Band
from flask_bcrypt import Bcrypt
from flask import flash


@app.route('/add-band', methods=["POST"])
def create_band():
    if "user_id" not in session:
        return ('/')
    print("Create Band--->", request.form)
    if not Band.validate_band(request.form):
        return redirect('/add-band')
    data = {
        "name" : request.form['add_name'],
        "genre" : request.form['add_genre'],
        "city" :request.form['add_city'],
        "user_id": session['user_id']
    }
    Band.create_band(data)
    return redirect ('/my-bands')


@app.route('/my-bands')
def get_my_bands():
    print("Get User Bands--->")
    if "user_id" not in session:
        return ('/')
    data = {
        "id": session['user_id']
    }
    return render_template("userdash.html", logged_in_user = User.get_id(data),  all_bands = Band.user_bands(data)
)


@app.route('/go_delete/<int:id>')
def delete_band(id):
    if "user_id" not in session:
        return ('/')
    data = {
        "id": id
    }
    Band.delete_band(data)
    return redirect('/my-bands')



@app.route('/go_edit/<int:band_id>')
def edit_band(band_id):
    if "user_id" not in session:
        return ('/')
    data = {
        "id": band_id
    }
    user_data = {
        "id": session["user_id"]
        }

    return render_template("editband.html",logged_in_user = User.get_id(user_data), this_band = Band.get_one_band(data))



@app.route('/update-band/<int:id>', methods=["POST"])
def update_band(id):
    if "user_id" not in session:
        return ('/')
    data = {
        "id" : request.form['id'],
        "name" : request.form['add_name'],
        "genre" : request.form['add_genre'],
        "city" :request.form['add_city'],
        "user_id": session['user_id']
    }

    print("Update Band--->", request.form)
    if not Band.validate_band(request.form):
        return redirect('/go_edit/<int:id>')
    Band.update_band(data)
    return redirect('/my-bands')
