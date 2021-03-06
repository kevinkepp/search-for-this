import os

from sft.runner.Tester import Tester

epsilon = 0.1
log_dir = "tmp/logs/"
exp = log_dir + sorted(os.listdir(log_dir))[-1]  # "0_paper/20170206-220842_exp_random_complex"
# testset_path = "tmp/tester/testworld_single"
# testset_path = "tmp/tester/testworld_line"
testset_path = "tmp/tester/testworlds_corner"
# testset_path = "tmp/tester/testwords_complex"
t = Tester(epsilon)
t.run_on_exp(exp, testset_path)
t.plot_results(exp, True, False)
# t.plot_paths(exp + "/tester", exp + "/world/world.py", 950)

# used for getting the q values (estimated by a certain model of an agent) for one state
if False:
	state_path = "tmp/tester/teststate/test_state"
	world_path = "tmp/logs/20170119-145057_exp/world/world.py"
	agent_path = "tmp/logs/20170119-145057_exp/agent_ah10_256/agent.py"
	model_path = "tmp/logs/20170119-145057_exp/agent_ah10_256/models/model_2900.h5.npz"
	b = Tester(epsilon)
	s = b.get_q_one_state(testset_path, world_path, agent_path, model_path)