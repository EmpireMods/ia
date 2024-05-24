import discord
import os
from dotenv import load_dotenv
import requests
import tempfile

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                await message.channel.send('Analisando a imagem...')

                # Salvar a imagem em um arquivo temporário
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    await attachment.save(temp_file.name)

                    # Analisar a imagem
                    analysis_result = analyze_image(temp_file.name)
                    await message.channel.send(analysis_result)

                    # Remover o arquivo temporário
                    os.remove(temp_file.name)

def analyze_image(image_path):
    url = "https://api.deepai.org/api/image-classification"
    headers = {
        'Api-Key': DEEPAI_API_KEY
    }
    files = {'image': open(image_path, 'rb')}

    try:
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            result = response.json()
            output = "Resultado da análise:\n"
            for concept in result['output']['concepts']:
                output += f"- {concept['name']}: {concept['value']}\n"
            return output
        else:
            return "Erro durante a análise"
    except Exception as e:
        return f"Erro durante a análise da imagem: {str(e)}"

client.run(DISCORD_TOKEN)
