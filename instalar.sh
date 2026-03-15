#!/bin/bash
# ═══════════════════════════════════════════
#  VideoDropper — Instalador para macOS
# ═══════════════════════════════════════════

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════╗${NC}"
echo -e "${BLUE}║     VideoDropper — Instalador    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════╝${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PY="$SCRIPT_DIR/VideoDropper.py"
DEST="$HOME/Applications"
APP_BUNDLE="$DEST/VideoDropper.app"

# 1. Verificar Python
echo -e "1️⃣  Verificando Python 3..."
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado. Instale em python.org${NC}"
    exit 1
fi
echo -e "${GREEN}   ✓ Python $(python3 --version | cut -d' ' -f2)${NC}"

# 2. Instalar yt-dlp
echo -e "2️⃣  Instalando/atualizando yt-dlp..."
if command -v brew &>/dev/null; then
    brew install yt-dlp 2>/dev/null || brew upgrade yt-dlp 2>/dev/null || true
elif command -v pip3 &>/dev/null; then
    pip3 install --upgrade yt-dlp --quiet
else
    python3 -m pip install --upgrade yt-dlp --quiet
fi

if command -v yt-dlp &>/dev/null; then
    echo -e "${GREEN}   ✓ yt-dlp $(yt-dlp --version)${NC}"
else
    echo -e "${YELLOW}   ⚠ yt-dlp instalado via pip (pode precisar de reinicialização)${NC}"
fi

# 3. Instalar ffmpeg (para merge de vídeo+áudio)
echo -e "3️⃣  Verificando ffmpeg..."
if ! command -v ffmpeg &>/dev/null; then
    if command -v brew &>/dev/null; then
        echo -e "   Instalando ffmpeg via Homebrew..."
        brew install ffmpeg --quiet
        echo -e "${GREEN}   ✓ ffmpeg instalado${NC}"
    else
        echo -e "${YELLOW}   ⚠ ffmpeg não encontrado. Instale com: brew install ffmpeg${NC}"
        echo -e "${YELLOW}     (vídeos serão baixados sem conversão de qualidade)${NC}"
    fi
else
    echo -e "${GREEN}   ✓ ffmpeg disponível${NC}"
fi

# 4. Criar .app bundle
echo -e "4️⃣  Criando VideoDropper.app..."
mkdir -p "$DEST"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Copiar script principal
cp "$APP_PY" "$APP_BUNDLE/Contents/Resources/VideoDropper.py"

# Launcher
cat > "$APP_BUNDLE/Contents/MacOS/VideoDropper" << 'LAUNCHER'
#!/bin/bash
# Adiciona caminhos comuns ao PATH para encontrar yt-dlp/ffmpeg
export PATH="$PATH:/usr/local/bin:/opt/homebrew/bin:/opt/local/bin:$HOME/.local/bin:$HOME/Library/Python/3.x/bin"
# Encontra o Python 3 disponível
PYTHON=""
for py in python3 /usr/bin/python3 /opt/homebrew/bin/python3 /usr/local/bin/python3; do
    if command -v "$py" &>/dev/null; then
        PYTHON="$py"
        break
    fi
done
if [ -z "$PYTHON" ]; then
    osascript -e 'display alert "Python 3 não encontrado" message "Instale Python 3 em python.org"'
    exit 1
fi
DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$PYTHON" "$DIR/../Resources/VideoDropper.py"
LAUNCHER

chmod +x "$APP_BUNDLE/Contents/MacOS/VideoDropper"

# Info.plist
cat > "$APP_BUNDLE/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>VideoDropper</string>
    <key>CFBundleDisplayName</key>
    <string>VideoDropper</string>
    <key>CFBundleIdentifier</key>
    <string>com.videodropper.app</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>VideoDropper</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
    <key>NSHumanReadableCopyright</key>
    <string>VideoDropper — Open Source</string>
</dict>
</plist>
PLIST

echo -e "${GREEN}   ✓ App criado em: $APP_BUNDLE${NC}"

# 5. Criar atalho no Desktop
echo -e "5️⃣  Criando atalho na área de trabalho..."
DESKTOP="$HOME/Desktop"
if [ -d "$DESKTOP" ]; then
    # Alias via AppleScript
    osascript << ASEND 2>/dev/null || true
tell application "Finder"
    make alias file to POSIX file "$APP_BUNDLE" at POSIX file "$DESKTOP"
end tell
ASEND
    echo -e "${GREEN}   ✓ Atalho criado no Desktop${NC}"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Instalação concluída com sucesso! ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "  Abra: ${BLUE}~/Applications/VideoDropper.app${NC}"
echo -e "  Ou clique no atalho criado no Desktop."
echo ""

# Abrir o app
read -p "  Deseja abrir o VideoDropper agora? [S/n] " ans
if [[ "$ans" != "n" && "$ans" != "N" ]]; then
    open "$APP_BUNDLE"
fi
