import sympy

x, y, z, t = sympy.symbols('x y z t')

syms = [x, y, z, t]

################## HARMONIC / LAPLACIAN ##################

def laplacian(func):
    f = 0

    for sym in syms:
        f += sympy.diff(func, sym, 2)

    return f

################## Homogeneous ##################

'''
    Given a degree, give back all possible degrees for each symbol that together sum to the degree.
    Used to generate all possible candidate terms for a homogeneous function
    
    Example, degree = 2 for three symbols
    [
        [0, 0, 2],
        [0, 1, 1],
        [0, 2, 0],
        [1, 0, 1],
        [1, 1, 0],
        [2, 0, 0]
    ]
'''
def generateExponentSets(numSymbols: int, degree: int):
    def generateExponentSetsHelper(degree: int, symIndex: int, buildingSet: [int]):
        if symIndex == 0:
            buildingSet.append(degree)
            return [buildingSet]

        sets = []

        for d in range(degree + 1):
            temp = buildingSet.copy()
            temp.append(d)
            for s in generateExponentSetsHelper(degree - d, symIndex - 1, temp):
                sets.append(s)

        return sets

    return generateExponentSetsHelper(degree, numSymbols - 1, [])

'''
    From the generated exponent sets, this will create all of the terms.
    A term is each symbol raised to the corresponding power in the exponent set.
    
    For 3 symbols (x, y, z) and a degree of 2, this is the output:
    [z**2, y*z, y**2, x*z, x*y, x**2]
'''
def generateHomogeneousTerms(syms, degree):
    termExponents = generateExponentSets(len(syms), degree)
    terms = []

    for exponents in termExponents:
        term = 1
        for i in range(len(exponents)):
            term *= syms[i]**exponents[i]
        terms.append(term)
    return terms

def generateLatexMatrix(syms, diffFunction, degree):
    terms = generateHomogeneousTerms(syms, degree)
    applied = [diffFunction(t) for t in terms]

    print("Latex String:")
    print("\\begin{pmatrix}")
    for i in range(0, len(terms) - 1):
        print(sympy.latex(terms[i]) + " & " + sympy.latex(applied[i]) + "\\\\")
    print(sympy.latex(terms[-1]) + " & " + sympy.latex(applied[-1]))
    print("\\end{pmatrix}")


def findUniqueSolutions(syms, diffFunction, degree):
    terms = generateHomogeneousTerms(syms, degree)
    applied = [diffFunction(t) for t in terms]

    # for every applied function term, if it is adding two terms separate the constants from each term. If not adding, then manually pull out that constant in the term and put into list
    # constant_separated_terms = [[b.as_independent(*syms) for b in a.args] if a.func == sympy.core.add.Add else [a.as_independent(*syms)] for a in applied]

    constant_separated_terms = []
    for a in applied:
        if a.func == sympy.core.add.Add:
            for b in a.as_ordered_terms():
                constant_separated_terms.append(b.as_independent(*syms))
        else:
            constant_separated_terms.append(a.as_independent(*syms))

    groups = {}

    term_index = 0
    for a in applied:
        if a.func == sympy.core.add.Add:
            for i in range(len(a.as_ordered_terms())):
                for j in range(len(a.as_ordered_terms())):
                    if i != j:
                        if i + term_index not in groups:
                            groups[i + term_index] = [j + term_index]
                        else:
                            groups[i + term_index].append(j + term_index)

            term_index += len(a.as_ordered_terms())

        else:
            term_index += 1

            # for term in a.args:
            #     separated = term.as_independent(*syms)
            #     all_terms.append(separated)
            #
            #     term_index += 1

    # go through and find what has like terms
    toLikeTerms = {}

    for i in range(len(constant_separated_terms)):
        for j in range(i + 1, len(constant_separated_terms)):
            if constant_separated_terms[i][1] == constant_separated_terms[j][1]:
                if i not in toLikeTerms:
                    toLikeTerms[i] = [j]
                else:
                    toLikeTerms[i].append(j)

                if j not in toLikeTerms:
                    toLikeTerms[j] = [i]
                else:
                    toLikeTerms[j].append(i)

    print(groups)
    print(terms)
    print(applied)
    print(constant_separated_terms)
    print(toLikeTerms)

    for key, value in toLikeTerms.items():
        for v in value:
                print(key, v)

    for key, value in groups.items():
        for v in value:
                print(key, v)

    '''
        For each term applied with the function, go through the rest of the generated terms and see what has like terms.
        We need this information in order to determine how to cancel the terms when finding unique solutions.
        
        Start at the first, and for each term in that polynomial, search the rest of the polynomials to see if like terms exist
        Write down what indecies have what common terms.
    '''
    # for i in range(len(applied)):
    #     for search_term in constant_separated_terms[i]:
    #         for j in range(i + 1, len(applied)):
    #             for temp_term in constant_separated_terms[j]:
    #                 if temp_term[1] == search_term[1]:
    #                     if i not in toLikeTerms:
    #                         toLikeTerms[i] = [j]
    #                     else:
    #                         toLikeTerms[i].append(j)
    #
    #                     if j not in toLikeTerms:
    #                         toLikeTerms[j] = [i]
    #                     else:
    #                         toLikeTerms[j].append(i)
    #
    # print(constant_separated_terms)
    # print(toLikeTerms)
    #
    # for key, value in toLikeTerms.items():
    #     for v in value:
    #         print(key, v)

if __name__ == '__main__':
    # f = x**2*2 + y**3 + y*z**3
    #
    # print(f.as_ordered_terms())
    # print([a.as_independent(*syms) for a in f.args])

    # print(generateExponentSets(3, 2))
    # print(generateHomogeneousTerms(syms, 2))
    #
    # print(sympy.latex(generateHomogeneousTerms(syms, 2)[0]))
    # generateLatexMatrix(syms, laplacian, 6)
    findUniqueSolutions(syms, laplacian, 6)