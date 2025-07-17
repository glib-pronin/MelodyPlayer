import pygame.mixer as mixer

class AudioPlayer:
    def __init__(self):
        mixer.init()

    def play_track(self, filepath):
        self.stop()
        mixer.music.load(filepath)
        mixer.music.play()

    def pause(self):
        mixer.music.pause()

    def resume(self):
        mixer.music.unpause()

    def set_volume(self, volume):
        mixer.music.set_volume(volume/100)

    def stop(self):
        mixer.music.stop()

    def get_track_position(self):
        return mixer.music.get_pos()
    
    def is_track_busy(self):
        return mixer.music.get_busy()