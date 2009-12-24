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
import time
from zope import interface
from zope.component import getUtility
from zope.component import getMultiAdapter, queryAdapter
from zope.location import Location, LocationProxy
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.app.component.hooks import getSite

from zope.datetime import rfc1123_date
from zope.datetime import time as timeFromDateTimeString

from zope.dublincore.interfaces import ICMFDublinCore

from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher

from zojax.resource.interfaces import IResource

from interfaces import \
    IStaticResource, IPersistentResources, IResourcesContainer

_marker = object()


class Resources(BrowserView, Location):
    interface.implements(IBrowserPublisher)

    def __init__(self, parent, context, request):
        self.__parent__ = parent
        self.__name__ = context.__name__

        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        resource = self.context.get(name)
        if resource is None:
            resource = queryAdapter(request, IStaticResource, name)
            if resource is None:
                raise NotFound(self, name, request)

        if IResourcesContainer.providedBy(resource):
            return Resources(self, resource, request)
        else:
            return ResourceWrapper(resource, request)

    def browserDefault(self, request):
        return empty, ()

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            if default is _marker:
                raise NotFound(None, name)
            return default

    def __getitem__(self, name):
        resource = self.context.get(name)

        if resource is None:
            raise KeyError(name)

        if IResourcesContainer.providedBy(resource):
            return Resources(self, resource, self.request)
        else:
            return ResourceWrapper(resource, self.request)


class ContainerResources(Resources):

    def __init__(self, request):
        self.__name__ = u'zojax-resources'

        self.request = request
        self.context = getUtility(IPersistentResources)


class ResourceWrapper(Location):
    interface.implements(IResource, IBrowserPublisher)

    def __init__(self, resource, request):
        self.request = request
        self.resource = resource

        self.__name__ = resource.__name__

    def __call__(self):
        name = self.__name__
        url = str(getMultiAdapter((getSite(), self.request), IAbsoluteURL))
        return "%s/@@/zojax-resources/%s" % (url, name)

    def publishTraverse(self, request, name):
        raise NotFound(None, name)

    def browserDefault(self, request):
        return getattr(self, request.method), ()

    def GET(self):
        request = self.request
        resource = self.resource
        response = request.response

        dc = ICMFDublinCore(resource, None)
        if dc is None:
            resource = IResource(resource)
            lmt = resource.modified()
            response.setHeader('Content-Type', resource.context.content_type)
        else:
            lmt = long(time.mktime(dc.modified.timetuple()))

        header = request.getHeader('If-Modified-Since', None)
        if header is not None:
            header = header.split(';')[0]
            try:    mod_since=long(timeFromDateTimeString(header))
            except: mod_since=None
            if mod_since is not None:
                if lmt > 0 and lmt <= mod_since:
                    response.setStatus(304)
                    return ''

        response.setHeader('Last-Modified', rfc1123_date(lmt))
        return resource.render(request)

    def HEAD(self):
        resource = self.resource
        response = self.request.response

        dc = ICMFDublinCore(resource, None)
        if dc is None:
            resource = IResource(resource)
            lmt = resource.modified()
            response.setHeader('Content-Type', resource.context.content_type)
        else:
            lmt = long(time.mktime(dc.modified.timetuple()))

        response.setHeader('Last-Modified', lmt)
        return ''

    def modified(self):
        dc = ICMFDublinCore(self.resource)
        return long(time.mktime(dc.modified.timetuple()))


def empty():
    return ''
