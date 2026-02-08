import os
from dotenv import load_dotenv

load_dotenv()

def yandex_maps_api_key(request):
    return {
        'yandex_maps_api_key': os.getenv('YANDEX_MAPS_API_KEY', ''),
    }