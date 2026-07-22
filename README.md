# OSINTool

Multi-platform OSINT search tool — username, name, and phone number lookup across 300+ sites with **authenticated scraping** and **recursive Instagram follower graph crawling**.

## Features

- **Public search** — 300+ sites (username / name / phone)
- **Authenticated search** — login with your own accounts for deep intel
  - **Instagram** — recursive follower/following graph crawler (2+ levels deep)
  - **GitHub** — profile info, repos, metadata
  - **Reddit** — posts, comments, karma stats
  - **Telegram** — profile, common groups, online status, profile photo
  - **WhatsApp Web** — contact lookup by phone number
- **Encrypted output** — results saved to `~/.founds.dat` (PBKDF2 + AES-256)
- **Encrypted credential storage** — API keys / passwords in `~/.osintool_auth.enc`

## Quick Install

```bash
git clone https://github.com/alisafakaya624-coder/osintool.git
cd osintool
pip install -e .

# Optional: for authenticated search features
pip install -e ".[auth]"
```

## Usage

### 1. Public Username Search (300+ sites)

```bash
# Tek kullanıcı adı ile her yerde ara
osintool -u hedefkullanici

# İsim ara
osintool -n "Ali Safa Kaya"

# Telefon numarası ara
osintool -p "+905551234567"

# Herşeyi dene
osintool --all "hedefkullanici"
```

---

### 2. Authenticated Search (Instagram, GitHub, Reddit, Telegram, WhatsApp)

Önce hesap bilgilerini kaydet (şifrelenerek saklanır):

```bash
osintool --auth-config --set-instagram    # Instagram email + şifre
osintool --auth-config --set-github       # GitHub personal access token
osintool --auth-config --set-reddit       # Reddit API credentials
osintool --auth-config --set-telegram     # Telegram telefon + API bilgileri
```

Bilgiler `~/.osintool_auth.enc` dosyasında şifrelenir.

---

### 3. Instagram Follower Graph (Recursive Crawler) 🔥

**En güçlü özellik.** Hesabına girip hedef kullanıcının takipçilerini ve takip ettiklerini çeker, sonra onların da takipçilerini çeker — zincirleme.

```bash
# Varsayılan: 2 seviye derinlik, her seviyede 5 kişi
osintool --auth hedefkullanici --auth-platforms instagram

# 3 seviye, her seviyede 15 kişi (daha derin)
osintool --auth hedefkullanici --auth-depth 3 --auth-max 15

# Sadece 1 seviye, 20 kişi (hızlı tarama)
osintool --auth hedefkullanici --auth-depth 1 --auth-max 20

# Tüm platformlarda ara (instagram + github + reddit + telegram)
osintool --auth hedefkullanici
```

**Çıktı örneği:**
```
@hedefkullanici (Ad Soyad) [15234F / 756FG]
  Takiptekiler: @kullanici1
    @kullanici1 (Kullanıcı Bir) [502F / 2054FG]
      Takiptekiler: @kullanici2
        ...
  Takip ettikleri: @kullanici3
    @kullanici3 (Kullanıcı Üç) [62181F / 6FG]
      Takip ettikleri: @kullanici4
        ...
```

Her kullanıcının profili detaylı gösterilir ve bağlantı grafı çıkarılır (kim kimi takip ediyor, kimler grafta ortak).

---

### 4. Telegram Search

```bash
# Username ile ara
osintool --auth hedefusername --auth-platforms telegram

# Telefon numarası ile ara
osintool --auth "+905551234567" --auth-platforms telegram
```

Telegram: profil fotoğrafını indirir, ortak grupları listeler, son görülme durumunu gösterir.

---

### 5. WhatsApp Web Contact Lookup

```bash
# Telefon numarası ile WhatsApp'ta ara
osintool --auth "+905551234567" --auth-platforms whatsapp
```

WhatsApp Web browser açılır. İlk seferde QR kodu telefonundan okutman gerekir. Session kaydedilir, bir daha QR istemez. Kişinin profil adı ve "about" bilgisi gösterilir.

---

### 6. Decrypt Saved Results

```bash
# GUI ile
founds

# Terminalden (headless)
founds --headless "şifren"
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OSINTOOL_PASSWORD` | `osintool_default_change_me` | Search results encryption password |
| `OSINTOOL_AUTH_PW` | `osintool_default_change_me` | Credential storage encryption password |
| `TELEGRAM_API_ID` | — | Telegram API ID (api_id) |
| `TELEGRAM_API_HASH` | — | Telegram API Hash (api_hash) |

## Security

| File | Purpose |
|------|---------|
| `~/.osintool_auth.enc` | Encrypted API keys & passwords |
| `~/.founds.dat` | Encrypted search results |
| `~/.founds.salt` | PBKDF2 salt |
| `~/.osintool_tg_session` | Telegram session file |
| `~/.osintool_wa_state/` | WhatsApp Web browser profile |

Data at rest is encrypted with **PBKDF2 + Fernet (AES-256)**. Change the default encryption password via environment variables.

## Disclaimer

This tool is for **educational and authorized security research purposes only**. Users are responsible for complying with applicable laws and platform Terms of Service.
