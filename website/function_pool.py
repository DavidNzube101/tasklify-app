from .db import dbORM
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
import base64
import imghdr
import datetime as dt
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from . import DateToolKit as dtk
import math as Math
import random
from . import id_generator
from . import encrypt



def getAppThemeData():
	AppTheme = dbORM.get_all("User")[f'{current_user.id}']['user_theme'],
	AppThemeOpposite = getOppositeTheme(dbORM.get_all("User")[f'{current_user.id}']['user_theme']),


	dark_app_theme = {
		"Main Background": "#0c1d2f",
		"Main Text": "antiquewhite",
		"Button Background": "#76b3e6",
		"Button Text": "white"
	}

	light_app_theme = {
		"Main Background": "ghostwhite",
		"Main Text": "black",
		"Button Background": "#2a69b3",
		"Button Text": "white"
	}

	# print(type(AppTheme))

	if AppTheme[0] == "light":
		app_theme = light_app_theme
	else:
		app_theme = dark_app_theme

	return app_theme

def encode_image(file_storage):
    image_data = file_storage.read()
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    return encoded_string

def calcTimeDifference(dpt, ct):
	return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]

def getDBItem(model, column, value):
	
	try:
		i = dbORM.get_all(model)[f'{dbORM.find_one(model, column, value)}']
	except Exception as e:
		i = {}

	return i

def loopAppendAndReverse(a, b):
	try:
		for k, v in a.items():
			b.append(v)
		return b[::-1]
	except Exception as e:
		return f"Error occured\nError: {e}"

def toJoin(i, j):
	return f"{i}{j}"

def thousandify(amount):
	amount = "{:,}".format(float(amount))
	return f"{amount}"

def referral_data():
	refs = 0 if (dbORM.get_all("UserTLFY")[f'{current_user.id}']['referral_count']) == "NULL" else (dbORM.get_all("UserTLFY")[f'{current_user.id}']['referral_count'])
	earnings = float(refs) * 1000
	return [f"{refs}", earnings]

def is_test():
	return "True"

def floatToInt(n):
	return f"{Math.ceil(float(n))}"

def getDateTime():
	# Getting Date-Time Info
	current_date = dt.date.today()
	current_time = datetime.now().strftime("%H:%M:%S")

	# Date Format: "YYYY-MM-DD"
	formatted_date = current_date.strftime("%Y-%m-%d")
	date = formatted_date
	time = current_time

	return [date, time]


def HTMLBreak(n):
	breaks = ""

	for x in range(int(n)):
		breaks = breaks + "\n<br>"	

	return breaks

def getOppositeTheme(theme):
	if theme == 'light':
		return 'dark'
	else:
		return 'light'

def oppositeCurrency(currency):
	return "NGN" if currency == "$" else "NGN"

def CurrencyExchange():
	v1 = float(f"0.{dtk.split_date(getDateTime()[0])['Day']}") # initial float
	v2 = float(f"0.{dtk.split_date(getDateTime()[0])['Month']}") # error margin

	return round(v1 * v2, 2)

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else ''