import json

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
		x = {
			"from": {
				"container": source,
				"location": source_well,
				"tip-offset": tip_offset,
				"delay": delay,
				"touch-tip": touch_tip
			},

			"to": {
				"container": dest,
				"location": dest_well,
				"touch-tip": touch_tip
			},
			"volume": volume,
			"blowout": blowout,
			"extra-pull": extra_pull
		}
            
		trans = {}
		trans["transfer"] = [x]
		self.instructions.append(trans) #trans is dictionary with key transfer and value a list of dictionaries





