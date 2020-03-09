import voter
import elections

import numpy as np
import random
import argparse
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# A simple model for elections.
# 

def main(num_elections, num_voters, laziness, verbose, quadratic, electoral_systems, display):

    if verbose: print('We assume party-like sets of utilities')
    candidates = ['a', 'b', 'c', 'd']
    p = [0.4,0.35,0.2,0.05]
    far_left_utils = {'a': 10, 'b':8, 'c': 6, 'd':0}
    left_utils = {'a': 6, 'b':10, 'c': 6, 'd':0}
    right_utils = {'a': 0, 'b':6, 'c': 10, 'd':8}
    far_right_utils = {'a': 0, 'b':2, 'c': 5, 'd':10}
    utils = [far_left_utils, left_utils, right_utils, far_right_utils]
    if quadratic:
        for util in utils: 
            for candidate in util.keys():
                util[candidate] = util[candidate]**2

    regrets = {system:[] for system in electoral_systems}
    for i in range(num_elections):

        random.shuffle(p)
        voter_utils = np.random.choice(utils, size=num_voters, p=p)
        voter_laziness = np.random.choice([voter.Laziest_Voter, voter.Honest_Voter], size=num_voters, p=[laziness,1-laziness])
        voters = [voter_laziness[v](utilities=voter_util, approval_rule='mean') for v,voter_util in enumerate(voter_utils)]

        for system in electoral_systems:
            if system=='Approval': vote = elections.ApprovalVote(voters, candidates)
            elif system=='Plurality': vote = elections.PluralityVote(voters, candidates)
            elif system=='IRV': vote = elections.InstantRunoffVote(voters, candidates)
            elif system=='Ranked Pairs': vote = elections.RankedPairsVote(voters, candidates)
            elif system=='Quadratic': vote = elections.QuadraticVote(voters, candidates)
            vote.compute_votes()
            vote.aggregate_votes()
            vote.get_regret()
            regrets[system].append(vote.regret)
            # top_2 = sorted(list(vote.tally.items()), key=lambda x: x[1], reverse=True)[:2]

    if display in [1,2]:
        for system in electoral_systems:
            print('Mean regret by electoral system:')
            print(system, round(np.mean(regrets[system]),1))
    if display in [0,2]:
        regret_df = pd.DataFrame.from_dict(regrets)
        order = regret_df.mean().sort_values().index
        regret_plot = sns.barplot(data=regret_df, orient='h', palette='Set2', order=order).set_title('Distribution of regrets under various electoral systems')
        plt.show()

    

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Run simulations of voters voting under different electoral systems and compare regret (i.e. utility lost)')
    parser.add_argument('-ne', '--num_elections', type=int, default=100, help='Set number of votes simulated')
    parser.add_argument('-nv', '--num_voters', type=int, default=250, help='Set number of voters per election')
    parser.add_argument('-e', '--electoral_systems', type=str, nargs='*', default=['Plurality', 'IRV', 'Ranked Pairs', 'Approval', 'Quadratic'], help='Set which electoral systems to simulate')
    parser.add_argument('-l', '--laziness', type=float, default=0.33, help='Set percentage of voterbase who will be drawn from lazy voter class')
    parser.add_argument('-v', '--verbose', action='store_true', help='Set output verbosity')
    parser.add_argument('-d', '--display', type=int, default=0, help='Set plot (0), print (1) or both (2)')
    parser.add_argument('-q', '--quadratic', action='store_true', help='Square voter utilities')

    kwargs = parser.parse_args()
    main(**vars(kwargs)) 