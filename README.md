Objet : obtenir un CSV de toutes les pages de formations de Comundi

Données à scraper :
- url
- name: titre de la formation
- sku: référence unique de la formation
- objectives: objectifs de la formation, contenu HTML, si présent
- parsed_duration: durée de la formation
- parsed_price: tarif de base HT de la formation

Il faut stocker une version brute de ces champs et en plus retraiter les champs suivants:
- processed_duration: durée au format numérique en heures de la formation, à savoir que par convention 1 jour = 7 heures
- processed_price: prix au format numérique (sans unité de monnaie ou autre texte)

#Prereqs : 

Install Python 3.6.1

apt-get install python

apt-get install python-pip

pip install Scrapy

pip install pandas


#Running the Crawler: :

git clone https://github.com/aymen-mansour/comundiscraping.git

cd comundiscraping

sh run.sh

----------------------------------------------------------------

# run.sh is:

1.crawling script

2.preprocessing data script
