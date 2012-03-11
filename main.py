#!/usr/bin/env python
# encoding: utf-8

import sys
try:
    from PyQt4.Qt import *
except ImportError as e:
    print "Falta instalar python-qt4"
    sys.exit()

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from datetime import datetime
def ahora():
    return datetime.now().strftime('%H:%M:%S')
    
class Echo(Protocol, QObject):
    '''
    El protocolo tambien es un QObject que puede emitir señales
    '''
    lectura = pyqtSignal(str)
    

    def connectionMade(self):
        print dir(self.transport)
        self.lectura.emit("Conexion con %s" % self.transport)
        

    def dataReceived(self, data):
        data = data.strip() # Sacar el \n del final
        self.lectura.emit(data)
        self.transport.write("Usted dijo: %s\n" % data)
        
        
class EchoFactory(Factory):
    def __init__(self, ventana):
        '''Constructor del factory'''
        self.ventana = ventana
        
    def buildProtocol(self, addr):
        """Crear una instancia de protocolo para atender la conexion"""
        protocol = Echo()
        # Conexión de la señal
        protocol.lectura.connect(self.ventana.protocolLectura)    
        return protocol
        
class Ventana(QWidget):
    '''
    La ventana es también el que instancia los prtocolos (ProtocolFactory)
    '''
    def __init__(self, padre = None):
        """docstring for __init__"""
        QWidget.__init__(self, padre) # Llamar al superconstructor
        self.setWindowTitle("Twisted + PyQt4")
        self.setupUi() # Construir la interfase
        
    def setupUi(self):
        """Construir la GUI"""
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Prueba de eco con Qt"))
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setReadOnly(True)
        layout.addWidget(self.plainTextEdit)
        layout.addWidget(QLabel(u'<b>Para conectarse al chat, inicar una sesión con:<br>'
            '<a href="#">telnet localhost 8888</a>'
            '</b>'))
        self.setLayout(layout)
        
    def protocolConectado(self, arg):
        """docstring for protocolConectado"""
        self.plainTextEdit.appendPlainText(arg)
    
    def protocolLectura(self, arg):
        """Un protocolo leyó algo"""
        print self.sender()
        self.plainTextEdit.appendPlainText("[%s] %s" % (ahora(), arg))
    
    
    
    
def main():
    app = QApplication(sys.argv)
    from qt4reactor import QTReactor
    # Código de install, crea un reactor que interactua
    # con Qt
    from twisted.internet import main
    reactor = QTReactor(app=app)
    main.installReactor(reactor)
    # Crear la ventana
    win = Ventana()
    # Mostrarla
    win.show()
    # Agregar un protocol factory para las conexiones
    # al puerto 8888
    factory = EchoFactory(ventana = win)
    reactor.listenTCP(8888, factory)
    
    # Ejecutar el bucle principal de twisted
    reactor.run() # En vez de app.exec_()
    

if __name__ == '__main__':
    sys.exit(main())