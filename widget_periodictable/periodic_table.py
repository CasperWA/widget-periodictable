#!/usr/bin/env python
# coding: utf-8

"""
Copyright (c) Dou Du.
Distributed under the terms of the Modified BSD License.

A Periodic Table widget for use in Jupyter Notebooks.
"""

from copy import deepcopy
import typing

from ipywidgets import DOMWidget, Layout
from traitlets import Unicode, Int, List, Dict, observe, validate, TraitError, Dict, Bool

from ._frontend import module_name, module_version
from .utils import faded_color


class PTableWidget(DOMWidget):
    """Periodic Table Widget
    """
    _model_name = Unicode('MCPTableModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('MCPTableView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    selected_elements = Dict({}).tag(sync=True)
    disabled_elements = List([]).tag(sync=True)
    display_names_replacements = Dict({}).tag(sync=True)
    disabled_colors = List([]).tag(sync=True)
    disabled_unselected_color = Unicode('gray').tag(sync=True)
    unselected_color = Unicode('pink').tag(sync=True)
    states = Int(1).tag(sync=True)
    selected_colors = List([]).tag(sync=True)
    border_color = Unicode('#cc7777').tag(sync=True)
    disabled = Bool(False, help="Enable or disable user changes.").tag(sync=True)
    width = Unicode('38px').tag(sync=True)
    allElements = List([
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg",
        "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe",
        "Co","Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y",
        "Zr", "Nb", "Mo",  "Tc", "Ru", "Rh","Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te",
        "I", "Xe", "Cs", "Ba", "Hf", "Ta", "W", "Re", "Os", "Ir","Pt", "Au", "Hg", "Tl",
        "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Rf", "Db", "Sg", "Bh", "Hs",
        "Mt","Ds", "Rg", "Cn", "Nh", "Fi", "Mc", "Lv", "Ts", "Og", "La", "Ce", "Pr",
        "Nd", "Pm", "Sm", "Eu","Gd",  "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu","Ac",
        "Th", "Pa", "U", "Np", "Pu", "Am","Cm", "Bk",  "Cf", "Es", "Fm", "Md", "No", "Lr"
    ]).tag(sync=True)

    _STANDARD_COLORS = [
        "#a6cee3", "#b2df8a", "#fdbf6f", "#6a3d9a", "#b15928", "#e31a1c", "#1f78b4",
        "#33a02c", "#ff7f00", "#cab2d6", "#ffff99",
    ]

    def __init__(
        self,
        states: int = None,
        selected_elements: list = None,
        unselected_color: str = None,
        selected_colors: list = None,
        border_color: str = None,
        width: str = None,
        layout: typing.Union[Layout, dict] = None,
    ):
        super(PTableWidget, self).__init__()
        self.states = states if states else 1
        self.unselected_color = unselected_color if unselected_color else 'pink'
        self.selected_colors = selected_colors if selected_colors else self._STANDARD_COLORS
        self.selected_elements = selected_elements if selected_elements else {}
        self.border_color = border_color if border_color else "#cc7777"
        self.width = width if width else "38px"

        if layout is not None:
            self.layout = layout 

        if len(selected_colors) < states:
            additional_colors = ["#a6cee3", "#b2df8a", "#fdbf6f", "#6a3d9a", "#b15928", "#e31a1c", "#1f78b4", "#33a02c", "#ff7f00", "#cab2d6", "#ffff99"]
            self.selected_colors = selected_colors + additional_colors * (1 + (states - len(selected_colors)) // len(additional_colors))
            self.selected_colors = self.selected_colors[:states]
        self.disabled_colors = [faded_color(i) for i in self.selected_colors]
        self.disabled_unselected_color = faded_color(self.unselected_color)
        self.disabled_elements = []

    def set_element_state(self, elementName, state):
        if elementName not in self.allElements:
            raise TraitError('Element not found')
        if state not in range(self.states):
            raise TraitError('State value is wrong')
        x = deepcopy(self.selected_elements)
        x[elementName] = state
        self.selected_elements = x

    @validate('selected_elements')
    def _selectedElements_change(self, proposal):
        for x, y in proposal['value'].items():
            if x not in self.allElements and x != 'Du':
                raise TraitError('Element not found')
            if not isinstance(y, int) or y not in range(self.states):
                raise TraitError('State value is wrong')
        return proposal['value']

    @observe('disabled')
    def _disabled_change(self, change):
        if change['new']:
            self.disabled_elements = self.allElements
        else:
            self.disabled_elements = []

    @observe('states')
    def _states_change(self, change):
        if change['new'] < 1:
            raise TraitError('State value cannot smaller than 1')
        else:
            if len(self.selected_colors) < change["new"]:
                additional_colors = ["#a6cee3", "#b2df8a", "#fdbf6f", "#6a3d9a", "#b15928", "#e31a1c", "#1f78b4", "#33a02c", "#ff7f00", "#cab2d6", "#ffff99"]
                self.selected_colors = self.selected_colors + additional_colors * (1 + (change["new"] - len(self.selected_colors)) // len(additional_colors))
                self.selected_colors = self.selected_colors[:change["new"]]
            elif len(self.selected_colors) > change["new"]:
                self.selected_colors = self.selected_colors[:change["new"]]
            self.disabled_colors = [faded_color(i) for i in self.selected_colors]

    def get_elements_by_state(self, state):
        if state not in range(self.states):
            raise TraitError("State value is wrong")
        else:
            return [i for i in self.selected_elements if self.selected_elements[i] == state]
