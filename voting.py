from abc import ABC, abstractmethod

class ElectoralSystem(ABC):

    def __init__(self, voters, candidates):
        self.voters = voters
        self.candidates = candidates
        self.tally = dict()

    def compute_votes(self,):
        for voter in self.voters: voter.get_vote()

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

    def aggregate_votes(self,):
        for candidate in self.candidates: self.tally[candidate]=0

        for voter in self.voters:
            for candidate, vote in voter.vote.items():
                self.tally[candidate] = self.tally[candidate]+vote
        favorite = [*list(self.tally.items())[0]]
        for candidate, votes in self.tally.items():
            if votes>favorite[1]: favorite = [candidate, votes]
        self.winner = favorite[0]