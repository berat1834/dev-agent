import os
import re
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from agent.scanner import scan_project_files
from agent.providers import (
    generate_analysis_prompt,
    generate_fix_prompt,
    query_gemini,
    query_fix_gemini,
    query_ollama
)
from agent.config import load_config
from agent.logger import logger

app = FastAPI(title="Dev-Agent Enterprise API", version="1.0.0")

# CORS Middleware (Web arayüzü entegrasyonu için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

class AnalyzeRequest(BaseModel):
    path: str = "."
    provider: str | None = None

class FixRequest(BaseModel):
    file_path: str
    provider: str | None = None

def clean_code_blocks(llm_response: str) -> str:
    pattern = r"```(?:\w+)?\n(.*?)```"
    match = re.search(pattern, llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return llm_response.replace("```", "").strip()

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = TEMPLATES_DIR / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Dev-Agent Dashboard (index.html bulunamadı)</h1>"

@app.get("/api/file")
def get_file_content(path: str):
    """Web arayüzünde dosya içeriğini önizlemek için."""
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"file_path": path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
def api_analyze(req: AnalyzeRequest):
    logger.info(f"Dizin analizi başlatıldı: {req.path}")
    config = load_config()
    final_provider = req.provider or config.get("provider", "gemini")
    final_api_key = config.get("api_key")
    final_model = config.get("model", "gemini-2.5-flash")

    if not os.path.exists(req.path):
        raise HTTPException(status_code=400, detail="Belirtilen dizin bulunamadı!")

    files = scan_project_files(req.path)
    if not files:
        return {"status": "warning", "message": "Taranacak uygun kod dosyası bulunamadı.", "scanned_files": []}

    prompt = generate_analysis_prompt(files)
    
    try:
        if final_provider == "gemini":
            if not final_api_key:
                raise HTTPException(status_code=400, detail="Gemini API key bulunamadı! 'agent init' çalıştırın.")
            result_text = query_gemini(prompt, final_api_key, final_model)
        elif final_provider == "ollama":
            result_text = query_ollama(prompt, final_model)
        else:
            raise HTTPException(status_code=400, detail="Geçersiz provider!")
            
        return {
            "status": "success",
            "provider": final_provider,
            "scanned_files": files,
            "analysis": result_text
        }
    except Exception as e:
        logger.error(f"Analiz hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fix")
def api_fix(req: FixRequest):
    logger.info(f"Dosya refactor isteği alındı: {req.file_path}")
    if not os.path.exists(req.file_path):
        raise HTTPException(status_code=404, detail="Dosya bulunamadı!")

    config = load_config()
    final_provider = req.provider or config.get("provider", "gemini")
    final_api_key = config.get("api_key")
    final_model = config.get("model", "gemini-2.5-flash")

    with open(req.file_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    prompt = generate_fix_prompt(req.file_path, original_code)
    
    try:
        if final_provider == "gemini":
            if not final_api_key:
                raise HTTPException(status_code=400, detail="Gemini API key bulunamadı!")
            fixed_raw = query_fix_gemini(prompt, final_api_key, final_model)
        else:
            raise HTTPException(status_code=400, detail="Fix işlemi şu an Gemini sağlayıcısı ile desteklenmektedir.")
            
        clean_code = clean_code_blocks(fixed_raw)
        
        with open(req.file_path, "w", encoding="utf-8") as f:
            f.write(clean_code)

        logger.info(f"Dosya başarıyla güncellendi: {req.file_path}")
        return {
            "status": "success",
            "message": f"'{req.file_path}' başarıyla güncellendi.",
            "updated_code": clean_code
        }
    except Exception as e:
        logger.error(f"Fix hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))