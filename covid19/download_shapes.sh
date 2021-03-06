#!/bin/bash

# This script is for mass downloading Brazilian States shapefiles, subdivided by municipality, from the Brazilian Institute of Geography and Statistics

for i in $(cat estados)
do

	lower_estado=$(echo $i |awk '{print tolower($0)}')
	wget ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2015/UFs/${i}/${lower_estado}"_municipios.zip"
done
