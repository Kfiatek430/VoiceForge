from voice_app import VoiceApp
import flet as ft

def main(page: ft.Page):
    VoiceApp(page)

if __name__ == '__main__':
    ft.app(target=main)