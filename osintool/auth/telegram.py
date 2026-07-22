import asyncio
import os

from colorama import Fore, Style

TELEGRAM_SESSION = os.path.expanduser("~/.osintool_tg_session")


class TelegramAuth:
    def __init__(self, credentials):
        self.phone = credentials.get("phone", "")

    def search(self, target):
        result = asyncio.run(self._async_search(target))
        return result

    async def _async_search(self, target):
        from telethon import TelegramClient, errors

        api_id = self.creds.get("api_id") or os.environ.get("TELEGRAM_API_ID", "20473423")
        api_hash = self.creds.get("api_hash") or os.environ.get("TELEGRAM_API_HASH", "")
        if not api_hash:
            print(f"{Fore.RED}[!] TELEGRAM_API_HASH not set. Set env var or use --auth-config --set-telegram{Style.RESET_ALL}")
            return

        client = TelegramClient(TELEGRAM_SESSION, int(api_id), api_hash)

        print(f"{Fore.CYAN}[Telegram] Bağlanılıyor...{Style.RESET_ALL}")
        await client.connect()

        if not await client.is_user_authorized():
            print(f"{Fore.YELLOW}[!] Telefonuna kod gönderiliyor: {self.phone}{Style.RESET_ALL}")
            await client.send_code_request(self.phone)
            code = input("Telegram'dan gelen kodu gir: ").strip()
            try:
                await client.sign_in(self.phone, code)
                print(f"{Fore.GREEN}[Telegram] Giriş başarılı{Style.RESET_ALL}")
            except errors.SessionPasswordNeededError:
                pwd = input("2FA şifreni gir: ").strip()
                await client.sign_in(password=pwd)
                print(f"{Fore.GREEN}[Telegram] 2FA ile giriş başarılı{Style.RESET_ALL}")

        if target.startswith("+"):
            try:
                user = await client.get_entity(target)
            except Exception:
                print(f"{Fore.RED}[!] Numara bulunamadı{Style.RESET_ALL}")
                await client.disconnect()
                return
        else:
            target_clean = target.lstrip("@")
            try:
                user = await client.get_entity(f"@{target_clean}")
            except Exception:
                print(f"{Fore.RED}[!] @{target_clean} bulunamadı{Style.RESET_ALL}")
                await client.disconnect()
                return

        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[Telegram] {user.first_name or ''} {user.last_name or ''}{Style.RESET_ALL}")
        print(f"{'='*50}")
        print(f"  Kullanıcı  : @{user.username or '-'}")
        print(f"  ID         : {user.id}")
        print(f"  Bio        : {getattr(user, 'about', '-') or '-'}")
        print(f"  Telefon    : {getattr(user, 'phone', '-') or '-'}")
        print(f"  Bot mu     : {'Evet' if user.bot else 'Hayır'}")

        try:
            photos = await client.get_profile_photos(user)
            if photos:
                first_photo = photos[0]
                photo_path = os.path.expanduser(f"~/.osintool_tg_{target_clean}.jpg")
                await client.download_media(first_photo, photo_path)
                print(f"  Fotoğraf   : {photo_path}")
        except Exception:
            pass

        try:
            common = await client.get_common_chats(user)
            if common:
                print(f"{Fore.YELLOW}[*] Ortak gruplar ({len(common)}):{Style.RESET_ALL}")
                for c in common[:5]:
                    print(f"    - {c.title or c.username or c.id}")
                if len(common) > 5:
                    print(f"    ... ve {len(common)-5} daha")
        except Exception:
            pass

        try:
            if hasattr(user, 'status') and user.status:
                from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserStatusRecently
                status = user.status
                if isinstance(status, UserStatusOnline):
                    print(f"  Durum      : Çevrimiçi")
                elif isinstance(status, UserStatusOffline):
                    from datetime import datetime
                    print(f"  Son görülme: {datetime.fromtimestamp(status.was_online).strftime('%Y-%m-%d %H:%M')}")
                elif isinstance(status, UserStatusRecently):
                    print(f"  Son görülme: Yakın zamanda")
                else:
                    print(f"  Durum      : Gizli")
        except Exception:
            pass

        print(f"  Profil     : https://t.me/{user.username or target_clean}")
        print(f"{'='*50}")

        await client.disconnect()
        return {"username": user.username, "id": user.id}
