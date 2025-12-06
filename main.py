import flet as ft
import time
import webbrowser
import wikipedia
import random

# --- HENEN V5.0 (LITE APK SÜRÜMÜ) ---

def main(page: ft.Page):
    # --- AYARLAR ---
    try:
        wikipedia.set_lang("tr")
        page.title = "HENEN"
        page.theme_mode = "dark"
        page.padding = 0
        page.bgcolor = "#0F172A" 
    except: pass

    # --- Görsel Bileşenler ---
    header = ft.Container(
        content=ft.Row([
            ft.Icon(name="android", color="#38BDF8", size=30), 
            ft.Text("HENEN", size=25, weight="bold", color="white"),
            ft.Container(expand=True), 
            ft.Icon(name="wifi", color="white54", size=20),
        ], alignment="center"),
        padding=20,
        bgcolor="#1E293B", 
    )

    chat_log = ft.Column(scroll="auto", expand=True, auto_scroll=True, spacing=15)
    
    # Mesaj Yazma Kutusu (Klavye için)
    txt_input = ft.TextField(
        hint_text="Bir şeyler sor...",
        border_radius=20,
        bgcolor="#1E293B",
        color="white",
        expand=True,
        border_color="transparent"
    )

    # --- Mesaj Ekleme ---
    def mesaj_ekle(mesaj, kimden="HENEN"):
        align = "start" if kimden == "HENEN" else "end"
        bg_renk = "#1E293B" if kimden == "HENEN" else "#0284C7" 
        chat_log.controls.append(
            ft.Row(
                controls=[ft.Container(content=ft.Text(f"{mesaj}", size=15, color="white"), padding=15, border_radius=20, bgcolor=bg_renk, width=250)],
                alignment=align
            )
        )
        page.update()

    # --- KOMUT MERKEZİ ---
    def cevapla(e):
        soru = txt_input.value
        if not soru: return
        
        mesaj_ekle(soru, "Sen")
        txt_input.value = ""
        page.update()
        
        # Basit Cevaplar
        komut = soru.lower()
        if "merhaba" in komut: mesaj_ekle("Merhaba İnanç! Telefonda çalışıyorum.")
        elif "nasılsın" in komut: mesaj_ekle("Süperim! APK testi başarılı.")
        elif "youtube" in komut: 
            mesaj_ekle("YouTube açılıyor...")
            webbrowser.open("https://youtube.com")
        elif "kimsin" in komut: mesaj_ekle("Ben HENEN, senin asistanınım.")
        else:
            try:
                mesaj_ekle("Wikipedia'ya bakıyorum...")
                ozet = wikipedia.summary(komut, sentences=1)
                mesaj_ekle(ozet)
            except:
                mesaj_ekle("Bunu bilemedim.")

    # --- Gönder Butonu ---
    btn_send = ft.IconButton(icon="send", icon_color="#38BDF8", on_click=cevapla)

    # --- Alt Panel ---
    bottom_bar = ft.Container(
        content=ft.Row([txt_input, btn_send], alignment="center"),
        padding=10,
        bgcolor="#0F172A",
    )

    page.add(ft.Column([header, ft.Container(content=chat_log, padding=20, expand=True), bottom_bar], spacing=0, expand=True))
    mesaj_ekle("HENEN Hazır! Klavyeden yazabilirsin.")

ft.app(target=main)