import pygame
import os

BASE_DIR = os.path.dirname(__file__)
MUSIC_DIR = os.path.join(BASE_DIR, "music")


class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self.load_playlist()

    def load_playlist(self):
        if not os.path.exists(MUSIC_DIR):
            return

        for file_name in os.listdir(MUSIC_DIR):
            if file_name.endswith(".wav") or file_name.endswith(".mp3"):
                self.playlist.append(os.path.join(MUSIC_DIR, file_name))

        self.playlist.sort()

    def play(self):
        if len(self.playlist) == 0:
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True
        else:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True

    def next_track(self):
        if len(self.playlist) == 0:
            return

        self.current_index += 1
        if self.current_index >= len(self.playlist):
            self.current_index = 0

        self.is_paused = False
        self.play()

    def previous_track(self):
        if len(self.playlist) == 0:
            return

        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.playlist) - 1

        self.is_paused = False
        self.play()

    def get_current_track_name(self):
        if len(self.playlist) == 0:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_index])

    def get_position(self):
        pos = pygame.mixer.music.get_pos()
        if pos < 0:
            return 0
        return pos // 1000