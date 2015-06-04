




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

	def deck(self, name, labware):
		"""Append a Deck object to deck list associated with protocol."""
		opts = {}
		opts["labware"] = labware
		self.decks[name] = Deck(name, opts)

	def set_head(self, head):
		self.head = head

	def as_dict(self):
		"""Return protocol as a dictionary"""
		return {
			"deck" : dict(
				(key,value.opts)
				for key, value in self.decks.items()
			),
			"head" : {self.head.name, self.head.opts} 
			#?????????
			"instructions": list(map(lambda x: self._refify(x.data),
                             		self.instructions))
		}
