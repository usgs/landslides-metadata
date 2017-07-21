# EQIL_metadata

## Introduction

GF_metadata is a supplemental tool used to create separate metadata files, following the USGS geospatial metadata format, for a series of datasets.  The code documentation can be found at: 

The format for USGS geospatial metadata can be found here: https://www.fgdc.gov/standards/projects/FGDC-standards-projects/metadata/base-metadata/v2_0698.pdf

Disclaimer: This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.

## Installation and Dependencies

This script requires packages that are available through the scipy installation.

    #stdlib imports
    from collections import OrderedDict
    import pandas as pd
    import dicttoxml
    from xml.dom.minidom import parseString, parse
    import xml.etree.ElementTree as ET
    import os


## Usage Example

Running this code requires a CSV file specified exactly so in order to be read into the code exactly as needed.  This file is organized based off of three rows of the titles.  Row 1 has the main metadata classifications, Row 2 has the metadata item names, and Row 3 has a general description for the user.  The CSV file should have the following categories:

|Row 1 Name|Row 2 Name|Row 3 Name|Description|
|---|---|---|---|
|Inventory| |Name|XML Item Name|
|Citation|origin|Authors|A list of authors divided by semicolons|
| |pubdate|Date|Date of publication of the data|
| |title|Title|Title of the publication|
| |onlink|DOI|DOI or other online link to the publication|
|Description|abstract|Abstract|Abstract either of original paper or of data release|
| |purpose|Purpose|Purpose pulled from paper or descibed by original author|
| |supplinf|Original Citation|Original citation of paper (data releases by the USGS require new citations)|
|Time|begdate|Begin Date|Begin date of research or event date|
| |enddate|End Date|End date of publication|
|Status|progress|Progress|Whether dataset is complete or not|
| |update|Update|How dataset will be updated if needed|
|Geographical Context|descgeog|Data Collected from:|Geographical location of data|
|Keywords|themekey|Theme|Theme keys for the dataset pulled from the USGS Thesaurus|
| |placekey|Place|Place keys for the dataset pulled from the USGS Thesaurus|
| |tempkey|Time|Temporal keys for the dataset pulled from the USGS Thesaurus|
|Contact|cntper|Contact Person|Person listed as the contact author for the dataset|
| |cntorg|Organization|Contact organization for the dataset|
| |address|Address|Mailing address for the contact organization|
| |city|City|City for the contact organization|
| |postal|Postal|Postal code for the contact organization|
| |country|Country|Country of the contact organization|
| |cntemail|Email|Email of the contact author or organization|
|source|source|source|Whether the origin is USGS (only put usgs for USGS datasets, otherwise leave blank)|


An example of this setup can be seen in the figure below.

![img1](Sample_Spreedsheet_Image.png)


To run the script, change lines 15 and 18. Line 15 should point to the CSV file being used.  Line 18 points to the output directory for results.
