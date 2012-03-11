# encoding: utf-8
try:
    from PyQt4.Qt import *
except ImportError as e:
    print "Falta instalar python-qt4"
    sys.exit()
    
import sys

def main():
    '''
    Crear una aplicaicon, una ventana y un layout con un label y un boton
    '''
    app = QApplication(sys.argv)
    win = QWidget()
    layout = QVBoxLayout() # Disposición vertical
    layout.addWidget(QLabel("Hola mundo"))
    botonCerrar = QPushButton(u"Botón")
    botonCerrar.pressed.connect(app.quit)
    layout.addWidget(botonCerrar)
    win.setLayout(layout)
    win.show()
    return app.exec_()
    
if __name__ == '__main__':
    main()
    