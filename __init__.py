from .qwmsship import QWmsShipPlugin

def classFactory(iface):
    return QWmsShipPlugin(iface)