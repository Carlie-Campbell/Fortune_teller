from flask import Flask, render_template, request, redirect,session
from flask_app.models.user_model import User
from flask_app.models.fortune_model import Fortune
from flask_app import app


@app.route('/dashboard')
def dashboard():
    # ----validator ----------
    if 'user_id' not in session:
        return redirect('/')
    # --creates dictionary to pass into User.get-by-id-------
    data = {
        'id': session['user_id']
    }
    # -------Specifies logged user and all recipes-----
    logged_user = User.get_by_id(data)
    all_fortunes = Fortune.get_all_fortunes()
    # -------Renders dashb temp and passes logged_user/all_recipes info
    return render_template('dashboard.html', logged_user=logged_user, all_fortunes=all_fortunes)


@app.route('/create/fortune', methods=['POST'])
def post_fortune():
    # ---validates if recipe meets criteria----
    if Fortune.validator(request.form):
        session['in'] = Fortune.fortune_response()
        if 'user_id' in session:
        # ---saves recipe then redirects to dashb-----
            Fortune.save({**request.form, 'user_id': session['user_id']})
        return redirect('/')
    # ----If does not meet criteria, will flash and redirect to fix recipe---
    return redirect('/')
