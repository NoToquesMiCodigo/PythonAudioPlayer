
from PySide import QtCore, QtGui, phonon, QtUiTools
from PySide.phonon import Phonon

from videopanel import player


class Reproductor(QtGui.QWidget):

    def __init__(self):
        super(Reproductor, self).__init__(parent=None)
        self.setWindowTitle("Python Simple Player")
        self.gridLayout = QtGui.QGridLayout(self)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile("repro.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()
        self.gridLayout.addWidget(self.ui, 0, 0, 1, 1)
        # seccion multimedia
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.setTickInterval(1000)
        #
        self.ui.lcdAvance.display("00:00")
        QtCore.QObject.connect(
            self.ui.btnArchivo,
            QtCore.SIGNAL("clicked()"),
            self.openFile)
        QtCore.QObject.connect(
            self.ui.btnPlay,
            QtCore.SIGNAL("clicked()"),
            self.play)
        self.mediaObject.tick.connect(self.alAvanzar)
        self.mediaObject.stateChanged.connect(self.alCambiarEstado)
        #----------------------
        self.player = None

    def alAvanzar(self, tiempo):
        displayTime = QtCore.QTime(
            0, (tiempo / 60000) %
            60, (tiempo / 1000) %
            60)
        self.ui.lcdAvance.display(displayTime.toString('mm:ss'))

    def alCambiarEstado(self, new, old):
        if self.mediaObject.state() == Phonon.State.StoppedState:
            self.ui.btnPlay.setEnabled(True)
        elif self.mediaObject.state() == Phonon.State.PlayingState:
            self.ui.btnPlay.setText("||")  # .setEnabled(False)

    def play(self):
        if self.player:
            if self.player.state() == Phonon.State.PlayingState:
                self.player.pause()
                self.player.show()
                self.ui.btnPlay.setText(">")
            else:
                self.player.show()
                self.player.play()
                self.ui.lblNombre.setText(self.player.file_path)
                self.ui.btnPlay.setText("||")
        else:
            if self.mediaObject.state() == Phonon.State.PlayingState:
                self.mediaObject.pause()
                self.ui.btnPlay.setText(">")
            else:
                self.mediaObject.play()
                #///////////////////////////////////
                meta = self.mediaObject.metaData()
                print(meta)
                meta["TITLE"] = meta[
                    "TITLE"] if "TITLE" in meta else "Indefinido"
                meta["ARTIST"] = meta[
                    "ARTIST"] if "ARTIST" in meta else "SinNombre"
                label = "{TITLE} by {ARTIST}".format(**meta)
                self.ui.lblNombre.setText(label)
                #///////////////////////////////////
                self.ui.btnPlay.setText("||")

    def openFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self,
            u"Abrir Archivo",
            u".",
            u"Archivos de Audio (*.mp3 *.wav *.ogg);;Archivos de Video (*.mp4 *.mpg *.avi)")
        if fileName[1]:
            self.path = fileName[0]
            self.mediaObject.setCurrentSource(
                Phonon.MediaSource(self.path))
            self.ui.btnPlay.setText(">")
            self.ui.lblNombre.setText("...")
            self.ui.lcdAvance.display("00:00")
            if fileName[0][-3:] in "mp4 mpg avi".split():
                self.player = player(fileName[0])
                self.player.alAvanzar = self.alAvanzar
                self.player.alCambiarEstado = self.alCambiarEstado
            else:
                self.player = None

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    rep = Reproductor()
    rep.show()
    sys.exit(app.exec_())
