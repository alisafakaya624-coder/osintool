# OSINTool

Multi-platform OSINT search tool — username, name, and phone number lookup across 300+ sites with **authenticated scraping** and **recursive Instagram follower graph crawling**.

## Features

- **Public search** — 300+ sites (username / name / phone)
- **Authenticated search** — login with your own accounts for deep intel
  - **Instagram** — recursive follower/following graph crawler (multi-level)
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

### 1. Public Search (300+ sites)

```bash
# Search username across 300+ platforms
osintool -u targetuser

# Search by full name
osintool -n "John Doe"

# Search by phone number
osintool -p "+14155552671"

# Try all types with the same query
osintool --all "targetuser"
```

---

### 2. Authenticated Search

Save your credentials first (stored encrypted):

```bash
osintool --auth-config --set-instagram    # Instagram email + password
osintool --auth-config --set-github       # GitHub personal access token
osintool --auth-config --set-reddit       # Reddit API credentials
osintool --auth-config --set-telegram     # Telegram phone + API credentials
```

Credentials are encrypted and stored in `~/.osintool_auth.enc`.

---

### 3. Instagram Follower Graph (Recursive Crawler) 🔥

Logs into your account and crawls the target's followers/following recursively — building a complete connection graph.

```bash
# Default: 2 levels deep, 5 users per level
osintool --auth targetuser --auth-platforms instagram

# 3 levels deep, 15 users per level (deeper crawl)
osintool --auth targetuser --auth-depth 3 --auth-max 15

# 1 level, 20 users (quick scan)
osintool --auth targetuser --auth-depth 1 --auth-max 20

# Search across all platforms (instagram + github + reddit + telegram)
osintool --auth targetuser
```

**Sample output:**
```
@targetuser (Full Name) [15234F / 756FG]
  Followers: @user1
    @user1 (User One) [502F / 2054FG]
      Followers: @user2
        ...
  Following: @user3
    @user3 (User Three) [62181F / 6FG]
      Following: @user4
        ...
```

Each user's profile is shown in detail (bio, follower counts, private/verified status), and the connection graph maps who follows whom.

---

### 4. Telegram Search

```bash
# Search by username
osintool --auth targetuser --auth-platforms telegram

# Search by phone number
osintool --auth "+905551234567" --auth-platforms telegram
```

Telegram: downloads profile photo, lists common groups, shows last seen status.

---

### 5. WhatsApp Web Contact Lookup

```bash
# Search a phone number on WhatsApp
osintool --auth "+905551234567" --auth-platforms whatsapp
```

Opens WhatsApp Web in a browser. First time requires QR code scan from your phone. Session is saved — no QR needed afterwards. Shows contact name and "about" info.

---

### 6. Decrypt Saved Results

```bash
# GUI mode
founds

# Headless (CLI mode)
founds --headless "your_password"
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OSINTOOL_PASSWORD` | `osintool_default_change_me` | Password for encrypting search results |
| `OSINTOOL_AUTH_PW` | `osintool_default_change_me` | Password for encrypting stored credentials |
| `TELEGRAM_API_ID` | — | Telegram API ID (optional, can be stored in config) |
| `TELEGRAM_API_HASH` | — | Telegram API Hash (optional, can be stored in config) |

## Security

| File | Purpose |
|------|---------|
| `~/.osintool_auth.enc` | Encrypted API keys & passwords (PBKDF2 + Fernet) |
| `~/.founds.dat` | Encrypted search results |
| `~/.founds.salt` | PBKDF2 salt |
| `~/.osintool_tg_session` | Telegram session file |
| `~/.osintool_wa_state/` | WhatsApp Web browser profile |

All stored data is encrypted with **PBKDF2 + Fernet (AES-256)**. Change the default encryption password via environment variables.

## Disclaimer

This tool is for **educational and authorized security research purposes only**. Users are responsible for complying with applicable laws and platform Terms of Service.
