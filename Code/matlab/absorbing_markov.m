clear all

n_states = 50
alpha = 3

min_pr = 0
max_pr = 1/alpha

i = 1;

for pr = min_pr:0.001:max_pr
    [Q, N] = gen_markov(n_states, alpha, pr);
    
    c = ones(n_states, 1);
    t = N * c;
    
    results(i) = t(1);
    prs(i) = pr;
    i = i + 1;
end

figure;
plot(prs, results)
xlabel("p")
ylabel("# Iterations")