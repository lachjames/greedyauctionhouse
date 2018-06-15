n_states = 5
alpha = 2
pr = 0.1

[Q, N] = gen_markov(n_states, alpha, pr)

c = ones(n_states, 1)
t = N * c