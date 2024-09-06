from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import uuid
from db.db import supabase

def scrape_and_add_link(data):
    chatbot_id = data.get('chatbotId')
    url = data.get('url')
    
    if not chatbot_id or not url:
        return {'message': 'Chatbot ID and URL are required', 'status': 400}

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else ''
        content = extract_content(soup)
        links = extract_links(soup, url)
        
        scrape_id = str(uuid.uuid4())
        
        insert_response = supabase.table('chatbot_scraped_content').insert({
            'id': scrape_id,
            'chatbot_id': chatbot_id,
            'url': url,
            'title': title,
            'content': content,
            'links': links
        }).execute()

        if insert_response.data:
            return {
                'message': 'Content scraped and saved successfully',
                'status': 200,
                'data': {
                    'id': scrape_id,
                    'chatbot_id': chatbot_id,
                    'url': url,
                    'title': title,
                    'content_preview': content[:200] + '...' if len(content) > 200 else content,
                    'links_count': len(links)
                }
            }
        else:
            return {'message': 'Failed to save scraped content', 'status': 500, 'error': insert_response.error.message}

    except Exception as e:
        return {'message': f'Error scraping {url}', 'status': 500, 'error': str(e)}

def extract_content(soup):
    content = []
    for paragraph in soup.find_all('p'):
        content.append(paragraph.text.strip())
    return ' '.join(content)

def extract_links(soup, base_url):
    links = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        if base_url in full_url:
            links.append({
                'url': full_url,
                'text': link.text.strip()
            })
    return links