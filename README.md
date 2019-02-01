Introduction
=========================================
Download BCL (binary base call) files from Illumina's BaseSpace Sequence Hub using [BaseSpacePy](https://github.com/basespace/basespace-python-sdk).

Requirements
=========================================
1. Install [BaseSpacePy](https://github.com/basespace/basespace-python-sdk) (version 0.3 tested, require Python 2).
1. Get client key, client secret and access token ([click here](https://help.basespace.illumina.com/articles/tutorials/using-the-python-run-downloader/) to get instructions).

Example
=========================================
The following example command will download files associated with sequencing run `180803_A00000_0000_XXXXXXXXXX` to `download` directory starting from offset `9620` and `4` files will be downloaded.

	pybs_bcl.py \
	    --key client_key \
	    --secret client_secret \
	    --token access_token \
	    --run 180803_A00000_0000_XXXXXXXXXX \
	    --directory download \
	    --num_items 4 \
	    --offset 9620
