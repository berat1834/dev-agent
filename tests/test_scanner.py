import os
from agent.scanner import scan_project_files

def test_scan_project_files(tmp_path):
    # Geçici bir proje yapısı simüle et
    d = tmp_path / "sub"
    d.mkdir()
    p1 = d / "main.py"
    p1.write_text("print('hello')", encoding="utf-8")
    p2 = d / "utils.js"
    p2.write_text("console.log('hi')", encoding="utf-8")

    # Yoksayılacak klasör simüle et
    venv = tmp_path / ".venv"
    venv.mkdir()
    p3 = venv / "ignored.py"
    p3.write_text("secret = 1", encoding="utf-8")

    # Tarama fonksiyonunu çalıştır
    files = scan_project_files(str(tmp_path))

    # Doğrulamalar
    assert len(files) == 2
    assert any("main.py" in f for f in files)
    assert any("utils.js" in f for f in files)
    assert not any(".venv" in f for f in files)