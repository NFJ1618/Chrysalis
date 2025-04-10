# Test cases
from search import MetamorphicRelation, MetamorphicSearch


def test_metamorphic_search():
    identity_mr = MetamorphicRelation("identity", "numeric", lambda x: x)
    double_neg_mr = MetamorphicRelation("double_negative", "numeric", lambda x: -1 * -1 * x)
    inverse_mr = MetamorphicRelation("inverse", "numeric", lambda x: -x)
    mrs = [identity_mr, double_neg_mr, inverse_mr]
    num_tests = 5
    
    search = MetamorphicSearch(mrs, strategy="random", num_tests=num_tests)
    orderings = search.execute_search()
    assert len(orderings) == 10
    assert all(isinstance(ordering, list) for ordering in orderings)
    assert all(isinstance(mr, MetamorphicRelation) for ordering in orderings for mr in ordering)
    
    search = MetamorphicSearch([identity_mr, double_neg_mr, inverse_mr], strategy="exhaustive", num_tests=5)
    orderings = search.execute_search()
    assert(len(orderings)) == 6
    assert all(isinstance(ordering, list) for ordering in orderings)
    assert all(isinstance(mr, MetamorphicRelation) for ordering in orderings for mr in ordering)
    
    print("All tests passed.")

if __name__ == "__main__":
    test_metamorphic_search()