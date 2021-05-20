from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request
import SafeZone.functions as Function
from flask_login import login_user, login_required, logout_user, current_user

admin_blueprint = Blueprint('admin',
                              __name__,
                              template_folder='templates/')

@admin_blueprint.route('/')
@login_required
def admin():
    data = Function.get_data()
    return render_template('admin.html',
                           admin_reader_list=data[0][0],
                           clients=data[0][1])

@admin_blueprint.route('/map/')
@login_required
def map():
    data = Function.get_data()
    return render_template('map.html',
                           admin_reader_list=data[0][0],
                           clients=data[0][1])