import asyncio

import flet as ft

from voice_generator import generate_audio

class VoiceApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Text to Speech Manager"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.width = 620
        self.page.window.height = 500
        self.page.window.resizable = False

        self.is_playing = False

        self.setup_ui()

    def setup_ui(self):
        self.text_field = ft.TextField(
            label="Enter text to play",
            width=600,
            multiline=True,
            min_lines=10,
        )
        self.page.add(self.text_field)

        self.convert_button = ft.Button(
            text="Convert",
            width=100,
            height=50,
            on_click=self.convert_button_handler,
        )
        self.page.add(self.convert_button)

        self.slider = ft.Slider(
            min=0,
            max=100,
            value=0,
            divisions=100,
            width=600,
            label="{value}%"
        )
        self.page.add(self.slider)

        self.buttons = ft.Row(
            controls=[
                ft.Button(
                    content=ft.Icon(name=ft.icons.REPLAY_10_SHARP),
                    width=50,
                    height=50,
                ),
                ft.Button(
                    content=ft.Icon(name=ft.icons.PLAY_ARROW),
                    width=50,
                    height=50,
                    on_click=self.play_button_handler,
                ),
                ft.Button(
                    content=ft.Icon(name=ft.icons.FORWARD_10),
                    width=50,
                    height=50,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        self.page.add(self.buttons)

    def convert_button_handler(self, e):
        output_file = asyncio.run(generate_audio(self.text_field.value))

    def play_button_handler(self, e):
        self.is_playing = not self.is_playing

        play_button = self.buttons.controls[1]

        if self.is_playing:
            play_button.content = ft.Icon(name=ft.icons.PAUSE)
        else:
            play_button.content = ft.Icon(name=ft.icons.PLAY_ARROW)

        play_button.update()