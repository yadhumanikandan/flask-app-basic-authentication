from flask import Blueprint, render_template

admin = Blueprint("admin", __name__)



@admin.route("/")
@admin.route("/home")
def admin_home():
    return "admin"