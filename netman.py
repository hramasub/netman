#!/usr/bin/env python

import sys
import subprocess
import dbus
import string
import os
import fcntl
import glib
import gobject
import dbus.service
import dbus.mainloop.glib

DBUS_NAME = 'org.openbmc.NetworkManager'
OBJ_NAME = '/org/openbmc/NetworkManager/Interface'

network_providers = {
    'networkd' : {
        'bus_name' : 'org.freedesktop.network1',
        'object_name' : '/org/freedesktop/network1/network/default',
        'interface_name' : 'org.freedesktop.network1.Network',
        'method' : 'org.freedesktop.network1.Network.SetAddr'
    },
    'NetworkManager' : {
        'bus_name' : 'org.freedesktop.NetworkManager',
        'object_name' : '/org/freedesktop/NetworkManager',
        'interface_name' : 'org.freedesktop.NetworkManager',
        'method' : 'org.freedesktop.NetworkManager' # FIXME:
    },
}

class NetMan (dbus.service.Object):
    def __init__(self, bus, name):
        self.bus = bus
        self.name = name
        dbus.service.Object.__init__(self,bus,name)

    def setNetworkProvider(self, provider):
        self.provider = provider

    def _setAddr (self, op, device, ipaddr, netmask, family, flags, scope, gatew
        netprov     = network_providers [self.provider]
        bus_name    = netprov ['bus_name']
        obj_path    = netprov ['object_name']
        intf_name   = netprov ['interface_name']

        obj = self.bus.get_object(bus_name, obj_path)
        intf = dbus.Interface(obj, intf_name)
 	if (op == "add"):
            intf.AddAddress (device, ipaddr, netmask, family, flags, scope, gate

        if (op == "del"):
            intf.DelAddress (device, ipaddr, netmask, family, flags, scope, gate


    @dbus.service.method(DBUS_NAME, "", "")
    def test(self):
        print("TEST")

    @dbus.service.method(DBUS_NAME, "ssss", "x")
    def AddAddress4 (self, device, ipaddr, netmask, gateway):
        self._setAddr ("add", device, ipaddr, netmask, 2, 0, 253, gateway)
        return 0

    @dbus.service.method(DBUS_NAME, "ssss", "x")
    def DelAddress4 (self, device, ipaddr, netmask, gateway):
        self._setAddr ("del", device, ipaddr, netmask, 2, 0, 253, gateway)
        return 0

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    name = dbus.service.BusName(DBUS_NAME, bus)
    obj = NetMan (bus, OBJ_NAME)
    obj.setNetworkProvider ("networkd")
    mainloop = gobject.MainLoop()
    print("Started")
    mainloop.run()

if __name__ == '__main__':
    sys.exit(main())

