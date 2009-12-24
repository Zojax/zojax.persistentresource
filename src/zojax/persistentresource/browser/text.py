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
from zope.proxy import removeAllProxies
from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL

from z3c.form.interfaces import IFieldWidget

from zojax.wizard.step import WizardStep
from zojax.content.forms.form import AddForm
from zojax.layoutform import Fields, PageletEditSubForm
from zojax.persistentresource.interfaces import ITextResource

from publisher import getPath


def customWidget(field, request):
    widget = getMultiAdapter((field, request), IFieldWidget)

    widget.rows = 30
    widget.style = u'font-family: monospace; font-size: 130%'

    return widget


class AddTextResource(AddForm):

    fields = Fields(ITextResource)
    fields['text'].widgetFactory = customWidget

    def nextURL(self):
        container = self.context.__parent__.__parent__
        return '%s/%s/context.html'%(
            absoluteURL(container, self.request), self._addedObject.__name__)


class ModifyTextResource(PageletEditSubForm):

    fields = Fields(ITextResource)
    fields['text'].widgetFactory = customWidget


class TextView(WizardStep):

    def path(self):
        return '%s/@@/zojax-resources/%s'%(
            absoluteURL(getSite(), self.request), getPath(self.context))
