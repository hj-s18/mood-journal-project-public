from flask import render_template, request, redirect, url_for

def user_join_service():
    if request.method == 'GET':
        return render_template('/user/join.html')