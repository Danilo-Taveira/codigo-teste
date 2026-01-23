import google.generativeai as genai

# COLE SUA API KEY AQUI
API_KEY = "AIzaSyDDsYbyay03fsy0kwSb7LDYXQlOBUgCHzg"
genai.configure(api_key=API_KEY)

print("Consultando modelos disponíveis para sua conta...")

try:
    for m in genai.list_models():
        # Filtra apenas modelos que geram texto (ignora modelos de 'embedding')
        if 'generateContent' in m.supported_generation_methods:
            print(f"Nome do Modelo: {m.name}")
except Exception as e:
    print(f"Erro ao listar modelos: {e}")