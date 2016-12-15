import cv2
import networkx as nx
import numpy as np

from sft.Scenario import Scenario
from sft import Point, Rectangle, normalize, submatrix, bbox, sample_normal, sample_point_within
from sft.sim.Simulator import Simulator
from sft.sim.PathGenerator import PathGenerator
from sft.sim.ScenarioGenerator import ScenarioGenerator


class PathWorldGenerator(ScenarioGenerator):
	PATH_LENGTH_MIN = 5
	PATH_LENGTH_MAX = 20
	PATH_LENGTH_MEAN = 12
	PATH_LENGTH_STD = 5
	PATH_THICKNESS = 1
	PATH_COLOR = 150

	TARGET_COLOR = int(Simulator.TARGET_VALUE * 255)
	TARGET_RADIUS = 2

	def __init__(self, view_size, world_size, path_in_init_view=False):
		self.view_size = view_size
		self.world_size = world_size
		self.bbox = bbox(world_size, view_size)
		self.path_in_init_view = path_in_init_view
		self.generator = PathGenerator(view_size, self.bbox)

	def get_next(self):
		world = self.init_world()
		pos = self.init_pos(world)
		return Scenario(world, pos)

	def init_world(self):
		world = np.full(self.world_size.tuple(), 0., dtype=np.float)
		graph = nx.Graph()
		self.init_path(world, graph)
		self.init_target(world, graph)
		world = np.array(world, np.float32)
		# normalize world image to [0, 1]
		normalize(world)
		return world

	def init_path(self, world, graph):
		# only add one path for now
		# sample length for path
		path_length = sample_normal(self.PATH_LENGTH_MEAN, self.PATH_LENGTH_STD, self.PATH_LENGTH_MIN,
									self.PATH_LENGTH_MAX)
		self.generator.generate_path(path_length, graph, path_id=0)
		self.render_paths(world, graph)

	def render_paths(self, image, graph):
		for u, v in graph.edges():
			e = graph[u][v]
			# here we can get edge attributes from e
			# TODO dotted line from http://stackoverflow.com/questions/26690932/opencv-rectangle-with-dotted-or-dashed-lines
			cv2.line(image, pt1=u.pos.tuple(), pt2=v.pos.tuple(), color=self.PATH_COLOR, thickness=self.PATH_THICKNESS)

	def init_target(self, world, graph):
		node_target = self.generate_target(graph)
		self.render_target(world, node_target)

	def generate_target(self, graph):
		# pick one of the graph nodes as target
		nodes = graph.nodes()
		node = np.random.choice(nodes)
		graph[node]['target'] = 1
		return node

	def render_target(self, image, node):
		# thickness -1 means fill circle
		cv2.circle(image, center=node.pos.tuple(), radius=self.TARGET_RADIUS, color=self.TARGET_COLOR, thickness=-1)

	def init_pos(self, world):
		pos = None
		view = None
		# when required find initial view where path is visible
		while view is None or (self.path_in_init_view and not self.is_path_in_view(view)):
			pos = sample_point_within(self.bbox)
			view = self.get_view(world, pos)
		return pos

	def get_view(self, world, pos):
		# find start of view because view_pos indicates center of view
		pos_start = pos - Point(self.view_size.w / 2, self.view_size.h / 2)
		view = submatrix(world, Rectangle(pos_start, self.view_size))
		return view

	def is_path_in_view(self, view):
		# for now just check if there are non-zero pixel
		return np.sum(view) > 0.