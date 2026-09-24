# ------------
# Thibaut Duvanel
# 2023 - 2026
# Lausanne University
# thibaut.duvanel@unil.ch
# ------------

# Data management
from pathlib import Path
import csv # Pandas is not available in Qgis python env

# GUI management
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QAction, QCompleter, QDialog, QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

# PyQgis
from qgis.core import QgsProject, QgsLayerTreeLayer, QgsLayerTreeGroup

class LinkConfigDialog(QDialog):
    """
    Describe the plugin configuration dashboard
    Inherited from QDialog
    """

    def __init__(self, plugin, parent=None):

        # Get the QDialog attributes
        super().__init__(parent)

        # Identify the plugin instance itself : a QWsmShip instance
        self.plugin = plugin

        # Rule the dashboard window settings
        self.setWindowTitle('RadioLayers configuration')
        self.resize(620, 260)

        # Define empty containers
        self.capture_slot = None
        self.shortcut_values = {}
        self.shortcut_widgets = {}

        # Add a short description about the visible layers
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Layers available in the Inputs tree'))

        # Configure the group containing the switchable layers
        inputs_group_layout = QHBoxLayout()
        inputs_group_layout.addWidget(QLabel('Inputs group'))
        self.inputs_group_widget = QLineEdit(self.plugin.inputs_group)
        inputs_group_layout.addWidget(self.inputs_group_widget)
        layout.addLayout(inputs_group_layout)

        # Define the table area
        # 4 for 4 attributes for each slot
        self.table = QTableWidget(self.plugin.n_slots, 4)
        self.table.setHorizontalHeaderLabels(['Slot', 'Short name', 'Layer', 'Shortcut'])
        self.table.verticalHeader().setVisible(False)

        # Rules each column behavior in relation with its content type
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        # Scan the available layer within the Input Tree
        layer_names = self.plugin.get_input_layer_names()

        # For each slot
        for slot in range(self.plugin.n_slots):

            # Metadata about the slot
            config = self.plugin.link_config.get(slot, {'shortname': f'Slot {slot}', 'layer': '', 'shortcut': ''})
            self.table.setItem(slot, 0, QTableWidgetItem(str(slot)))

            # ---
            # Shortname field
            # ---
            short_name = QLineEdit(config.get('shortname', ''))
            self.table.setCellWidget(slot, 1, short_name)

            # Layer choice from layer name : text edit
            layer_text = QLineEdit(config.get('layer', ''))
            layer_text.setPlaceholderText('Type first letters...')

            # With auto completion
            layer_completer = QCompleter(layer_names)
            layer_completer.setCaseSensitivity(Qt.CaseInsensitive)
            layer_completer.setFilterMode(Qt.MatchContains)
            layer_text.setCompleter(layer_completer)

            # Place it in the third dashboard column
            self.table.setCellWidget(slot, 2, layer_text)

            # ---
            # Shortcut field
            # ---
            shortcut_value = config.get('shortcut', '').strip()
            self.shortcut_values[slot] = shortcut_value

            # Works with the capture functions defined below
            shortcut_widget = QWidget()
            shortcut_layout = QHBoxLayout(shortcut_widget)
            shortcut_layout.setContentsMargins(0, 0, 0, 0)
            shortcut_label = QLabel(shortcut_value if shortcut_value else 'None')
            shortcut_button = QPushButton('Set shortcut')
            shortcut_button.clicked.connect(lambda checked=False, slot_index=slot: self.start_shortcut_capture(slot_index))
            shortcut_layout.addWidget(shortcut_label)
            shortcut_layout.addWidget(shortcut_button)
            self.shortcut_widgets[slot] = {'label': shortcut_label, 'button': shortcut_button}
            self.table.setCellWidget(slot, 3, shortcut_widget)

        # Finally add the table to the dashboard window
        layout.addWidget(self.table)

        # Add two buttons below the config table : accept or cancel
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_config)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def start_shortcut_capture(self, slot):
        """
        Open the capture user keyboard input to set the shortcuts
        """
        self.capture_slot = slot
        button = self.shortcut_widgets.get(slot, {}).get('button')
        if button is not None:
            button.setText('Press keys...')
        self.grabKeyboard()

    def cancel_shortcut_capture(self):
        """
        Cancel the capture
        """
        if self.capture_slot is None:
            return
        button = self.shortcut_widgets.get(self.capture_slot, {}).get('button')
        if button is not None:
            button.setText('Set shortcut')
        self.releaseKeyboard()

        # Reinit the shortcut
        self.capture_slot = None

    def set_shortcut_for_slot(self, slot, shortcut_text):
        """
        Once the shortcut has been typed, assign it to the button
        """
        self.shortcut_values[slot] = shortcut_text
        widget = self.shortcut_widgets.get(slot)
        if widget is not None:
            widget['label'].setText(shortcut_text if shortcut_text else 'None')
            widget['button'].setText('Set shortcut')
        self.releaseKeyboard()
        self.capture_slot = None

    def keyPressEvent(self, event):
        if self.capture_slot is not None:
            if event.key() in (Qt.Key_Escape, Qt.Key_Return, Qt.Key_Enter):
                self.cancel_shortcut_capture()
                event.accept()
                return
            if event.key() in (Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta):
                event.ignore()
                return
            shortcut = QKeySequence(event.modifiers() | event.key())
            shortcut_text = shortcut.toString()
            if shortcut_text:
                self.set_shortcut_for_slot(self.capture_slot, shortcut_text)
                event.accept()
                return
        super().keyPressEvent(event)

    def save_config(self):
        """
        Write the data of each slot into the csv file
        """

        # Define empty container
        rows = []
        inputs_group = self.inputs_group_widget.text().strip()
        if inputs_group:
            self.plugin.inputs_group = inputs_group

        # For each slot
        for slot in range(self.table.rowCount()):

            # Get its widgets from the table
            short_name_widget = self.table.cellWidget(slot, 1)
            layer_widget = self.table.cellWidget(slot, 2)

            # Get its attributes from the widgets
            short_name = short_name_widget.text().strip() if short_name_widget else ''
            layer_name = layer_widget.text().strip() if layer_widget else ''
            shortcut = self.shortcut_values.get(slot, '').strip()

            # Write everything to the container
            rows.append((slot, short_name, layer_name, shortcut))

        # Write the content to the csv config file
        with self.plugin.config_path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['inputs_group', self.plugin.inputs_group])
            writer.writerow(['slot', 'shortname', 'layer', 'shortcut'])
            for slot, short_name, layer_name, shortcut in rows:
                writer.writerow([slot, short_name, layer_name, shortcut])

        # Refresh buttons of the plugin toolbar
        self.plugin.link_config = self.plugin.load_link_config()
        self.plugin.refresh_slot_buttons()
        self.accept()

class RadioLayersPlugin:
    """
    Describe the RadioLayers plugin 
    """

    def __init__(self, iface):

        # Gives the plugin access to the QGIS interface (iface)
        self.iface = iface
        self.n_slots = 10
        self.config_path = Path(__file__).with_name('user_links.csv')
        self.inputs_group = 'RadioChannels'

        self.actions = []
        self.button_slots = {}
        self.link_config = self.load_link_config()

    def load_link_config(self):
        """
        Read Config File and load associated settings
        """

        # Define empty container
        slots = {}
        inputs_group = self.inputs_group
        if not self.config_path.exists():
            return slots

        # Open the config file
        with self.config_path.open('r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)

            # For each row / each slot
            for row in reader:

                # Invalid row / slot
                if not row:
                    continue

                # Get the label and skip the header row
                slot_label = row[0].strip()
                if slot_label.lower() == 'inputs_group':
                    if len(row) > 1 and row[1].strip():
                        inputs_group = row[1].strip().strip("'\"")
                    continue
                if slot_label.lower() == 'slot':
                    continue

                if len(row) < 3:
                    continue

                # Process the slot number
                try:
                    slot = int(slot_label)
                except ValueError:
                    continue

                # Ensure we have a valid slot number
                if 0 <= slot < self.n_slots:

                    # Extract the slot attributes from the line
                    shortname = row[1].strip().strip("'\"")
                    layer_name = row[2].strip().strip("'\"")
                    shortcut = row[3].strip().strip("'\"") if len(row) > 3 else ''

                    # Write it in the container
                    slots[slot] = {'shortname': shortname, 'layer': layer_name, 'shortcut': shortcut}

        # For each slot, we set emptyy strigns as default - the method check if its empty
        for slot in range(self.n_slots):
            slots.setdefault(slot, {'shortname': f'Slot {slot}', 'layer': '', 'shortcut': ''})
        self.inputs_group = inputs_group
        return slots

    # ---
    # Research functions through the Layers Trees
    # ---
    def get_input_layer_names(self):

        # Look  for the layer group named self.inputs_group in the Qgis project
        inputs_tree = getLayersTreeGroups(name=self.inputs_group)
        if isinstance(inputs_tree, str) or not inputs_tree:
            return []

        # Extract a list of its layers
        inputs_root = inputs_tree[0]
        layers = getLayersTreeLayers(tree=inputs_root)
        if isinstance(layers, str):
            return []

        return [layer.name() for layer in layers]

    def slot_is_used(self, slot):
        config = self.link_config.get(slot, {})
        layer_name = str(config.get('layer', '')).strip()
        return bool(layer_name)

    # Called whe the plugin is loaded by Qgis
    def initGui(self):

        # Récupère l'arbre racine des couches du projet
        self.root_group = QgsProject.instance().layerTreeRoot()

        # For each slot
        for slot in range(self.n_slots):

            # Initialize the buttons from the config state
            config = self.link_config.get(slot, {'shortname': f'Slot {slot}', 'layer': '', 'shortcut': ''})
            label = config.get('shortname') or f'Slot {slot}'

            # Create the button with the label
            button = QAction(label, self.iface.mainWindow())

            # Connect it to its function
            button.triggered.connect(lambda checked=False, slot_index=slot: self.run_button(slot_index))

            # Associate the button to the shortcut
            shortcut = config.get('shortcut', '').strip()
            if shortcut:
                button.setShortcut(QKeySequence(shortcut))
            button.setVisible(self.slot_is_used(slot))

            # Add it to the toolbar
            self.iface.addToolBarIcon(button)

            # Keep it in the instance button container (easier to destroy them when the plugin is reloaded)
            self.actions.append(button)
            self.button_slots[slot] = button

        # Set the config button with the crank icon
        icon_path = str(Path(__file__).resolve().parent / 'resources' / 'config_logo.png')
        self.config_button = QAction(QIcon(icon_path), '', self.iface.mainWindow())
        self.config_button.triggered.connect(self.open_config_dialog)
        self.iface.addToolBarIcon(self.config_button)
        self.actions.append(self.config_button)

    def refresh_slot_buttons(self):

        # For each slot
        for slot in range(self.n_slots):

            # Get the slots affected to a layer
            button = self.button_slots.get(slot)
            if button is None:
                continue

            # Reload its shortcut
            config = self.link_config.get(slot, {'shortname': f'Slot {slot}', 'layer': '', 'shortcut': ''})
            button.setText(config.get('shortname') or f'Slot {slot}')
            shortcut = config.get('shortcut', '').strip()
            if shortcut:
                button.setShortcut(QKeySequence(shortcut))
            else:
                button.setShortcut('')
            button.setVisible(self.slot_is_used(slot))

    def open_config_dialog(self):
        dialog = LinkConfigDialog(self, self.iface.mainWindow())
        dialog.exec_()

    # Called when the plugin is unloaded
    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

    def run_button(self, slot):
        """
        Core function
            - hide all the layers of the Inputs group
            - display only the one associated to the slot
        """

        # Get slot data
        config = self.link_config.get(slot, {'shortname': '', 'layer': ''})
        layer_name = config.get('layer', '').strip()
        if not layer_name:
            return

        # Scan the Inputs Group
        inputs_tree = getLayersTreeGroups(name=self.inputs_group)[0]

        # Make each sub group visible
        for group in getLayersTreeGroups(tree=inputs_tree):
            group.setItemVisibilityChecked(True)

        # And hide each layer
        for layer in getLayersTreeLayers(tree=inputs_tree):
            layer.setItemVisibilityChecked(False)

        # Now, get the target layer
        target = getLayersTreeLayers(tree=inputs_tree, name=layer_name)
        if isinstance(target, str) or len(target) == 0:
            return

        # And show it
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