import flet as ft
import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import threading
import time
import webbrowser
import wikipedia
import datetime
import random

# --- HENEN V4.1 (MOBİL UYUMLU SÜRÜM) ---

def main(page: ft.Page):
    # --- AYARLAR ---
    wikipedia.set_lang("tr")
    page.title = "HENEN"
    page.theme_mode = "dark"
    page.window_width = 360   
    page.window_height = 740  
    # Telefondan girince otomatik tam ekran olsun
    page.window_resizable = True 
    page.padding = 0
    page.bgcolor = "#0F172A" 

    r = sr.Recognizer()

    # --- KİŞİSEL BİLGİLER ---
    kullanici_bilgisi = {
        "isim": "İnanç",
        "yas": "20",
        "dogum_gunu": "29 Nisan",
        "memleket": "Erzurum, Hınıs",
        "yasam_yeri": "Denizli, Pamukkale",
        "okul": "Pamukkale Üniversitesi, Sosyal Bilgiler Öğretmenliği 3. Sınıf",
        "takim": "Fenerbahçe",
        "renk": "Mavi"
    }

    # --- Görsel Bileşenler ---
    header = ft.Container(
        content=ft.Row([
            ft.Icon(name="android", color="#38BDF8", size=30), 
            ft.Text("HENEN", size=25, weight="bold", color="white", font_family="Segoe UI"),
            ft.Container(expand=True), 
            ft.Icon(name="wifi", color="white54", size=20),
            ft.Icon(name="battery_full", color="white54", size=20),
        ], alignment="center"),
        padding=ft.padding.only(left=20, right=20, top=15, bottom=15),
        bgcolor="#1E293B", 
    )

    chat_log = ft.Column(scroll="auto", expand=True, auto_scroll=True, spacing=15)
    
    chat_container = ft.Container(
        content=chat_log,
        padding=20,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#0F172A", "#000000"],
        )
    )

    durum_metni = ft.Text("Dokun ve konuş...", color="#94A3B8", size=14)

    # --- Ses Çalma (Mobil Uyumlu) ---
    def ses_cal(metin):
        def thread_ses():
            try:
                # Mobilde dosya yolları farklıdır, basit isim yeterli
                dosya_ismi = "yanit.mp3"
                tts = gTTS(text=metin, lang='tr')
                tts.save(dosya_ismi)
                
                pygame.mixer.init()
                pygame.mixer.music.load(dosya_ismi)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy(): 
                    pygame.time.Clock().tick(10)
                
                pygame.mixer.quit()
                try: os.remove(dosya_ismi)
                except: pass
            except Exception as e: 
                print(f"Ses Hatası: {e}")
        threading.Thread(target=thread_ses, daemon=True).start()

    # --- Mesaj Ekleme ---
    def mesaj_ekle(mesaj, kimden="HENEN"):
        try:
            align = "start" if kimden == "HENEN" else "end"
            bg_renk = "#1E293B" if kimden == "HENEN" else "#0284C7" 
            yazi_renk = "#FFFFFF"
            radius = ft.border_radius.only(top_left=20, top_right=20, bottom_left=0 if kimden=="HENEN" else 20, bottom_right=20 if kimden=="HENEN" else 0)

            chat_log.controls.append(
                ft.Row(
                    controls=[ft.Container(content=ft.Text(f"{mesaj}", size=15, color=yazi_renk), padding=15, border_radius=radius, bgcolor=bg_renk, width=250)],
                    alignment=align
                )
            )
            page.update()
            if kimden == "HENEN": ses_cal(mesaj)
        except: pass

    # --- KOMUT MERKEZİ ---
    def komut_islet(komut):
        komut = komut.lower()
        
        # 1. HAFIZA
        if "adım ne" in komut or "kimim ben" in komut:
            mesaj_ekle(f"Sen {kullanici_bilgisi['isim']}. {kullanici_bilgisi['yas']} yaşındasın.")
        elif "takım" in komut:
            mesaj_ekle(f"En büyük {kullanici_bilgisi['takim']}!")
        elif "nereliyim" in komut:
            mesaj_ekle(f"{kullanici_bilgisi['memleket']} doğumlusun.")
        elif "okul" in komut:
            mesaj_ekle(f"{kullanici_bilgisi['okul']} öğrencisisin.")

        # 2. ARAMA (Mobil)
        elif "ara" in komut:
            # Mobilde "tel:" linki telefon uygulamasını açar
            if "kudret" in komut: webbrowser.open("tel:05550000000")
            elif "baba" in komut: webbrowser.open("tel:05320000000")
            else: mesaj_ekle("Kimi arayacağımı tam anlamadım.")

        # 3. HARİTA
        elif "neredeyim" in komut or "konum" in komut:
            mesaj_ekle("Haritalar açılıyor...")
            webbrowser.open("geo:0,0?q=") # Mobilde harita uygulamasını tetikler

        # 4. WEB / YOUTUBE
        elif "youtube" in komut:
            mesaj_ekle("YouTube açılıyor...")
            webbrowser.open("https://youtube.com")
        elif "google" in komut:
            mesaj_ekle("Google açılıyor...")
            webbrowser.open("https://google.com")
        
        # 5. HAVA DURUMU
        elif "hava durumu" in komut:
             mesaj_ekle("Hava durumu açılıyor...")
             webbrowser.open("https://www.google.com/search?q=hava+durumu+denizli")

        # 6. SOHBET
        elif "merhaba" in komut: mesaj_ekle("Merhaba İnanç!")
        elif "nasılsın" in komut: mesaj_ekle("Süperim!")
        elif "kapat" in komut: 
            mesaj_ekle("Uygulamadan çıkılıyor...")
            time.sleep(1)
            page.window_close()
            
        else:
            # Anlamazsa Wikipedia'ya sorsun
            try:
                mesaj_ekle("Bunu araştırıyorum...")
                aranan = komut.replace("kimdir","").replace("nedir","").strip()
                ozet = wikipedia.summary(aranan, sentences=1)
                mesaj_ekle(ozet)
            except:
                mesaj_ekle("Bunu tam anlayamadım.")

    # --- DİNLEME ---
    def dinleme_islemi():
        try:
            mic_button.content.color = "#38BDF8" 
            mic_button.bgcolor = "#1E293B"
            durum_metni.value = "Dinliyorum..."
            page.update()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source, timeout=4, phrase_time_limit=5)
            
            durum_metni.value = "İşleniyor..."
            page.update()

            text = r.recognize_google(audio, language='tr-TR')
            mesaj_ekle(text, "Sen")
            komut_islet(text)

        except sr.UnknownValueError:
            durum_metni.value = "Anlaşılamadı."
        except Exception as e:
            # Telefondaki hata mesajını görmek için
            print(e) 
            durum_metni.value = "Hata."
        
        finally:
            time.sleep(0.5)
            mic_button.content.color = "white"
            mic_button.bgcolor = "#0EA5E9" 
            durum_metni.value = "Dokun ve konuş..."
            page.update()

    def butona_basildi(e):
        threading.Thread(target=dinleme_islemi, daemon=True).start()

    # --- Arayüz ---
    mic_button = ft.Container(
        content=ft.Icon(name="mic", color="white", size=30),
        width=70, height=70,
        bgcolor="#0EA5E9", 
        border_radius=35, 
        on_click=butona_basildi,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=15, color="#0EA5E9"), 
    )
    
    mic_border = ft.Container(content=mic_button, padding=5, border_radius=50)
    bottom_bar = ft.Container(content=ft.Column([durum_metni, ft.Container(height=10), mic_border], horizontal_alignment="center"), padding=20, bgcolor="#0F172A")

    page.add(ft.Column([header, chat_container, bottom_bar], spacing=0, expand=True))
    mesaj_ekle("HENEN Mobile Hazır! APK Yapabiliriz.")

ft.app(target=main)