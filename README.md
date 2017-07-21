# EQIL_metadata

## Introduction

GF_metadata is a supplemental tool used to create metadata files, following the USGS geospatial metadata format, for a data series release.  The code takes metadata information, compiled into a CSV document, for a series of data sets and produces separate XML metadata files for each data set.  The code documentation can be found at: https://github.com/kbiegel-usgs/EQIL_metadata

The format for USGS geospatial metadata can be found here:  https://www.fgdc.gov/standards/projects/FGDC-standards-projects/metadata/base-metadata/v2_0698.pdf

This script compiles the background metadata provided from source documentation.  It does not incorporate any of the geographical or geospatial metadata which can be completed by running the USGS metadata tool:  https://geology.usgs.gov/tools/metadata/tools/doc/mp.html

Disclaimer: This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.

## Installation and Dependencies

This script requires packages that are available through the scipy installation.  All packages required to run the script can be seen below:

    #stdlib imports
    from collections import OrderedDict
    import pandas as pd
    import dicttoxml
    from xml.dom.minidom import parseString, parse
    import xml.etree.ElementTree as ET
    import os

Any packages that need to be installed can be installed via the 'pip install' or 'conda install' commands.

## Usage Example

Running this code requires a CSV file filled with the background metadata.  This file has three rows of the titles which are required to run this script.  Row 1 has the main metadata classifications, Row 2 has the metadata item names, and Row 3 has a general description for the user.  All empty spaces create an item in the XML tree that reads 'TBD'.  The CSV file should have the following categories:

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


An example of this setup can be seen in the figure below.

![img1](Sample_Spreedsheet_Image.png)


To run the script, the user will have to make several changes to the script.  At a minimum, lines 15 and 18 need to be changed to point to the correct file locations in the users computer. Line 15 should point to the CSV file being used.  Line 18 points to the output directory for results.  

Additionally, there are a series of hardcoded variables that need to be changed dependent on commonalities among the data sets being used.  These are default to the original publication for which this script was created.  All changes that can or should be made to the code can be seen in the table below:

|Line number|Description of item|Default|
|---|---|---|
|15|Filename of the input CSV file.| |
|18|Directory name for the output files.| |
|46|The mode in which the geospatial data is presented.|'Electronic'|
|47|The name of the city (or more general location) where the data set was published.|'None'|
|48|The name of the individual or organization that published the data.|'None'|
|49|The information identifying a larger work in which the data set is included.| |
|96|Reference to a thesaurus or similar source of keywords. For theme keys.|'USGS Thesaurus'|
|97|Reference to a thesaurus or similar source of keywords. For temporal keys.|'USGS Thesaurus'|
|98|Reference to a thesaurus or similar source of keywords. For place keys.|'USGS Thesaurus'|
|117|The state of the contact organization. To specify this for each data set, it needs to be added to the end of the CSV file and the code needs to be adapted.|'None'|
|118|The voicemail or telephone number for the contact organization or individual.  To specify this for each data set, it needs to be added to the end of the CSV file and the code needs to be adapted.|'None'|
|123-129|Data quality attributes.  These lines should be updated according to accuracy tests and processing steps that were applied to the entire database.|Many defaults.|
|136-146|Distributor contact information.|Sciencebase|
|147-150|Liability statements.  Dependent on the source of data.|USGS and non-USGS version.|
|153-166|Metadata contact information.|GHSC Data Steward|
