from flask import Blueprint
from routes.generateChatbot import ChatbotRoutes
from routes.create_user import createUser
from routes.get_session import getSessions
from routes.test import test
from routes.add_chat import AddChat
from routes.get_chat import GetChat
from routes.add_link_scrape import Scrap
from routes.lead_routes import LeadRoutes 
def register_apps(app):
    app.register_blueprint(test.testRoute)
    app.register_blueprint(ChatbotRoutes.chatbot_bp)
    app.register_blueprint(createUser.user_bp)
    app.register_blueprint(getSessions.getSessions)
    app.register_blueprint(AddChat.chat_bp)
    app.register_blueprint(GetChat.get_chat_bp)
    app.register_blueprint(Scrap.scrape_bp)
    app.register_blueprint(LeadRoutes.lead_bp) 