SHELL=/bin/bash

../../@input-data/DeriNetFA-UfalFormat.tsv:
	@echo "$$(tput setaf 1)You need DeriNetFA-UfalFormat.tsv. Contact the authors."

get-data-v05: ../../@input-data/DeriNetFA-UfalFormat.tsv
	mkdir original-data/
	../../py3env/bin/python3 0.5/reformat_data.py ../../@input-data/DeriNetFA-UfalFormat.tsv > original-data/derinet-fa-V1.tsv


UDer-0.5-fa-DeriNetFA.tsv: get-data-v05
	# 1. get-data-v05
	# 2. harmonise
	../../py3env/bin/python3 ../../derinet2/process_scenario.py \
		Load -f DERINET_V1 original-data/derinet-fa-V1.tsv \
		Save UDer-0.5-fa-DeriNetFA.tsv

UDer-1.0-fa-DeriNetFA.tsv: UDer-0.5-fa-DeriNetFA.tsv
	cp UDer-0.5-fa-DeriNetFA.tsv UDer-1.0-fa-DeriNetFA.tsv

UDer-1.1-fa-DeriNetFA.tsv: UDer-1.0-fa-DeriNetFA.tsv
	cp UDer-1.0-fa-DeriNetFA.tsv UDer-1.1-fa-DeriNetFA.tsv


clean:
	rm -rf original-data/ UDer-0.5-fa-DeriNetFA.tsv
	rm -rf UDer-1.0-fa-DeriNetFA.tsv UDer-1.1-fa-DeriNetFA.tsv
