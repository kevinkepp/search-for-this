from sft import Point
from sft.sim import sample_normal, sample_point_within, sample_uniform


class PathNode:
	def __init__(self, id_, pos, path_id=-1):
		self.id = id_
		self.path_id = path_id
		self.pos = pos


class PathGenerator:
	def __init__(self, view_size, bbox):
		self.view_size = view_size
		self.bbox = bbox

	def generate_path(self, length, graph, path_id):
		self._generate_path(length, graph, path_id, [])

	def _generate_path(self, length, graph, path_id, nodes):
		if len(nodes) == 0:
			# sample starting node uniformly
			pos = sample_point_within(self.bbox)
			node_new = PathNode(0, pos, path_id)
		else:
			# sample next node based on previous one
			id_ = len(graph.nodes())
			# sample node and only accept it if new edge does not intersect existing edges, maximally sample 20 times
			for i in range(20):
				# try to sample step, maximally 10 times
				for j in range(10):
					pos = self.sample_step_from(nodes[-1])
					if pos is not None:
						break
				else:  # when loop ended normally we stop building path because we can't sample new steps anymore
					return
				node_new = PathNode(id_, pos, path_id)
				if not self.is_intersecting_any((nodes[-1], node_new), graph.edges()):
					break
			else:  # when loop ended normally we stop building path because we can't find node with non-intersecting edge anymore
				return
		# add new node to the graph
		graph.add_node(node_new)
		# add edge from previous node to new node
		if len(nodes) > 0:
			graph.add_edge(nodes[-1], node_new)
		# recurse if length not reached
		nodes.append(node_new)
		if length > 0:
			self._generate_path(length - 1, graph, path_id, nodes)

	# samples a location for a new node based on a given previous node
	def sample_step_from(self, prev_node, step_size_min=-1):
		direction = sample_uniform(4)
		step = Point(0, 0)
		if step_size_min == -1:
			step_size_min = max(min(self.view_size.tuple()) / 2., 2)
		if direction == 0:  # up
			step_size_max = prev_node.pos.y - self.bbox.y
			step.y = -1
		elif direction == 1:  # down
			step_size_max = self.bbox.y + self.bbox.h - prev_node.pos.y
			step.y = 1
		elif direction == 2:  # left
			step_size_max = prev_node.pos.x - self.bbox.x
			step.x = -1
		else:  # right
			step_size_max = self.bbox.x + self.bbox.w - prev_node.pos.x
			step.x = 1
		step_size_diff = step_size_max - step_size_min
		# check if step not possible
		if step_size_diff <= 1:
			return None
		step_size_mean = step_size_diff / 2 + step_size_min
		step_size_std = max(step_size_diff / 5., 1)
		step_size = sample_normal(step_size_mean, step_size_std, step_size_min, step_size_max)
		step *= step_size
		return prev_node.pos + step

	def is_intersecting_any(self, edge_new, edges):
		for e in edges:
			if self.is_intersecting(edge_new, e):
				return True
		return False

	def is_intersecting(self, e1, e2):
		v1, v2 = e1
		v3, v4 = e2
		p1 = v1.pos
		p2 = v2.pos
		p3 = v3.pos
		p4 = v4.pos
		# Before anything else check if lines have a mutual abcisses
		interval_1 = [min(p1.x, p2.x), max(p1.x, p2.x)]
		interval_2 = [min(p3.x, p4.x), max(p3.x, p4.x)]
		interval = [
			min(interval_1[1], interval_2[1]),
			max(interval_1[0], interval_2[0])
		]
		if interval_1[1] < interval_2[0]:
			return False  # no mutual abcisses

		# Try to compute interception
		def line(p1, p2):
			A = (p1.y - p2.y)
			B = (p2.x - p1.x)
			C = (p1.x * p2.y - p2.x * p1.y)
			return A, B, -C

		L1 = line(p1, p2)
		L2 = line(p3, p4)
		D = L1[0] * L2[1] - L1[1] * L2[0]
		Dx = L1[2] * L2[1] - L1[1] * L2[2]
		Dy = L1[0] * L2[2] - L1[2] * L2[0]
		if D != 0:
			x = Dx / D
			y = Dy / D
			p = Point(x, y)
			if p.x < interval[1] or p.x > interval[0]:
				return False  # out of bounds
			else:
				# it's an intersection if new edge does not originate from previous one
				return not (p == p1 == p3 or p == p1 == p4)
		else:
			return False  # not intersecting