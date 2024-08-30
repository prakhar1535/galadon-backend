from flask import Blueprint, request, jsonify, render_template_string
class test:
    testRoute = Blueprint('test', __name__)

    @testRoute.route('/', methods=['GET'])
    def home():
      return render_template_string('<h1>Welcome to Galadon</h1>')