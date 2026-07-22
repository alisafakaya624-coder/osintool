# OSINTool

Multi-platform OSINT search tool — username, name, and phone number lookup across 300+ sites with optional authenticated scraping.

## Features

- **Public search** — 300+ sites (username / name / phone)
- **Authenticated search** — login to platforms for deeper intel
  - Instagram (follower/following graph, recursive crawling)
  - GitHub (profile, repos, metadata)
  - Reddit (posts, comments, karma)
  - Telegram (profile, common groups, status)
  - WhatsApp Web (contact name, about)
- **Encrypted output** — results saved to `~/.founds.dat` (PBKDF2 + Fernet)
- **Encrypted credential storage** — API keys and passwords stored in `~/.osintool_auth.enc`

## Install

```bash
git clone https://github.com/alisafakaya624-coder/osintool.git
cd osintool
pip install -e .
```

Optional dependencies for authenticated search:

```bash
pip install -e .[auth]
```

## Usage

### Public search

```bash
osintool -u username           # username search (300+ sites)
osintool -n "John Doe"         # name search
osintool -p "+14155552671"     # phone search
osintool --all "query"         # try all 3 types
```

### Authenticated search

First save your credentials (stored encrypted):

```bash
osintool --auth-config --set-instagram
osintool --auth-config --set-github
osintool --auth-config --set-reddit
osintool --auth-config --set-telegram
```

Then search:

```bash
osintool --auth targetuser                     # all platforms
osintool --auth targetuser --auth-platforms instagram
osintool --auth targetuser --auth-depth 3 --auth-max 10
```

Instagram supports recursive follower/following graph crawling (default depth: 2, max: 5 per level).

### Decrypt saved results

```bash
founds --headless "your_password"
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OSINTOOL_PASSWORD` | Password for encrypting search results (default: `osintool_default_change_me`) |
| `OSINTOOL_AUTH_PW` | Password for encrypting stored credentials (default: `osintool_default_change_me`) |
| `TELEGRAM_API_ID` | Telegram API ID (optional, can be stored in config) |
| `TELEGRAM_API_HASH` | Telegram API Hash (optional, can be stored in config) |

## Security

- Credentials are stored encrypted at `~/.osintool_auth.enc` using PBKDF2 + Fernet (AES-256)
- Search results are saved encrypted at `~/.founds.dat`
- Session files (Telegram, WhatsApp) are stored in `~/.osintool_tg_session` and `~/.osintool_wa_state`
- Change the default encryption password via environment variables
