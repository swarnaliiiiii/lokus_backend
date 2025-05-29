from flask import Flask, request, jsonify, Blueprint
from datetime import datetime

userinput_blueprint = Blueprint('userinput', __name__)
