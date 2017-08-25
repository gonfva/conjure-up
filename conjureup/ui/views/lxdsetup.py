from ubuntui.utils import Color
from ubuntui.widgets.hr import HR
from ubuntui.widgets.input import SelectorHorizontal
from urwid import Columns, Pile, Text

from conjureup.ui.views.base import BaseView


class LXDSetupViewError(Exception):
    pass


class LXDSetupView(BaseView):
    title = "LXD Configuration"

    def __init__(self, devices, cb, *args, **kwargs):
        self.devices = devices
        self.cb = cb
        self.lxd_config = {
            'network': SelectorHorizontal(
                [net for net in self.devices['networks'].keys()]
            ),
            'storage-pool': SelectorHorizontal(
                [pool for pool in self.devices['storage-pools'].keys()]
            )
        }

        try:
            self.lxd_config['network'].set_default(
                self.lxd_config['network'].group[0].label, True
            )

            self.lxd_config['storage-pool'].set_default(
                self.lxd_config['storage-pool'].group[0].label, True
            )
        except IndexError:
            raise LXDSetupViewError(
                "Could not locate any network or storage "
                "devices to continue. Please make sure you "
                "have at least 1 network bridge and 1 storage "
                "pool: see `lxc network list` and `lxc storage "
                "list`")
        super().__init__(*args, **kwargs)

    def build_buttons(self):
        return [self.button('SAVE', self.submit)]

    def submit(self, result):
        network = self.lxd_config['network'].value
        storage_pool = self.lxd_config['storage-pool'].value
        self.cb(self.devices['networks'][network],
                self.devices['storage-pools'][storage_pool])

    def build_widget(self):
        rows = [
            Text("Select a network bridge and storage pool "
                 "for this deployment:"),
            HR(),
            Columns([
                ('weight', 0.5, Text('network bridge', align="right")),
                Color.string_input(
                    self.lxd_config['network'],
                    focus_map='string_input focus')
            ], dividechars=1),
            HR(),
            Columns([
                ('weight', 0.5, Text('storage pool',
                                     align="right")),
                Color.string_input(
                    self.lxd_config['storage-pool'],
                    focus_map='string_input focus')
            ], dividechars=1),
        ]
        self.pile = Pile(rows)
        return self.pile
