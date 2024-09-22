import gzip
import hashlib
import requests

CLOUDINARY_URL = "https://galadon.s3.amazonaws.com/index.js"
script_cache = {}

def get_script(chatbot_id):
    if not chatbot_id:
        return {"error": "Chatbot ID is required"}, 400

    cache_key = f"script_{chatbot_id}"
    
    if cache_key in script_cache:
        return script_cache[cache_key], 200

    response = requests.get(CLOUDINARY_URL)
    if response.status_code != 200:
        return {"error": "Failed to fetch script from Cloudinary"}, 500
    
    cloudinary_script = response.text

    mount_script = f"""
    {cloudinary_script}

    window.mountChainlitWidget({{
        chainlitServer: "https://livechat.galadon.com/live",
        theme: "light",
        chatBotID: "{chatbot_id}",
    }});
    """

    compressed_script = gzip.compress(mount_script.encode('utf-8'))
    etag = hashlib.md5(compressed_script).hexdigest()

    script_data = {
        'content': compressed_script,
        'etag': etag,
        'media_type': "application/javascript",
        'headers': {
            "Content-Encoding": "gzip",
            "ETag": etag,
            "Cache-Control": "public, max-age=3600"
        }
    }

    script_cache[cache_key] = script_data
    return script_data, 200