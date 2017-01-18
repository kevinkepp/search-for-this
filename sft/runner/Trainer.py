import os
import pkgutil
from importlib import import_module

import threading

from sft.runner.Runner import Runner


class Trainer(Runner):

	def run(self, experiment, threaded=False):
		self.set_seed()
		world_config, agent_configs = self.get_configs(experiment)
		scenarios = self.init_scenarios(world_config)
		if threaded:
			threads = []
			for agent in agent_configs:
				thread = threading.Thread(target=self.run_agent, args=(agent, scenarios))
				thread.daemon = False
				thread.start()
				threads.append(thread)
			for t in threads:
				t.join()
		else:
			for agent in agent_configs:
				self.run_agent(agent, scenarios)
		world_config.world_logger.close_files()

	def get_configs(self, experiment):
		world_config = import_module("." + self.WORLD_CONFIG_NAME, experiment.__name__)
		agent_configs = []
		experiment_dir = os.path.dirname(experiment.__file__)
		agents_dir = os.path.join(experiment_dir, self.AGENT_CONFIG_NAME_DIR)
		for loader, module, is_pkg in pkgutil.iter_modules([agents_dir]):
			if not is_pkg and module != "__init__":
				agent_config = import_module("." + module, experiment.__name__ + "." + self.AGENT_CONFIG_NAME_DIR)
				agent_configs.append(agent_config)
		return world_config, agent_configs

	def init_scenarios(self, config):
		scenarios = []
		for n in range(config.epochs):
			scenario = config.world_gen.get_next()
			scenarios.append(scenario)
			config.world_logger.log_init_state_and_world(scenario.world, scenario.pos)
			config.world_logger.next_epoch()
			config.sampler.next_epoch()
		return scenarios

	def _get_eps(self, config, epoch):
		eps = config.epsilon_update.get_value(epoch)
		return eps

	def _incorp_agent_reward(self, agent, state, action, state2, reward_value):
		agent.incorporate_reward(state, action, state2, reward_value)

