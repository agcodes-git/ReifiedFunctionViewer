# CS423: Project 3
# Andre' Green
import functions as f
import matplotlib.pyplot as plt

K = 4
r = 3

NUM_RULES = 2**(2**r)
NUM_INPUTS = 2**K

# Each mapping maps one k-bit string to another.
mappings = []

# Construct the unary mappings between all K-bit strings for each r-bit to 1-bit rule.
for rule_number in range(NUM_RULES):

    mapping = [-1 for x in range(0,NUM_INPUTS)]
    rule_bitstring = f.n2s(rule_number,2, 2**r)

    for input_number in range(NUM_INPUTS):
        input_bitstring = f.n2s(input_number, 2, K)
        next_bitstring = f.step(input_bitstring, rule_bitstring)
        mapping[f.bin_to_num(input_bitstring)] = f.bin_to_num(next_bitstring)

    mappings.append( mapping )

colors = f.get_cmap(NUM_INPUTS, 'nipy_spectral')
# Graph the unary functions for each k-bit string.
rule = 83
for x in range(len(mappings[rule])):
    repeated_composition = []
    for t in range(NUM_INPUTS): # The maximum-length cycle of the unary function is the number of inputs.
        if len(repeated_composition) == 0: repeated_composition.append(x)
        else: repeated_composition.append(mappings[rule][repeated_composition[len(repeated_composition)-1]])

    plt.plot(range(NUM_INPUTS), repeated_composition, color=colors(x), linewidth=1)
    plt.xlabel("# of times CA applied", fontsize=14)
    plt.ylabel("K-bit string's corresponding decimal #", fontsize=14)
    plt.title(("Rule "+str(rule)+" ("+f.n2s(rule,2,2**r)+")"),  fontsize=16 )
    plt.yticks(range(0,2**K))
    plt.xticks(range(0,2**K))
    plt.grid(color='#d8dcd6', linestyle='-', linewidth=0.5)

plt.show()