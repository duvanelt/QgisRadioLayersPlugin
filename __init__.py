from .radioLayers import RadioLayersPlugin

def classFactory(iface):
    return RadioLayersPlugin(iface)