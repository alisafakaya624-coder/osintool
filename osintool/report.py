import os
import time
from datetime import datetime

from fpdf import FPDF


CASE_NUMBER = 0


def _next_case():
    global CASE_NUMBER
    CASE_NUMBER += 1
    return CASE_NUMBER


class CyberCrimePDF(FPDF):
    def header(self):
        self.set_font("Courier", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 4, "GIZLILIK DERECESI: KISITLI", align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Sayfa {self.page_no()}/{{nb}}  |  {datetime.now().strftime('%d/%m/%Y %H:%M')}", align="C")


def generate_report(graph_data, root_user, output_dir=None):
    if output_dir is None:
        output_dir = os.path.expanduser("~")
    os.makedirs(output_dir, exist_ok=True)

    case = _next_case()
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"siber_suc_dosyasi_{case:03d}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    pdf = CyberCrimePDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    total_users = len(graph_data)
    _add_cover(pdf, case, root_user, total_users, now)
    _add_case_summary(pdf, graph_data, root_user)
    _add_user_details(pdf, graph_data)
    _add_connection_map(pdf, graph_data)

    pdf.output(filepath)
    print(f"\n[PDF] Kaydedildi: {filepath}")
    return filepath


def _add_cover(pdf, case, root_user, total_users, now):
    pdf.add_page()
    pdf.set_font("Courier", "B", 18)
    pdf.set_text_color(180, 0, 0)
    pdf.ln(20)
    pdf.cell(0, 10, "T.C.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "SIBER SUCLARLA MUCADELE", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "SUBE MUDURLUGU", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(180, 0, 0)
    pdf.set_line_width(1)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(15)
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "SORUSTURMA DOSYASI", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Courier", "", 11)
    pdf.cell(0, 8, f"Dosya No : 2026/{case:03d}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Hedef    : @{root_user}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Tarih    : {now.strftime('%d/%m/%Y %H:%M')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Kisi     : {total_users}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(180, 0, 0)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(15)
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, "Bu belge 5271 sayili Ceza Muhakemesi Kanunu'nun 153. maddesi", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "kapsaminda gizlilik kararina tabidir.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Courier", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "--- SADECE RESMI KULLANIM ICINDIR ---", align="C", new_x="LMARGIN", new_y="NEXT")


def _add_case_summary(pdf, graph_data, root_user):
    pdf.add_page()
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 8, "1. OZET BILGILER", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_draw_color(180, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(0, 0, 0)

    root = graph_data.get(root_user, {})
    pdf.cell(0, 6, f"Hedef Kullanici : @{root_user}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Ad Soyad       : {root.get('full_name', '-')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Biyografi      : {root.get('bio', '-')[:80]}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Takipci        : {root.get('followers', 0)}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Takip          : {root.get('following', 0)}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Gizli Hesap    : {'EVET' if root.get('is_private') else 'HAYIR'}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Dogru Hesap    : {'EVET' if root.get('is_verified') else 'HAYIR'}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Profil         : {root.get('url', '-')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    total_followers = sum(d.get("followers", 0) for d in graph_data.values())
    total_following = sum(d.get("following", 0) for d in graph_data.values())
    private_count = sum(1 for d in graph_data.values() if d.get("is_private"))
    verified_count = sum(1 for d in graph_data.values() if d.get("is_verified"))

    pdf.set_draw_color(180, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Courier", "B", 10)
    pdf.cell(0, 6, "TARANAN AG ISTATISTIKLERI", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Courier", "", 10)
    pdf.ln(3)
    pdf.cell(0, 6, f"Toplam Kullanici       : {len(graph_data)}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Toplam Takipci Sayisi  : {total_followers}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Toplam Takip Sayisi    : {total_following}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Gizli Hesap Sayisi     : {private_count}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Dogru Hesap Sayisi     : {verified_count}", new_x="LMARGIN", new_y="NEXT")


def _add_user_details(pdf, graph_data):
    pdf.add_page()
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 8, "2. KULLANICI DETAYLARI", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_draw_color(180, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    for idx, (username, data) in enumerate(graph_data.items(), 1):
        if pdf.get_y() > 240:
            pdf.add_page()
            pdf.set_font("Courier", "B", 12)
            pdf.set_text_color(180, 0, 0)
            pdf.cell(0, 8, "2. KULLANICI DETAYLARI (devam)", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
            pdf.set_draw_color(180, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

        pdf.set_font("Courier", "B", 9)
        pdf.set_text_color(20, 40, 120)
        pdf.cell(0, 5, f"[{idx:03d}] @{username}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Courier", "", 8)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 4, f"    ID              : {data.get('id', '-')}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f"    Ad Soyad        : {data.get('full_name', '-')}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f"    Biyografi       : {data.get('bio', '-')[:100]}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f"    Takipci/Takip   : {data.get('followers', 0)} / {data.get('following', 0)}", new_x="LMARGIN", new_y="NEXT")
        flags = []
        if data.get("is_private"):
            flags.append("GIZLI")
        if data.get("is_verified"):
            flags.append("DOGRULANMIS")
        pdf.cell(0, 4, f"    Durum           : {' - '.join(flags) if flags else 'Acik'}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f"    Profil          : {data.get('url', '-')}", new_x="LMARGIN", new_y="NEXT")

        conns = data.get("follower_list", []) + data.get("following_list", [])
        if conns:
            conns_str = ", ".join(f"@{c}" for c in conns[:8])
            if len(conns) > 8:
                conns_str += f" ... (+{len(conns)-8} daha)"
            pdf.cell(0, 4, f"    Baglantilar     : {conns_str}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)


def _add_connection_map(pdf, graph_data):
    pdf.add_page()
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 8, "3. BAGLANTI HARITASI", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_draw_color(180, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(0, 0, 0)

    for username, data in graph_data.items():
        if pdf.get_y() > 250:
            pdf.add_page()
            pdf.set_font("Courier", "B", 12)
            pdf.set_text_color(180, 0, 0)
            pdf.cell(0, 8, "3. BAGLANTI HARITASI (devam)", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
            pdf.set_draw_color(180, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Courier", "", 8)
            pdf.set_text_color(0, 0, 0)

        pdf.set_text_color(20, 40, 120)
        pdf.cell(0, 5, f"@{username}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)

        followers = data.get("follower_list", [])
        following = data.get("following_list", [])

        if followers:
            for f in followers:
                mark = "  <<"
                mutual = " [M]" if f in graph_data else ""
                pdf.cell(0, 4, f"    {mark} @{f}{mutual}", new_x="LMARGIN", new_y="NEXT")

        if following:
            for f in following:
                mark = "  >>"
                mutual = " [M]" if f in graph_data else ""
                pdf.cell(0, 4, f"    {mark} @{f}{mutual}", new_x="LMARGIN", new_y="NEXT")

        if not followers and not following:
            pdf.cell(0, 4, "    (baglanti yok)", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(1)

    pdf.ln(5)
    pdf.set_font("Courier", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "Gosterim: << takipci, >> takip edilen, [M] bu dosyada kayitli", new_x="LMARGIN", new_y="NEXT")
