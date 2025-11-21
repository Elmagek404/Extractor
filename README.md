# Extractor

Extractor is a Python tool to automatically discover target URLs, forms, inputs, and Downloaded JavaScript files from websites. 

## Features
- Crawl links
- Extract forms and inputs
- Download JavaScript files
- Randomize user-agents
- Delay requests

## Usage
```bash
magic-extractor -l urls.txt -o results.txt --crawl --random-agents


magic-extractor -t https://TARGET-HERE.com  --crawl -f 

magic-extractor -h for more details
