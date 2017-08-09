# EQIL_metadata

## Introduction

EQIL_metadata is a supplemental tool used to create metadata files, following the USGS geospatial metadata format, for a data series release of numerous ground failure inventories (Schmitt and others, 2017). The purpose of the code is to streamline and semi-automate the production of metadata for projects like this that require numerous individual metadata files. The code takes metadata information, compiled into a csv file, for a series of data sets and produces separate XML metadata files for each data set.  The code documentation can be found at: https://github.com/kbiegel-usgs/EQIL_metadata

The format for USGS geospatial metadata can be found here:  https://www.fgdc.gov/standards/projects/FGDC-standards-projects/metadata/base-metadata/v2_0698.pdf

This module compiles the background metadata provided from source documentation.  It does not incorporate any of the geographical or geospatial metadata which must be completed after this step. This can be done by running the [USGS metadata tool](https://geology.usgs.gov/tools/metadata/tools/doc/mp.html) or using the [Metadata Wizard in ESRI's ArcGIS](https://pubs.er.usgs.gov/publication/ofr20141132).

## Installation and Dependencies

To install this package:
```python
pip install git+git://github.com/kbiegel-usgs/EQIL_metadata.git
```

To upgrade:
```python
pip install -U git+git://github.com/kbiegel-usgs/EQIL_metadata.git
```

This module must be run using Python 3. It requires the Python standard library (xml, collections, configobj, datetime, and os) as well as the following packages:

* SciPy (version number 0.17.1)
* Pandas (version number 0.20.2)
* dicttoxml (version number 1.7.4)

These can be installed using the 'pip install' or 'conda install' commands.

To install the entire environment at once you can use the setup script
```python
setup_env.sh
```
which is included in the repository.  Run this using the following command:
```python
bash setup_env.sh
```

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

### Config file

One of the variable required to run the code is the config file.  The full filename should be specified when designating this variable.
```python
configfilepath = '/Users/user/Documents/EQIL/Example_config.ini'
```

The attached example config file (Example_config.ini) has all the necessary variables as well as example or default items.  This file must be changed by the user to reflect desired information.

### Running the code

To run the code, use a python environment such as ipython terminal.  First import the script, for it to load, you must either be in the folder it's located in, or add it to your PYTHONPATH:
```python
import readMetadata as rm
```
Next designate the filepath locations for the input file (Example_metadata.csv) and the output directory location.  The configfilepath location was designated above.
```python
inputfile = '/Users/user/Documents/EQIL/Example_metadata.csv'
outpath = '/Users/user/Documents/EQIL/Outputs/'
```

After specifying the file locations of the three variables, run the function as shown:
```python
# Create xml files
rm.readmetadata(configfilepath, inputfile, outpath)
```

### Output

An example output of the XML file can be seen in the attached Example_output.xml file.  This metadata file does not include geographic or geospatial information so additional processing is required as described in the introduction.

## References

Schmitt, R., Tanyas, H., Jessee, M.A., Zhu, J., Biegel, K.M., Allstadt, K.E., Jibson, R.W., Thompson, E.M., van Westen, C.J., Sato, H.P., Wald, D.J., Godt, J.W., Gorum, T., Xu, C., Rathje, E.M., Knudsen, K.L., 2017, An Open Repository of Earthquake-triggered Ground Failure Inventories, U.S. Geological Survey data release collection, accessed 21 July 2017, at https://doi.org/10.5066/F7H70DB4.
