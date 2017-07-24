#!/usr/bin/env python

""" Read in excel metadata file (.csv) to make separate .xml metadata files for inventory."""

#stdlib imports
from collections import OrderedDict
import pandas as pd
import dicttoxml
from xml.dom.minidom import parseString, parse
import xml.etree.ElementTree as ET
import os


def readmetadata(inputfile, outpath, citeinfo='None', distinfo='None', dataqual='None', geoform='Electronic', pubplace='None', publish='None', disclaimer='default', metainfo='default'):
    """
    This function runs creates metadata files from a common CSV input.
    ####
    Variables
    ####
    inputfile = string, full path to input file
    outpath = string, full path to output file directory
    citeinfo = dictionary, containing full citation information in the form:
                {'origin': 'Schmitt, R.; Tanyas, H.; Jessee, M.A.; Zhu, J.; Biegel, K.; Allstadt, K.E.; Jibson, R.W.; Thompson, E.M.;
                            van Westen, C.; Sato, H.P.; Wald, D.J.; Godt, J.W.; Gorum, T.; Moss, R.E.S.; Xu, C.',
                 'pubdate': '2017',
                 'pubinfo': {'publish': 'U.S. Geological Survey data release collection', 'pubplace': 'Golden, CO'},
                 'title': 'An Open Repository of Earthquake-triggered Ground Failure Inventories',
                 'onlink': 'https://doi.org/10.5066/xxxxxxx'}
    distinfo = dictionary, containing distributor contact information. If None, will use ScienceBase as distributor.
                {'cntperp': {'cntper': 'ScienceBase', 'cntorg': 'U.S. Geological Survey - ScienceBase'},
                 'cntaddr': {'addrtype': 'mailing and physical', 'address': 'Denver Federal Center, Building 810', 'city':
                            'Denver', 'state': 'CO', 'postal': '80225', 'country': 'USA'},
                 'cntvoice': '1-888-275-8747',
                 'cntemail': 'sciencebase@usgs.gov'}
    dataqual = dictionary, containing data quality information. If None, will use default of no data quality checks.
                {'attracc': {'attraccr': 'No formal attribute accuracy tests were conducted.'},
                 'logic': 'No formal logical accuracy tests were conducted.',
                 'complete': 'Data set is considered complete for the information presented, as described in the abstract.
                              Users are advised to read the rest of the metadata record carefully for additional details.',
                 'postacc': {'horizpa': {'horizpar': 'No formal positional accuracy tests were conducted.'}, 'vertacc':
                            {'vertaccr': 'No formal positional accuracy tests were conducted.''}},
                 'lineage': {'procstep': {'procdesc': 'All dataset projection systems were converted to WGS84.',
                                          'procdate': 'General Processing Data when provided.'}}}
    geoform = string, mode in which the geospatial data is presented.
    pubplace = string, geographical place data was published
    publish = string, publisher of data.
    disclaimer = string, custom disclaimer, if 'default', will use a default USGS disclaimer
    metainfo = dictionary, containing metadata contact information.  If default, will use GHSC Data Steward.
                {'cntperp': {'cntper': 'GHSC Data Steward', 'cntorg': 'U.S. Geological Survey, Geological Hazards Science Center'},
                 'cntpos': 'Open Data Policy Coordinator',
                 'cntaddr': {'addrtype': 'mailing and physical', 'address': '1711 Illinois St.', 'city': 'Golden',
                             'state': 'CO', 'postal': '80401', 'country': 'USA'},
                 'cntvoice': '303-273-8500',
                 'cntemail': 'ghsc_metadata@usgs.gov'}
    """

    # read in excel file (must be csv)
    xl = pd.read_csv(inputfile)

    # run through for-loop to make into OrderedDict
    # Declare variables
    string = []
    metadata = OrderedDict()
    a, b = xl.shape

    #run through for loop of the same size as the number of inventories
    for i in range(2, a):
        #start new dictionary element for each repository with similar basic structure
        metadata.update({'metadata': {'eainfo': {'overview': {}}, 'idinfo': {'citation': {'citeinfo': {'pubinfo': {}}}, 'descript': {}, 'timeperd': {'timeinfo': {'rngdates': {}}}, 'status': {}, 'spdom': {'bounding': {}}, 'keywords': {'theme': {}, 'place': {}}, 'ptcontac': {'cntinfo': {'cntperp': {}, 'cntaddr': {}}}}, 'dataqual': {'attracc': {}, 'posacc': {'horizpa': {}, 'vertacc': {}}, 'lineage': {'procstep': {}}}, 'distinfo': {'stdorder': {'digform': {'digtopt': {'onlinopt': {'computer': {'networka': {}}}}}}, 'distrib': {'cntinfo': {'cntperp': {}, 'cntaddr': {}}}}, 'metainfo': {'metc': {'cntinfo': {'cntperp': {}, 'cntaddr': {}}}}}})

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

        metadata['metadata']['idinfo']['citation']['citeinfo']['geoform'] = geoform
        metadata['metadata']['idinfo']['citation']['citeinfo']['pubinfo']['pubplace'] = pubplace
        metadata['metadata']['idinfo']['citation']['citeinfo']['pubinfo']['publish'] = publish
        if citeinfo == 'None':
            metadata['metadata']['idinfo']['citation']['citeinfo']['lworkcit'] = {'citeinfo': {'origin': 'Schmitt, R.; Tanyas, H.; Jessee, M.A.; Zhu, J.; Biegel, K.; Allstadt, K.E.; Jibson, R.W.; Thompson, E.M.; van Westen, C.; Sato, H.P.; Wald, D.J.; Godt, J.W.; Gorum, T.; Moss, R.E.S.; Xu, C.', 'pubdate': '2017', 'pubinfo': {'publish': 'U.S. Geological Survey data release collection', 'pubplace': 'Golden, CO'}, 'title': 'An Open Repository of Earthquake-triggered Ground Failure Inventories', 'onlink': 'https://doi.org/10.5066/xxxxxxx'}}
        else:
            metadata['metadata']['idinfo']['citation']['citeinfo']['lworkcit'] = {'citeinfo': citeinfo}

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
        if dataqual == 'None':
            metadata['metadata']['dataqual']['attracc']['attraccr'] = 'No formal attribute accuracy tests were conducted.'
            metadata['metadata']['dataqual']['logic'] = 'No formal logical accuracy tests were conducted.'
            metadata['metadata']['dataqual']['complete'] = 'Data set is considered complete for the information presented, as described in the abstract. Users are advised to read the rest of the metadata record carefully for additional details.'
            metadata['metadata']['dataqual']['posacc']['horizpa']['horizpar'] = 'No formal positional accuracy tests were conducted.'
            metadata['metadata']['dataqual']['posacc']['vertacc']['vertaccr'] = 'No formal positional accuracy tests were conducted.'
            metadata['metadata']['dataqual']['lineage']['procstep']['procdesc'] = 'All dataset projection systems were converted to WGS84.'
            metadata['metadata']['dataqual']['lineage']['procstep']['procdate'] = 'General Processing Data when provided.'
        else:
            metadata['metadata']['dataqual'] = dataqual

        # eainfo
        metadata['metadata']['eainfo']['overview']['eaover'] = 'TBD'
        metadata['metadata']['eainfo']['overview']['eadetcit'] = 'Unknown'

        # distinfo
        metadata['metadata']['distinfo']['stdorder']['digform']['digtopt']['onlinopt']['computer']['networka']['networkr'] = 'Specific Dataset Link'
        metadata['metadata']['distinfo']['stdorder']['fees'] = 'None'
        metadata['metadata']['distinfo']['stdorder']['digform']['digtinfo'] = {'formname': 'ASCII'}
        if distinfo == 'None':
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntperp']['cntper'] = 'ScienceBase'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntperp']['cntorg'] = 'U.S. Geological Survey - ScienceBase'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntaddr']['addrtype'] = 'mailing and physical'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntaddr']['address'] = 'Denver Federal Center, Building 810, Mail Stop 302'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntaddr']['city'] = 'Denver'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntaddr']['state'] = 'CO'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntaddr']['postal'] = '80225'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntaddr']['country'] = 'USA'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntvoice'] = '1-888-275-8747'
            metadata['metadata']['distinfo']['distrib']['cntinfo']['cntemail'] = 'sciencebase@usgs.gov'
        else:
            metadata['metadata']['distinfo']['distrib']['cntinfo'] = distinfo

        if disclaimer == 'default':
            metadata['metadata']['distinfo']['distliab'] = 'Unless otherwise stated, all data, metadata and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data on any other system or for general or scientific purposes, nor shall the act of distribution constitute any such warranty.'
        else:
            metadata['metadata']['distinfo']['distliab'] = disclaimer

        # metainfo
        metadata['metadata']['metainfo']['metstdn'] = 'FGDC Content Standard for Digital Geospatial Metadata'
        metadata['metadata']['metainfo']['metstdv'] = 'FGDC-STD-001-1998'
        metadata['metadata']['metainfo']['metd'] = 'TBD'
        if metainfo is 'default':
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntperp']['cntper'] = 'GHSC Data Steward'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntperp']['cntorg'] = 'U.S. Geological Survey, Geological Hazards Science Center'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntpos'] = 'Open Data Policy coordinator'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntaddr']['addrtype'] = 'mailing and physical'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntaddr']['address'] = '1711 Illinois Street'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntaddr']['city'] = 'Golden'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntaddr']['state'] = 'CO'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntaddr']['postal'] = '80401'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntaddr']['country'] = 'USA'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntvoice'] = '303-273-8500'
            metadata['metadata']['metainfo']['metc']['cntinfo']['cntemail'] = 'ghsc_metadata@usgs.gov'
        else:
            metadata['metadata']['metainfo']['metc']['cntinfo'] = metainfo

        # print OrderedDict to xml file
        xml = dicttoxml.dicttoxml(metadata)
        # Print xml to file
        dom = parseString(xml)
        filename = open('%s/metadata_%s_%i.xml' % (outpath, xl['Inventory'].loc[i], i), 'w')
        #flename.write(str(dom.toprettyxml()))
        filename.write(str(dom.toxml()))
        filename.close()

        #######################################################
        # If any entries have more than one item.
        #######################################################

        # deal with duplicate entries / split into new elements
        # reopen file
        tree = ET.parse('%s/metadata_%s_%i.xml' % (outpath, xl['Inventory'].loc[i], i))
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

        try:
            os.path.mkdir('%s/xml' % outpath)
        except:
            print('xml subdirectory already exists')

        # write changes to xml tree item
        tree.write('%s/xml/metadata_%s_%i.xml' % (outpath, xl['Inventory'].loc[i], i))

        # write changes to file
        dom1 = parse('%s/xml/metadata_%s_%i.xml' % (outpath, xl['Inventory'].loc[i], i))
        filename = open('%s/xml/metadata_%s_%i.xml' % (outpath, xl['Inventory'].loc[i], i), 'w')
        filename.write(str(dom1.toprettyxml()))
        filename.close()

        #######################################################
        # XML FILES HAVE BEEN WRITTEN. THE FOLLOWING IS ADDITIONAL.
        #######################################################

        ##########################################
        # THE FOLLOWING IS JUST FOR PRINTING CITATIONS TO FILE.
        ##########################################

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
            tempstring += 'accessed May 15, 2017, '  # REPLACE THIS WITH CURRENT DATE
            for r in q.iter('onlink'):
                tempstring += 'at ' + r.text
        tempstring += '.'
        string.append(str(tempstring))

    filename = open('%s/citations.doc' % outpath, 'w')
    for i in range(2, a):
        filename.write(str(xl['Inventory'].loc[i]))
        filename.write('\n\n %s \n\n' % string[i-2])
    filename.close()
    
