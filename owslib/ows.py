# -*- coding: ISO-8859-15 -*-
# =============================================================================
# Copyright (c) 2008 Tom Kralidis
#
# Authors : Tom Kralidis <tomkralidis@hotmail.com>
#
# Contact email: tomkralidis@hotmail.com
# =============================================================================

"""
API for OGC Web Services Common (OWS) constructs and metadata.

OWS Common: http://www.opengeospatial.org/standards/common

Currently supports version 1.1.0 (06-121r3).
"""

from owslib.etree import etree
from owslib import crs, util

OWS_NAMESPACE_1_0_0 = 'http://www.opengis.net/ows'
OWS_NAMESPACE_1_1_0 = 'http://www.opengis.net/ows/1.1'
OWS_NAMESPACE_2_0 = 'http://www.opengis.net/ows/2.0'
XSI_NAMESPACE       = 'http://www.w3.org/2001/XMLSchema-instance'
XLINK_NAMESPACE     = 'http://www.w3.org/1999/xlink'

DEFAULT_OWS_NAMESPACE=OWS_NAMESPACE_1_1_0     #Use this as default for OWSCommon objects

class OwsCommon(object):
    """Initialize OWS Common object"""
    def __init__(self,version):
        self.version = version
        if version == '1.0.0':
            self.namespace = OWS_NAMESPACE_1_0_0
        else:
            self.namespace = OWS_NAMESPACE_1_1_0
    
class ServiceIdentification(object):
    """Initialize an OWS Common ServiceIdentification construct"""
    def __init__(self,infoset,namespace=DEFAULT_OWS_NAMESPACE): 
        self._root = infoset

        val = self._root.find(util.nspath('Title', namespace))
        self.title = util.testXMLValue(val)

        val = self._root.find(util.nspath('Abstract', namespace))
        self.abstract = util.testXMLValue(val)

        self.keywords = []
        for f in self._root.findall(util.nspath('Keywords/Keyword', namespace)):
            if f.text is not None:
                self.keywords.append(f.text)
    

        val = self._root.find(util.nspath('AccessConstraints', namespace))
        self.accessconstraints = util.testXMLValue(val)

        val = self._root.find(util.nspath('Fees', namespace))
        self.fees = util.testXMLValue(val)

        val = self._root.find(util.nspath('ServiceType', namespace))
        self.type = util.testXMLValue(val)
        self.service=self.type #alternative? keep both?discuss

        val = self._root.find(util.nspath('ServiceTypeVersion', namespace))
        self.version = util.testXMLValue(val)

        self.profiles = []
        for p in self._root.findall(util.nspath('Profile', namespace)):
            self.profiles.append(util.testXMLValue(val))

class ServiceProvider(object):
    """Initialize an OWS Common ServiceProvider construct"""
    def __init__(self, infoset,namespace=DEFAULT_OWS_NAMESPACE):
        self._root = infoset
        val = self._root.find(util.nspath('ProviderName', namespace))
        self.name = util.testXMLValue(val)
        self.contact = ServiceContact(infoset, namespace)
        val = self._root.find(util.nspath('ProviderSite', namespace))
        if val is not None:
            urlattrib=val.attrib[util.nspath('href', XLINK_NAMESPACE)]
            self.url = util.testXMLValue(urlattrib, True)
        else:
            self.url =None

class ServiceContact(object):
    """Initialize an OWS Common ServiceContact construct"""
    def __init__(self, infoset,namespace=DEFAULT_OWS_NAMESPACE):
        self._root = infoset
        val = self._root.find(util.nspath('ProviderName', namespace))
        self.name = util.testXMLValue(val)
        
        self.organization=util.testXMLValue(self._root.find(util.nspath('ContactPersonPrimary/ContactOrganization', namespace)))
        
        val = self._root.find(util.nspath('ProviderSite', namespace))
        if val is not None:
            self.site = util.testXMLValue(val.attrib.get(util.nspath('href', XLINK_NAMESPACE)), True)
        else:
            self.site = None

        val = self._root.find(util.nspath('ServiceContact/Role', namespace))
        self.role = util.testXMLValue(val)

        val = self._root.find(util.nspath('ServiceContact/IndividualName', namespace))
        self.name = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/PositionName', namespace))
        self.position = util.testXMLValue(val)
 
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Phone/Voice', namespace))
        self.phone = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Phone/Facsimile', namespace))
        self.fax = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Address/DeliveryPoint', namespace))
        self.address = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Address/City', namespace))
        self.city = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Address/AdministrativeArea', namespace))
        self.region = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Address/PostalCode', namespace))
        self.postcode = util.testXMLValue(val)

        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Address/Country', namespace))
        self.country = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/Address/ElectronicMailAddress', namespace))
        self.email = util.testXMLValue(val)

        val = self._root.find(util.nspath('ServiceContact/ContactInfo/OnlineResource', namespace))
        if val is not None:
            self.url = util.testXMLValue(val.attrib.get(util.nspath('href', XLINK_NAMESPACE)), True)
        else:
            self.url = None

        val = self._root.find(util.nspath('ServiceContact/ContactInfo/HoursOfService', namespace))
        self.hours = util.testXMLValue(val)
    
        val = self._root.find(util.nspath('ServiceContact/ContactInfo/ContactInstructions', namespace))
        self.instructions = util.testXMLValue(val)
   
class OperationsMetadata(object):
    """Initialize an OWS OperationMetadata construct"""
    def __init__(self,elem,namespace=DEFAULT_OWS_NAMESPACE):
        self.name = elem.attrib['name']
        self.formatOptions = ['text/xml']
        methods = []
        parameters = []
        constraints = []

        for verb in elem.findall(util.nspath('DCP/HTTP/*', namespace)):
            methods.append((util.xmltag_split(verb.tag), {'url': verb.attrib[util.nspath('href', XLINK_NAMESPACE)]}))
        self.methods = dict(methods)

        for parameter in elem.findall(util.nspath('Parameter', namespace)):
            if namespace == OWS_NAMESPACE_1_1_0:
                parameters.append((parameter.attrib['name'], {'values': [i.text for i in parameter.findall(util.nspath('AllowedValues/Value', namespace))]}))
            else:
                parameters.append((parameter.attrib['name'], {'values': [i.text for i in parameter.findall(util.nspath('Value', namespace))]}))
        self.parameters = dict(parameters)

        for constraint in elem.findall(util.nspath('Constraint', namespace)):
            constraints.append((constraint.attrib['name'], {'values': [i.text for i in constraint.findall(util.nspath('Value', namespace))]}))
        self.constraints = dict(constraints)

class BoundingBox(object):
    """Initialize an OWS BoundingBox construct"""
    def __init__(self, elem, namespace=DEFAULT_OWS_NAMESPACE): 
        self.minx = None
        self.miny = None
        self.maxx = None
        self.maxy = None

        val = elem.attrib.get('crs')
        if val is not None:
            self.crs = crs.Crs(val)
        else:
            self.crs = None

        val = elem.attrib.get('dimensions')
        if val is not None:
            self.dimensions = int(util.testXMLValue(val, True))
        else:  # assume 2
            self.dimensions = 2

        val = elem.find(util.nspath('LowerCorner', namespace))
        tmp = util.testXMLValue(val)
        if tmp is not None:
            xy = tmp.split()
            if len(xy) > 1:
                if self.crs is not None and self.crs.axisorder == 'yx':
                    self.minx, self.miny = xy[1], xy[0] 
                else:
                    self.minx, self.miny = xy[0], xy[1]

        val = elem.find(util.nspath('UpperCorner', namespace))
        tmp = util.testXMLValue(val)
        if tmp is not None:
            xy = tmp.split()
            if len(xy) > 1:
                if self.crs is not None and self.crs.axisorder == 'yx':
                    self.maxx, self.maxy = xy[1], xy[0]
                else:
                    self.maxx, self.maxy = xy[0], xy[1]

class WGS84BoundingBox(BoundingBox):
    """WGS84 bbox, axis order xy"""
    def __init__(self, elem, namespace=DEFAULT_OWS_NAMESPACE):
        BoundingBox.__init__(self, elem, namespace)
        self.dimensions = 2
        self.crs = crs.Crs('urn:ogc:def:crs:OGC:2:84')



class ExceptionReport(Exception):
    """OWS ExceptionReport"""

    def __init__(self, elem, namespace=DEFAULT_OWS_NAMESPACE):
        self.exceptions = []
        for i in elem.findall(util.nspath('Exception', namespace)):
            tmp = {}
            val = i.attrib.get('exceptionCode')
            tmp['exceptionCode'] = util.testXMLValue(val, True)
            val = i.attrib.get('locator')
            tmp['locator'] = util.testXMLValue(val, True)
            val = i.find(util.nspath('ExceptionText', namespace))
            tmp['ExceptionText'] = util.testXMLValue(val)
            self.exceptions.append(tmp)

        # set topmost stacktrace as return message
        self.code = self.exceptions[0]['exceptionCode']
        self.locator = self.exceptions[0]['locator']
        self.msg = self.exceptions[0]['ExceptionText']
        self.xml = etree.tostring(elem)

    def __str__(self):
        return repr(self.msg)
