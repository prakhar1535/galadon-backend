import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import uuid
from db.db import supabase
import json


def deep_scrape(url, base_url, visited_urls=None, depth=1):
    if depth == 0 or (visited_urls and url in visited_urls):
        return None

    visited_urls = visited_urls or set()
    visited_urls.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else ''
        content = extract_content(soup)
        content_length = len(content)
        
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if base_url in full_url and full_url not in visited_urls:
                sub_content = deep_scrape(full_url, base_url, visited_urls, depth - 1)
                if sub_content:
                    # Add a unique ID for each link
                    sub_content['id'] = str(uuid.uuid4())
                    # Check for duplicate URLs or titles
                    if not any(l['url'] == sub_content['url'] or l['title'] == sub_content['title'] for l in links):
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
        
        # Include the main URL in the links array
        main_link = {
            'id': str(uuid.uuid4()),
            'url': url,
            'title': scraped_data['title'],
            'content': scraped_data['content'],
            'content_length': scraped_data['content_length']
        }
        
        insert_data = {
            'id': scrape_id,
            'chatbot_id': chatbot_id,
            'url': url,
            'title': scraped_data['title'],
            'content': scraped_data['content'],
            'content_length': total_content_length,
            'links': [main_link] + [{
                'id': link['id'],
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
                'id': scrape_id,
                'chatbot_id': chatbot_id,
                'url': url,
                'title': scraped_data['title'],
                'content_length': total_content_length,
                'links_count': len(insert_data['links']),
                'links': [{
                    'id': link['id'],
                    'url': link['url'],
                    'title': link['title'],
                    'content_length': link['content_length']
                } for link in insert_data['links']]
            }
        else:
            return {'message': 'Failed to save scraped content', 'status': 500, 'error': insert_response.error.message}

    except Exception as e:
        return {'message': f'Error scraping {url}', 'status': 500, 'error': str(e)}


def get_chatbot_links(chatbot_id):
    try:
        print(f"Attempting to retrieve links for chatbot ID: {chatbot_id}")

        # Query the chatbot_content_scraped table
        response = supabase.table('chatbot_scraped_content').select('*').eq('chatbot_id', chatbot_id).execute()
        print(f"Query result: {response}")

        if not response.data:
            return {
                'message': f'No scraped content found for chatbot ID: {chatbot_id}',
                'status': 404
            }

        # Process the data
        processed_data = []
        for item in response.data:
            content = item.get('content', '')
            links = json.loads(item.get('links', '[]'))  # Assuming links are stored as a JSON string

            processed_item = {
                'id': item.get('id'),
                'url': item.get('url', ''),
                'title': item.get('title', ''),
                'content_length': item.get('content_length', ''),
                'links_count': len(links),
                'links': []
            }

            for link in links:
                processed_item['links'].append({
                    'url': link.get('url', ''),
                    'content_length': link.get('content_length', 0)
                })

            processed_data.append(processed_item)

        return {
            'message': 'Data retrieved successfully',
            'status': 200,
            'data': processed_data
        }

    except Exception as e:
        print(f"Error in get_chatbot_links: {str(e)}")
        return {
            'message': f'Error retrieving data: {str(e)}',
            'status': 500
        }

def extract_content(soup):
    content = []
    for paragraph in soup.find_all('p'):
        content.append(paragraph.text.strip())
    return ' '.join(content)