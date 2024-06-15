import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db, admin
from functools import wraps
from app.main import bp
from app.models import Show, User



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET'])

def index():
    
    page = request.args.get('page', 1, type=int)
    shows = Show.query.paginate(
        page=page, per_page=5, error_out=False)
    next_url = url_for('main.index', page=shows.next_num) \
        if shows.has_next else None
    prev_url = url_for('main.index', page=shows.prev_num) \
        if shows.has_prev else None
    return render_template('index.html', title='Home', 
                           shows=shows.items, next_url=next_url,
                           prev_url=prev_url)