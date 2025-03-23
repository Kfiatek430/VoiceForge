import os
import pygame

pygame.mixer.init()

class AudioPlayer:
    def __init__(self, file):
        self.file = file
        self.is_playing = False
        self.playback_position = 0
        self.length = 0
        self.load_audio()

    def load_audio(self):
        pygame.mixer.music.load(self.file)
        self.length = pygame.mixer.Sound(self.file).get_length()
        self.play()

    def play(self):
        if not self.is_playing:
            pygame.mixer.music.play(start=self.playback_position)
            self.is_playing = True

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def resume(self):
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
        self.unload()

    def unload(self):
        pygame.mixer.music.unload()
        self.is_playing = False
        self.playback_position = 0
        if os.path.exists(self.file):
            try:
                os.remove(self.file)
            except Exception as e:
                print(f"Failed to remove file {self.file}: {e}")

    def jump_forward(self, seconds=10):
        self.playback_position = min(self.playback_position + seconds, self.length)
        self.update_playback()

    def jump_backward(self, seconds=10):
        self.playback_position = max(self.playback_position - seconds, 0)
        self.update_playback()

    def update_playback(self):
        if self.is_playing:
            self.pause()
            pygame.mixer.music.set_pos(self.playback_position)
            self.resume()
        else:
            pygame.mixer.music.play(start=self.playback_position)

    def set_position(self, position):
        self.playback_position = position
        self.update_playback()

    def get_current_position(self):
        if self.is_playing:
            return self.playback_position + pygame.mixer.music.get_pos() / 1000
        return self.playback_position