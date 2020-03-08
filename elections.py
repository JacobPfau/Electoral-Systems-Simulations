from abc import ABC, abstractmethod
import utils

class ElectoralSystem(ABC):

    def __init__(self, voters, candidates):
        self.voters = voters
        self.candidates = candidates
        self.tally = dict()
        self.winner = None

    def compute_votes(self,):
        for voter in self.voters: _ = voter.compute_vote(self.name)

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
        self.winner = max(self.tally.items(), key=lambda x:x[1])[0]

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
        self.winner = max(self.tally.items(), key=lambda x:x[1])[0]

class InstantRunoffVote(ElectoralSystem):
    name = 'InstantRunoffVote'

    def aggregate_votes(self):
        for candidate in self.candidates: self.tally[candidate]=0

        total_votes = len(self.voters)
        losing_candidates = []
        while self.winner is None:
            for voter in self.voters:
                top_preference = voter.vote[-1]
                while top_preference in losing_candidates:
                    voter.vote.pop()
                    top_preference = voter.vote[-1]
                self.tally[top_preference]+=1

            if max(self.tally.values())>total_votes/2:
                self.winner = max(self.tally.items(), key=lambda x:x[1])[0]
            else: 
                losing_candidates.append(min(self.tally.items(), key=lambda x:x[1])[0])

class QuadraticVote(ElectoralSystem):
    name = 'QuadraticVote'

    def aggregate_votes(self):
        for candidate in self.candidates: self.tally[candidate]=0
        for voter in self.voters:
            for candidate, vote in voter.vote.items():
                self.tally[candidate] = self.tally[candidate]+vote
        self.winner = max(self.tally.items(), key=lambda x:x[1])[0]

class RankedPairsVote(ElectoralSystem):
    '''
    For a definition see for instance, https://www.aaai.org/ocs/index.php/AAAI/AAAI12/paper/download/5018/5461
    Tie-breaks have not been properly implemented
    '''
    name = 'RankedPairsVote'

    def aggregate_votes(self):
        # First tally votes
        for candidate in self.candidates:
            for other_candidate in self.candidates:
                if candidate!=other_candidate: self.tally[(candidate,other_candidate)]=0
        for voter in self.voters:
            for c,candidate in enumerate(voter.vote[::-1]):
                if c==len(voter.vote)-1: break
                for worse_candidate in voter.vote[len(voter.vote)-c-2::-1]:
                    self.tally[(candidate,worse_candidate)]+=1
        
        # Second build preference DAG
        ranked_pairs = list(self.tally.items())
        ranked_pairs = sorted(ranked_pairs, key=lambda tally_pair: tally_pair[1], reverse=True)
        ranked_pairs = [candidate_votes[0] for candidate_votes in ranked_pairs]

        self.candidate_dag = utils.NamedGraph(vertices = {candidate:utils.Vertex(name=candidate) for candidate in self.candidates})
        for p,pair in enumerate(ranked_pairs):
            pair_source, pair_target = self.candidate_dag.vertices[pair[0]], self.candidate_dag.vertices[pair[1]]
            if not utils.find_cycle([pair_source], pair_target, max_depth=p):
                self.candidate_dag.add_edge(pair_source.name, pair_target.name)
        
        # Third find a source with in-degree = 0
        for vertex in self.candidate_dag.vertices.values():
            if len(vertex.in_vertices)==0 and len(vertex.out_vertices)>0: # Second condition guarantees this candidate had some votes cast for them
                self.winner = vertex.name