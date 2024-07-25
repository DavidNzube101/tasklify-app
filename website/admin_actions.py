from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user


import base64
import imghdr
import random
from datetime import datetime, timedelta
import datetime as dt

from . import DateToolKit as dtk
from .db import db
from .db import dbORM
from . import encrypt
from . import ScreenGoRoute
from . import function_pool
from . import id_generator

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("User"), None


today = dt.datetime.now().date()


admin_actions = Blueprint('admin_actions', __name__)
aa = admin_actions

@aa.route("/create-task", methods=['POST'])
@login_required
def createTask():

    if dbORM.get_all("UserTLFY")[f"{current_user.id}"]['user_type'] == "admin" :
        image = request.files['task_image']

        if image:
            filename = str(secure_filename(image.filename))
            task_temp_id = id_generator.generateTID()

            task_data = {
                "name": request.form['task_name'],
                "task_link": request.form['task_link'],
                "task_type": request.form['task_type'],
                "points": f"{request.form['task_points']}",
                "description": request.form['description'],
                "image_name": f"{filename}",
                "image_raw": f"{task_temp_id}",
                "datestamp": f"{function_pool.getDateTime()[0]}",
                "users_id": "[]",
                "timestamp": f"{function_pool.getDateTime()[1]}",
                "users_id_done": "[]",
                "expiry_date": f"{dt.date.today() + timedelta(days=int(random.choice(['4', '5', '6', '3', '2', '1'])))}"
            }

            dbORM.add_entry("TaskTLFY", encrypt.encrypter(str(task_data)))
            dbORM.update_entry(
                "TaskTLFY", 
                f"{dbORM.find_one('TaskTLFY', 'image_raw', str(task_temp_id))}", 
                str(
                    {
                        "image_raw": f"{function_pool.encode_image(image)}"
                    }
                ), 
                dnd=True
            )

        else:
            filename = "Default_TT_logo.png"

            task_data = {
                "name": request.form['task_name'],
                "task_link": request.form['task_link'],
                "task_type": request.form['task_type'],
                "points": f"{request.form['task_points']}",
                "description": request.form['description'],
                "image_name": filename,
                "image_raw": "Default-Logo",
                "datestamp": f"{function_pool.getDateTime()[0]}",
                "users_id": "[]",
                "timestamp": f"{function_pool.getDateTime()[1]}",
                "users_id_done": "[]",
                "expiry_date": f"{dt.date.today() + timedelta(days=int(random.choice(['4', '5', '6', '3', '2', '1'])))}"
            }

            dbORM.add_entry("TaskTLFY", encrypt.encrypter(str(task_data)))
        
    
    return ScreenGoRoute.go_to("1", _redirect=True)

@aa.route("/sign-withdrwal", methods=['POST'])
@login_required
def sign_statement():
    withdrawal_id = request.form['withdrawal_id']
    theWithdrawal = dbORM.get_all("WithdrawTLFY")[f'{withdrawal_id}']
    statement = request.form['sign_statement']

    dbORM.update_entry(
        "WithdrawTLFY", 
        f"{dbORM.find_one('WithdrawTLFY', 'id', withdrawal_id)}", 
        encrypt.encrypter(str(
            {
                "status": statement
            }
        )), 
        dnd=False
    )

    if statement == "failed":
        theUser = dbORM.get_all("UserTLFY")[f"{dbORM.find_one('UserTLFY', 'user_id', theWithdrawal['user_wallet_address'])}"]
        dbORM.update_entry(
            "UserTLFY", 
            f"{dbORM.find_one('UserTLFY', 'user_id', theWithdrawal['user_wallet_address'])}", 
            encrypt.encrypter(str(
                {
                    "wallet_balance": f"{float(theUser['wallet_balance']) + (float(theWithdrawal['amount']) / float(function_pool.CurrencyExchange()))}"
                }
            )), 
            dnd=False
        )

    return ScreenGoRoute.go_to("1", _redirect=True)