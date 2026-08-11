import os
import re
import typer
import uvicorn
from rich.console import Console
from rich.panel import Panel
from agent.scanner import scan_project_files
from agent.providers import (
    generate_analysis_prompt, 
    generate_fix_prompt, 
    query_gemini, 
    query_fix_gemini, 
    query_ollama
)
from agent.config import load_config, save_config, CONFIG_FILE

app = typer.Typer(
    help="Sen tanıt, o yapsın - AI CLI Agent",
    no_args_is_help=True
)
console = Console()

def clean_code_blocks(llm_response: str) -> str:
    """LLM çıktısındaki ```python veya ``` markdown işaretlerini temizler."""
    pattern = r"```(?:\w+)?\n(.*?)```"
    match = re.search(pattern, llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return llm_response.replace("```", "").strip()

@app.command(name="init")
def init():
    """
    Agent tercihlerini ve API anahtarını ~/.agentrc dosyasına kaydeder.
    """
    console.print("[bold cyan]⚙️  Agent Yapılandırma Sihirbazı[/bold cyan]\n")
    
    current_config = load_config()
    default_key = current_config.get("api_key", "")
    default_provider = current_config.get("provider", "gemini")
    
    if default_provider not in ["gemini", "ollama"]:
        default_provider = "gemini"

    api_key = typer.prompt(
        "Gemini API Anahtarınızı girin",
        default=default_key if default_key else "",
        hide_input=True
    )
    
    provider = typer.prompt(
        "Varsayılan AI Sağlayıcısı (gemini/ollama)",
        default=default_provider
    )
    
    if provider.lower() not in ["gemini", "ollama"]:
        console.print("[yellow]Geçersiz sağlayıcı algılandı, 'gemini' olarak ayarlanıyor.[/yellow]")
        provider = "gemini"

    model = typer.prompt(
        "Varsayılan Model Adı",
        default="gemini-2.5-flash" if provider == "gemini" else "llama3.2"
    )
    
    config_data = {
        "api_key": api_key,
        "provider": provider.lower(),
        "model": model
    }
    save_config(config_data)
    
    console.print(f"\n[bold green]✅ Yapılandırma başarıyla kaydedildi:[/bold green] {CONFIG_FILE}")

@app.command(name="analyze")
def analyze(
    path: str = typer.Option(".", help="Taranacak proje dizini"),
    provider: str = typer.Option(None, help="Model sağlayıcı: 'gemini' veya 'ollama'"),
    api_key: str = typer.Option(None, envvar="GEMINI_API_KEY", help="Gemini API Key"),
    model_name: str = typer.Option(None, help="Özel model adı")
):
    """
    Yerel kod deposunu analiz eder ve geliştirme adımlarını sunar.
    """
    config = load_config()
    
    final_provider = provider or config.get("provider", "gemini")
    if final_provider not in ["gemini", "ollama"]:
        final_provider = "gemini"

    final_api_key = api_key or config.get("api_key")
    final_model = model_name or config.get("model") or ("gemini-2.5-flash" if final_provider == "gemini" else "llama3.2")

    console.print(f"[bold blue]🔍 Dizin taranıyor:[/bold blue] {os.path.abspath(path)}")
    
    files = scan_project_files(path)
    if not files:
        console.print("[yellow]Taranacak uygun kod dosyası bulunamadı.[/yellow]")
        return

    prompt = generate_analysis_prompt(files)
    result_text = ""

    if final_provider.lower() == "gemini":
        if not final_api_key:
            console.print("[bold red]Hata:[/bold red] Gemini API anahtarı bulunamadı! 'agent init' çalıştırın.")
            raise typer.Exit(code=1)
            
        with console.status(f"[bold green]Gemini ({final_model}) analiz ediyor...[/bold green]"):
            try:
                result_text = query_gemini(prompt, final_api_key, final_model)
            except Exception as e:
                console.print(f"[bold red]Gemini Hatası:[/bold red] {e}")
                raise typer.Exit(code=1)

    elif final_provider.lower() == "ollama":
        with console.status(f"[bold green]Yerel Ollama ({final_model}) analiz ediyor...[/bold green]"):
            try:
                result_text = query_ollama(prompt, final_model)
            except Exception as e:
                console.print(f"[bold red]Ollama Bağlantı Hatası:[/bold red] {e}")
                raise typer.Exit(code=1)

    console.print(Panel(result_text, title=f"[bold gold1]Agent Analiz Raporu ({final_provider.upper()})[/bold gold1]", border_style="green"))

@app.command(name="fix")
def fix(
    file_path: str = typer.Argument(..., help="Düzeltilecek ve refactor edilecek dosya yolu"),
    provider: str = typer.Option(None, help="Model sağlayıcı: 'gemini' veya 'ollama'"),
    api_key: str = typer.Option(None, envvar="GEMINI_API_KEY", help="Gemini API Key")
):
    """
    Belirtilen koda refactoring uygular, eksikleri tamamlar ve dosyayı günceller.
    """
    if not os.path.exists(file_path):
        console.print(f"[bold red]Hata:[/bold red] '{file_path}' dosyası bulunamadı!")
        raise typer.Exit(code=1)

    config = load_config()
    final_provider = provider or config.get("provider", "gemini")
    final_api_key = api_key or config.get("api_key")
    final_model = config.get("model", "gemini-2.5-flash")

    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    console.print(f"[bold blue]🛠️  Dosya inceleniyor ve refactor ediliyor:[/bold blue] {file_path}")
    prompt = generate_fix_prompt(file_path, original_code)
    fixed_code_raw = ""

    if final_provider.lower() == "gemini":
        if not final_api_key:
            console.print("[bold red]Hata:[/bold red] Gemini API anahtarı bulunamadı! 'agent init' çalıştırın.")
            raise typer.Exit(code=1)
            
        with console.status(f"[bold green]Gemini koda dokunuş yapıyor...[/bold green]"):
            try:
                fixed_code_raw = query_fix_gemini(prompt, final_api_key, final_model)
            except Exception as e:
                console.print(f"[bold red]Gemini Hatası:[/bold red] {e}")
                raise typer.Exit(code=1)
    else:
        console.print("[bold red]Şu an fix komutu Gemini sağlayıcısı ile en kararlı çalışır.[/bold red]")
        raise typer.Exit(code=1)

    clean_code = clean_code_blocks(fixed_code_raw)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_code)

    console.print(Panel(
        f"[bold green]✅ '{file_path}' başarıyla refactor edildi ve güncellendi![/bold green]\n\n"
        "Eklenenler: Type Hinting, Docstringler ve Temiz Kod Yapısı.",
        title="[bold gold1]Agent Refactoring Başarılı[/bold gold1]",
        border_style="green"
    ))

@app.command(name="version")
def version():
    """CLI Sürümünü gösterir."""
    console.print("[bold cyan]CLI Agent v0.5.0 (Full Features)[/bold cyan]")

def main():
    app()

if __name__ == "__main__":
    main()
    
    import uvicorn  # Dosyanın en üstüne import eklemeyi unutma

@app.command(name="ui")
def ui(port: int = typer.Option(8000, help="Web arayüzünün çalışacağı port")):
    """
    Dev-Agent Web API ve Arayüz sunucusunu başlatır.
    """
    console.print(f"[bold green]🚀 Web Arayüz Sunucusu Başlatılıyor:[/bold green] [http://127.0.0.1](http://127.0.0.1):{port}")
    console.print(f"[bold cyan]📖 Swagger Dokümantasyonu (Interactive UI):[/bold cyan] [http://127.0.0.1](http://127.0.0.1):{port}/docs\n")
    uvicorn.run("agent.api:app", host="127.0.0.1", port=port, reload=True)