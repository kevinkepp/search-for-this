import numpy as np


class Point:
	def __init__(self, x, y=None):
		if x is None:
			assert isinstance(x, tuple)
			self.x = x[0]
			self.y = x[1]
		else:
			self.x = x
			self.y = y

	def __add__(self, other):
		if isinstance(other, Point):
			return Point(self.x + other.x, self.y + other.y)
		elif isinstance(other, (float, int, long)):
			return Point(self.x + other, self.y + other)
		else:
			return NotImplemented

	def __sub__(self, other):
		if isinstance(other, Point):
			return Point(self.x - other.x, self.y - other.y)
		elif isinstance(other, (float, int, long)):
			return Point(self.x - other, self.y - other)
		else:
			return NotImplemented

	def __mul__(self, other):
		if isinstance(other, Point):
			return Point(self.x * other.x, self.y * other.y)
		elif isinstance(other, (float, int, long)):
			return Point(self.x * other, self.y * other)
		else:
			return NotImplemented

	def __div__(self, other):
		if isinstance(other, Point):
			return Point(self.x / other.x, self.y / other.y)
		elif isinstance(other, (float, int, long)):
			return Point(self.x / other, self.y / other)
		else:
			return NotImplemented

	def tuple(self):
		return self.x, self.y

	def __str__(self):
		return "Point(x={0},y={1})".format(self.x, self.y)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		return NotImplemented

	def __ne__(self, other):
		if isinstance(other, self.__class__):
			return not self.__eq__(other)
		return NotImplemented

	def __hash__(self):
		return hash(tuple(sorted(self.__dict__.items())))


class Size:
	def __init__(self, w, h=None):
		if h is None:
			assert isinstance(w, tuple)
			self.w = w[0]
			self.h = w[1]
		else:
			self.w = w
			self.h = h

	def tuple(self):
		return self.w, self.h

	def __str__(self):
		return "Size(w={0},h={1})".format(self.w, self.h)


class Rectangle:
	def __init__(self, start_point, size):
		self.start = start_point
		self.x = start_point.x
		self.y = start_point.y
		self.size = size
		self.w = size.w
		self.h = size.h

	def contains(self, point):
		return self.x <= point.x <= self.x + self.w and self.y <= point.y <= self.y + self.h

	def __str__(self):
		return "Rectangle(start={0},size={1})".format(self.start, self.size)


# normalize array to [0, 1]
def normalize(arr):
	_min = np.min(arr)
	_max = np.max(arr)
	diff = _max - _min
	if diff != 0:
		arr -= _min
		arr /= diff


def submatrix(mat, rect):
	return mat[rect.x:rect.x + rect.w, rect.y:rect.y + rect.h]
