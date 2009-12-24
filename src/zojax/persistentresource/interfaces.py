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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.filefield.field import FileField
from zojax.content.type.interfaces import IItem

_ = MessageFactory('zojax.persistentresource')


class IResource(interface.Interface):

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Resource title'),
        default = u'',
        missing_value = u'',
        required = False)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Resource description'),
        default = u'',
        missing_value = u'',
        required = False)

    def render(request):
        """ render resource """


class IFileResource(IResource):
    """ file """

    data = FileField(
        title = _(u'Resource data'),
        description = _(u'Upload resource data.'),
        required = True)


class ICSSResource(IResource):
    """ css """

    data = schema.SourceText(
        title = _(u'Source'),
        description = _(u'The source of css data.'),
        required = True)


class ITextResource(IResource):
    """ text """

    contentType = schema.TextLine(
        title = _(u'Content type'),
        default = u'text/plain',
        required = True)

    text = schema.SourceText(
        title = _(u'Text'),
        description = _(u'Resource text.'),
        required = True)


class IResourcesContainer(IItem):
    """ container """


class IRootResourcesContainer(IResourcesContainer):
    """ root resources container """


class IPersistentResources(interface.Interface):
    """ persistent resources configlet """


class IStaticResource(interface.Interface):
    """ static resource """
