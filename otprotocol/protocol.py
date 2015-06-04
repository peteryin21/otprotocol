from .container import Container, Well, WellGroup
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

	def deck(self, name, labware):
		"""Append a Deck object to deck list associated with protocol."""
		opts = {}
		opts["labware"] = labware
		self.decks[name] = Deck(name, opts)
		container = Container(labware)
		return container

	def set_head(self, head):
		self.head = head

	def as_dict(self):
		"""Return protocol as a dictionary"""
		return {
			"deck" : dict(
				(key,value.opts)
				for key, value in self.decks.items()),
			"head" : {self.head.name: self.head.opts},
			"instructions": list(map(lambda x: self._refify(x.data),
                             		self.instructions))
		}

	def transfer(self, source, dest, volume, touch_tip=True, blowout=True, extra_pull=True, tip_offset=-2, delay=2000):
		source = WellGroup(source)
		dest = WellGroup(dest)
		opts = []
		len_source = len(source.wells)
		len_dest = len(dest.wells)



		for s,d,v in list(zip(source.wells, dest.wells, volume)):
			xfer = {
				"from": s, #add tipp offset, delay, and touch-tip to s, source.wells
    	    	"to": d, #add touch-tip to d, dest.wells
    		}

			assign(xfer, "volume", v)
			assign(xfer, "blowout", blowout)
			assign(xfer, "extra_pull", extra_pull)
            
			opts.append(xfer)


		for x in opts:
		    trans = {}
		    trans["transfer"] = [x]
		    #self._pipette([trans]) #add later for multiple groups
		    self.instructions.append(Pipette([trans]))


	def _refify(self, op_data):
		if type(op_data) is dict:
			return {k: self._refify(v) for k, v in op_data.items()}
		elif type(op_data) is list:
			return [self._refify(i) for i in op_data]
		elif isinstance(op_data, Well):
			return self._ref_for_well(op_data)
		elif isinstance(op_data, WellGroup):
			return [self._ref_for_well(w) for w in op_data.wells]
		elif isinstance(op_data, Container):
			return self._ref_for_container(op_data)
		else:
			return op_data

	def _ref_for_well(self, well):
		return "%s/%d" % (self._ref_for_container(well.container), well.index)

	def _ref_for_container(self, container):
		for k in self.decks:
			v = self.decks[k]
			if v.container is container:
				return k


class Instruction(object):
	def __init__(self, data):
		self.data = data
		self.__dict__.update(data)

	def json(self):
		return json.dumps(self.data, indent=2)


class Pipette(Instruction):
	def __init__(self, groups):
		super(Pipette,self).__init__({
			"tool":"p200", #link this to head.name?
			"groups":groups
			})

def assign(obj, key, var):
    if var is not None:
        obj[key] = var


