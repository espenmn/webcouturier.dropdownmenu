# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from plone import api
#from zope.schema.interfaces import IVocabularyFactory

from webcouturier.dropdownmenu import msg_fact as _

try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite

def format_size(size):
    return size.split(' ')[0]


def SizeVocabulary(context):
    site = getSite()
    #default vocabulary if everything else fails
    sizes = None
    terms = [
            SimpleTerm('mini', 'mini', u'Mini'),
            SimpleTerm('preview', 'preview', u'Preview'),
            SimpleTerm('icon', 'icon', u'Icon'),
            SimpleTerm('none', 'none', u'none'),
        ]
        
    try:
        #Plone 5
        sizes = api.portal.get_registry_record('plone.allowed_sizes')
    except: 
        #Plone 4
        portal_properties = api.portal.get_tool(name='portal_properties')
        if 'imaging_properties' in portal_properties.objectIds():
            sizes = portal_properties.imaging_properties.getProperty('allowed_sizes')

    if sizes:
        if not 'none' in sizes:
            sizes += ('none',)
        terms = [ SimpleTerm(value=format_size(pair), token=format_size(pair), title=pair) for pair in sizes ]
      
    return SimpleVocabulary(terms)
    
 