from collections import *

#from bitarray import *

class Bjorklund:
	"""https://gist.github.com/unohee/d4f32b3222b42de84a5f"""
	@staticmethod
	def factory (lengthOfSeq, pulseAmt, rotateAmt=0):
		ret = Bjorklund (lengthOfSeq, pulseAmt)
		ret.bjorklund ()
		ret.rotate (rotateAmt)
		return ret

	def __init__ (self, lengthOfSeq, pulseAmt):
		self.lengthOfSeq = lengthOfSeq
		self.pulseAmt = pulseAmt
		
		self.remainder = []
		self.count = []
		self.sequence = deque ()
		#self.sequence = bitarray (lengthOfSeq)
	
	def __len__ (self): return self.lengthOfSeq
	def __iter__ (self): return iter (self.sequence)
	def __repr__ (self):
		return "Bjorklund (", self.lengthOfSeq, ",", self.pulseAmt, ")"
	def __str__ (self): return str (list (self.sequence))
	def __getitem__ (self, key): return self.sequence[key]
	def __reversed__ (self): return reversed (self.sequence)

	def buildSeq (self, slot):		
		if   slot is -1: self.sequence.append (0)
		elif slot is -2: self.sequence.append (1)
		else:
			i = 0
			while i < self.count[slot]:
				self.buildSeq (slot - 1)
				i += 1
			if self.remainder[slot] is not 0:
				self.buildSeq (slot - 2)
		
	def bjorklund (self):
		divisor = self.lengthOfSeq - self.pulseAmt
		if divisor < 0: raise Exception ()

		self.remainder.append (self.pulseAmt)
	
		index = 0
		while True:
			#self.count.append (floor (divisor / self.remainder[index]))
			self.count.append (divisor / self.remainder[index])
			self.remainder.append (divisor % self.remainder[index])
			divisor = self.remainder[index]
			index += 1
			if self.remainder[index] <= 1: break
		self.count.append (divisor)
		self.buildSeq (index)
		self.sequence.reverse ()
	
		zeroCount = 0
		if self.sequence[0] is not 1:
			zeroCount += 1
			while self.sequence[zeroCount] is 0:
				zeroCount += 1
			self.sequence.rotate (zeroCount)

	def rotate (self, amt):
		self.sequence.rotate (amt)

if __name__ == "__main__":
	print Bjorklund.factory (12, 5, 0)