import asyncio
import flet as ft
import pygame.mixer

from voice_generator import generate_audio
from audio_player import AudioPlayer

class VoiceApp:
    def __init__(self, page: ft.Page):
        self.buttons = None
        self.convert_button = None
        self.text_field = None
        self.page = page
        self.audio_player = None
        self.is_paused = False
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        self.page.title = "Text to Speech Manager"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.width = 620
        self.page.window.height = 500
        self.page.window.resizable = False
        self.page.window.prevent_close = True
        self.page.window.on_event = self.handle_window_event

    def setup_ui(self):
        self.text_field = ft.TextField(
            label="Enter text to play",
            width=600,
            multiline=True,
            min_lines=10,
            max_lines=10
        )
        self.page.add(self.text_field)

        self.convert_button = ft.Button(
            text="Convert",
            width=100,
            height=50,
            on_click=self.convert_button_handler,
        )
        self.page.add(self.convert_button)

        self.buttons = ft.Row(
            controls=[
                ft.Button(
                    content=ft.Icon(name=ft.icons.REPLAY_10_SHARP),
                    width=50,
                    height=50,
                    on_click=self.jump_backward_button_handler
                ),
                ft.Button(
                    content=ft.Icon(name=ft.icons.PLAY_ARROW),
                    width=50,
                    height=50,
                    on_click=self.play_button_handler
                ),
                ft.Button(
                    content=ft.Icon(name=ft.icons.FORWARD_10),
                    width=50,
                    height=50,
                    on_click=self.jump_forward_button_handler
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        self.page.add(self.buttons)

    async def create_check_playback_status(self):
        asyncio.create_task(self.check_playback_status())

    async def check_playback_status(self):
        while True:
            if self.audio_player and not self.is_paused:
                if not pygame.mixer.music.get_busy():
                    self.audio_player.unload()
                    self.audio_player = None
                    play_button = self.buttons.controls[1]
                    play_button.content = ft.Icon(name=ft.icons.PLAY_ARROW)
                    play_button.update()
            await asyncio.sleep(1)

    async def convert_button_handler(self, e):
        if self.audio_player:
            self.audio_player.stop()
            self.audio_player = None

        if not self.text_field.value.strip():
            return

        output_file = await generate_audio(self.text_field.value)
        self.audio_player = AudioPlayer(output_file)

        play_button = self.buttons.controls[1]
        play_button.content = ft.Icon(name=ft.icons.PAUSE)
        play_button.update()

    def play_button_handler(self, e):
        if not self.audio_player:
            return

        play_button = self.buttons.controls[1]

        if self.audio_player.is_playing:
            play_button.content = ft.Icon(name=ft.icons.PLAY_ARROW)
            self.is_paused = True
            self.audio_player.pause()
        else:
            play_button.content = ft.Icon(name=ft.icons.PAUSE)
            self.is_paused = False
            self.audio_player.resume()

        play_button.update()

    def handle_window_event(self, e):
        if e.data == "close":
            if self.audio_player:
                self.audio_player.stop()
            self.page.window.destroy()

    def jump_forward_button_handler(self, e):
        if self.audio_player:
            self.audio_player.jump_forward()

    def jump_backward_button_handler(self, e):
        if self.audio_player:
            self.audio_player.jump_backward()