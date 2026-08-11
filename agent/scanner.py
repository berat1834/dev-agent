import os
from typing import List, Tuple, Set

# --- Modül Düzeyi Sabitleri ---
_IGNORED_DIRS: Set[str] = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",  # Yaygın bir sanal ortam dizini
    "build",
    "dist",
    ".idea", # Yaygın IDE dizini
    ".vscode", # Yaygın IDE dizini
}
"""Proje taraması sırasında yoksayılacak dizin adları."""

_ALLOWED_EXTENSIONS: Tuple[str, ...] = (
    '.py', '.js', '.ts', '.html', '.css', '.dart', '.json', '.go', '.java',
    '.jsx', '.tsx', '.vue', '.rb', '.php', '.c', '.cpp', '.h', '.hpp', '.sh',
    '.yaml', '.yml', '.toml', '.md', '.xml', '.sql', '.dockerfile', '.ini',
    '.swift', '.kt', '.m', '.scala', '.r', '.elm', '.zig', '.rs', '.asm',
)
"""Kod veya yapılandırma dosyaları olarak kabul edilen dosya uzantıları."""


def _is_ignored_directory(directory_name: str) -> bool:
    """
    Belirtilen dizin adının yoksayılması gerekip gerekmediğini kontrol eder.

    Args:
        directory_name: Kontrol edilecek dizin adı.

    Returns:
        Dizin, yoksayılan dizinler listesindeyse True, aksi takdirde False.
    """
    return directory_name in _IGNORED_DIRS


def _is_allowed_file_extension(file_name: str) -> bool:
    """
    Belirtilen dosya adının izin verilen bir uzantıya sahip olup olmadığını kontrol eder.

    Args:
        file_name: Kontrol edilecek dosya adı.

    Returns:
        Dosya izin verilen uzantılardan birine sahipse True, aksi takdirde False.
    """
    # Dosya uzantısı kontrolü küçük harfe dönüştürülerek yapılır.
    # Bu, "README.MD" gibi dosyaların da yakalanmasını sağlar.
    return file_name.lower().endswith(_ALLOWED_EXTENSIONS)


def scan_project_files(path: str, max_files: int = 25) -> List[str]:
    """
    Belirtilen dizindeki kod dosyalarını tarar ve bağıntılı yollarını döndürür.

    Fonksiyon, `_IGNORED_DIRS` sabitinde belirtilen dizinleri atlar ve yalnızca
    `_ALLOWED_EXTENSIONS` sabitinde tanımlanmış kod dosyası uzantılarına sahip
    dosyaları dahil eder. Tarama, `max_files` sayısına ulaşıldığında durur.

    Args:
        path: Taranacak projenin kök dizin yolu.
        max_files: Döndürülecek maksimum dosya sayısı. Tarama bu sayıya
                   ulaşıldığında durdurulur. Negatif veya sıfır olarak
                   belirtilirse, tüm uygun dosyalar döndürülür.

    Returns:
        Proje kök dizinine göre bağıntılı yollarının bir listesi.
        Dizin bulunamazsa, erişilemezse veya uygun dosya yoksa boş bir liste dönebilir.
    """
    if not os.path.isdir(path):
        # Belirtilen yol bir dizin değilse veya yoksa boş bir liste döndür.
        return []

    found_files: List[str] = []
    
    # max_files negatif veya sıfır ise, bir limit olmadığını varsay.
    # Aksi takdirde, karşılaştırma için pozitif bir tamsayı olduğundan emin ol.
    effective_max_files = max_files if max_files > 0 else float('inf')

    for root, dirs, files in os.walk(path):
        # Yoksayılacak klasörleri filtrele.
        # `dirs[:]` kullanarak listeyi yerinde değiştiriyoruz, böylece os.walk
        # bu dizinlere inmeyecektir.
        dirs[:] = [d for d in dirs if not _is_ignored_directory(d)]

        for file in files:
            if _is_allowed_file_extension(file):
                # Dosyanın anahtar dizine göre bağıntılı yolunu al.
                rel_path = os.path.relpath(os.path.join(root, file), path)
                found_files.append(rel_path)

                # max_files limitine ulaşıldığında taramayı durdur ve hemen dön.
                if len(found_files) >= effective_max_files:
                    return found_files

    # Limit dolmadıysa veya limit yoksa bulunan tüm dosyaları döndür.
    return found_files