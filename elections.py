from abc import ABC, abstractmethod

class ElectoralSystem(ABC):

    def __init__(self, voters, candidates):
        self.voters = voters
        self.candidates = candidates
        self.tally = dict()
        self.winner = None

    def compute_votes(self,):
        for voter in self.voters: _ = voter.policy(self)

    @abstractmethod
    def aggregate_votes(self,):
        '''
        Runs elections and sets self.winner
        '''
        pass

    def get_regret(self,):
        total_utils = {candidate:sum([voter.utilities[candidate] for voter in self.voters]) for candidate in self.candidates}
        election_util = total_utils[self.winner]
        self.regret = max(total_utils.values())-election_util

class ApprovalVote(ElectoralSystem):
    name = 'ApprovalVote'

    def aggregate_votes(self,):
        for candidate in self.candidates: self.tally[candidate]=0
        for voter in self.voters:
            for candidate, vote in voter.vote.items():
                assert vote==0 or vote==1
                self.tally[candidate] = self.tally[candidate]+vote
        favorite = [*list(self.tally.items())[0]]
        for candidate, votes in self.tally.items():
            if votes>favorite[1]: favorite = [candidate, votes]
        self.winner = favorite[0]

class PluralityVote(ElectoralSystem):
    name = 'PluralityVote'

    def aggregate_votes(self):
        '''
        If more than one vote is cast, the vote will be discarded without counting.
        '''
        for candidate in self.candidates: self.tally[candidate]=0
        for voter in self.voters:
            if len(voter.vote.items())!=1: # 1P1V
                print('Incorrect number of votes:', voter.vote.items())
                continue
            for candidate, vote in voter.vote.items(): # trivial i.e. one item loop
                assert vote==0 or vote==1
                self.tally[candidate] = self.tally[candidate]+vote
        favorite = [*list(self.tally.items())[0]]
        for candidate, votes in self.tally.items():
            if votes>favorite[1]: favorite = [candidate, votes]
        self.winner = favorite[0]