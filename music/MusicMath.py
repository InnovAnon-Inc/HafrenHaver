from __future__ import division

class MusicMath:
	@staticmethod
	def generate_coprime_pairs (p):
		return generate_coprime_pairs_leaves (
			generate_coprime_pairs_roots (p), p)
	@staticmethod
	def generate_coprime_pairs_roots (p):
		return [(m, 1) for m in [2, 3] if m <= p]
	@staticmethod
	def generate_coprime_pairs_leaves (q, p):
		todo = []
		todo.extend (q)
		map (todo.extend, [
			generate_coprime_pairs_leaves (
				generate_coprime_pairs_leaf (e[0], e[1], p), p)
			for e in q])
		return todo
	#	for e in q:
	#		leaf = generatef3 (e[0], e[1], p)
	#		todo.extend (generate_coprime_pairs_leaves (leaf, p))
	#	return todo
	@staticmethod
	def generate_coprime_pairs_leaf (m, n, p):
		return [k for k in [
			(2 * m - n, m),
			(2 * m + n, m),
			(m + 2 * n, n)]
			if k[0] <= p]
		"""leaf = []
		for k in [
			(2 * m - n, m),
			(2 * m + n, m),
			(m + 2 * n, n)]:
			if k[0] <= p:
				leaf.append (k)
		return leaf"""
	@staticmethod	
	def euclid (h, k, l):
		#l[h] = l[k] ** a * b
		#(l[h] / b) = l[k] ** a
		#log base l[k] of (l[h] / b) = a
		#log (l[h] / b) / log l[k]) = a
		#log l[h] - log b = a log l[k]
		a = floor (log (l[h]) / log (l[k]))
		b = l[h] / (l[k] ** a)
		#print l[h], "=", l[k], "**", a, "+", b
		for i in xrange (len (l)):
			if (l[i] == b):
				#yield euclid (k, i, l)
				#break
				return euclid (k, i, l)
		epsilon = 10/9
		epsilon = (2 ** 485) / (3 ** 306)
		epsilon = 531441 / 524288
		if b < epsilon:
			return l
		l += [b]
		return euclid (k, len (l) - 1, l)