import json
import pdb
class Deck(object):
    """Elements of OT deck"""
    def __init__(self, name, opts):
    	self.name = name
    	self.opts = opts

class Head(object):
	"""Pipette tool(s) of OT"""
	def __init__(self, name, opts):
		self.name = name
		self.opts = opts

class Protocol(object):
	""" Sequence of instructions to be executed and set of deck elements 
		on which instructions act"""
	def __init__(self, decks=[], head=None, instructions=None):
		self.decks = {}
		for deck in decks:
			self.decks[deck.name] = deck
		self.instructions = instructions or []

	def deck(self, name, labware, slot):
		"""Append a Deck object to deck list associated with protocol."""
		opts = {}
		opts["labware"] = labware
		opts["slot"] = slot
		self.decks[name] = Deck(name, opts)

	def set_head(self, head):
		self.head = head

	def as_dict(self):
		"""Return protocol as a dictionary"""
		return {
			"deck" : dict(
				(key,value.opts)
				for key, value in self.decks.items()),
			"head" : {self.head.name: self.head.opts},

			"instructions": [{
							"tool":self.head.name,
							"groups": self.instructions
							}]
		}

	def transfer(self, source, source_well, dest, dest_well, volume, touch_tip=True, blowout=True, extra_pull=True, tip_offset=-2, delay=2000):
		if not isinstance(source_well,list):
			source_well = [source_well]
		if not isinstance(dest_well,list):
			dest_well = [dest_well]
		if not isinstance(volume, list):
			volume = [volume]*len(source_well)
		trans = {}
		trans["transfer"] = []
		for a, b, v in zip(source_well, dest_well, volume):
			x = {
				"from": {
					"container": source,
					"location": a,
					"tip-offset": tip_offset,
					"delay": delay,
					"touch-tip": touch_tip
				},

				"to": {
					"container": dest,
					"location": b,
					"touch-tip": touch_tip
				},
				"volume": v,
				"blowout": blowout,
				"extra-pull": extra_pull
			}
            
			trans["transfer"].append(x)

		self.instructions.append(trans) #trans is dictionary with key transfer and value a list of dictionaries


	def distribute(self, source, source_well, dest, dest_wells, volumes, touch_tip=True, blowout=True):
		dest_groups = []
		#pdb.set_trace()
		if not isinstance(volumes,list):
			volumes = [volumes]*len(dest_wells)

		for well, vol in zip(dest_wells, volumes):
			d = {
				"container": dest,
				"location": well,
				"volume": vol,
				"touch-tip":touch_tip
			}
			dest_groups.append(d)

		x = { 	
			"from": {
				"container": source,
				"location": source_well,

			},

			"to": dest_groups,
			"blowout": blowout,
		}

		dist = {}
		dist["distribute"] = x
		self.instructions.append(dist)


	def consolidate(self, source, source_wells, dest, dest_well, volumes, touch_tip=True, blowout=True):
		source_groups = []
		#pdb.set_trace()
		if not isinstance(volumes,list):
			volumes = [volumes]*len(source_wells)

		for well, vol in zip(source_wells, volumes):
			d = {
				"container": source,
				"location": well,
				"volume": vol,
				"touch-tip":touch_tip
			}
			source_groups.append(d)

		x = { 	
			"from": source_groups,

			"to": {
				"container": dest,
				"location": dest_well,

			},
			"blowout": blowout,
		}

		cons = {}
		cons["consolidate"] = x
		self.instructions.append(cons)

	def mix(self, source, source_well, volume, repetitions=5, blowout=True, liquid_tracking=True):     
		x = {
			"conatiner": source,
			"location": source_well,
			"volume": volume,
			"repetitions": repetitions,
			"blowout": blowout,
			"liquid-tracking": liquid_tracking
		}

		mix = {}
		mix["mix"] = [x]
		self.instructions.append(mix)





