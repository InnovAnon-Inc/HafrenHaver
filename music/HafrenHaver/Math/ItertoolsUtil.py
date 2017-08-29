"""InnovAnon Inc. Proprietary"""

from operator import *

class ItertoolsUtil:
	"""https://docs.python.org/3/library/itertools.html#itertools.accumulate"""
	@staticmethod
	def accumulate (iterable, func=add):
		'Return running totals'
		# accumulate([1,2,3,4,5]) --> 1 3 6 10 15
		# accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
		it = iter (iterable)
		try: total = next (it)
		except StopIteration: return
		yield total
		for element in it:
			total = func (total, element)
			yield total