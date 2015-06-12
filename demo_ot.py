import json
from otprotocol.protocol import Protocol, Head

#instantiate new Protocol object
p = Protocol()

#append decks to Protocol object
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
p.transfer("trough","A1","plate_1","A1",100)
p.transfer("trough", ["A1","A2"],"plate_1", ["B1","B2"],[100,20])
p.distribute("trough","A1","plate_1",["A1","A2","A3"],[20, 30, 100])
p.consolidate("plate_1",["A1","A2","A3"],"plate_2","A1",[20, 30, 100])
p.mix("plate_2", "A1", 20)

print json.dumps(p.as_dict(), indent=2)