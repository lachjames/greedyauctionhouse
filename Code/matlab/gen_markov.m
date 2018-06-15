function [Q, N] = gen_markov(n_states, alpha, pr)

n = n_states + 1

P = zeros(n, n);

% First alpha+1 columns always do giveback phase
for i=1:alpha
    P(i, i+1) = 1;
end

for i=alpha+1:n_states
    P(i, i+1) = 1 - pr;
    P(i, i - alpha) = pr;
end

P(n, n) = 1;

Q = P(1:n_states, 1:n_states);

N = inv(eye(n_states) - Q);