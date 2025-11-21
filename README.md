## magic-extractor

Magic Extractor is a Python tool used to automatically discover URLs, forms, inputs, and JavaScript files from target websites — useful for reconnaissance, bug bounty hunting, and web security testing.

## Features
- Crawl links
- Extract forms and input fields
- Download JavaScript files
- Randomize user-agents
- Delay requests
- save the output


## installation
git clone https://github.com/Elmagek404/magic-extractor
cd magic-extractor
pip install -e .
magic-extractor -h
 

## Usage 
magic-extractor -h
extract inputs - forms 
magic-extractor -u https://example.com 
magic-extractor -l urls.txt -f -crawl --radnom-agent -o result
