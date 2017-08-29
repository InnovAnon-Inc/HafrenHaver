from __future__ import division
from collections import *
from math import *

class Bjorklund:
	@staticmethod
	def factory (lengthOfSeq, pulseAmt, rotateAmt):
		ret = Bjorklund (lengthOfSeq, pulseAmt)
		ret.bjorklund ()
		ret.rotate (rotateAmt)
		return ret
	"""
	lengthOfSeq = -1
	pulseAmt = -1
	
	remainder = []
	count = []
	sequence = deque ()
	"""
	def __init__ (self, lengthOfSeq, pulseAmt):
		self.lengthOfSeq = lengthOfSeq
		self.pulseAmt = pulseAmt
		
		self.remainder = []
		self.count = []
		self.sequence = deque ()

	def buildSeq (self, slot):
		#lengthOfSeq = self.lengthOfSeq
		#pulseAmt = self.pulseAmt
		
		#remainder = self.remainder
		#count = self.count
		#sequence = self.sequence
		
		#print "buildSeq (", slot, sequence, ")"
		
		if slot is -1:
			self.sequence.append (0)
			#print "sequence=", sequence
		elif slot is -2:
			self.sequence.append (1)
			#print "sequence=", sequence
		else:
			i = 0
			while i < self.count[slot]:
				self.buildSeq (slot - 1)
				#print "sequence=", sequence
				i += 1
			if self.remainder[slot] is not 0:
				self.buildSeq (slot - 2)
				#print "sequence=", sequence
			#else:
			#	self.buildSeq (slot - 3)
			#	print "SEQUENCE=", sequence
		
	def bjorklund (self):
		#lengthOfSeq = self.lengthOfSeq
		#pulseAmt = self.pulseAmt
		
		#remainder = self.remainder
		#count = self.count
		#sequence = self.sequence
		
		divisor = self.lengthOfSeq - self.pulseAmt
		if divisor < 0: raise Exception ()
		
		# TODO
		#if self.lengthOfSeq is 1:
		#	self.sequence = [self.pulseAmt]
		#	return
		#print self.lengthOfSeq, self.pulseAmt, self.remainder

		self.remainder.append (self.pulseAmt)
	
		index = 0
		# TODO verify correctness of if-statement
		#if remainder[index] > 1:
		if True:
			while True:
				self.count.append (floor (divisor / self.remainder[index]))
				self.remainder.append (divisor % self.remainder[index])
				divisor = self.remainder[index]
				index += 1
				if self.remainder[index] <= 1: break
				#if remainder[index] is 0: break
		self.count.append (divisor)
		#print "divisor=", divisor
		#print "count=", count
		#print "remainder=", remainder
		#count.reverse ()
		#remainder.reverse ()
		self.buildSeq (index)
		#print "sequence=", sequence
		self.sequence.reverse ()
		#print "sequence=", sequence
	
		zeroCount = 0
		if self.sequence[0] is not 1:
			zeroCount += 1
			while self.sequence[zeroCount] is 0:
				zeroCount += 1
			self.sequence.rotate (zeroCount)
	def rotate (self, amt):
		self.sequence.rotate (amt)