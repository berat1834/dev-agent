import requests
from google import genai

def generate_analysis_prompt(files: list[str]) -> str:
    files_str = "\n".join(files)
    return f"""
    Sen kıdemli bir yazılım mimarısın. Aşağıda bir projenin dosya yapısı verilmiştir:
    
    {files_str}
    
    Bu projeyi incele ve geliştiriciye şu 3 sorunun cevabını ver:
    1. Bu projenin eksik veya geliştirilmesi gereken ana mimari adımı nedir?
    2. Bugün ilk olarak yapılması gereken 2 mikro görev nedir?
    3. Kod kalitesini artırmak için ne yapılmalı?
    Cevabı kısa, net ve Türkçe maddeler halinde ver.
    """

def query_gemini(prompt: str, api_key: str, model_name: str = "gemini-2.5-flash") -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text

def query_ollama(prompt: str, model_name: str = "llama3.2") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    if response.status_code == 200:
        return response.json().get("response", "")
    raise Exception(f"Ollama HTTP Hatası: {response.status_code}")

def generate_fix_prompt(file_path: str, code_content: str) -> str:
    return f"""
    Sen kıdemli bir yazılım mühendisisin. Aşağıda '{file_path}' dosyasının mevcut kaynak kodu verilmiştir:
    
    ```
    {code_content}
    ```
    
    Lütfen bu kodu refactor et, hatalarını düzelt, tip ipuçlarını (type hinting) ve docstring'leri ekle. 
    Ayrıca kodu daha temiz ve modüler hale getir.
    
    ÇIKTI FORMATI KURALLARI:
    1. Yanıtında SADECE güncellenmiş ve çalışmaya hazır tam kaynak kodunu ver.
    2. Kod dışı hiçbir açıklama, selamlama veya giriş metni yazma.
    3. Kodu varsayılan kod bloğu (markdown ```) içinde döndür.
    """

def query_fix_gemini(prompt: str, api_key: str, model_name: str = "gemini-2.5-flash") -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text