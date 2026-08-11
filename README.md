# 🤖 Dev-Agent: AI-Powered CLI & Web Developer Assistant

> **"Sen tanıt, o yapsın."** — Terminalinizden veya Web Kontrol Paneli üzerinden kod deponuzu analiz eden, mimari tavsiyeler veren ve kodunuzu otomatik refactor eden otonom AI Agent.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Providers](https://img.shields.io/badge/AI_Providers-Gemini_%7C_Ollama-orange)

---

## ✨ Özellikler

- 🔍 **`agent analyze`**: Projenizin yerel dosya yapısını tarar ve eksik mimari adımları, günün mikro görevlerini ve kod kalitesi tavsiyelerini sunar.
- 🛠️ **`agent fix <dosya>`**: Belirtilen dosyayı okur, tip ipuçları (type hinting), docstring ve PEP8 standartları ekleyerek kodu otomatik günceller.
- 🌐 **`agent ui`**: FastAPI ve Tailwind CSS ile güçlendirilmiş Web Kontrol Panelini başlatır (`http://127.0.0.1:8000`).
- ⚙️ **`agent init`**: API anahtarınızı ve varsayılan model tercihlerinizi `~/.agentrc` dosyasına güvenle kaydeder.
- 🤖 **Çoklu AI Desteği**: Google Gemini API veya yerel bilgisayarınızda çalışan ücretsiz **Ollama** arasında esnek seçim.

---

## 🚀 Kurulum

Projeyi yerel ortamınıza klonlayın ve geliştirici modunda kurun:


git clone [https://github.com/berat1834/dev-agent.git](https://github.com/berat1834/dev-agent.git)
cd dev-agent
pip install -e .

### 💻 Kullanım

1. Yapılandırma (İlk Kurulum)

agent init
1. Yapılandırma (İlk Kurulum)
Bash
agent init
2. Proje Analizi (Terminal)
Bash
agent analyze
3. Otomatik Kod Refactoring / Düzeltme
Bash
agent fix main.py
4. Web Dashboard (Arayüz)
Bash
agent ui

🛠️ Teknolojiler

Python 3.12

Typer & Rich (Terminal CLI UI)

FastAPI & Uvicorn (REST API & Web Backend)

Tailwind CSS & FontAwesome (Web Dashboard UI)

Google GenAI SDK (Gemini 2.5 Flash)

Ollama API (Local LLM Integration)

📝 Lisans
Bu proje MIT Lisansı ile lisanslanmıştır.
