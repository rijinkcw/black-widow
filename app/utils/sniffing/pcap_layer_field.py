"""
*********************************************************************************
*                                                                               *
* pcap_layer_field.py -- Packet Capture Layer Field                             *
*                                                                               *
********************** IMPORTANT BLACK-WIDOW LICENSE TERMS **********************
*                                                                               *
* This file is part of black-widow.                                             *
*                                                                               *
* black-widow is free software: you can redistribute it and/or modify           *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* black-widow is distributed in the hope that it will be useful,                *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with black-widow.  If not, see <http://www.gnu.org/licenses/>.          *
*                                                                               *
*********************************************************************************
"""

from anytree import Node
from pyshark.packet.fields import LayerField


class PcapLayerField(Node):
    """
    """

    def __init__(self, layer_field: LayerField = None, parent=None, children=None):
        """
        :param layer_field: The LayerField of this Node
        :type parent: PcapLayerField
        :param children: The children of this Node
        """
        kwargs = {}
        if layer_field is not None:
            kwargs.update({
                'field': layer_field
            })
            name = layer_field.name
            self.is_main = False
        else:
            name = 'root'
            self.is_main = True
        self.field = layer_field
        super().__init__(name, parent, children, **kwargs)

    @property
    def label(self):
        if self.field is None:
            return self.name
        field_label: str = self.field.showname_key
        if not field_label:
            return self.name
        return field_label

    @property
    def value(self):
        if self.field is None:
            return self.name
        field_value: str = self.field.showname_value
        if not field_value:
            field_value = self.field.get_default_value()
        if field_value is not None:
            field_value = field_value.encode('utf-8').decode('unicode-escape').replace('Âµs', 'µs')
        return field_value

    @property
    def size(self) -> float or None:
        if self.field is None:
            return 0
        return float(self.field.size)

    @property
    def pos(self) -> int or None:
        if self.field is None:
            return 0
        return int(self.field.pos)

    def get_dict(self) -> dict:
        node_dict = {
            'children': []
        }
        if not self.is_main:
            node_dict.update({
                'label': self.label,
                'value': self.value,
                'pos': self.pos,
                'name': self.name,
                'size': self.size   # byte
            })
        for child in self.children:
            child: PcapLayerField
            node_dict['children'].append(child.get_dict())
        return node_dict

    def __str__(self, depth: int = 0):
        """
        :param depth: The current printing depth
        """
        pcap_layer_field_header = '   |' * depth
        pcap_layer_field_row = pcap_layer_field_header + '   ├── [ ' + str(self.label) + ' ]'
        if self.value is not None:
            value = str(self.value)
            if len(value) > 30:
                value = value[0:30] + '...'
            pcap_layer_field_row += ' = ' + value
        else:
            pcap_layer_field_row += ' : PARENT NAME'
        pcap_layer_field_row += ', key=' + self.name + ', size=' + str(self.size) + ', pos=' + str(self.pos)
        for pcap_layer_field_child in self.children:
            pcap_layer_field_child: PcapLayerField
            pcap_layer_field_row += "    \n" + pcap_layer_field_child.__str__(depth+1)
        if len(self.children) > 0:
            pcap_layer_field_row += "   |\n" + pcap_layer_field_header
        return pcap_layer_field_row