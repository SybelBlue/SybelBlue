import random

# range bound
k = 10

# team sizes
n = 10
m = 7


def preprocess(t0, t1):
    def freq_list(t):
        out = [0] * k
        for height in t:
            out[height] += 1
        return out

    freq0 = freq_list(t0)
    freq1 = freq_list(t1)

    team0_val = [0] * k
    team1_val = [0] * k
    team_last = [0, 0]

    for i in range(k):
        team_last[0] += freq0[i]
        team_last[1] += freq1[i]

        team0_val[i] += team_last[0]
        team1_val[i] += team_last[1]

    return team0_val, team1_val


def evaluate(team_vals, a, b):
    def player_count(team_number):
        team = team_vals[team_number]
        top = min(k - 1, b)

        if a == 0:
            lower = 0
        else:
            # in order to include players
            # of height a
            lower = team[a - 1]

        return team[top] - lower

    return player_count(0), player_count(1)


if __name__ == '__main__':
    def build_team(size):
        return [random.randint(0, k - 1) for _ in range(size)]

    teams = build_team(m), build_team(n)
    team_vals = preprocess(teams[0], teams[1])
    print(teams)
    print(team_vals)

    a, b = 0, 0
    while a >= 0 and b >= 0:
        a = int(input(":"))
        b = int(input(":"))

        eval = evaluate(team_vals, a, b)
        print(eval)
        print(eval[0] >= eval[1])
