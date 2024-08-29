from flask import Blueprint
from routes.generateChatbot import generateChatbot
from routes.create_user import createUser
from routes.get_session import getSessions
def register_apps(app):
       app.register_blueprint(generateChatbot.chatbot)
       app.register_blueprint(createUser.user_bp)
       app.register_blueprint(getSessions.getSessions)