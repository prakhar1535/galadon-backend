from flask import Blueprint
from routes.generateChatbot import ChatbotRoutes
from routes.create_user import createUser
from routes.get_session import getSessions
from routes.test import test
from routes.add_chat import AddChat
from routes.get_chat import GetChat
from routes.add_link_scrape import Scrap
from routes.lead_routes import LeadRoutes
from routes.addClient import  ClientRoutes
from routes.addCredits import CreditsRoutes
from routes.file_upload import FileUploadRoutes
from routes.getCredits import GetCreditsRoutes
from utils.query_chatbot import query_assistant_bp
from routes.get_script import GetChatbotScript
def register_apps(app):
    app.register_blueprint(test.testRoute)
    app.register_blueprint(ChatbotRoutes.chatbot_bp)
    app.register_blueprint(createUser.user_bp)
    app.register_blueprint(getSessions.getSessions)
    app.register_blueprint(AddChat.chat_bp)
    app.register_blueprint(GetChat.get_chat_bp)
    app.register_blueprint(Scrap.scrape_bp)
    app.register_blueprint(LeadRoutes.lead_bp) 
    app.register_blueprint(ClientRoutes.client_bp) 
    app.register_blueprint(CreditsRoutes.credits_bp)
    app.register_blueprint(FileUploadRoutes.file_upload_bp)
    app.register_blueprint(GetCreditsRoutes.get_credits_bp)
    app.register_blueprint(query_assistant_bp)
    app.register_blueprint(GetChatbotScript.getChatbotScript)