import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import uuid
from db.db import supabase

def deep_scrape(url, base_url, depth=1):
    if depth == 0:
        return None

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else ''
        content = extract_content(soup)
        content_length = len(content)
        
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if base_url in full_url:
                sub_content = deep_scrape(full_url, base_url, depth - 1)
                if sub_content:
                    links.append(sub_content)
        
        return {
            'url': url,
            'title': title,
            'content': content,
            'content_length': content_length,
            'links': links
        }
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def scrape_and_add_link(data):
    chatbot_id = data.get('chatbotId')
    url = data.get('url')
    
    if not chatbot_id or not url:
        return {'message': 'Chatbot ID and URL are required', 'status': 400}

    try:
        scraped_data = deep_scrape(url, url, depth=2)  # Adjust depth as needed
        
        if not scraped_data:
            return {'message': f'Failed to scrape {url}', 'status': 500}
        
        total_content_length = scraped_data['content_length'] + sum(link['content_length'] for link in scraped_data['links'])
        
        scrape_id = str(uuid.uuid4())
        
        insert_data = {
            'id': scrape_id,
            'chatbot_id': chatbot_id,
            'url': url,
            'title': scraped_data['title'],
            'content': scraped_data['content'],
            'content_length': total_content_length,
            'links': [{
                'url': link['url'],
                'title': link['title'],
                'content': link['content'],
                'content_length': link['content_length']
            } for link in scraped_data['links']]
        }
        
        insert_response = supabase.table('chatbot_scraped_content').insert(insert_data).execute()

        if insert_response.data:
            return {
                'message': 'Content scraped and saved successfully',
                'status': 200,
                'data': {
                    'id': scrape_id,
                    'chatbot_id': chatbot_id,
                    'url': url,
                    'title': scraped_data['title'],
                    'content_length': total_content_length,
                    'links_count': len(scraped_data['links']),
                    'links': [{
                        'url': link['url'],
                        'title': link['title'],
                        'content_length': link['content_length']
                    } for link in scraped_data['links']]
                }
            }
        else:
            return {'message': 'Failed to save scraped content', 'status': 500, 'error': insert_response.error.message}

    except Exception as e:
        return {'message': f'Error scraping {url}', 'status': 500, 'error': str(e)}

def get_chatbot_links(chatbot_id):
    try:
        response = supabase.table('chatbot_scraped_content').select('id', 'url', 'title', 'content_length', 'links').eq('chatbot_id', chatbot_id).execute()
        
        if response.data:
            processed_data = [{
                'id': item['id'],
                'url': item['url'],
                'title': item['title'],
                'content_length': int(item['content_length']),
                'links_count': len(item['links']),
                'links': [{
                    'url': link['url'],
                    'title': link['title'],
                    'content_length': int(link['content_length'])
                } for link in item['links']]
            } for item in response.data]
            
            return {
                'message': 'Data retrieved successfully',
                'status': 200,
                'data': processed_data
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

def extract_content(soup):
    content = []
    for paragraph in soup.find_all('p'):
        content.append(paragraph.text.strip())
    return ' '.join(content)