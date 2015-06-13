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