SHELL=/bin/bash

../../@input-data/etymwn-20130208.zip:
	wget --no-check-certificate -O ../../@input-data/etymwn-20130208.zip https://cs.rutgers.edu/~gd343/downloads/etymwn-20130208.zip

get-data-v10: ../../@input-data/etymwn-20130208.zip
	mkdir -p original-data/
	# 1. download data
	unzip ../../@input-data/etymwn-20130208.zip -d original-data/
	# 2. preproces data
	cat original-data/etymwn.tsv | grep -e 'cat:.*cat:' | grep -e 'rel:is_derived_from' | sed -e 's/cat: //g' -e 's/\trel:is_derived_from//g' | awk -F "\t" '{ print $$2 "\t" $$1}' > 1.0/relations.tsv
	cat original-data/etymwn.tsv | grep -e 'cat:.*cat:' | grep -e 'rel:has_derived_form' | sed -e 's/cat: //g' -e 's/\trel:has_derived_form//g' | awk -F "\t" '{ print $$1 "\t" $$2}' >> 1.0/relations.tsv
	cat 1.0/relations.tsv | grep -ve '[[:punct:]]' -ve ' ' -ve '[0-9]' | sort | uniq > 1.0/relations-copy.tsv
	mv 1.0/relations-copy.tsv 1.0/relations.tsv


UDer-1.0-ca-EtymWordNetCA.tsv: get-data-v10
	# 1. get-data-v10
	# 2. proces annotations
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/01-harm-annotated/annotation-data-1.json -o 1.0/01-harm-annotated/all-annotations.tsv -j2c
	# 3. harmonise
	../../py3env/bin/python3 1.0/spanning_trees.py -r 1.0/relations.tsv -w 1.0/01-harm-annotated/all-annotations.tsv -o 1.0/harmonized.pickle
	mkdir -p ../../derinet2/derinet/modules/uder
	cp 1.0/harmonizeetymwordnetca.py ../../derinet2/derinet/modules/uder/
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		uder.HarmonizeEtymWordNetCA 1.0/harmonized.pickle \
		Save UDer-1.0-ca-EtymWordNetCA.tsv
	../../py3env/bin/python3 1.0/edit-json-column.py UDer-1.0-ca-EtymWordNetCA.tsv > UDer-1.0-ca-EtymWordNetCA-v2.tsv
	mv UDer-1.0-ca-EtymWordNetCA-v2.tsv UDer-1.0-ca-EtymWordNetCA.tsv

UDer-1.1-ca-EtymWordNetCA.tsv: UDer-1.0-ca-EtymWordNetCA.tsv
	cp UDer-1.0-ca-EtymWordNetCA.tsv UDer-1.1-ca-EtymWordNetCA.tsv


01-harm-annotation: get-data-v10
	../../py3env/bin/python3 ../../@shared-scripts/annot_data.py -i 1.0/relations.tsv -o 1.0/01-harm-annotated/annotation-data.json -j


clean:
	rm -rf original-data/ 1.0/relations.tsv 1.0/01-harm-annotated/all-annotations.tsv 1.0/harmonized.pickle UDer-1.0-ca-EtymWordNetCA.tsv
	rm -rf UDer-1.1-ca-EtymWordNetCA.tsv
