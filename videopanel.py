#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PySide.QtGui import QApplication
from PySide.phonon import Phonon
from PySide import QtCore, QtGui


class player(Phonon.VideoWidget):

    def __init__(self, file_path):
        super(player, self).__init__(parent=None)
        self.setWindowTitle("Video")
        QtGui.QApplication.addLibraryPath(
            os.path.join(os.path.dirname(__file__), 'plugins'))
        media_src = Phonon.MediaSource(file_path)
        self.file_path = file_path
        media_obj = Phonon.MediaObject()
        media_obj.setCurrentSource(media_src)
        Phonon.createPath(media_obj, self)
        self.media_obj = media_obj
        audio_out = Phonon.AudioOutput(Phonon.VideoCategory)
        Phonon.createPath(media_obj, audio_out)
        self.audio_out = audio_out
        self.media_obj.setTickInterval(1000)
        self.media_obj.tick.connect(self.alAvanzar)
        self.media_obj.stateChanged.connect(self.alCambiarEstado)

    def alAvanzar(self, tiempo):
        pass

    def alCambiarEstado(self, new, old):
        pass

    def play(self):
        self.media_obj.play()

    def pause(self):
        self.media_obj.pause()

    def stop(self):
        self.media_obj.stop()

    def state(self):
        return self.media_obj.state()


if __name__ == "__main__":
    app = QApplication([])
    p = player(file_path=os.path.join(os.path.dirname(__file__), 'steve.mp4'))
    p.show()
    p.play()
    app.exec_()
