import voter
import voting

def all_in(voter, electoral_system):
    if electoral_system.__name__=='ApprovalVote':
        favorite = [*voter.utilities.items()[0]]
        for candidate, utility in voter.utilities.items():
            if utility>favorite[1]: favorite = [candidate, utility]
        votes = {candidate:0 if candidate!= favorite[0] else 1 for candidate in voter.utilities.keys()}
        return votes

def top_2(voter, electoral_system):
    if electoral_system.__name__=='ApprovalVote':
        utility_list = list(voter.utilities.items())
        utility_list = sorted(utility_list, key=lambda x:x[1], reverse=True)
        votes = {candidate:0 for candidate in voter.utilities.keys()}
        votes[utility_list[0][0]]=1
        votes[utility_list[1][0]]=1
        return votes


def main():
    candidates = ['a', 'b', 'c', 'd']
    utilities_lexico = {candidate:4-c for c,candidate in enumerate(candidates)}
    utilities_inverse_lexico = {candidate:c for c,candidate in enumerate(candidates)}
    voters = []
    voters.append(voter.Voter(all_in, utilities_lexico))
    voters.append(voter.Voter(all_in, utilities_lexico))

    vote = voting.ApprovalVote(voters, candidates)
    vote.aggregate_votes()
    print(vote.winner)
    vote.get_regret()
    print(vote.regret)

if __name__=="__main__":
    main() 