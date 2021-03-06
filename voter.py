import numpy as np
import copy

class Voter():
    def __init__(self, ideology=None, utilities=None, beliefs=None, **kwargs):
        '''
        Params
        ideology: np array, defines the voters location in n-dimensional ideology vector space
        policy: dict str to object, defines the voter's policy under electoral systems
        utility: None or dict str to float, defines the voter's utility gained from electoral outcomes
        beliefs: not implemented, for strategic voting purposes
        '''
        self.utilities = utilities
        self.beliefs = beliefs
        self.ideology = ideology

        self.vote = dict() # List for IRV
    
    def generate_utilities(self, candidate_ideologies):
        raise NotImplementedError
    
    def compute_vote(self, electoral_system):
        self.vote = dict()
        if electoral_system=='ApprovalVote': self.approval_policy()
        elif electoral_system=='PluralityVote': self.plurality_policy()
        elif electoral_system=='InstantRunoffVote': self.irv_policy()
        elif electoral_system=='QuadraticVote': self.quadratic_policy()
        elif electoral_system=='RankedPairsVote': self.rp_policy()

    def approval_policy(self,):
        raise NotImplementedError
    def plurality_policy(self,):
        raise NotImplementedError
    def irv_policy(self,):
        raise NotImplementedError
    def quadratic_policy(self,):
        raise NotImplementedError
    def rp_policy(self,):
        raise NotImplementedError

class Honest_Voter(Voter):
    '''
    Voter class modelling self-interested voters without strategic/manipulative voting.
    For some electoral systems the honest voter class is non-unique in which case an arg may be passed to specify the desired behavior.

    Args:
    approval_rule: str in ['median', 'mean'], Voter will approval vote for all candidates above their median, or mean utility respectively.
    '''

    def __init__(self, approval_rule='mean', ideology=None, utilities=None, beliefs=None, **kwargs):
        super().__init__(ideology=ideology, utilities=utilities, beliefs=beliefs, **kwargs)
        self.approval_rule = approval_rule

    def approval_policy(self,):
        if self.approval_rule == 'median':
            utility_threshold = np.median(list(self.utilities.values()))
        elif self.approval_rule == 'mean':
            utility_threshold = np.mean(list(self.utilities.values()))
        else:
            raise NotImplementedError
        votes = {candidate:0 for candidate in self.utilities.keys()}
        for candidate, utility in self.utilities.items():
            if utility>=utility_threshold: votes[candidate]=1
        self.vote = votes
        return self.vote

    def plurality_policy(self):
        favorite_candidate = max(self.utilities.items(), key=lambda x:x[1])[0]
        self.vote[favorite_candidate] = 1
        return self.vote
    
    def irv_policy(self,):
        sorted_candidates = sorted(list(self.utilities.items()), key=lambda x:x[1])
        self.vote = [pair[0] for pair in sorted_candidates]
        return self.vote

    def rp_policy(self,):
        sorted_candidates = sorted(list(self.utilities.items()), key=lambda x:x[1])
        self.vote = [pair[0] for pair in sorted_candidates]
        return self.vote

    def quadratic_policy(self):
        utility_list = list(self.utilities.items())
        utility_values = [pair[1] for pair in utility_list]
        utility_mean, utility_std = np.mean(utility_values), np.std(utility_values)
        self.vote = {pair[0]:(pair[1]-utility_mean)/utility_std for pair in utility_list}
        return self.vote

class Laziest_Voter(Honest_Voter):
    def approval_policy(self,):
        '''
        Only vote for one candidate
        '''
        favorite_candidate = max(self.utilities.items(), key=lambda x:x[1])[0]
        for candidate in self.utilities.keys():
            if candidate!= favorite_candidate: self.vote[candidate] = 0
        return self.vote

    def plurality_policy(self):
        return super().plurality_policy()

    def irv_policy(self):
        '''
        Swap one of the non-favorite candidates with adjacent candidate
        '''
        sorted_candidates = sorted(list(self.utilities.items()), key=lambda x:x[1])
        self.vote = [pair[0] for pair in sorted_candidates]
        swap = np.random.choice(range(1,len(self.vote)-1))
        to_swap = copy.copy(self.vote[swap])
        self.vote[swap] = self.vote[swap-1]
        self.vote[swap-1] = to_swap
        return self.vote

    def quadratic_policy(self):
        '''
        Bullet vote
        '''
        utility_list = list(self.utilities.items())
        max_utility = max(utility_list, key=lambda x:x[1])[1]
        bullet_utilities = [1 if value[1]==max_utility else 0 for value in utility_list]
        utility_mean, utility_std = np.mean(bullet_utilities), np.std(bullet_utilities)
        self.vote = {pair[0]:(bullet_utilities[p]-utility_mean)/utility_std for p,pair in enumerate(utility_list)}
        return self.vote

    def rp_policy(self):
        '''
        Swap one of the non-favorite candidates with adjacent candidate
        '''
        sorted_candidates = sorted(list(self.utilities.items()), key=lambda x:x[1])
        self.vote = [pair[0] for pair in sorted_candidates]
        swap = np.random.choice(range(1,len(self.vote)-1))
        to_swap = copy.copy(self.vote[swap])
        self.vote[swap] = self.vote[swap-1]
        self.vote[swap-1] = to_swap
        return self.vote

class Lazy_Voter(Honest_Voter):
    def approval_policy(self,):
        # Vote for top two candidates regardless of num candidates
        utility_list = list(self.utilities.items())
        utility_list = sorted(utility_list, key=lambda x:x[1], reverse=True)
        votes = {candidate:0 for candidate in self.utilities.keys()}
        votes[utility_list[0][0]]=1
        votes[utility_list[1][0]]=1
        self.vote = votes
        return self.vote
    def plurality_policy(self):
        # Behave honestly here
        return super().plurality_policy()