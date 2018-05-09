#!/usr/bin/env python3

from sys import argv
from time import sleep

from esp_link_controller.esplink import EspLink


class UpgradeCtl(EspLink):
    def __init__(self, ip_address):
        super().__init__(ip_address)

    def set_nrst(self, value):
        if value == True:
            self.set_dtr(False)
        else:
            self.set_dtr(True)

    def set_boot0(self, value):
        if value == True:
            self.set_rts(True)
        else:
            self.set_rts(False)

    def reset_stm(self):
        self.set_nrst(False)
        # you'd think telnet is slow enough for this sleep not to be necessary :)
        sleep(0.1)
        self.set_nrst(True)

    def start_application(self):
        self.set_boot0(False)
        self.reset_stm()

    def start_dfu(self):
        self.set_boot0(True)
        self.reset_stm()


def main():
    ip_address = argv[1]
    action = argv[2]

    upgrade_ctl = UpgradeCtl(ip_address)
    if action in ['reset', 'rst', 'reboot']:
        upgrade_ctl.reset_stm()
    elif action in ['application', 'app', 'user']:
        upgrade_ctl.start_application()
    elif action == 'dfu':
        upgrade_ctl.start_dfu()
    else:
        raise BaseException('Unsupported action %s' % action)


if __name__ == "__main__":
    main()
