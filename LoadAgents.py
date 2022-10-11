import numpy as np

def vrni_agenta(agent_num):
    name = "res/AI_agents/agent" + str(agent_num) + ".txt"
    agent = np.loadtxt(name, dtype=float)
    return agent