A skeleton for creating a Google Refine 2.0 reconciliation service.

This repository is intended to be a basic template for a Google Refine reconciliation service.  It is expected that you would modify the included code for your own purposes.

Requirements:
1. Python

Instructions:

1. Download the files in this repository to a directory on your computer. e.g. 'git clone git://github.com/mblwhoi/reconciliation_service_skeleton.git recon_skeleton'

2. Download and unzip the Pleiades name data: 'wget http://atlantides.org/downloads/pleiades/dumps/pleiades-names-latest.csv.gz && gunzip pleiades-names-latest.csv.gz'

3. Run 'pleiades_service.py' e.g. 'python example_composers_reconciliation_service.py'.  This will start a reconciliation service on port 5000 which you can use with Google Refine.
