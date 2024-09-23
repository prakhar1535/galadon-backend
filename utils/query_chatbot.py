from flask import Blueprint, request, jsonify
from db.db import supabase
from openai import AsyncOpenAI
import os
import json
import asyncio

api_key = os.getenv("OPENAI_API_KEY")
aclient = AsyncOpenAI(api_key=api_key)

query_assistant_bp = Blueprint('query_assistant_bp', __name__)

async def get_session(chatbot_id):
    response = supabase.table('chatbots').select('*').eq('chatbotId', chatbot_id).execute()

    if not response.data:
        return None
    session_data = response.data[0]
    print(f"Model: {session_data.get('model', 'Not found')}")
    return session_data

async def get_ai_response(message, chatbot_id):
    session_data = await get_session(chatbot_id)
    
    if not session_data:
        raise Exception(f"Session not found for chatbot ID: {chatbot_id}")
    
    model = session_data.get("model", "gpt-3.5-turbo") 
    
    response = await aclient.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a lead generation chatbot.  Pretend you are a potential customer with no information on COMPANY - ask me 5 common questions that they would ask. Starting with the most common. And then answer each question based on your knowledgebase"},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content

async def answer_query(query, system_prompt, chatbot_id, knowledge_base):
    if knowledge_base:
        kb_info = "\n".join([f"{key}: {data['title']} (Type: {data['type']})" for key, data in knowledge_base.items()])
        prompt = f"""
        Basic Prompt: {system_prompt}

        Given the following knowledge base information and tells who are you what are you supposed to do:
        {kb_info}

        Please answer the user's query using the knowledge base. For links, include the URL if relevant. For file content, use the information provided in the content field.

        User query: {query}

        If you don't have enough information to answer the query, please say so and offer to help with something else. Include the most relevant link or mention that there's additional file content available, if applicable.
        """
    else:
        prompt = f"""
        Basic Prompt: {system_prompt}

        Please answer the user's query to the best of your ability. If you don't have enough information to answer the query, please say so and offer to help with something else.

        User query: {query}
        """
    
    response = await get_ai_response(prompt, chatbot_id)
    return response

async def fetch_knowledge_base(chatbot_id):
    knowledge_base = {}
    try:
        response = await get_all_links(chatbot_id)
        if isinstance(response, dict) and 'data' in response:
            for item in response['data']:
                main_url = item.get('url')
                main_title = item.get('title')
                if main_url:
                    knowledge_base[main_url] = {'title': main_title, 'content': '', 'type': 'main_link'}

                links = item.get('links', [])
                if isinstance(links, str):
                    try:
                        links = json.loads(links)
                    except json.JSONDecodeError:
                        print(f"Error decoding links JSON for {main_url}")
                        links = []

                for link in links:
                    if isinstance(link, dict):
                        link_url = link.get('url')
                        link_title = link.get('title')
                        if link_url:
                            knowledge_base[link_url] = {'title': link_title, 'content': '', 'type': 'sub_link'}

            print(f"Successfully fetched knowledge base for chatbot ID: {chatbot_id}")
            print(f"Total knowledge base entries: {len(knowledge_base)}")
        elif isinstance(response, dict) and response.get('status') == 404:
            print(f"No additional link data found for chatbot ID: {chatbot_id}. Proceeding with basic information.")
        else:
            print(f"Unexpected format for response: {response}")

    except Exception as e:
        print(f"Error fetching knowledge base: {str(e)}")

    if not knowledge_base:
        print("No additional knowledge base available. The chatbot will operate with basic information.")

    return knowledge_base

async def get_all_links(chatbot_id):
    try:
        response = supabase.table('chatbot_scraped_content').select('url', 'title', 'links').eq('chatbot_id', chatbot_id).execute()

        if response.data:
            return {
                'message': 'Data retrieved successfully',
                'status': 200,
                'data': response.data
            }
        else:
            return {
                'message': 'No data found for the given chatbot ID',
                'status': 404
            }

    except Exception as e:
        return {
            'message': f'Error retrieving data: {str(e)}',
            'status': 500
        }

@query_assistant_bp.route('/query-assistant', methods=['POST'])
def query_assistant():
    data = request.json
    chatbot_id = data.get('chatbotId')
    message = data.get('message')
    question_prompt = data.get('questionPrompt')

    if not chatbot_id or not message:
        return jsonify({'message': 'Chatbot ID and message are required', 'status': 400}), 400

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        knowledge_base = loop.run_until_complete(fetch_knowledge_base(chatbot_id))
        if question_prompt:
            system_prompt = f"""You are a helpful assistant for a lead generation chatbot.  Pretend you are a potential customer with no information on COMPANY - ask me 5 common questions that they would ask. Starting with the most common. And then answer each question based on your knowledgebase for this question : {question_prompt}"""
        else:
            system_prompt = knowledge_base
        
        response = loop.run_until_complete(answer_query(message, system_prompt, chatbot_id, knowledge_base))

        return jsonify({
            'message': 'Response generated successfully',
            'status': 200,
            'data': response
        }), 200

    except Exception as e:
        return jsonify({'message': f'Error processing request: {str(e)}', 'status': 500}), 500