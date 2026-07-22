import asyncio
import os
import time

from colorama import Fore, Style

WHATSAPP_STATE = os.path.expanduser("~/.osintool_wa_state")


class WhatsAppAuth:
    def __init__(self, credentials=None):
        self.creds = credentials or {}
        self.browser = None
        self.page = None

    def search(self, target):
        result = asyncio.run(self._async_search(target))
        return result

    async def _async_search(self, target):
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            user_dir = WHATSAPP_STATE
            os.makedirs(user_dir, exist_ok=True)

            self.browser = await pw.chromium.launch_persistent_context(
                user_data_dir=user_dir,
                headless=False,
                no_viewport=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )

            self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()

            print(f"{Fore.CYAN}[WhatsApp] Web açılıyor...{Style.RESET_ALL}")
            await self.page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")

            try:
                await self.page.wait_for_selector(
                    'div[contenteditable="true"][data-tab="3"]',
                    timeout=120000,
                )
                print(f"{Fore.GREEN}[WhatsApp] Giriş başarılı{Style.RESET_ALL}")
            except Exception:
                print(f"{Fore.YELLOW}[!] QR kodunu telefonundan tara (120sn){Style.RESET_ALL}")
                try:
                    await self.page.wait_for_selector(
                        'div[contenteditable="true"][data-tab="3"]',
                        timeout=120000,
                    )
                    print(f"{Fore.GREEN}[WhatsApp] Giriş başarılı{Style.RESET_ALL}")
                except Exception:
                    print(f"{Fore.RED}[!] QR zaman aşımı{Style.RESET_ALL}")
                    await self.browser.close()
                    return

            await self.page.wait_for_timeout(2000)

            search_box = await self.page.wait_for_selector(
                'div[contenteditable="true"][data-tab="3"]',
                timeout=10000,
            )
            await search_box.click()
            await search_box.fill("")

            await self.page.keyboard.type(target, delay=50)
            await self.page.wait_for_timeout(3000)

            try:
                contact = await self.page.wait_for_selector(
                    f'//span[@dir="auto" and contains(text(), "{target[-7:]}")]',
                    timeout=8000,
                    state="visible",
                )
                await contact.click()
            except Exception:
                contact = await self.page.wait_for_selector(
                    'div[role="listitem"]',
                    timeout=8000,
                )
                if contact:
                    await contact.click()
                else:
                    print(f"{Fore.RED}[!] Numara bulunamadı: {target}{Style.RESET_ALL}")
                    await self.browser.close()
                    return

            await self.page.wait_for_timeout(2000)

            try:
                header_name = await self.page.wait_for_selector(
                    'header span[dir="auto"]',
                    timeout=5000,
                )
                name = await header_name.inner_text()
            except Exception:
                name = target

            await header_name.click()
            await self.page.wait_for_timeout(1500)

            print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[WhatsApp] {name}{Style.RESET_ALL}")
            print(f"{'='*50}")

            try:
                about_el = await self.page.query_selector(
                    'span[data-testid="profile-info-about"]'
                )
                if about_el:
                    about = await about_el.inner_text()
                    print(f"  About   : {about}")
            except Exception:
                pass

            print(f"  Numara  : {target}")
            print(f"{'='*50}")

            print(f"{Fore.YELLOW}[*] Enter'a basınca kapanır...{Style.RESET_ALL}")
            input()

            await self.browser.close()
            return {"name": name, "phone": target}
