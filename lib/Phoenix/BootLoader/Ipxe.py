#!/usr/bin/env python
"""Phoenix bootloader support for iPXE"""
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from Phoenix.BootLoader import BootLoader

class Ipxe(BootLoader):
    bootloadertype = 'ipxe'

    @classmethod
    def script(cls, node):
        default_args = "BOOTIF=${mac} ip=${ip}::${gateway}:${netmask}:${hostname} rw"

        try:
            server_ip = node['http_server']
        except KeyError:
            server_ip = '${dhcp-server}'

        try:
            console = node['console']
        except KeyError:
            console = 'ttyS0,115200'

        try:
            kcmdline = node['kcmdline']
        except KeyError:
            kcmdline = ''

        result = list()
        result.append('#!ipxe')
        result.append('kernel http://%s/phoenix/images/%s/vmlinuz initrd=initramfs.gz %s console=%s %s' %
                            (server_ip, node['image'], default_args, console, kcmdline))
        result.append('initrd http://%s/phoenix/images/%s/initramfs.gz' % (server_ip, node['image']))
        result.append('boot')

        return '\n'.join(result)
