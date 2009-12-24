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
from zope import interface
from zojax.content.type.item import PersistentItem

from interfaces import ITextResource


class TextResource(PersistentItem):
    interface.implements(ITextResource)

    def render(self, request):
        response = request.response

        response.setHeader('Content-Type', self.contentType)
        response.setHeader('Content-Length', len(self.text))
        response.setHeader(
            'Content-Disposition',
            'inline; filename="%s"'%self.__name__.encode('utf-8'))
        return self.text
