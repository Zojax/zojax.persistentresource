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
from zope.lifecycleevent.interfaces import IObjectCopiedEvent

from zojax.content.type.item import PersistentItem
from zojax.filefield.field import FileFieldProperty
from zojax.filefield.interfaces import IFile

from interfaces import IFileResource


class FileResource(PersistentItem):
    interface.implements(IFileResource)

    data = FileFieldProperty(IFileResource['data'])

    def render(self, request):
        return self.data.show(request, filename=self.__name__)


@component.adapter(IFileResource, IObjectCopiedEvent)
def fileCopiedEvent(resource, event):
    if IFileResource.providedBy(event.original) and \
           IFile.providedBy(resource.data):
        resource.data.afterCopy(event.original.data)
