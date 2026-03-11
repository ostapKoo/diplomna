Write-Host "Початок автоматичного оновлення Production середовища..." -ForegroundColor Cyan

# 1. Створення бекапу .env файлу
Copy-Item -Path "..\..\.env" -Destination "..\..\.env.backup" -ErrorAction SilentlyContinue
Write-Host "[OK] Створено бекап конфігурації" -ForegroundColor Green

# 2. Оновлення коду
git pull origin main
Write-Host "[OK] Код оновлено з репозиторію" -ForegroundColor Green

# 3. Оновлення залежностей
pip install -r ..\..\requirements.txt
Write-Host "[OK] Залежності оновлено" -ForegroundColor Green

Write-Host "Оновлення завершено! Перезапустіть служби." -ForegroundColor Magenta