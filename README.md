## GF_metadata

# Introduction

GF_metadata is a supplemental tool used to create separate metadata files, following the USGS geospatial metadata format, for a series of datasets.  The code documentation can be found at: 

# Installation and Dependencies

This script mostly requires packages that are available through the scipy installation.

# Usage Example

Running this code requires a CSV file specified exactly so in order to be read into the code exactly as needed.  This file is organized based off of three rows of the titles.  Row 1 has the main metadata classifications, Row 2 has the metadata item names, and Row 3 has a general description for the user.  The CSV file should have the following categories:

|Row 1 Name|Row 2 Name|Row 3 Name|
|---|---|---|
|Inventory| |Name|
|Citation|origin|Authors|
| |pubdate|Date|
| |title|Title|
| |onlink|DOI|
|Description|abstract|Abstract|
| |purpose|Purpose|
| |supplinf|Original Citation|
|Time|begdate|Begin Date|
| |enddate|End Date|
|Status|progress|Progress|
| |update|Update|
|Geographical Context|descgeog|Data Collected from:|
|Keywords|themekey|Theme|
| |placekey|Place|
| |tempkey|Time|
|Contact|cntper|Contact Person|
| |cntorg|Organization|
| |address|Address|
| |city|City|
| |postal|Postal|
| |country|Country|
| |cntemail|Email|
|source|source|source|


An example of this setup can be seen in the figure below.

![img1](Sample_Spreedsheet_Image.png)


To run the script, change lines 15 and 18. Line 15 should point to the CSV file being used.  Line 18 points to the output directory for results.
