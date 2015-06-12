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

#append deck elements to Protocol object
p200_rack = p.deck("p200_rack", labware="tiprack-200ul")
trough = p.deck("trough", labware="trough-12row")
plate_1 = p.deck("plate_1", labware="96-flat")
plate_2 = p.deck("plate_2", labware="96-flat")
trash = p.deck("trash", labware="point")

#create head object
p200 = Head( "p200", #name
	{#opts
	"tool" : "pipette", 
	"tip_racks" : [{"container":"p200_rack"}],
	"trash_container" : {"container":"trash"},
	"multi_channel" : True,
	"axis" : "a",
	"volume" : 250,
	"down_plunger_speed" : 300,
	"up_plunger_speed" : 500,
	"tip_plunge" : 8,
	"extra_pull_volume" : 20,
	"extra_pull_delay" : 200,
	"distribute_percentage" : 0.1,
	"points" : [{"f1": 10,"f2": 6},{"f1": 25,"f2": 23},{"f1": 50,"f2": 49},{"f1": 200,"f2": 200}]
		}
	)

#add head object to protocol
p.set_head(p200)

#append instructions 
p.transfer("trough","A1","plate_1","A1", 100)
#multiple transfers in same group
p.transfer("trough", ["A1","A2"],"plate_1", ["B1","B2"],[100,20])
p.distribute("trough","A1","plate_1",["A1","A2","A3"],[20, 30, 100])
p.consolidate("plate_1",["A1","A2","A3"],"plate_2","A1",[20, 30, 100])
p.mix("plate_2", "A1", 20)

print json.dumps(p.as_dict(), indent=2)
```

This produces the following JSON:

```
{
  "head": {
    "p200": {
      "up_plunger_speed": 500, 
      "tool": "pipette", 
      "multi_channel": true, 
      "volume": 250, 
      "trash_container": {
        "container": "trash"
      }, 
      "down_plunger_speed": 300, 
      "axis": "a", 
      "tip_plunge": 8, 
      "extra_pull_volume": 20, 
      "tip_racks": [
        {
          "container": "p200_rack"
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
      "distribute_percentage": 0.1, 
      "extra_pull_delay": 200
    }
  }, 
  "instructions": [
    {
      "tool": "p200", 
      "groups": [
        {
          "transfer": [
            {
              "volume": 100, 
              "to": {
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "A1"
              }, 
              "extra-pull": true, 
              "from": {
                "delay": 2000, 
                "touch-tip": true, 
                "tip-offset": -2, 
                "container": "trough", 
                "location": "A1"
              }, 
              "blowout": true
            }
          ]
        }, 
        {
          "transfer": [
            {
              "volume": 100, 
              "to": {
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "B1"
              }, 
              "extra-pull": true, 
              "from": {
                "delay": 2000, 
                "touch-tip": true, 
                "tip-offset": -2, 
                "container": "trough", 
                "location": "A1"
              }, 
              "blowout": true
            }, 
            {
              "volume": 20, 
              "to": {
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "B2"
              }, 
              "extra-pull": true, 
              "from": {
                "delay": 2000, 
                "touch-tip": true, 
                "tip-offset": -2, 
                "container": "trough", 
                "location": "A2"
              }, 
              "blowout": true
            }
          ]
        }, 
        {
          "distribute": {
            "to": [
              {
                "volume": 20, 
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "A1"
              }, 
              {
                "volume": 30, 
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "A2"
              }, 
              {
                "volume": 100, 
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "A3"
              }
            ], 
            "from": {
              "container": "trough", 
              "location": "A1"
            }, 
            "blowout": true
          }
        }, 
        {
          "consolidate": {
            "to": {
              "container": "plate_2", 
              "location": "A1"
            }, 
            "from": [
              {
                "volume": 20, 
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "A1"
              }, 
              {
                "volume": 30, 
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "A2"
              }, 
              {
                "volume": 100, 
                "touch-tip": true, 
                "container": "plate_1", 
                "location": "A3"
              }
            ], 
            "blowout": true
          }
        }, 
        {
          "mix": [
            {
              "liquid-tracking": true, 
              "blowout": true, 
              "repetitions": 5, 
              "conatiner": "plate_2", 
              "volume": 20, 
              "location": "A1"
            }
          ]
        }
      ]
    }
  ], 
  "deck": {
    "trash": {
      "labware": "point"
    }, 
    "plate_2": {
      "labware": "96-flat"
    }, 
    "p200_rack": {
      "labware": "tiprack-200ul"
    }, 
    "trough": {
      "labware": "trough-12row"
    }, 
    "plate_1": {
      "labware": "96-flat"
    }
  }
}
```