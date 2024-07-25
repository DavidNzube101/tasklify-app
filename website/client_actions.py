from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user


from datetime import datetime
import base64
import random
import imghdr
import datetime as dt

from . import DateToolKit as dtk
from .db import db
from . import function_pool
from .db import dbORM
from . import encrypt
from . import ScreenGoRoute
from . import id_generator

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("UserTLFY"), None




client_actions = Blueprint('client_actions', __name__)
ca = client_actions

@ca.route("/task/<string:rad_id_two>/<string:tid>/<string:rad_id_one>")
@login_required
def vT(tid, rad_id_one, rad_id_two):
    theTask = dbORM.get_all("TaskTLFY")[f'{tid}']

    if str(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) == "0" or int(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) <= 0:
        dbORM.delete_entry("TaskTLFY", tid)

        return ScreenGoRoute.go_to("1", _redirect=True)
    else:
        return render_template("ViewTask.html", getMIME=function_pool.get_mime_type, CUser=User[f'{current_user.id}'], Task=theTask, DTK=dtk, Thousandify=function_pool.thousandify, TaskIsDone=0)
    
@ca.route("/dashboard/update-status")
def update_status():
    
    u = dbORM.get_all("UserTLFY")[f"{current_user.id}"]
    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
        encrypt.encrypter(str(
            {
                "referral_earning": f"1"
            }
        )), 
        dnd=False
    )

    return ScreenGoRoute.go_to("1", _redirect=True)

@ca.route("/task/<string:rad_id>/<string:task_id>")
@login_required
def viewTask(rad_id, task_id):
    # try:
    theTask = dbORM.get_all("TaskTLFY")[f'{task_id}']

    def is_done():
        pool = []
        for p in range(41):
            pool.append(p)

        return random.choice(pool)

    if int(current_user.id) in eval(theTask['users_id_done']):
        return ScreenGoRoute.go_to("1", _redirect=True)
    else:
        participating_users_id = eval(theTask['users_id'])
        if int(current_user.id) in participating_users_id:
            new_participating_users_id = participating_users_id
            new_participating_users_id.append(int(current_user.id))

            dbORM.update_entry(
                "TaskTLFY", 
                f"{dbORM.find_one('TaskTLFY', 'id', task_id)}", 
                encrypt.encrypter(str(
                    {
                        "users_id": f"{new_participating_users_id}"
                    }
                )), 
                dnd=False
            )

        return render_template("ViewTask.html", getMIME=function_pool.get_mime_type, CUser=User[f'{current_user.id}'], Task=theTask, DTK=dtk, Thousandify=function_pool.thousandify, TaskIsDone=is_done())
    # except Exception as e:
        
    #     return ScreenGoRoute.go_to("1", _redirect=True)

@ca.route("/withdrawTaskBalance/<string:task_id>/<string:rad_id>")
@login_required
def WithdrawTaskPoint(task_id, rad_id):

    theTask = dbORM.get_all("TaskTLFY")[f'{task_id}']

    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
        encrypt.encrypter(str(
            {
                "wallet_balance": f"{float(dbORM.get_all('UserTLFY')[current_user.id]['wallet_balance']) + float(theTask['points'])}"
            }
        )), 
        dnd=False
    )

    # participating_users_id = eval(theTask['users_id'])
    # if int(current_user.id) in participating_users_id:
    participating_users_id_done = eval(theTask['users_id_done'])
    participating_users_id_done.append(int(current_user.id))

    dbORM.update_entry(
        "TaskTLFY", 
        f"{dbORM.find_one('TaskTLFY', 'id', task_id)}", 
        encrypt.encrypter(str(
            {
                "users_id_done": f"{participating_users_id_done}"
            }
        )), 
        dnd=False
    )

    return ScreenGoRoute.go_to("1", _redirect=True)

@ca.route("/withdrawBalance", methods=['POST'])
@login_required
def withdrawBalance():
    _ = {
        'user_wallet_address': dbORM.get_all("UserTLFY")[f'{current_user.id}']["user_id"],
        'dob': dbORM.get_all("UserTLFY")[f'{current_user.id}']["dob"],
        'tid': f"{id_generator.generateTID()}-{id_generator.generateTID()}-{id_generator.generateTID()}",
        'username': dbORM.get_all("UserTLFY")[f'{current_user.id}']["username"],
        'user_first_name': dbORM.get_all("UserTLFY")[f'{current_user.id}']["first_name"],
        'user_last_name': dbORM.get_all("UserTLFY")[f'{current_user.id}']["last_name"],
        'timestamp': f"{function_pool.getDateTime()[1]}",
        'datestamp': f"{function_pool.getDateTime()[0]}",
        'status': "Pending",
        'amount': f"{round(float(request.form['amount']) * float(request.form['CEx']), 2)}",
        'bank': request.form['bank'],
        'account_number': request.form['account_number']
    }
    dbORM.add_entry("WithdrawTLFY", encrypt.encrypter(str(_)))

    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
        encrypt.encrypter(str(
            {
                "wallet_balance": f"{float(dbORM.get_all('UserTLFY')[current_user.id]['wallet_balance']) - float(request.form['amount'])}"
            }
        )), 
        dnd=False
    )

    return ScreenGoRoute.go_to("1", _redirect=True)

@ca.route("/send-points", methods=['POST'])
@login_required
def sendPoints():
    amount = request.form['amount']
    recipient_address = request.form['rec_wallet_address']

    try:
        theUser = dbORM.get_all("UserTLFY")[f"{dbORM.find_one('UserTLFY', 'user_id', recipient_address)}"]
        dbORM.update_entry(
            "UserTLFY", 
            f"{dbORM.find_one('UserTLFY', 'user_id', recipient_address)}", 
            encrypt.encrypter(str(
                {
                    "wallet_balance": f"{float(theUser['wallet_balance']) + float(amount)}"
                }
            )), 
            dnd=False
        )
        u = dbORM.get_all("UserTLFY")[f"{current_user.id}"]
        dbORM.update_entry(
            "UserTLFY", 
            f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
            encrypt.encrypter(str(
                {
                    "wallet_balance": f"{float(u['wallet_balance']) - float(amount)}"
                }
            )), 
            dnd=False
        )
    except:
        pass

    return ScreenGoRoute.go_to("1", _redirect=True)