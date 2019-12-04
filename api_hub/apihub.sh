!#/bin/bash

USER="{username}"
PSWD="{password}"


# cercar totes els productes de l'arxiu Data Hub, i desa els primers 25 resultats en un arxiu
#wget --no-check-certificate --user="$USER" --password="$PSWD" --output-document=query_results.txt "https://scihub.copernicus.eu/dhus/search?q=*&rows=25"

# cercar productes SLC en base a una data
#wget --no-check-certificate --user="$USER" --password="$PSWD" --output-document=query_results.txt "https://scihub.copernicus.eu/dhus/search?q=ingestiondate:[NOW-1DAY TO NOW] AND producttype:SLC&rows=100&start=0&format=json"

# descarregar productes coneixent el seu identificador únic {UUID}
#wget --content-disposition --continue --user="$USER" --password="$PSWD" "https://scihub.copernicus.eu/dhus/odata/v1/Products('22e7af63-07ad-4076-8541-f6655388dc5e')/\$value"

# usar l'script dhusget.sh per a cercar i descarregar imatges
./dhusget.sh -u $USER -p $PSWD -m Sentinel-3 -i SLSTR -t 12 -c 2.99,2.56:42.23,41.94 -T SL_2_LST___ -o product -O /home/josep/SIGTE/PROJECTES/Compartim_copernicus
