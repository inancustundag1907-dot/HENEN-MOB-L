import flet as ft

def main(page: ft.Page):
    page.title = "Test APK"
    page.bgcolor = "#0F172A"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    page.add(
        ft.Icon(name="check_circle", size=100, color="green"),
        ft.Text("BAŞARDIN İNANÇ!", size=30, color="white", weight="bold"),
        ft.Text("Bu APK çalışıyor.", size=20, color="grey")
    )

ft.app(target=main)