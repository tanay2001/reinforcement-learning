# -*- coding: utf-8 -*-
"""Assignment2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KOhrQT6DLey0RIfJZCjs24N6WXwMcKXm

# What is the notebook about?

## Problem - Taxi Environment Algorithms
This problem deals with a taxi environment and stochastic actions. The tasks you have to do are:
- Implement Policy Iteration
- Visualize the results
- Explain the results

## How to use this notebook? 📝

- This is a shared template and any edits you make here will not be saved.**You
should make a copy in your own drive**. Click the "File" menu (top-left), then "Save a Copy in Drive". You will be working in your copy however you like.

- **Update the config parameters**. You can define the common variables here

Variable | Description
--- | ---
`AICROWD_DATASET_PATH` | Path to the file containing test data. This should be an absolute path.
`AICROWD_RESULTS_DIR` | Path to write the output to.
`AICROWD_ASSETS_DIR` | In case your notebook needs additional files (like model weights, etc.,), you can add them to a directory and specify the path to the directory here (please specify relative path). The contents of this directory will be sent to AIcrowd for evaluation.
`AICROWD_API_KEY` | In order to submit your code to AIcrowd, you need to provide your account's API key. This key is available at https://www.aicrowd.com/participants/me

- **Installing packages**. Please use the [Install packages 🗃](#install-packages-) section to install the packages
"""

"""# Setup AIcrowd Utilities 🛠

We use this to bundle the files for submission and create a submission on AIcrowd. Do not edit this block.
"""

!pip install -U aicrowd-cli > /dev/null

"""# AIcrowd Runtime Configuration 🧷

Define configuration parameters.
"""

import os

AICROWD_DATASET_PATH = os.getenv("DATASET_PATH", os.getcwd()+"/407e4f07-d470-427d-8758-4f888ae03fe6_data.zip")
AICROWD_RESULTS_DIR = os.getenv("OUTPUTS_DIR", "results")
API_KEY = "a822a19a0429f6683900b1197f296387" # Get your key from https://www.aicrowd.com/participants/me (ctrl + click the link)

!aicrowd login --api-key $API_KEY
!aicrowd dataset download -c rl-assignment-2-taxi

DATASET_DIR = 'data'
!unzip $AICROWD_DATASET_PATH

"""# Install packages 🗃

Please add all package installations in this section
"""



"""# Import packages 💻"""

import numpy as np
import matplotlib.pyplot as plt 
import os
# ADD ANY IMPORTS YOU WANT HERE

"""# Prediction Phase

## Taxi Environment

Read the environment to understand the functions, but do not edit anything
"""

import numpy as np

class TaxiEnv_HW2:
    
    def __init__(self, states, actions, probabilities, rewards, initial_policy):        
        probabilities, rewards = self._build_prob_mapping(states, actions, probabilities,rewards)
        self.possible_states = states
        self._possible_actions = {st: actions for st in states}
        self._ride_probabilities = {st: pr for st, pr in zip(states, probabilities)}
        self._ride_rewards = {st: rw for st, rw in zip(states, rewards)}
        self.initial_policy = initial_policy
        self._verify()

    def _build_prob_mapping(self,states, actions, probabilities,rewards):
        n_cities = len(states)
        n_actions = len(actions)

        probs = np.zeros((n_cities, n_actions, n_cities))
        
        rewards[0] = [0,0,0,0,0,0]    
        rews = np.zeros((n_cities, n_actions, n_cities))

        for src in range(n_cities):
          for action in ('1', '2'):
              for c, prob in probabilities[action].items():
                  dst = (src+c) % n_cities
                  probs[src][actions.index(action)][dst] = prob
                  rews[src][actions.index(action)][dst] = rewards[c][src]
          action = '3'
          action = actions.index(action)
          probs[src][action][0] = 1
        return probs, rews

    def _check_state(self, state):
        assert state in self.possible_states, "State %s is not a valid state" % state

    def _verify(self):
        """ 
        Verify that data conditions are met:
        Number of actions matches shape of next state and actions
        Every probability distribution adds up to 1 
        """
        ns = len(self.possible_states)
        for state in self.possible_states:
            ac = self._possible_actions[state]
            na = len(ac)
            rp = self._ride_probabilities[state]
            assert np.all(rp.shape == (na, ns)), "Probabilities shape mismatch"
        
            rr = self._ride_rewards[state]
            assert np.all(rr.shape == (na, ns)), "Rewards shape mismatch"

            assert np.allclose(rp.sum(axis=1), 1), "Probabilities don't add up to 1"

    def possible_actions(self, state):
        """ Return all possible actions from a given state """
        self._check_state(state)
        return self._possible_actions[state]

    def ride_probabilities(self, state, action):
        """ 
        Returns all possible ride probabilities from a state for a given action
        For every action a list with the returned with values in the same order as self.possible_states
        """
        actions = self.possible_actions(state)
        ac_idx = actions.index(action)
        return self._ride_probabilities[state][ac_idx]

    def ride_rewards(self, state, action):
        actions = self.possible_actions(state)
        ac_idx = actions.index(action)
        return self._ride_rewards[state][ac_idx]

"""## Example of Environment usage"""

import numpy as np 

def check_taxienv():
    # These are the values as used in the assignment document, but they may be changed during submission, so do not hardcode anything

    states = [0, 1, 2, 3, 4, 5]

    actions = ['1','2','3']

    probs = {}
    probs['1'] = {-1: 1/2, 0: 1/4, 1: 1/4}
    probs['2'] = {-1: 1/16, 0: 3/4, 1: 3/16}
    #probs['2'] = {-1: 3/4, 0: 1/16, 1: 3/16}

    rewards = {}
    rewards[-1] = [8,7,3,2,1,2]
    rewards[1]  = [8,8,5,1,3,9]

    initial_policy = {0:'1', 1:'1', 2:'1', 3:'1', 4:'1', 5:'1'}

    ##################################


    env = TaxiEnv_HW2(states, actions, probs, rewards, initial_policy)
    print("All possible states", env.possible_states)
    print("All possible actions from state B", env.possible_actions(1))
    print("Ride probabilities from state A with action 2", env.ride_probabilities(2, '2'))
    print("Ride rewards from state C with action 3", env.ride_rewards(2, '2'))

    base_kwargs = {"states": states, "actions": actions, 
                "probabilities": probs, "rewards": rewards,
                "initial_policy": initial_policy}
    return base_kwargs

base_kwargs = check_taxienv()

"""## Task - Policy Iteration
Run policy iteration on the environment and generate the policy and expected reward
"""

# 1.1 Policy Iteration
def policy_iteration(taxienv, gamma):
    # A list of all the states
    states = taxienv.possible_states
    # Initial values
    values = {s: 0 for s in states}
    # This is a dictionary of states to policies -> e.g {'A': '1', 'B': '2', 'C': '1'}
    policy = taxienv.initial_policy.copy()
    extra_info = {}
    num_of_iterations =0
    while True:
      while True:
        delta =0
        for s in taxienv.possible_states:
            v = 0
            for id,ls in enumerate(zip(taxienv.ride_probabilities(s, policy[s]), taxienv.ride_rewards(s, policy[s]))):
              prob, reward = ls[0], ls[1]
              next_state = taxienv.possible_states[id]
              v = v +  prob * (reward + gamma * values[next_state])
            delta = max(delta, np.abs(v - values[s]))
            values[s] = v
        if delta < 1e-8:
            break
      done =1
      for s in taxienv.possible_states:
        old_a = policy[s]
        A = {a:0 for a in taxienv.possible_actions(s)}
        for a in taxienv.possible_actions(s):
            for id, ls in enumerate(zip(taxienv.ride_probabilities(s, a), taxienv.ride_rewards(s, a))):
              prob, reward = ls[0], ls[1]
              next_state = taxienv.possible_states[id]
              A[a] = A[a] + prob*(reward + gamma*values[next_state])
        best_a = max(A, key = lambda x: A[x])
        policy[s] = best_a
        if old_a != best_a:
            done =0
      num_of_iterations +=1
      if done ==1:
        extra_info[gamma] = num_of_iterations
        break
    
    ## Do not edit below this line
    # Final results
    return {"Expected Reward": values, "Policy": policy}, extra_info

"""Policy Iteration with different values of gamma

"""

# 1.2 Policy Iteration with different values of gamma
def run_policy_iteration(env):
    gamma_values = np.arange(5, 100, 5)/100
    results, extra_info = {}, {}
    for gamma in gamma_values:
        results[gamma], extra_info[gamma] = policy_iteration(env, gamma)
    return results, extra_info

# Do not edit this cell
def get_results(kwargs):

    taxienv = TaxiEnv_HW2(**kwargs)

    policy_iteration_results = run_policy_iteration(taxienv)[0]

    final_results = {}
    final_results["policy_iteration"] = policy_iteration_results

    return final_results

get_results(base_kwargs)

taxienv = TaxiEnv_HW2(**base_kwargs)
run_policy_iteration(taxienv)[1]

if not os.path.exists(AICROWD_RESULTS_DIR):
  os.mkdir(AICROWD_RESULTS_DIR)
if not os.path.exists(DATASET_DIR+'/inputs'):
  os.mkdir(DATASET_DIR+'/inputs')

# Do not edit this cell, generate results with it as is

input_dir = os.path.join(DATASET_DIR, 'inputs')

if not os.path.exists(AICROWD_RESULTS_DIR):
    os.mkdir(AICROWD_RESULTS_DIR)

for params_file in os.listdir(input_dir):
  kwargs = np.load(os.path.join(input_dir, params_file), allow_pickle=True).item()
  print(kwargs)
  results = get_results(kwargs)
  idx = params_file.split('_')[-1][:-4]
  np.save(os.path.join(AICROWD_RESULTS_DIR, 'results_' + idx), results)

# Check your score on the given test cases (There are more private test cases not provided)
result_folder = AICROWD_RESULTS_DIR
target_folder = os.path.join(DATASET_DIR, 'targets')

def check_algo_match(results, targets):
    param_matches = []
    for k in results:
        param_results = results[k]
        param_targets = targets[k]
        policy_match = param_results['Policy'] == param_targets['Policy']
        rv = [v for k, v in param_results['Expected Reward'].items()]
        tv = [v for k, v in param_targets['Expected Reward'].items()]
        rewards_match = np.allclose(rv, tv, atol=1e-1)
        equal = rewards_match and policy_match
        param_matches.append(equal)
    return np.mean(param_matches)

def check_score(target_folder, result_folder):
    match = []
    for out_file in os.listdir(result_folder):
        res_file = os.path.join(result_folder, out_file)
        results = np.load(res_file, allow_pickle=True).item()
        idx = out_file.split('_')[-1][:-4]  # Extract the file number
        target_file = os.path.join(target_folder, f"targets_{idx}.npy")
        targets = np.load(target_file, allow_pickle=True).item()
        algo_match = []
        for k in targets:
            algo_results = results[k]
            algo_targets = targets[k]
            # print('Target', algo_targets)
            # print('Results', algo_results)
            algo_match.append(check_algo_match(algo_results, algo_targets))
        match.append(np.mean(algo_match))
    return np.mean(match)

if os.path.exists(target_folder):
    print("Shared data Score (normalized to 1):", check_score(target_folder, result_folder))

"""## Answer the following

1. How is different values of γ affecting the policy iteration from 1.2? Explain your findings

Your Answer: 
As gamma increase action3 becomes more prominent in states 3,4 , as previously the risk of breakdown on travelling to stop was high so rather take a lower reward , but now as breakdown chances decrease one can consider going back as a better option. Also for the given initializing condition we can see that as gamma increases it takes more set of policy eval and improvement steps (extra info)

We also note that states 3, 4 have lower expetced rewards in general, the reason as gamma helps to take action 3 in state 3,4 is even though it has a 0 reward the value of state 0 is comparatably high as a result high gamma favours trasition to state 0 from 3,4

2. Give alternate transition probabilities for action 2(if exists) such that optimal policy consists of action 2. Explain your answer

Your Answer: as rewards for c = -1 and c = 1 are non zero it makes most sense to increase the probabilities of these outcomes compared to c =0 , hence then the optimal polciy could contain action 2 like probs['2'] = {-1: 3/4, 0: 1/16, 1: 3/16}
 on using these probabilities values the optimial value consists of action2

# Submit to AIcrowd 🚀
"""

!DATASET_PATH=$AICROWD_DATASET_PATH \
aicrowd notebook submit \
    -c rl-assignment-2-taxi -a assets