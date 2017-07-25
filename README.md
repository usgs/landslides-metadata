# EQIL_metadata

## Introduction

EQIL_metadata is a supplemental tool used to create metadata files, following the USGS geospatial metadata format, for a data series release of numerous ground failure inventories (Schmitt and others, 2017). The purpose of the code is to streamline and semi-automate the production of metadata for projects like this that require numerous individual metadata files. The code takes metadata information, compiled into a excel spreadsheet (xlsx), for a series of data sets and produces separate XML metadata files for each data set.  The code documentation can be found at: https://github.com/kbiegel-usgs/EQIL_metadata

The format for USGS geospatial metadata can be found here:  https://www.fgdc.gov/standards/projects/FGDC-standards-projects/metadata/base-metadata/v2_0698.pdf

This module compiles the background metadata provided from source documentation.  It does not incorporate any of the geographical or geospatial metadata which must be completed after this step. This can be done by running the [USGS metadata tool](https://geology.usgs.gov/tools/metadata/tools/doc/mp.html) or using the [Metadata Wizard in ESRI's ArcGIS](https://pubs.er.usgs.gov/publication/ofr20141132).

Disclaimer: This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.

## Installation and Dependencies

This module must be run using Python 3. It requires the Python standard library (xml, collections, datetime, and os) as well as the following packages:

* SciPy
* Pandas
* dicttoxml

These can be installed using the 'pip install' or 'conda install' commands.

## Usage Example

### Inputs

Running this code requires creating a csv file containing the background metadata that will be used to populate the xml files. An example of this setup can be seen in the attached Example_metadata.csv. This file has three rows of the titles which are required to run this script.  Row 1 contains the main metadata classifications, Row 2 contains the metadata item names, and Row 3 contains a general description of what the Row 2 metadata name is for the user.  Row 4 contains the values that should be placed in the xml files for each variable. All empty spaces create an item in the XML tree that reads 'TBD'.  The csv file should have the following categories:

|Row 1 Name|Row 2 Name|Row 3 Name|Description|
|---|---|---|---|
|Inventory| |Name|XML Item Name|
|Citation|origin|Authors|The name of the organization or individual that developed the data set. List separated by semicolons.|
| |pubdate|Date|The date when the data set was published or made public. YYYYMMDD|
| |title|Title|Title of the publication or data set.|
| |onlink|DOI|Name of the online computer resource that contains the data.  DOI or other link to the publication.|
|Description|abstract|Abstract|Brief narrative summary of the data set.|
| |purpose|Purpose|Summary of the intentions of developing the data set.|
| |supplinf|Original Citation|Other descriptive information.  In this case, the original citation of paper (data releases by the USGS require new citations).|
|Time|begdate|Begin Date|Begin date or event date|
| |enddate|End Date|End date of publication or research|
|Status|progress|Progress|The state of the data set whether complete or incomplete.|
| |update|Update|The frequency with which changes and additions are made to the data after initial completion.|
|Geographical Context|descgeog|Data Collected from:|Geographical location of data|
|Keywords|themekey|Theme|Common-use words or phrases used to describe the dataset.  List separated by semicolons.|
| |placekey|Place|Description of the geographic location covered by the data set.  List separated by semicolons.|
| |tempkey|Time|Description of the time period covered by the data set.  List separated by semicolons.|
|Contact|cntper|Contact Person|The individual associated with data set.|
| |cntorg|Organization|The contact organization associated with the data set.|
| |address|Address|The mailing address for the contact organization.|
| |city|City|The city for the contact organization.|
| |postal|Postal|The postal code for the contact organization.|
| |country|Country|The country of the contact organization.|
| |cntemail|Email|The email of the individual or organization specified as the point of contact.|
|source|source|source|Whether the origin is USGS (only put usgs for USGS datasets, otherwise leave blank).  This column is only used to distinguish disclaimer or liability statements.|

### Variables

The function requires at minimum two inputs, the input csv file and the output location. In addition, there are several other inputs that can be modified from their defaults, which are summarized on the Table below.

|Variable Name|Variable Tyep|Description of Item|Default|
|---|---|---|---|
|inputfile|String|Filename of the input file.| |
|outpath|String|Directory name for the output files.| |
|citeinfo|Dictionary|The information identifying a larger work in which the data set is included.|'None'|
|distinfo|Dictionary|Distributor contact information|'None'|
|dataqual|Dictionary|Contains data quality information|'None'|
|geoform|String|Mode in which data is presented|'Electronic'|
|pubplace|String|Geographic location of data published|'None'|
|publish|String|Name of data published|'None'|
|disclaimer|String|Custom disclaimed|'default'|
|metainfo|Dictionary|Containing metadata contact information|'default'|
|printcitations|Boolean|Whether to output a word document containing the full citations|False|

The dictionary variables must contain specific keys, an example form of the specified dictionary can be seen in the function description in the attached script.  Examples (which are the defaults) can also be seen below:

```python
# citeinfo example:
citeinfo = {'origin': 'Schmitt, R.; Tanyas, H.; Jessee, M.A.; Zhu, J.; Biegel, K.; Allstadt, K.E.; Jibson, R.W.; '
                      'Thompson, E.M.; van Westen, C.; Sato, H.P.; Wald, D.J.; Godt, J.W.; Gorum, T.; Moss, R.E.S.; '
                      'Xu, C.; Rathje, E.M., Knudsen, K.L.',
           'pubdate': '2017',
           'pubinfo': {'publish': 'U.S. Geological Survey data release collection', 'pubplace': 'Golden, CO'},
           'title': 'An Open Repository of Earthquake-triggered Ground Failure Inventories',
           'onlink': 'https://doi.org/10.5066/F7H70DB4'}
# distinfo example
distinfo = {'cntperp': {'cntper': 'ScienceBase', 'cntorg': 'U.S. Geological Survey - ScienceBase'},
            'cntaddr': {'addrtype': 'mailing and physical', 'address': 'Denver Federal Center, Building 810', 'city':
                        'Denver', 'state': 'CO', 'postal': '80225', 'country': 'USA'},
            'cntvoice': '1-888-275-8747',
            'cntemail': 'sciencebase@usgs.gov'}
# dataqual example
dataqual = {'attracc': {'attraccr': 'No formal attribute accuracy tests were conducted.'},
            'logic': 'No formal logical accuracy tests were conducted.''',
            'complete': 'Data set is considered complete for the information presented, as described in the abstract. '
                        'Users are advised to read the rest of the metadata record carefully for additional details.',
            'postacc': {'horizpa': {'horizpar': 'No formal positional accuracy tests were conducted.'}, 'vertacc':
                     {'vertaccr': 'No formal positional accuracy tests were conducted.'}},
            'lineage': {'procstep': {'procdesc': 'All dataset projection systems were converted to WGS84.',
                                   'procdate': 'General Processing Data when provided.'}}}
# metainfo example
metainfo = {'cntperp': {'cntper': 'GHSC Data Steward', 'cntorg': 'U.S. Geological Survey, '
                        'Geologic Hazards Science Center'},
          'cntpos': 'Open Data Policy Coordinator',
          'cntaddr': {'addrtype': 'mailing and physical', 'address': '1711 Illinois St.', 'city': 'Golden',
                      'state': 'CO', 'postal': '80401', 'country': 'USA'},
          'cntvoice': '303-273-8500',
          'cntemail': 'ghsc_metadata@usgs.gov'}
```

Additionally, the disclaimer can be modified, below is the default disclaimer:
```
disclaimer = 'Unless otherwise stated, all data, metadata and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data on any other system or for general or scientific purposes, nor shall the act of distribution constitute any such warranty.'
```     
### Running the code

To run the code, use a python environment such as ipython terminal.  First import the script, for it to load, you must either be in the folder it's located in, or add it to your PYTHONPATH:
```python
import readMetadata as rm
```
 
To run the function that creates the xml files, you must specify the inputfile and outpath.  All other variables have a default and are therefore optional.  To run the function:
```python
# Create xml files with all defaults
rm.readmetadata(inputfile='Example_metadata.csv', outpath='.')

# Create xml files with changes to defaults
rm.readmetadata(inputfile='Example_metadata.csv', outpath='.', printcitations=True, citeinfo=citeinfo,
                distinfo=distinfo, dataqual=dataqual, geoform='Electronic', pubplace='Earth',
                publish='Yes please', disclaimer='Words', metainfo=metainfo)
```

### Output

An example output of the XML file can be seen in the attached Example_output.xml file.  This metadata file does not include geographic or geospatial information so additional processing is required as described in the introduction.

## References

Schmitt, R., Tanyas, H., Jessee, M.A., Zhu, J., Biegel, K.M., Allstadt, K.E., Jibson, R.W., Thompson, E.M., van Westen, C.J., Sato, H.P., Wald, D.J., Godt, J.W., Gorum, T., Xu, C., Rathje, E.M., Knudsen, K.L., 2017, An Open Repository of Earthquake-triggered Ground Failure Inventories, U.S. Geological Survey data release collection, accessed 21 July 2017, at https://doi.org/10.5066/F7H70DB4.
