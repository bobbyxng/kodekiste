**GDP_per_capita_PPP_1990_2015_v2.nc**
- Gross Domestic Product per capita (PPP) from years 1999 to 2015
- Rectangular cutout for non-NUTS3 countries in PyPSA-Eur, i.e. MD and UA, including a 10 km buffer
- Kummu et al. "Data from: Gridded global datasets for Gross Domestic Product and Human Development Index over 1990-2015" 
- **Source:** https://doi.org/10.1038/sdata.2018.4 and associated dataset https://doi.org/10.1038/sdata.2018.4
- **Extract from usage notes:**
    > **Administrative units:**
Represents the administrative units used for GDP per capita (PPP) and HDI data products. National administrative units have id 1-999, sub-national ones 1001-
admin_areas_GDP_HDI.nc

    >**GDP_per_capita_PPP_1990_2015:**
The GDP per capita (PPP) dataset represents average gross domestic production per capita in a given administrative area unit. GDP is given in 2011 international US dollars. Gap-filled sub-national data were used, supplemented by national data where necessary. Datagaps were filled by using national temporal pattern. Dataset has global extent at 5 arc-min resolution for the 26-year period of 1990-2015. Detail description is given in a linked article and metadata is provided as an attribute in the NetCDF file itself.

**ppp_2013_1km_Aggregated.tif**

- The spatial distribution of population in 2020: Estimated total number of people per grid-cell. The dataset is available to download in Geotiff format at a resolution of 30 arc (approximately 1km at the equator). The projection is Geographic Coordinate System, WGS84. The units are number of people per pixel. The mapping approach is Random Forest-based dasymetric redistribution. 
- Rectangular cutout for non-NUTS3 countries in PyPSA-Eur, i.e. MD and UA, including a 10 km buffer
- WorldPop (www.worldpop.org - School of Geography and Environmental Science, University of Southampton; Department of Geography and Geosciences, University of Louisville; Departement de Geographie, Universite de Namur) and Center for International Earth Science Information Network (CIESIN), Columbia University (2018). Global High Resolution Population Denominators Project - Funded by The Bill and Melinda Gates Foundation (OPP1134076). https://dx.doi.org/10.5258/SOTON/WP00647 
- **Source**: https://data.humdata.org/dataset/worldpop-population-counts-for-world and https://hub.worldpop.org/geodata/summary?id=24777
- **Extract from Terms of Use:**
    >  WorldPop datasets are available under the Creative Commons Attribution 4.0 International License. This means that you are free to share (copy and redistribute the material in any medium or format) and adapt (remix, transform, and build upon the material) for any purpose, even commercially, provided attribution is included (appropriate credit and a link to the licence).      