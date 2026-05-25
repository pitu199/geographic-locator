\# Geographic Locator



> \*\*Author:\*\* Assam's Hacker  

> \*\*Platform:\*\* Kali Linux / Windows / macOS



IP geolocation, WiFi positioning, and altitude/elevation tool for authorized pentesting.



\## Quick Install



```bash

git clone https://github.com/pitu199/geographic-locator.git

cd geographic-locator

pip install -r requirements.txt

python geographic\_locator.py -h
Command	Description
python geographic_locator.py -m	My IP geolocation
python geographic_locator.py -t 8.8.8.8	Target IP lookup
python geographic_locator.py -t example.com	Domain lookup
python geographic_locator.py -a 27.5 94.0	Altitude lookup
python geographic_locator.py -i	Interactive mode
python geographic_locator.py -m -g	Open in Google Maps
```cmd
notepad LICENSE
MIT License
Copyright (c) 2026 Assam's Hacker
Permission is hereby granted, free of charge...
notepad .gitignore
__pycache__/
*.pyc
.DS_Store
Thumbs.db
.env
venv/

