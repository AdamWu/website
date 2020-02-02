from flask import Blueprint

main = Blueprint("main", __name__) #"main" 为这个蓝图的名字

from . import views