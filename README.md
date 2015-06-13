# OTprotocol Python

Python library for generating [Autoprotocol](http://www.autoprotocol.org) for the [OpenTrons](http://www.opentrons.com) OT.one.

Based off of [Autoprotocol-python](http://github.com/autoprotocol/autoprotocol-python) library.


## Installation and Demo

	$ git clone https://github.com/peteryin21/otprotocol
	$ cd otprotocol
	$ sudo python setup.py install
	$ python demo_ot.py

## Usage
```python
import json
from otprotocol.protocol import Protocol, Head

#instantiate new Protocol object
p = Protocol()

#create head object
p200 = Head( "p200", #name
  {#opts
  "tool" : "pipette", 
  "tip-racks" : [{"container":"p200-rack"}],
  "trash-container" : {"container":"trash"},
  "multi-channel" : True,
  "axis" : "a",
  "volume" : 250,
  "down-plunger-speed" : 300,
  "up-plunger-speed" : 500,
  "tip-plunge" : 8,
  "extra-pull-volume" : 20,
  "extra-pull-delay" : 200,
  "distribute-percentage" : 0.1,
  "points" : [{"f1": 10,"f2": 6},{"f1": 25,"f2": 23},{"f1": 50,"f2": 49},{"f1": 200,"f2": 200}]
    }
  )

#append decks to Protocol object
p200_rack = p.deck("p200-rack", labware="tiprack-200ul")
trough = p.deck("trough", labware="trough-12row")
plate_1 = p.deck("plate-1", labware="96-flat")
plate_2 = p.deck("plate-2", labware="96-flat")
trash = p.deck("trash", labware="point")

#add ingredients
p.add_ingredient("ReagentA", "Reagents-1", "A3", 25000)

#add head object to protocol
p.set_head(p200)

#append instructions 
p.transfer("trough","A1","plate-1","A1",100)
p.transfer("trough", ["A1","A2"],"plate-1", ["B1","B2"],[100,20])
p.distribute("trough","A1","plate-1",["A1","A2","A3"],[20, 30, 100])
p.consolidate("plate-1",["A1","A2","A3"],"plate-2","A1",[20, 30, 100])
p.mix("plate-2", "A1", 20)

print json.dumps(p.as_dict(), indent=2)
```

This produces the following JSON:

```
{
  "head": {
    "p200": {
      "extra-pull-delay": 200, 
      "tool": "pipette", 
      "up-plunger-speed": 500, 
      "multi-channel": true, 
      "volume": 250, 
      "trash-container": {
        "container": "trash"
      }, 
      "distribute-percentage": 0.1, 
      "axis": "a", 
      "extra-pull-volume": 20, 
      "tip-plunge": 8, 
      "tip-racks": [
        {
          "container": "p200-rack"
        }
      ], 
      "points": [
        {
          "f1": 10, 
          "f2": 6
        }, 
        {
          "f1": 25, 
          "f2": 23
        }, 
        {
          "f1": 50, 
          "f2": 49
        }, 
        {
          "f1": 200, 
          "f2": 200
        }
      ], 
      "down-plunger-speed": 300
    }
  }, 
  "deck": {
    "trash": {
      "labware": "point"
    }, 
    "p200-rack": {
      "labware": "tiprack-200ul"
    }, 
    "trough": {
      "labware": "trough-12row"
    }, 
    "plate-2": {
      "labware": "96-flat"
    }, 
    "plate-1": {
      "labware": "96-flat"
    }
  }, 
  "ingredients": {
    "ReagentA": [
      {
        "container": "Reagents-1", 
        "location": "A3", 
        "volume": 25000
      }
    ]
  }, 
  "instructions": [
    {
      "tool": "p200", 
      "groups": [
        {
          "transfer": [
            {
              "from": {
                "delay": 2000, 
                "touch-tip": true, 
                "tip-offset": -2, 
                "container": "trough", 
                "location": "A1"
              }, 
              "to": {
                "touch-tip": true, 
                "container": "plate-1", 
                "location": "A1"
              }, 
              "volume": 100, 
              "blowout": true, 
              "extra-pull": true
            }
          ]
        }, 
        {
          "transfer": [
            {
              "from": {
                "delay": 2000, 
                "touch-tip": true, 
                "tip-offset": -2, 
                "container": "trough", 
                "location": "A1"
              }, 
              "to": {
                "touch-tip": true, 
                "container": "plate-1", 
                "location": "B1"
              }, 
              "volume": 100, 
              "blowout": true, 
              "extra-pull": true
            }, 
            {
              "from": {
                "delay": 2000, 
                "touch-tip": true, 
                "tip-offset": -2, 
                "container": "trough", 
                "location": "A2"
              }, 
              "to": {
                "touch-tip": true, 
                "container": "plate-1", 
                "location": "B2"
              }, 
              "volume": 20, 
              "blowout": true, 
              "extra-pull": true
            }
          ]
        }, 
        {
          "distribute": {
            "from": {
              "container": "trough", 
              "location": "A1"
            }, 
            "to": [
              {
                "container": "plate-1", 
                "location": "A1", 
                "volume": 20, 
                "touch-tip": true
              }, 
              {
                "container": "plate-1", 
                "location": "A2", 
                "volume": 30, 
                "touch-tip": true
              }, 
              {
                "container": "plate-1", 
                "location": "A3", 
                "volume": 100, 
                "touch-tip": true
              }
            ], 
            "blowout": true
          }
        }, 
        {
          "consolidate": {
            "from": [
              [
                {
                  "container": "plate-1", 
                  "location": "A1", 
                  "volume": 20, 
                  "touch-tip": true
                }, 
                {
                  "container": "plate-1", 
                  "location": "A2", 
                  "volume": 30, 
                  "touch-tip": true
                }, 
                {
                  "container": "plate-1", 
                  "location": "A3", 
                  "volume": 100, 
                  "touch-tip": true
                }
              ]
            ], 
            "to": {
              "container": "plate-2", 
              "location": "A1"
            }, 
            "blowout": true
          }
        }, 
        {
          "mix": [
            {
              "container": "plate-2", 
              "location": "A1", 
              "volume": 20, 
              "repetitions": 5, 
              "blowout": true, 
              "liquid-tracking": true
            }
          ]
        }
      ]
    }
  ]
}

```