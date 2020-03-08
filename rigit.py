import voter
import elections
import numpy as np
import random

def main():
    laziness_rate = 0.35
    election_sample_size = 100
    num_voters = 100
    verbose = False
    quadratic_utilities = True

    if verbose: print('We assume party-like sets of utilities')
    candidates = ['a', 'b', 'c', 'd']
    far_left_utils = {'a': 10, 'b':8, 'c': 6, 'd':0}
    left_utils = {'a': 6, 'b':10, 'c': 6, 'd':0}
    right_utils = {'a': 0, 'b':6, 'c': 10, 'd':8}
    far_right_utils = {'a': 0, 'b':2, 'c': 5, 'd':10}
    utils = [far_left_utils, left_utils, right_utils, far_right_utils]
    if quadratic_utilities:
        for util in utils: 
            for candidate in util.keys():
                util[candidate] = util[candidate]**2

    regrets = {'approval':[], 'plurality':[], 'IRV':[], 'QV':[], 'RP':[]}
    for i in range(election_sample_size):
        p = [0.4,0.35,0.2,0.05]
        random.shuffle(p)
        voter_utils = np.random.choice(utils, size=num_voters, p=p)
        voter_laziness = np.random.choice([voter.Laziest_Voter, voter.Honest_Voter], size=num_voters, p=[laziness_rate,1-laziness_rate])
        voters = [voter_laziness[v](utilities=voter_util, approval_rule='mean') for v,voter_util in enumerate(voter_utils)]
        
        if verbose: print('Under Approval Voting:')
        vote = elections.ApprovalVote(voters, candidates)
        vote.compute_votes()
        vote.aggregate_votes()
        vote.get_regret()
        regrets['approval'].append(vote.regret)
        top_2 = sorted(list(vote.tally.items()), key=lambda x: x[1], reverse=True)[:2]
        if verbose: print('Votes by candidate', top_2)
        if verbose: print('Regret:', vote.regret)

        if verbose: print('Under Plurality Voting: ')
        for person in voters: person.vote = dict()
        vote = elections.PluralityVote(voters, candidates)
        vote.compute_votes()
        vote.aggregate_votes()
        vote.get_regret()
        regrets['plurality'].append(vote.regret)
        top_2 = sorted(list(vote.tally.items()), key=lambda x: x[1], reverse=True)[:2]
        if verbose: print('Votes by candidate', top_2)
        if verbose: print('Regret:', vote.regret)

        if verbose: print('Under IRV: ')
        for person in voters: person.vote = dict()
        vote = elections.InstantRunoffVote(voters, candidates)
        vote.compute_votes()
        vote.aggregate_votes()
        vote.get_regret()
        regrets['IRV'].append(vote.regret)
        top_2 = sorted(list(vote.tally.items()), key=lambda x: x[1], reverse=True)[:2]
        if verbose: print('Votes by candidate', top_2)
        if verbose: print('Regret:', vote.regret)

        if verbose: print('Under RP: ')
        for person in voters: person.vote = dict()
        vote = elections.RankedPairsVote(voters, candidates)
        vote.compute_votes()
        vote.aggregate_votes()
        vote.get_regret()
        regrets['RP'].append(vote.regret)
        top_2 = sorted(list(vote.tally.items()), key=lambda x: x[1], reverse=True)[:2]
        if verbose: print('Votes by candidate', top_2)
        if verbose: print('Regret:', vote.regret)

        if verbose: print('Under QV: ')
        for person in voters: person.vote = dict()
        vote = elections.QuadraticVote(voters, candidates)
        vote.compute_votes()
        vote.aggregate_votes()
        vote.get_regret()
        regrets['QV'].append(vote.regret)
        top_2 = sorted(list(vote.tally.items()), key=lambda x: x[1], reverse=True)[:2]
        if verbose: print('Votes by candidate', top_2)
        if verbose: print('Regret:', vote.regret)

        if verbose: print('_________________________')


    print('Plurality %.4f, IRV %.4f, RP %.4f, Approval %.4f, QV %.4f' 
    %(np.mean(regrets['plurality']), np.mean(regrets['IRV']), np.mean(regrets['RP']), np.mean(regrets['approval']),  np.mean(regrets['QV'])))
if __name__=="__main__":
    main() 