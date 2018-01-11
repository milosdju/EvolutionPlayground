""" 
Here are included unit tests of some more important features
"""

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from Gene import Gene
    else:
        from ..Gene import Gene

""" Initialize Gene """
gene = Gene()

""" Test CREATION of Gene """
import random
random.seed(5)
def creation_strategy(strand_len):
    strand = ''
    for i in range(strand_len):
        strand += str(random.randint(0,1))
    return strand

gene.creation_strategy(creation_strategy)
gene.create(strand_len = 8)
print("Strand: %s" % gene.strand())
assert isinstance(gene.strand(), str), "Created strand must be string"
assert gene.strand() == "11010000", "Strand has invalid value" 

""" Test ENCODING to strand """
def encoding_strategy(phenotype):
    return bin(phenotype)[2:]
gene.encoding_strategy(encoding_strategy)
phenotype_param = 255
encoded_strand = gene.encode(phenotype = phenotype_param)
print("Encoded strand: %s" % encoded_strand)
assert encoded_strand == "11111111", "Encoded strand is invalid"

""" Test DECODING to phenotype """
def decoding_strategy(strand):
    return int(strand, 2)
gene.decoding_strategy(decoding_strategy)
decoded_phenotype = gene.decode(strand = "1110011")
print("Decoded phenotype: %d" % decoded_phenotype)
assert decoded_phenotype == 115, "Decoded phenotype is invalid"

""" Test SLICING strand """
sliced_strand = gene.slice(2,5)
print("Sliced strand: %s" % sliced_strand)
assert sliced_strand == "010", "Sliced strand is invalid"

""" Test REPLACING part of strand """
new_part = "101"
gene.replace(2, 5, new_part)
print("Replaced part of strand: %s" % new_part)
assert gene.strand() == "11101000", "Replaced part of strand is invalid"

""" Test CROSSOVER technique """
other_gene = Gene("10010011")
print("First strand before crossover: %s" % gene.strand())
print("Second strand before crossover: %s" % other_gene.strand())
gene.crossover(other_gene, [3,2,3])
print("First strand after crossover: %s" % gene.strand())
print("Second strand after crossover: %s" % other_gene.strand())
assert gene.strand() == "11110000", "First strand is invalid"
assert other_gene.strand() == "10001011", "Second strand is invalid"

""" Test MUTATION technique """
def mutation_strategy(strand):
    rand_pos = random.randint(0, len(strand))
    flipped = str(1 - int(strand[rand_pos]))
    strand_list = list(strand)
    strand_list[rand_pos] = flipped
    return ''.join(strand_list)
# 0% chance for mutation
gene.mutation_strategy(mutation_strategy, 0)
gene.mutate()
print("Strand after 0%% chance for mutation: %s" % gene.strand())
assert gene.strand() == "11110000", "Gene should not be mutated"
# 100% chance for mutation
gene.mutation_strategy(mutation_strategy, 1)
gene.mutate()
print("Strand after 100%% chance for mutation: %s" % gene.strand())
assert gene.strand() == "11110010", "Gene should be mutated"
