Write-Host "=== Setup automatique de l'environnement Python ===" -ForegroundColor Cyan

# Vérifie la présence de Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Host "❌ Python n'est pas installé sur ce PC. Installez Python 3.10+ puis relancez." -ForegroundColor Red
    exit 1
}

Write-Host "✔ Python détecté : $($python.Source)" -ForegroundColor Green

# Supprime l'ancien environnement
if (Test-Path ".venv") {
    Write-Host "🗑 Suppression de l'ancien environnement virtuel..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".venv"
}

# Crée un nouvel environnement
Write-Host "⚙ Création du nouvel environnement virtuel..." -ForegroundColor Cyan

if ($python.Name -eq "py.exe") {
    py -3 -m venv .venv
} else {
    python -m venv .venv
}

# Active l'environnement (dot sourcing !!!)
Write-Host "🔄 Activation de l'environnement..." -ForegroundColor Cyan
. ".\.venv\Scripts\Activate.ps1"

# Installation des dépendances
if (Test-Path "requirements.txt") {
    Write-Host "📦 Installation des dépendances..." -ForegroundColor Cyan
    pip install -r requirements.txt
} else {
    Write-Host "⚠ Aucun fichier requirements.txt trouvé, aucune dépendance installée." -ForegroundColor Yellow
}

Write-Host "🚀 Lancement de l'application run_app.py..." -ForegroundColor Cyan

# Lance ton application
python run_app.py

Write-Host "🎉 Environnement prêt et application lancée !" -ForegroundColor Green
