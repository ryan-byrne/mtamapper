# MTAMapper

## Installation

### Using PIP
```console
pip install mtamapper
```
### From Source

Clone the repository
```console
git clone https://github.com/ryan-byrne/mta-map
```
Then install using ```setup.py```
```console
cd mta-map && python setup.py install
```

## Usage

```console

$ mta-map -h

usage: mta-map [-h] [-v] [-s] [-i [IP_ADDR]] [-p [PORT]] [--run-startup]

A Python Package for controlling an LED map of the MTA Subway system

optional arguments:
  -h, --help     show this help message and exit
  -v             Run in Verbose Mode
  -s             Run in Simulation Mode
  -i [IP_ADDR]   IP Address for OPC Server (Defaults to localhost)
  -p [PORT]      Port for the OPC Server (defaults to )
  --run-startup  Run a startup script that illuminates each light one by
                 one
```
