import requests
import os

def analyze_image(image_path):
    DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')
    url = "https://api.deepai.org/api/image-classification"
    headers = {
        'Api-Key': DEEPAI_API_KEY
    }
    files = {'image': open(image_path, 'rb')}

    response = requests.post(url, headers=headers, files=files)
    os.remove(image_path)

    if response.status_code == 200:
        result = response.json()
        output = "Resultado da análise:\n"
        for concept in result['output']['concepts']:
            output += f"- {concept['name']}: {concept['value']}\n"
        return output
    else:
        return "Erro durante a análise"
