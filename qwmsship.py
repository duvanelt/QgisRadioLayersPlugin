import csv
from pathlib import Path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QComboBox, QDialog, QDialogButtonBox, QHeaderView, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout
from qgis.core import QgsProject, QgsLayerTreeLayer, QgsLayerTreeGroup


class LinkConfigDialog(QDialog):

    def __init__(self, plugin, parent=None):
        super().__init__(parent)
        self.plugin = plugin
        self.setWindowTitle('SwitchLayers configuration')
        self.resize(620, 260)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Layers available in the Inputs tree'))

        self.table = QTableWidget(10, 3)
        self.table.setHorizontalHeaderLabels(['Slot', 'Short name', 'Layer'])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        layer_names = self.plugin.get_input_layer_names()

        for slot in range(10):
            config = self.plugin.link_config.get(slot, {'shortname': f'Slot {slot}', 'layer': ''})
            self.table.setItem(slot, 0, QTableWidgetItem(str(slot)))

            short_name = QLineEdit(config.get('shortname', ''))
            self.table.setCellWidget(slot, 1, short_name)

            layer_combo = QComboBox()
            layer_combo.addItem('')
            for layer_name in layer_names:
                layer_combo.addItem(layer_name)

            selected_layer = config.get('layer', '')
            if selected_layer and selected_layer in layer_names:
                layer_combo.setCurrentText(selected_layer)
            self.table.setCellWidget(slot, 2, layer_combo)

        layout.addWidget(self.table)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_config)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def save_config(self):
        rows = []
        for slot in range(self.table.rowCount()):
            short_name_widget = self.table.cellWidget(slot, 1)
            layer_widget = self.table.cellWidget(slot, 2)

            short_name = short_name_widget.text().strip() if short_name_widget else ''
            layer_name = layer_widget.currentText().strip() if layer_widget else ''
            rows.append((slot, short_name, layer_name))

        config_path = self.plugin.get_config_path()
        with config_path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['slot', 'shortname', 'layer'])
            for slot, short_name, layer_name in rows:
                writer.writerow([slot, short_name, layer_name])

        self.plugin.link_config = self.plugin.load_link_config()
        self.plugin.refresh_slot_buttons()
        self.accept()


class QWmsShipPlugin:

    def __init__(self, iface):

        # Gives the plugin access to the QGIS interface (iface)
        self.iface = iface
        self.actions = []
        self.button_slots = {}
        self.link_config = self.load_link_config()

    def get_config_path(self):
        csv_path = Path(__file__).with_name('user_links.csv')
        txt_path = Path(__file__).with_name('user_links.txt')
        if csv_path.exists():
            return csv_path
        if txt_path.exists():
            return txt_path
        return csv_path

    def load_link_config(self):
        config_path = self.get_config_path()
        slots = {}

        if not config_path.exists():
            return slots

        with config_path.open('r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row or len(row) < 3:
                    continue

                slot_label = row[0].strip()
                if slot_label.lower() == 'slot':
                    continue

                try:
                    slot = int(slot_label)
                except ValueError:
                    continue

                if 0 <= slot < 10:
                    shortname = row[1].strip().strip("'\"")
                    layer_name = row[2].strip().strip("'\"")
                    slots[slot] = {'shortname': shortname, 'layer': layer_name}

        for slot in range(10):
            slots.setdefault(slot, {'shortname': f'Slot {slot}', 'layer': ''})

        return slots

    def get_input_layer_names(self):
        inputs_tree = getLayersTreeGroups(name='inputs')
        if not inputs_tree:
            return []

        inputs_root = inputs_tree[0]
        layers = getLayersTreeLayers(tree=inputs_root)
        if isinstance(layers, str):
            return []

        return [layer.name() for layer in layers]

    # Called whe the plugin is loaded by Qgis
    def initGui(self):

        # Found logofiles path
        resources = Path(Path(__file__).parent, 'resources')

        # Récupère l'arbre racine des couches du projet
        self.root_group = QgsProject.instance().layerTreeRoot()

        for slot in range(10):
            config = self.link_config.get(slot, {'shortname': f'Slot {slot}', 'layer': ''})
            label = config.get('shortname') or f'Slot {slot}'
            button = QAction(label, self.iface.mainWindow())
            button.triggered.connect(lambda checked=False, slot_index=slot: self.run_button(slot_index))
            self.iface.addToolBarIcon(button)
            self.actions.append(button)
            self.button_slots[slot] = button

        icon_path = str(Path(__file__).resolve().parent / 'resources' / 'config_logo.png')
        self.config_button = QAction(QIcon(icon_path), '', self.iface.mainWindow())
        self.config_button.triggered.connect(self.open_config_dialog)
        self.iface.addToolBarIcon(self.config_button)
        self.actions.append(self.config_button)

    def refresh_slot_buttons(self):
        for slot in range(10):
            button = self.button_slots.get(slot)
            if button is None:
                continue
            config = self.link_config.get(slot, {'shortname': f'Slot {slot}', 'layer': ''})
            button.setText(config.get('shortname') or f'Slot {slot}')

    def open_config_dialog(self):
        dialog = LinkConfigDialog(self, self.iface.mainWindow())
        dialog.exec_()

    # Called when the plugin is unloaded
    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

    def run_button(self, slot):
        config = self.link_config.get(slot, {'shortname': '', 'layer': ''})
        layer_name = config.get('layer', '').strip()
        if not layer_name:
            return

        inputs_tree = getLayersTreeGroups(name='inputs')[0]
        for group in getLayersTreeGroups(tree=inputs_tree):
            group.setItemVisibilityChecked(True)
        for layer in getLayersTreeLayers(tree=inputs_tree):
            layer.setItemVisibilityChecked(False)

        target = getLayersTreeLayers(name=layer_name)
        if isinstance(target, str) or len(target) == 0:
            return
        target[0].setItemVisibilityChecked(True)

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