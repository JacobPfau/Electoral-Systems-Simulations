import voter
import voting
import numpy as np

def main():
    print('Compare approval voting to plurality voting assuming 30% the voters are lazy and 60% vote using median threshold.')
    print('We assume two sets of party-like sets of utilities')
    candidates = ['a', 'b', 'c', 'd']
    # utilities_lexico = {candidate:4-c for c,candidate in enumerate(candidates)}
    # utilities_inverse_lexico = {candidate:c for c,candidate in enumerate(candidates)}
    left_utils = {'a': 10, 'b':8, 'c': 6, 'd':0}
    right_utils = {'a': 0, 'b':2, 'c': 5, 'd':10}
    regrets = {'approval':[], 'plurality':[]}
    for i in range(10):
        party_affil = np.random.binomial(1,0.55,size=100)
        voters = []
        for v in range(30): 
            if party_affil[v]==0: voters.append(voter.Laziest_Voter(left_utils))
            else: voters.append(voter.Laziest_Voter(right_utils))
        for v in range(30,100):
            if party_affil[v]==0: voters.append(voter.Honest_Voter(left_utils))
            else: voters.append(voter.Honest_Voter(right_utils))
        
        print('Under Approval Voting: ')
        vote = voting.ApprovalVote(voters, candidates)
        vote.compute_votes()
        vote.aggregate_votes()
        print('Election winner is:', vote.winner)
        vote.get_regret()
        regrets['approval'].append(vote.regret)
        print('Regret:', vote.regret)

        print('Under Plurality Voting: ')
        for person in voters: person.vote = dict()
        vote = voting.PluralityVote(voters, candidates)
        vote.compute_votes()
        vote.aggregate_votes()
        print('Election winner is:', vote.winner)
        vote.get_regret()
        regrets['plurality'].append(vote.regret)
        print('Regret:', vote.regret)

    print(np.mean(regrets['approval']), np.mean(regrets['plurality']))
if __name__=="__main__":
    main() 