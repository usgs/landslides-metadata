#!/usr/bin/env python

""" Read in excel metadata file (.csv) to make separate .xml metadata files for each inventory.
Must be run using Python 3"""

""" Disclaimer: This software is preliminary or provisional and is subject to revision. 
It is being provided to meet the need for timely best science. The software has not received final approval 
by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. 
Government as to the functionality of the software and related material nor shall the fact of release constitute 
any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government 
shall be held liable for any damages resulting from the authorized or unauthorized use of the software."""

#stdlib imports
from collections import OrderedDict
import pandas as pd
import dicttoxml
from xml.dom.minidom import parseString, parse
import xml.etree.ElementTree as ET
import os
import datetime
from configobj import ConfigObj


def readmetadata(config):
    """
    This function runs creates metadata files from a common CSV input for 
    individual files that are part of a data collection.
    
    :param config: filepath defining configobj location
    :type config: string
    """

    # Load config
    config = ConfigObj(config)
    config = config['metadata']

    # read in excel file (must be csv)
    xl = pd.read_csv(config['inputfile']['file'])

    # run through for-loop to make into OrderedDict
    # Declare variables
    string = []
    metadata = OrderedDict()
    a, b = xl.shape

    #run through for loop of the same size as the number of inventories
    for i in range(2, a):
        #start new dictionary element for each repository with similar basic structure
        metadata.update({'metadata': {'eainfo': {'overview': {}}, 
                                      'idinfo': {'citation': {'citeinfo': {'pubinfo': {}}}, 
                                                 'descript': {}, 'timeperd': {'timeinfo': {'rngdates': {}}}, 
                                                 'status': {}, 'spdom': {'bounding': {}}, 
                                                 'keywords': {'theme': {}, 'place': {}}, 
                                                 'ptcontac': {'cntinfo': {'cntperp': {}, 'cntaddr': {}}}}, 
                                      'dataqual': {'attracc': {}, 'posacc': {'horizpa': {}, 'vertacc': {}}, 
                                                   'lineage': {'procstep': {}}}, 
                                      'distinfo': {'stdorder': {'digform': {'digtopt': {'onlinopt': {'computer': {'networka': {}}}}}}, 
                                                   'distrib': {'cntinfo': {'cntperp': {}, 'cntaddr': {}}}}, 
                                      'metainfo': {'metc': {'cntinfo': {'cntperp': {}, 'cntaddr': {}}}}}})

        # add unique inventory information

        # for citation/citeinfo
        for j in range(2, 6):
            # set citation info
            if j == 2:
                metadata['metadata']['idinfo']['citation']['citeinfo'][xl['Citation'].loc[0]] = xl['Citation'].loc[i]
            else:
                if pd.isnull(xl['Unnamed: %i' % (j-1)].loc[i]):
                    metadata['metadata']['idinfo']['citation']['citeinfo'][xl['Unnamed: %i' % (j-1)].loc[0]] = 'TBD'
                else:
                    metadata['metadata']['idinfo']['citation']['citeinfo'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]
            if j == 5:
                metadata['metadata']['idinfo']['citation']['citeinfo'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]

        metadata['metadata']['idinfo']['citation']['citeinfo']['geoform'] = config['geoform']
        metadata['metadata']['idinfo']['citation']['citeinfo']['pubinfo']['pubplace'] = config['pubplace']
        metadata['metadata']['idinfo']['citation']['citeinfo']['pubinfo']['publish'] = config['publish']
        metadata['metadata']['idinfo']['citation']['citeinfo']['lworkcit'] = {'citeinfo': config['citeinfo']}

        # for descript
        for j in range(6, 9):
            # set description info
            if j == 6:
                metadata['metadata']['idinfo']['descript'][xl['Description'].loc[0]] = 'TBD'
            else:
                if pd.isnull(xl['Unnamed: %i' % (j-1)].loc[i]):
                    metadata['metadata']['idinfo']['descript'][xl['Unnamed: %i' % (j-1)].loc[0]] = 'TBD'
                else:
                    metadata['metadata']['idinfo']['descript'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]

        # for timeperd/timeinfo/rngdates
        for j in range(9, 11):
            # set time info
            if j == 9:
                metadata['metadata']['idinfo']['timeperd']['timeinfo']['rngdates'][xl['Time'].loc[0]] = xl['Time'].loc[i]
                metadata['metadata']['idinfo']['timeperd']['current'] = xl['Time'].loc[i]
            else:
                metadata['metadata']['idinfo']['timeperd']['timeinfo']['rngdates'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]

        # for status
        for j in range(11, 13):
            # set time info
            if j == 11:
                metadata['metadata']['idinfo']['status'][xl['Status'].loc[0]] = xl['Status'].loc[i]
            else:
                metadata['metadata']['idinfo']['status'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]

        # for spdom
        for j in range(13, 14):
            if j == 13:
                metadata['metadata']['idinfo']['spdom']['descgeog'] = xl['Geographical Context'].loc[i]
        metadata['metadata']['idinfo']['spdom']['bounding']['westbc'] = 'TBD'
        metadata['metadata']['idinfo']['spdom']['bounding']['eastbc'] = 'TBD'
        metadata['metadata']['idinfo']['spdom']['bounding']['northbc'] = 'TBD'
        metadata['metadata']['idinfo']['spdom']['bounding']['southbc'] = 'TBD'

        # for keywords
        for j in range(14, 17):
            if j == 14:
                metadata['metadata']['idinfo']['keywords']['theme'][xl['Keywords'].loc[0]] = 'TBD'
            if j == 15:
                metadata['metadata']['idinfo']['keywords']['place'][xl['Unnamed: %i' % (j-1)].loc[0]] = 'TBD'
        #if j == 16:
        #    metadata['metadata']['idinfo']['keywords']['temporal'][xl['Unnamed: %i' % (j-1)].loc[0]] = 'TBD'
        metadata['metadata']['idinfo']['keywords']['theme']['themekt'] = 'USGS Thesaurus'
        #metadata['metadata']['idinfo']['keywords']['temporal']['tempkt'] = 'USGS Thesaurus'
        metadata['metadata']['idinfo']['keywords']['place']['placekt'] = 'USGS Thesaurus'

        metadata['metadata']['idinfo']['accconst'] = 'none'
        metadata['metadata']['idinfo']['useconst'] = 'none'

        # for ptcontact
        for j in range(17, b):
            if j == 17:
                metadata['metadata']['idinfo']['ptcontac']['cntinfo']['cntperp'][xl['Contact'].loc[0]] = xl['Contact'].loc[i]
            elif j == 18:
                metadata['metadata']['idinfo']['ptcontac']['cntinfo']['cntperp'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]
            elif j == b-1:
                metadata['metadata']['idinfo']['ptcontac']['cntinfo'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]
            else:
                if pd.isnull(xl['Unnamed: %i' % (j-1)].loc[i]):
                    metadata['metadata']['idinfo']['ptcontac']['cntinfo']['cntaddr'][xl['Unnamed: %i' % (j-1)].loc[0]] = 'TBD'
                else:
                    metadata['metadata']['idinfo']['ptcontac']['cntinfo']['cntaddr'][xl['Unnamed: %i' % (j-1)].loc[0]] = xl['Unnamed: %i' % (j-1)].loc[i]
        metadata['metadata']['idinfo']['ptcontac']['cntinfo']['cntaddr']['addrtype'] = 'mailing and physical'
        metadata['metadata']['idinfo']['ptcontac']['cntinfo']['cntaddr']['state'] = 'none'
        metadata['metadata']['idinfo']['ptcontac']['cntinfo']['cntvoice'] = 'none'

        # set database-wide info (these do not change from iteration to iteration)

        # dataqual
        metadata['metadata']['dataqual'] = config['dataqual']

        # eainfo
        metadata['metadata']['eainfo']['overview']['eaover'] = 'TBD'
        metadata['metadata']['eainfo']['overview']['eadetcit'] = 'Unknown'

        # distinfo
        metadata['metadata']['distinfo']['stdorder']['digform']['digtopt']['onlinopt']['computer']['networka']['networkr'] = 'Specific Dataset Link'
        metadata['metadata']['distinfo']['stdorder']['fees'] = 'None'
        metadata['metadata']['distinfo']['stdorder']['digform']['digtinfo'] = {'formname': 'ASCII'}
        metadata['metadata']['distinfo']['distrib']['cntinfo'] = config['distinfo']

        metadata['metadata']['distinfo']['distliab'] = config['disclaimer']

        # metainfo
        metadata['metadata']['metainfo']['metstdn'] = 'FGDC Content Standard for Digital Geospatial Metadata'
        metadata['metadata']['metainfo']['metstdv'] = 'FGDC-STD-001-1998'
        metadata['metadata']['metainfo']['metd'] = 'TBD'
        metadata['metadata']['metainfo']['metc']['cntinfo'] = config['metainfo']

        # clean up name
        invname = str(xl['Inventory'].loc[i]).replace(', ', '_')
        invname = invname.replace(',', '_')
        invname = invname.replace(' ', '_')
        fullname = 'metadata_%s_%i.xml' % (invname, i)

        # print OrderedDict to xml file
        xml = dicttoxml.dicttoxml(metadata)
        # Print xml to file
        try:
            dom = parseString(xml)
            filename = open(os.path.join(config['outpath']['file'], fullname), 'w')
            filename.write(str(dom.toxml()))
            filename.close()
        except:
            print('Error parsing xml to file.  Check lines 183 to 186')

        #######################################################
        # If any entries have more than one item.
        #######################################################

        # deal with duplicate entries / split into new elements
        # reopen file

        tree = ET.parse(os.path.join(config['outpath']['file'], fullname))
        root = tree.getroot()

        # For multiple original citations
        for q in root.iter('descript'):
            for s in q.iter('suppleinf'):
                t = s.text
                u = t.split('; ')
                for w in range(0, len(u)):
                    if w == 0:
                        s.text = u[w]
                    else:
                        el = ET.SubElement(q, 'suppleinf')
                        el.text = u[w]

        db_authors = ''
        # For database authors
        for m in root.iter('lworkcit'):
            for q in m.iter('citeinfo'):
                for s in q.iter('origin'):
                    t = s.text
                    u = t.split('; ')
                    for w in range(0, len(u)):
                        #db_authors += u[w] + ', '
                        if w == 0:
                            s.text = u[w]
                            db_authors += u[w] + ', '
                        else:
                            el = ET.SubElement(q, 'origin')
                            el.text = u[w]
                            #db_authors += u[w] + ', '
                        #db_authors += u[w] + ', '

        authors = ''
        # For dataset authors
        for q in root.iter('citeinfo'):
            for s in q.iter('origin'):
                t = s.text
                if t.find('; ') != -1:
                    l = t.split('; ')
                    for w in range(0, len(l)):
                        #authors += l[w] + ', '
                        if w == 0:
                            s.text = l[w]
                            authors += l[w] + ', '
                        else:
                            el = ET.SubElement(q, 'origin')
                            el.text = l[w]
                            authors += l[w] + ', '
                        #authors += l[w] + ', '
                        #import pdb; pdb.set_trace()

        # For points of contact cntemail
        if root.find('./metadata/idinfo/ptcontac/cntinfo/cntperp/cntper').text.find(';') != -1:
            for m in root.iter('ptcontac'):
                el = ET.SubElement(m, 'cntinfo')
                for q in m.iter('cntinfo'):
                    for s in q.iter('cntemail'):
                        t = s.text
                        u = t.split('; ')
                        for w in range(0, len(u)):
                            if w == 0:
                                s.text = u[w]
                            else:
                                el2 = ET.SubElement(el, 'cntemail')
                                el2.text = u[w]
                # For contact addrinfo
                address = ['addrtype', 'city', 'postal', 'address', 'country', 'state']
                for q in m.iter('cntaddr'):
                    for x in range(0, len(address)):
                        for s in q.iter(address[x]):
                            t = s.text
                            if t.find(';') != -1:
                                u = t.split('; ')
                                for w in range(0, len(u)):
                                    if w == 0:
                                        s.text = u[w]
                                    else:
                                        el2 = ET.SubElement(el, address[x])
                                        el2.text = u[w]
                            else:
                                el2 = ET.SubElement(el, address[x])
                                el2.text = t
                # For contact person info
                person = ['cntper', 'cntorg']
                for q in m.iter('cntperp'):
                    for x in range(0, len(person)):
                        for s in q.iter(person[x]):
                            t = s.text
                            if t.find(';') != -1:
                                u = t.split('; ')
                                for w in range(0, len(u)):
                                    if w == 0:
                                        s.text = u[w]
                                    else:
                                        el2 = ET.SubElement(el, person[x])
                                        el2.text = u[w]
                            else:
                                el2 = ET.SubElement(el, person[x])
                                el2.text = t

        # Elso for dual emails
        for m in root.iter('ptcontac'):
            for q in m.iter('cntinfo'):
                for s in q.iter('cntemail'):
                    t = s.text
                    u = t.split('; ')
                    for w in range(0, len(u)):
                        if w == 0:
                            s.text = u[w]
                        else:
                            el = ET.SubElement(q, 'cntemail')
                            el.text = u[w]

        # write changes to xml tree item
        tree.write(os.path.join(config['outpath']['file'], fullname))

        # write changes to file
        try:
            dom1 = parse(os.path.join(config['outpath']['file'], fullname))
            filename = open(os.path.join(config['outpath']['file'], fullname), 'w')
            filename.write(str(dom1.toprettyxml()))
            filename.close()
        except:
            print('Could not parse updated xml to file.  Check lines 316 to 319.')

        #######################################################
        # XML FILES HAVE BEEN WRITTEN. THE FOLLOWING IS ADDITIONAL.
        #######################################################

        ##########################################
        # THE FOLLOWING IS JUST FOR PRINTING CITATIONS TO FILE.
        ##########################################
        date = datetime.datetime.now()

        if config['printcitations']:
            tempstring = authors
            # Write citations to file
            for q in root.iter('citeinfo'):
                r = q.iter('pubdate')
                next(r)
                for items in r:
                    tempstring += items.text + ', '
                r = q.iter('title')
                next(r)
                for items in r:
                    tempstring += items.text + ', '
                r = q.iter('onlink')
                next(r)
                for items in r:
                    tempstring += items.text + ', '
            tempstring += 'in '
            for q in root.iter('lworkcit'):
                tempstring += db_authors
                for r in q.iter('pubdate'):
                    tempstring += r.text + ', '
                for r in q.iter('title'):
                    tempstring += r.text + ', '
                for r in q.iter('publish'):
                    tempstring += r.text + ', '
                tempstring += 'accessed on' + date.strftime("%B %d, %Y") + ', '
                for r in q.iter('onlink'):
                    tempstring += 'at ' + r.text
            tempstring += '.'
            string.append(str(tempstring))

    if config['printcitations']:
        try:
            filename = open(os.path.join(config['outpath']['file'], 'citations.doc'), 'w')
            for i in range(2, a):
                filename.write(str(invname))
                filename.write('\n\n %s \n\n' % string[i-2])
            filename.close()
        except:
            print('Could not print citations to file.  Check lines 365 to 369.')
