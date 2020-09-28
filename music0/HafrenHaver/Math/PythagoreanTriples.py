"""InnovAnon Inc. Proprietary"""

from itertools import *

class PythagoreanTriples:
	"""https://en.wikipedia.org/wiki/Coprime_integers#Generating_all_coprime_pairs"""
	#roots = [(2, 1), (3, 1)]
	roots = zip ([2, 3], [1] * 2)

	@staticmethod
	def leaves (m, n): return [
		(2 * m - n, m),
		(2 * m + n, m),
		(m + 2 * n, n)]
	@staticmethod
	def next_row (row): return [
		PythagoreanTriples.leaves (m, n) for m, n in row]
	@staticmethod
	def rec (*arr):
		arr = list (arr)
		#row = list (chain.from_iterable (next_row (arr)))
		#tail = chain.from_iterable (starmap (rec, [row]))
		#return chain (arr, tail)
		return chain (arr, chain.from_iterable (starmap (
			PythagoreanTriples.rec, [
				chain.from_iterable (PythagoreanTriples.next_row (arr))])))
	@staticmethod
	def generate_coprime_pairs ():
		return PythagoreanTriples.rec (*PythagoreanTriples.roots)

if __name__ == "__main__":
	for k in PythagoreanTriples.generate_coprime_pairs ():
		print k
		#time.sleep (1)