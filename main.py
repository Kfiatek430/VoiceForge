from voice_app import VoiceApp
import flet as ft

async def main(page: ft.Page):
    voice_app = VoiceApp(page)
    await voice_app.create_check_playback_status()

if __name__ == '__main__':
    ft.app(target=main)