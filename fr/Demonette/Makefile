SHELL=/bin/bash

get-data-v05:
	mkdir -p original-data/
	# 1. download data
	wget -O ../../@input-data/demonette-1.2.zip http://redac.univ-tlse2.fr/lexiques/demonette/demonette-1.2.zip
	unzip ../../@input-data/demonette-1.2.zip -d original-data/
	# 2. preproces data
	../../py3env/bin/python3 0.5/extract_relations.py original-data/demonette-1.2.xml > 0.5/relations.tsv


UDer-0.5-fr-Demonette.tsv: get-data-v05
	# 1. get-data-v05
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonise
	../../py3env/bin/python3 0.5/spanning_trees.py -r 0.5/relations.tsv -w 0.5/01-harm-annotated/all-annotations.tsv -o 0.5/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 0.5/harmonizedemonette.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDemonette 0.5/harmonized.pickle \
		Save UDer-0.5-fr-Demonette.tsv

UDer-1.0-fr-Demonette.tsv: UDer-0.5-fr-Demonette.tsv
	cp UDer-0.5-fr-Demonette.tsv UDer-1.0-fr-Demonette.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-fr-Demonette.tsv > UDer-1.0-fr-Demonette-v2.tsv
	mv UDer-1.0-fr-Demonette-v2.tsv UDer-1.0-fr-Demonette.tsv

UDer-1.1-fr-Demonette.tsv: get-data-v05
	# 1. get-data-v05
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/01-harm-annotated/annotation-data-1.json -o 0.5/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonise
	../../py3env/bin/python3 1.1/spanning_trees.py -r 0.5/relations.tsv -w 0.5/01-harm-annotated/all-annotations.tsv -o 1.1/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.1/harmonizedemonette.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeDemonette 1.1/harmonized.pickle \
		Save UDer-1.1-fr-Demonette.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.1-fr-Demonette.tsv > UDer-1.1-fr-Demonette-v2.tsv
	mv UDer-1.1-fr-Demonette-v2.tsv UDer-1.1-fr-Demonette.tsv


01-harm-annotation: get-data-v05
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 0.5/relations.tsv -o 0.5/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 0.5/relations.tsv 0.5/01-harm-annotated/all-annotations.tsv 0.5/harmonized.pickle UDer-0.5-fr-Demonette.tsv
	rm -rf UDer-1.0-fr-Demonette-v2.tsv UDer-1.0-fr-Demonette.tsv
	rm -rf 1.1/harmonized.pickle UDer-1.1-fr-Demonette-v2.tsv UDer-1.1-fr-Demonette.tsv
