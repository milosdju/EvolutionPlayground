import random

class Gene():

    """
    Initialization methods
    """
    def __init__(self, strand = None):
        # State
        self.__strand = strand

        # Strategy
        self.__creation_strategy = None
        #self.__crossover_strategy = None
        self.__mutation_strategy = None
        self.__encoding_strategy = None
        self.__decoding_strategy = None

        self.__mutation_prob = None

    """ Create strand following creation strategy"""
    def create(self, **kwargs):
        # Primary check
        if self.__creation_strategy is None:
            raise Exception("Gene can not be created. Creation strategy is not set")
        
        strand = self.__creation_strategy(**kwargs)
        # Check returned strand type
        if not isinstance(strand, str):
             raise Exception("Returned strand type must be string")
        
        self.__strand = strand

    """
    Converting methods
    """
    """ Encode phenotype into genotype (i.e strand) following encoding strategy"""
    def encode(self, phenotype):
        # Primary check
        if self.__encoding_strategy is None:
            raise Exception("Gene can not be encoded. Encoding strategy is not set")
        if phenotype is None:
            raise Exception("Phenotype must be passed")
        return self.__encoding_strategy(phenotype = phenotype)

    """ Decode strand into phenotype following decoding strategy"""
    def decode(self, strand = None):
        # Primary check
        if self.__decoding_strategy is None:
            raise Exception("Gene can not be decoded. Decoding strategy is not set")
        
        # Default strand value
        if strand is None:
            strand = self.__strand
        return self.__decoding_strategy(strand = strand)

    """
    Manipulating gene methods
    """
    """ Return: sliced strand """
    def slice(self, start, end):
        # Primary checks
        if start < 0 or end < start or end > len(self.__strand):
            raise Exception("Invalid range")

        return self.__strand[start : end]

    """ Replace certain part of strand """
    def replace(self, start, end, new_part):
        # Primary checks
        if start < 0 or end < start or end > len(self.__strand):
            raise Exception("Invalid range")

        strand_list = list(self.__strand)
        strand_list[start : end] = new_part
        self.__strand = ''.join(strand_list)

    """ Make crossover with other gene """
    def crossover(self, other_gene, pattern):
        # Primary checks
        if not isinstance(other_gene, Gene):
            raise Exception("Second gene must be Gene instance")
        if not isinstance(pattern, list):
            raise Exception("'Crossover pattern' must be an array")
        if not all(isinstance(num, int) for num in pattern):
            raise Exception("All 'crossover pattern' elements must be integers")
        if sum(pattern) != len(self.strand()) or sum(pattern) != len(other_gene.strand()):
            raise Exception("'Crossover pattern' must be the same length as two genes")
        
        # Return result
        pos = 0
        for idx, part_len in enumerate(pattern):
            if (idx % 2 == 1):
                temp_part = self.slice(pos, pos + part_len)
                self.replace(pos, pos + part_len, other_gene.slice(pos, pos + part_len))
                other_gene.replace(pos, pos + part_len, temp_part)
            pos += part_len

    """ Mutate gene following mutation strategy on mutation rate """
    def mutate(self):
        if random.random() < self.__mutation_prob:
            mutated_strand = self.__mutation_strategy(self.__strand)
            self.__strand = mutated_strand

    """
    Getters & Setters
    """
    def strand(self, strand = None):
        if strand is None:
            return self.__strand
        else:
            self.__strand = strand

    def creation_strategy(self, creation_strategy = None):
        if creation_strategy is None:
            return self.__creation_strategy
        else:
            # Type check
            if not callable(creation_strategy):
                raise Exception("Creation strategy must be function. \
                Hint: Pass it without parenthesis")
            self.__creation_strategy = creation_strategy

    def mutation_strategy(self, mutation_strategy = None, mutation_prob = None):
        if mutation_strategy is None:
            return (self.__mutation_strategy, self.__mutation_prob)
        else:
            # Type checks
            if not callable(mutation_strategy):
                raise Exception("Mutation strategy must be function. \
                Hint: Pass it without parenthesis")
            if not (mutation_prob, float) or mutation_prob < 0 or mutation_prob > 1:
                raise Exception("Mutation probability must be float [0..1]")
            self.__mutation_strategy = mutation_strategy
            self.__mutation_prob = mutation_prob

    def encoding_strategy(self, encoding_strategy = None):
        if encoding_strategy is None:
            return self.__encoding_strategy
        else:
            # Type check
            if not callable(encoding_strategy):
                raise Exception("Encoding strategy must be function. \
                Hint: Pass it without parenthesis")

            self.__encoding_strategy = encoding_strategy

    def decoding_strategy(self, decoding_strategy = None):
        if decoding_strategy is None:
            return self.__decoding_strategy
        else:
            # Type check
            if not callable(decoding_strategy):
                raise Exception("Decoding strategy must be function. \
                Hint: Pass it without parenthesis")
            self.__decoding_strategy = decoding_strategy
