from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import QSize, Qt

class AnaliticsDialog(QDialog):
    def __init__(self, row):
        super().__init__()
        #widgets
        homeTeam = QLabel(row[2])
        homeTeam.setStyleSheet("font-size: 20px; font-weight: bold;")
        awayTeam = QLabel(row[3])
        awayTeam.setStyleSheet("font-size: 20px; font-weight: bold;")
        vs = QLabel(" VS ")
        vs.setStyleSheet("font-size: 18px; font-weight: bold;")
        ok = QPushButton("OK")
    
        
        fecha = QLabel("Match´s date: " + row[0] + "  " + row[1])

        pghd        = QLabel("PGHD: " + str(row[5]))
        pgad        = QLabel("PGAD: " + str(row[6]))
        phd         = QLabel("PHD: " + str(row[7]))
        pad         = QLabel("PAD: " + str(row[8]))
        ppghome     = QLabel("PPGHome: " + str(row[9]))
        ppgaway     = QLabel("PPGAway: " + str(row[10]))
        tgpg        = QLabel("TGPG: " + str(row[11]))
        pjhome      = QLabel("PJHome: " + str(row[12]))
        pjaway      = QLabel("PJAway: " + str(row[13]))
        rempate     = QLabel("REmpate: " + str(row[14]))
        odd1        = QLabel("Odds1: " + str(row[15]))
        odd2        = QLabel("Odds2: " + str(row[16]))
        odd_under25 = QLabel("Odds under25: " + str(row[17]))

        #conections
        ok.clicked.connect(self.close)

        #layout
        nameLayout = QHBoxLayout()
        buttonLAyout = QHBoxLayout()
        layout = QVBoxLayout()
        datosLayout = QGridLayout()

        nameLayout.addWidget(homeTeam)
        nameLayout.addStretch()
        nameLayout.addWidget(vs)
        nameLayout.addStretch()
        nameLayout.addWidget(awayTeam)

        buttonLAyout.addStretch()
        buttonLAyout.addWidget(ok)

        datosLayout.addWidget(fecha, 0, 0, 1, 1)
        datosLayout.addWidget(pghd, 1, 0, 1, 1)
        datosLayout.addWidget(pgad, 1, 1, 1, 1)
        datosLayout.addWidget(phd, 2, 0, 1, 1)
        datosLayout.addWidget(pad, 2, 1, 1, 1)
        datosLayout.addWidget(ppghome, 3, 0, 1, 1)
        datosLayout.addWidget(ppgaway, 3, 1, 1, 1)
        datosLayout.addWidget(tgpg, 4, 0, 1, 1)
        datosLayout.addWidget(rempate, 4, 1, 1, 1)
        datosLayout.addWidget(pjhome, 5, 0, 1, 1)
        datosLayout.addWidget(pjaway, 5, 1, 1, 1)
        datosLayout.addWidget(odd1, 6, 0, 1, 1)
        datosLayout.addWidget(odd2, 6, 1, 1, 1)
        datosLayout.addWidget(odd_under25, 7, 0, 1, 1)

        layout.addLayout(nameLayout)
        layout.addLayout(datosLayout)
        layout.addLayout(buttonLAyout)

        self.setLayout(layout) 