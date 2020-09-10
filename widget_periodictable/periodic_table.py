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
from traitlets import Unicode, Int, List, Dict, observe, validate, TraitError, Bool

from ._frontend import module_name, module_version
from .utils import faded_color, CHEMICAL_ELEMENTS


class PTableWidget(DOMWidget):
    """Periodic Table Widget"""

    _model_name = Unicode('MCPTableModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('MCPTableView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    selected_elements = Dict({}).tag(sync=True)
    display_names_replacements = Dict({}).tag(sync=True)
    disabled_colors = List([]).tag(sync=True)
    disabled_unselected_color = Unicode('gray').tag(sync=True)
    unselected_color = Unicode('pink').tag(sync=True)
    states = Int(1).tag(sync=True)
    selected_colors = List([]).tag(sync=True)
    border_color = Unicode('#cc7777').tag(sync=True)
    disabled = Bool(False, help='Enable or disable widget.').tag(sync=True)
    width = Unicode('38px').tag(sync=True)
    all_elements = List(CHEMICAL_ELEMENTS).tag(sync=True)

    _STANDARD_COLORS = [
        '#a6cee3',
        '#b2df8a',
        '#fdbf6f',
        '#6a3d9a',
        '#b15928',
        '#e31a1c',
        '#1f78b4',
        '#33a02c',
        '#ff7f00',
        '#cab2d6',
        '#ffff99',
    ]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        states: int = None,
        selected_elements: dict = None,
        unselected_color: str = None,
        selected_colors: list = None,
        border_color: str = None,
        width: str = None,
        layout: typing.Union[Layout, dict] = None,
    ):
        super(PTableWidget, self).__init__()
        self.states = states if states else 1
        self.unselected_color = unselected_color if unselected_color else 'pink'
        self.selected_colors = (
            selected_colors if selected_colors else self._STANDARD_COLORS
        )
        self.selected_elements = selected_elements if selected_elements else {}
        self.border_color = border_color if border_color else '#cc7777'
        self.width = width if width else '38px'

        if layout is not None:
            self.layout = layout

        if len(selected_colors) < states:
            self.selected_colors = selected_colors + self._STANDARD_COLORS * (
                1 + (states - len(selected_colors)) // len(self._STANDARD_COLORS)
            )
            self.selected_colors = self.selected_colors[:states]
        self.disabled_colors = [faded_color(i) for i in self.selected_colors]
        self.disabled_unselected_color = faded_color(self.unselected_color)

    def set_element_state(self, elementName, state):
        if elementName not in self.all_elements:
            raise TraitError('Element not found')
        if state not in range(self.states):
            raise TraitError('State value is wrong')
        x = deepcopy(self.selected_elements)
        x[elementName] = state
        self.selected_elements = x

    @validate('selected_elements')
    def _selectedElements_change(self, proposal):
        for x, y in proposal['value'].items():
            if x not in self.all_elements and x != 'Du':
                raise TraitError('Element not found')
            if not isinstance(y, int) or y not in range(self.states):
                raise TraitError('State value is wrong')
        return proposal['value']

    @validate('states')
    def _validate_states(self, proposal):
        if proposal['value'] < 1:
            raise TraitError('State value cannot smaller than 1')
        return proposal['value']

    @observe('states')
    def _states_change(self, change):
        if len(self.selected_colors) < change['new']:
            self.selected_colors = self.selected_colors + self._STANDARD_COLORS * (
                1
                + (change['new'] - len(self.selected_colors))
                // len(self._STANDARD_COLORS)
            )
            self.selected_colors = self.selected_colors[: change['new']]
        elif len(self.selected_colors) > change['new']:
            self.selected_colors = self.selected_colors[: change['new']]
        self.disabled_colors = [faded_color(i) for i in self.selected_colors]

    def get_elements_by_state(self, state):
        if state not in range(self.states):
            raise TraitError('State value is wrong')

        return [i for i in self.selected_elements if self.selected_elements[i] == state]
