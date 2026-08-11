# 🤖 Dev-Agent: AI-Powered CLI Developer Assistant

> **"Sen tanıt, o yapsın."** — Terminalinizden çıkmadan kod deponuzu analiz eden, mimari tavsiyeler veren ve kodunuzu otomatik refactor eden otonom AI Agent.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Providers](https://img.shields.io/badge/AI_Providers-Gemini_%7C_Ollama-orange)

---

## ✨ Özellikler

- 🔍 **`agent analyze`**: Projenizin yerel dosya yapısını tarar ve eksik mimari adımları, günün mikro görevlerini ve kod kalitesi tavsiyelerini sunar.
- 🛠️ **`agent fix <dosya>`**: Belirtilen dosyayı okur, tip ipuçları (type hinting), docstring ve PEP8 standartları ekleyerek kodu otomatik günceller.
- ⚙️ **`agent init`**: API anahtarınızı ve varsayılan model tercihlerinizi `~/.agentrc` dosyasına güvenle kaydeder.
- 🌐 **Çoklu AI Desteği**: Google Gemini API veya yerel bilgisayarınızda çalışan ücretsiz **Ollama** arasında esnek seçim.

---

## 🚀 Kurulum

Projeyi yerel ortamınıza klonlayın ve geliştirici modunda kurun:

```bash
git clone [https://github.com/kullaniciadi/dev-agent.git](https://github.com/kullaniciadi/dev-agent.git)
cd dev-agent
pip install -e .