from pathlib import Path
from PyQt5.QtWidgets import QAction
from qgis.core import QgsProject, QgsLayerTreeLayer, QgsLayerTreeGroup

class QWmsShipPlugin:

    def __init__(self, iface):

        # Gives the plugin access to the QGIS interface (iface)
        self.iface = iface
        self.actions = []

    # Called whe the plugin is loaded by Qgis
    def initGui(self):

        # Found logofiles path
        resources = Path(Path(__file__).parent, 'resources')
        icon_load = str(Path(resources, 'logo.png'))

        # Récupère l'arbre racine des couches du projet
        self.root_group = QgsProject.instance().layerTreeRoot()

        # Add buttons
        self.button_SwAlti3D_Mono = QAction('A3D 1', self.iface.mainWindow())
        self.button_SwAlti3D_Multi = QAction('A3D *', self.iface.mainWindow())
        self.button_SwSurf3D_Multi = QAction('S3D *', self.iface.mainWindow())
        self.button_SwSurf3D_Mono = QAction('S3D 1', self.iface.mainWindow())
        self.button_SWISSIMAGE_2023 = QAction('2023', self.iface.mainWindow())
        self.button_SWISSIMAGE_2020 = QAction('2020', self.iface.mainWindow())
        self.button_SWISSIMAGE_2017 = QAction('2017', self.iface.mainWindow())
        self.button_SWISSIMAGE_2014 = QAction('2014', self.iface.mainWindow())
        self.button_SWISSIMAGE_2012 = QAction('2012', self.iface.mainWindow())
        self.button_SWISSIMAGE_2009 = QAction('2009', self.iface.mainWindow())
        self.button_SWISSIMAGE_2005 = QAction('2005', self.iface.mainWindow())
        self.button_SWISSIMAGE_2000 = QAction('2000', self.iface.mainWindow())

        self.button_SWISSIMAGE_1995 = QAction('1995', self.iface.mainWindow())
        self.button_SWISSIMAGE_1985 = QAction('1985', self.iface.mainWindow())
        self.button_SWISSIMAGE_1977 = QAction('1977', self.iface.mainWindow())
        self.button_SWISSIMAGE_1968 = QAction('1968', self.iface.mainWindow())
        self.button_SWISSIMAGE_1960 = QAction('1960', self.iface.mainWindow())
        self.button_SWISSIMAGE_1946 = QAction('1946', self.iface.mainWindow())

        self.button_TopoMapCol      = QAction('TPCOL', self.iface.mainWindow())
        self.button_TopoMapGr       = QAction('TPGR', self.iface.mainWindow())

        # Connect them to their function
        self.button_SwAlti3D_Mono.triggered.connect(self.run_button_SwAlti3D_Mono)
        self.button_SwAlti3D_Multi.triggered.connect(self.run_button_SwAlti3D_Multi)
        self.button_SwSurf3D_Multi.triggered.connect(self.run_button_SwSurf3D_Multi)
        self.button_SwSurf3D_Mono.triggered.connect(self.run_button_SwSurf3D_Mono)
        self.button_SWISSIMAGE_2023.triggered.connect(self.run_button_SWISSIMAGE_2023)
        self.button_SWISSIMAGE_2020.triggered.connect(self.run_button_SWISSIMAGE_2020)
        self.button_SWISSIMAGE_2017.triggered.connect(self.run_button_SWISSIMAGE_2017)
        self.button_SWISSIMAGE_2014.triggered.connect(self.run_button_SWISSIMAGE_2014)
        self.button_SWISSIMAGE_2012.triggered.connect(self.run_button_SWISSIMAGE_2012)
        self.button_SWISSIMAGE_2009.triggered.connect(self.run_button_SWISSIMAGE_2009)
        self.button_SWISSIMAGE_2005.triggered.connect(self.run_button_SWISSIMAGE_2005)
        self.button_SWISSIMAGE_2000.triggered.connect(self.run_button_SWISSIMAGE_2000)
        self.button_SWISSIMAGE_1995.triggered.connect(self.run_button_SWISSIMAGE_1995)
        self.button_SWISSIMAGE_1985.triggered.connect(self.run_button_SWISSIMAGE_1985)
        self.button_SWISSIMAGE_1977.triggered.connect(self.run_button_SWISSIMAGE_1977)
        self.button_SWISSIMAGE_1968.triggered.connect(self.run_button_SWISSIMAGE_1968)
        self.button_SWISSIMAGE_1960.triggered.connect(self.run_button_SWISSIMAGE_1960)
        self.button_SWISSIMAGE_1946.triggered.connect(self.run_button_SWISSIMAGE_1946)

        self.button_TopoMapCol.triggered.connect(self.run_button_TopoMapCol)
        self.button_TopoMapGr.triggered.connect(self.run_button_TopoMapGr)

        # Add them to the interface
        self.iface.addToolBarIcon(self.button_SwAlti3D_Mono)
        self.iface.addToolBarIcon(self.button_SwAlti3D_Multi)
        self.iface.addToolBarIcon(self.button_SwSurf3D_Multi)
        self.iface.addToolBarIcon(self.button_SwSurf3D_Mono)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2023)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2020)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2017)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2014)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2012)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2009)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2005)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_2000)

        self.iface.addToolBarIcon(self.button_SWISSIMAGE_1995)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_1985)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_1977)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_1968)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_1960)
        self.iface.addToolBarIcon(self.button_SWISSIMAGE_1946)

        self.iface.addToolBarIcon(self.button_TopoMapCol)
        self.iface.addToolBarIcon(self.button_TopoMapGr)        

        # Put them in a list
        self.actions = [self.button_SwAlti3D_Mono, self.button_SwAlti3D_Multi, self.button_SwSurf3D_Multi, self.button_SwSurf3D_Mono, self.button_SWISSIMAGE_2023, self.button_SWISSIMAGE_2020, self.button_SWISSIMAGE_2017, self.button_SWISSIMAGE_2014, self.button_SWISSIMAGE_2012, self.button_SWISSIMAGE_2009, self.button_SWISSIMAGE_2005, self.button_SWISSIMAGE_2000, self.button_SWISSIMAGE_1995,self.button_SWISSIMAGE_1985,self.button_SWISSIMAGE_1977,self.button_SWISSIMAGE_1968,self.button_SWISSIMAGE_1960,self.button_SWISSIMAGE_1946, self.button_TopoMapCol, self.button_TopoMapGr]

    # Called when the plugin is unloaded      
    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

    def run_button_SwAlti3D_Mono(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SwAlti3D_Mono')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SwAlti3D_Multi(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SwAlti3D_Multi')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SwSurf3D_Multi(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SwSurf3D_Multi')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SwSurf3D_Mono(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SwSurf3D_Mono')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_2023(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2023')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_2020(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2020')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_2017(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2017')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SWISSIMAGE_2014(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2014')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SWISSIMAGE_2012(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2012')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_2009(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2009')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_2005(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2005')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_2000(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 2000')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SWISSIMAGE_1995(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 1995')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_1985(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 1985')[0]
        target.setItemVisibilityChecked(True)
     
    def run_button_SWISSIMAGE_1977(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 1977')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SWISSIMAGE_1968(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 1968')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SWISSIMAGE_1960(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 1960')[0]
        target.setItemVisibilityChecked(True)

    def run_button_SWISSIMAGE_1946(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'SWISSIMAGE 1946')[0]
        target.setItemVisibilityChecked(True)

    def run_button_TopoMapCol(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'Landeskarten (farbig)')[0]
        target.setItemVisibilityChecked(True)

    def run_button_TopoMapGr(self):
        inputs_tree = getLayersTreeGroups(name = 'inputs')[0]
        for group in getLayersTreeGroups(tree = inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree = inputs_tree):
            layer.setItemVisibilityChecked(False)
        target = getLayersTreeLayers(name = 'Landeskarten (grau)')[0]
        target.setItemVisibilityChecked(True)

def getLayersTreeGroups(tree='', name=''):
    """
    Here is a search engine for groups contained in a tree
    """

    # By default, the tree is the root of the project
    if tree == '':
        tree = QgsProject.instance().layerTreeRoot()

    # This is our basket
    # We gonna fill it
    layersTreeGroups = []

    # Recursive Loop on the tree childrens
    for child in tree.children():

        # If the child is a layer we didn't do anything
        if type(child) == QgsLayerTreeLayer:
            continue
        
        # If it's a group
        elif type(child) == QgsLayerTreeGroup:
            
            # We integrate it into the list of groups
            layersTreeGroups += [child]

            # And we call the same function on himself to find his child groups
            layersTreeGroups += (getLayersTreeGroups(child))

    # Now we apply a filter to select only the layer with the good name
    if name != '':
        layersTreeGroups = list(filter(lambda row: row.name().lower()==name.lower(), layersTreeGroups))
        if len(layersTreeGroups) == 0:
            return f'No Group or SubGroup with the name {name} in the tree {tree}'

    return layersTreeGroups

def getLayersTreeLayers(tree='', name=''):
    """
    Here is a search engine for layers 
    (vector or raster or wms, whatever) 
    contained in a tree
    """

    # By default, the tree is the root of the project
    if tree == '':
        tree = QgsProject.instance().layerTreeRoot()

    # This is our basket
    # We gonna fill it
    layersTreeLayers = []

    # Recursive Loop on the tree childrens
    for child in tree.children():

        # If the child is a layer, we integrate it to the basket
        if type(child) == QgsLayerTreeLayer:
            layersTreeLayers += [child]

        # If it's a group, we have to check what's inside
        elif type(child) == QgsLayerTreeGroup:
            
            # So we call the function on himself
            layersTreeLayers += getLayersTreeLayers(child)

    # Now we apply a filter to select only the layer with the good name
    if name != '':
        layersTreeLayers = list(filter(lambda row: row.name().lower()==name.lower(), layersTreeLayers))
        if len(layersTreeLayers) == 0:
            return f'No layer with the name {name} in the tree {tree}'

    return layersTreeLayers