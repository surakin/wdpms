# This file has been autogenerated by the pywayland scanner

# SPDX-FileCopyrightText: 2015 Martin Gräßlin
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from __future__ import annotations

import enum

from pywayland.protocol_core import (
    Argument,
    ArgumentType,
    Global,
    Interface,
    Proxy,
    Resource,
)


class OrgKdeKwinDpms(Interface):
    """Dpms for a :class:`~pywayland.protocol.wayland.WlOutput`

    This interface provides information about the VESA DPMS state for a
    :class:`~pywayland.protocol.wayland.WlOutput`. It gets created through the
    request get on the :class:`~pywayland.protocol.dpms.OrgKdeKwinDpmsManager`
    interface.

    On creating the resource the server will push whether DPSM is supported for
    the output, the currently used DPMS state and notifies the client through
    the done event once all states are pushed. Whenever a state changes the set
    of changes is committed with the done event.
    """

    name = "org_kde_kwin_dpms"
    version = 1

    class mode(enum.IntEnum):
        On = 0
        Standby = 1
        Suspend = 2
        Off = 3


class OrgKdeKwinDpmsProxy(Proxy[OrgKdeKwinDpms]):
    interface = OrgKdeKwinDpms

    @OrgKdeKwinDpms.request(
        Argument(ArgumentType.Uint),
    )
    def set(self, mode: int) -> None:
        """Request dpms state change for the :class:`~pywayland.protocol.wayland.WlOutput`

        Requests that the compositor puts the
        :class:`~pywayland.protocol.wayland.WlOutput` into the passed mode. The
        compositor is not obliged to change the state. In addition the
        compositor might leave the mode whenever it seems suitable. E.g. the
        compositor might return to On state on user input.

        The client should not assume that the mode changed after requesting a
        new mode. Instead the client should listen for the mode event.

        :param mode:
            Requested mode
        :type mode:
            `ArgumentType.Uint`
        """
        self._marshal(0, mode)

    @OrgKdeKwinDpms.request()
    def release(self) -> None:
        """Release the dpms object
        """
        self._marshal(1)
        self._destroy()


class OrgKdeKwinDpmsResource(Resource):
    interface = OrgKdeKwinDpms

    @OrgKdeKwinDpms.event(
        Argument(ArgumentType.Uint),
    )
    def supported(self, supported: int) -> None:
        """Event indicating whether dpms is supported on the :class:`~pywayland.protocol.wayland.WlOutput`

        This event gets pushed on binding the resource and indicates whether
        the :class:`~pywayland.protocol.wayland.WlOutput` supports DPMS. There
        are operation modes of a Wayland server where DPMS might not make sense
        (e.g. nested compositors).

        :param supported:
            Boolean value whether DPMS is supported (1) for the
            :class:`~pywayland.protocol.wayland.WlOutput` or not (0)
        :type supported:
            `ArgumentType.Uint`
        """
        self._post_event(0, supported)

    @OrgKdeKwinDpms.event(
        Argument(ArgumentType.Uint),
    )
    def mode(self, mode: int) -> None:
        """Event indicating used dpms mode

        This mode gets pushed on binding the resource and provides the
        currently used DPMS mode. It also gets pushed if DPMS is not supported
        for the :class:`~pywayland.protocol.wayland.WlOutput`, in that case the
        value will be On.

        The event is also pushed whenever the state changes.

        :param mode:
            The new currently used mode
        :type mode:
            `ArgumentType.Uint`
        """
        self._post_event(1, mode)

    @OrgKdeKwinDpms.event()
    def done(self) -> None:
        """All changes are pushed

        This event gets pushed on binding the resource once all other states
        are pushed.

        In addition it gets pushed whenever a state changes to tell the client
        that all state changes have been pushed.
        """
        self._post_event(2)


class OrgKdeKwinDpmsGlobal(Global):
    interface = OrgKdeKwinDpms


OrgKdeKwinDpms._gen_c()
OrgKdeKwinDpms.proxy_class = OrgKdeKwinDpmsProxy
OrgKdeKwinDpms.resource_class = OrgKdeKwinDpmsResource
OrgKdeKwinDpms.global_class = OrgKdeKwinDpmsGlobal