#!/data/data/com.termux/files/usr/bin/bash

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║     OSINTool Termux Kurulum              ║"
echo "  ║     Termux'ta tam destekli OSINT aracı   ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

# Depoları güncelle
echo "[*] Paket listesi güncelleniyor..."
pkg update -y -qq 2>/dev/null

# Temel bağımlılıklar
echo "[*] Python ve araçlar kuruluyor..."
pkg install -y python git clang libxml2 libxslt openssl binutils -qq 2>/dev/null

# pip güncelle
pip install --upgrade pip -q

# OSINTool'u kur
echo "[*] OSINTool kuruluyor..."
pip install osintool -q 2>/dev/null || {
    echo "[!] pip paketi bulunamadi, repodan kuruluyor..."
    pip install git+https://github.com/alisafakaya624-coder/osintool.git -q
}

# İsteğe bağlı modüller
echo "[*] Ek modüller kuruluyor..."
pip install colorama requests beautifulsoup4 cryptography fpdf2 -q

# instagrapi (Instagram auth için)
echo ""
echo "[?] Instagram auth kullanmak istiyor musun? (E/h)"
read -r insta_choice
if [[ "$insta_choice" != "h" && "$insta_choice" != "H" ]]; then
    echo "[*] instagrapi kuruluyor..."
    pip install instagrapi -q
    echo "[✓] Instagram destegi eklendi"
fi

# Playwright (WhatsApp için - opsiyonel)
echo ""
echo "[?] WhatsApp Web auth kullanmak istiyor musun? (e/H)"
echo "    Uyari: Termux'ta Playwright/Chromium sorun cikarabilir."
read -r wa_choice
if [[ "$wa_choice" == "e" || "$wa_choice" == "E" ]]; then
    echo "[*] Playwright ve Chromium kuruluyor..."
    pip install playwright playwright-stealth -q
    playwright install chromium 2>/dev/null
    echo "[✓] WhatsApp destegi eklendi"
fi

# Telethon (Telegram auth için)
echo ""
echo "[?] Telegram auth kullanmak istiyor musun? (E/h)"
read -r tg_choice
if [[ "$tg_choice" != "h" && "$tg_choice" != "H" ]]; then
    echo "[*] Telethon kuruluyor..."
    pip install telethon -q
    echo "[✓] Telegram destegi eklendi"
fi

# Kullanıcıyı gruba ekle
echo ""
echo "[*] Termux:depo izinleri ayarlaniyor..."
chmod +x "$PREFIX/bin/osintool" 2>/dev/null

# Bash alias
echo "" >> ~/.bashrc
echo "# OSINTool" >> ~/.bashrc
echo "alias osintool='python3 -m osintool'" >> ~/.bashrc
echo "alias osint='python3 -m osintool'" >> ~/.bashrc

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║  KURULUM TAMAM!                          ║"
echo "  ╠══════════════════════════════════════════╣"
echo "  ║  Kullanım:                               ║"
echo "  ║    osintool -u kullaniciadi              ║"
echo "  ║    osintool -n \"Ad Soyad\"              ║"
echo "  ║    osintool -p +905551234567             ║"
echo "  ║    osintool --gh-search \"yapay zeka\"   ║"
echo "  ║    osintool --help                       ║"
echo "  ╠══════════════════════════════════════════╣"
echo "  ║  Termux ipuçları:                        ║"
echo "  ║  • pip install osintool ile dogrudan     ║"
echo "  ║  • pip install -r requirements.txt       ║"
echo "  ║  • Python 3.11+ gerekli                  ║"
echo "  ║  • Playwright/Chromium WhatsApp icin     ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""
