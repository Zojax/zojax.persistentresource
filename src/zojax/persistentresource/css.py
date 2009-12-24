##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component
from zope.proxy import removeAllProxies
from zope.app.component.hooks import getSite
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from z3c.zrtresource.replace import Replace
from z3c.zrtresource.processor import ZRTProcessor

from zojax.content.type.item import PersistentItem

from interfaces import ICSSResource


class CSSResource(PersistentItem):
    interface.implements(ICSSResource)

    _v_cache = None

    contentType = u'text/css'

    def render(self, request):
        response = request.response

        if self._v_cache is None:
            p = ZRTProcessor(
                "/* zrt-cssregistry: */ \n"+self.data,
                commands={'replace': Replace})
            self._v_cache = p.process(getSite(), request)

        data = self._v_cache
        response.setHeader('Content-Length', len(data))
        response.setHeader('Content-Type', self.contentType)
        return data


@component.adapter(ICSSResource, IObjectModifiedEvent)
def cssModifiedHandler(resource, event):
    removeAllProxies(resource)._v_cache = None
