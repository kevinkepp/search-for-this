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

	def at_matrix(self, mat):
		"""Returns the value in a given matrix at the position represented by this point"""
		return mat[self.y, self.x]

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
		self.start = start_point if start_point is not None else Point(0, 0)
		self.x = self.start.x
		self.y = self.start.y
		self.size = size
		self.w = size.w
		self.h = size.h

	def contains(self, point):
		return self.x <= point.x <= self.x + self.w and self.y <= point.y <= self.y + self.h

	def intersection(self, other_rect):
		"""get intersection of other rectangle with this(self) rectangle"""
		x_min = max(self.x, other_rect.x)
		y_min = max(self.y, other_rect.y)
		y_max = min(self.y + self.h, other_rect.y + other_rect.h)
		x_max = min(self.x + self.w, other_rect.x + other_rect.w)
		pt_up_left = Point(x_min, y_min)
		w = x_max - x_min
		h = y_max - y_min
		inter_size = Size(w, h)
		intersect_rect = Rectangle(pt_up_left, inter_size)
		return intersect_rect

	def crop_matrix(self, mat):
		"""Returns a sub-matrix of the given matrix defined by the bounds of this rectangle"""
		return mat[self.y:self.y + self.h, self.x:self.x + self.w]

	def get_middle(self):
		return Point(self.x + int(self.w / 2), self.y + int(self.h / 2))

	def __str__(self):
		return "Rectangle(start={0},size={1})".format(self.start, self.size)


# normalize array to [0, 1]
# TODO test
def normalize(arr):
	_min = np.min(arr)
	_max = np.max(arr)
	diff = _max - _min
	if diff != 0:
		arr -= _min
		arr /= diff


def get_bbox(world_size, view_size):
	border = Point(view_size.w + 1, view_size.h + 1)
	size = Size(world_size.w - 2 * border.x, world_size.h - 2 * border.y)
	return Rectangle(border, size)


def sample_int_uniform(low, high=None):
	return np.random.randint(low, high)


def sample_int_normal(mean, std):
	return int(np.random.normal(mean, std, 1))


def sample_int_normal_bounded(low, high, mean=-1, std=-1):
	diff = high - low
	if mean == -1:
		mean = low + diff / 2.
	if std == -1:
		std = mean - low
	if std <= 0:
		return mean
	while True:
		rnd = sample_int_normal(mean, std)
		if low <= rnd <= high:
			return rnd


def sample_point_within(rect):
	x = sample_int_uniform(rect.x, rect.x + rect.w)
	y = sample_int_uniform(rect.y, rect.y + rect.h)
	return Point(x, y)
