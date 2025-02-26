import itertools
import random
from typing import List, Callable, Dict, Any, Union, Set


class MetamorphicRelation:
    """
    Not the actual class, but a standin
    """
    def __init__(self, name: str, relation_type: str, transformation: Callable[[Any], Any]):
        self.name = name
        self.relation_type = relation_type
        self.transformation = transformation
    
    def apply(self, data: Any) -> Any:
        return self.transformation(data)
    
    def __eq__(self, value):
        return self.name == value.name
    
    def __hash__(self):
        return hash(str(self.name))
    
    def __repr__(self):
        return self.name

def check_compatibility(mr1: MetamorphicRelation, mr2: MetamorphicRelation) -> bool:
    """
    Determines if two MRs are compatible based on their relation types.
    """
    # Temporary implementation, heavily depends on a few design choices, and order definitely matters
    return mr1.relation_type == mr2.relation_type
    

class MetamorphicSearch:
    """
    Performs search over the relation space
    """
    def __init__(self, mrs: List[MetamorphicRelation], strategy: str = "random", num_tests: int = 10):
        self.mrs = mrs
        self.strategy = strategy
        self.num_tests = num_tests
        self.possible_next_relations = MetamorphicSearch.get_next_relations(self.mrs)
    
    def get_next_relations(
        mrs: List[MetamorphicRelation]
        ) -> Dict[MetamorphicRelation, Set[MetamorphicRelation]]:
        possible_next_relations = {}
        for mr1 in mrs:
            if mr1 not in possible_next_relations:
                possible_next_relations[mr1] = set()
            for mr2 in mrs:
                if mr1 != mr2 and check_compatibility(mr1, mr2):
                    possible_next_relations[mr1].add(mr2)
        return possible_next_relations


    def exhaustive_search(self, 
                          starting_relation: MetamorphicRelation, 
                          orderings: List[List[MetamorphicRelation]]= None,
                          current_path: List[MetamorphicRelation] = None,
                          used_relations: Set[MetamorphicRelation] = None
                          ) -> List[List[MetamorphicRelation]]:
        if current_path is None:
            current_path = []
        if used_relations is None:
            used_relations = set()
        if orderings is None:
            orderings = []
            
        current_path.append(starting_relation)
        used_relations.add(starting_relation)
        
        unused_and_possible_relations = self.possible_next_relations[starting_relation].difference(used_relations)
        
        if len(unused_and_possible_relations) == 0:
            orderings.append(list(current_path))
        
        for mr in unused_and_possible_relations:
            self.exhaustive_search(mr, orderings, current_path, used_relations)
            
        current_path.pop()
        used_relations.remove(starting_relation)
        return
        

    def generate_orderings(self,
        mrs: List[MetamorphicRelation], 
        strategy: str, 
        num_tests: int
        ) -> List[List[MetamorphicRelation]]:
        """
        Generates sets of orderings for metamorphic relations based on a given search strategy.
        """
        if strategy == "random":
            start = random.choices(mrs, k=num_tests)
        
        elif strategy == "exhaustive":
            start = list(mrs)
        
        elif strategy == "dynamic":
            """Dynamically selects relations based on compatibility and previous results."""
            raise NotImplementedError()
        
        else:
            raise ValueError("Unknown search strategy")
        
        orderings = []
        for mr in start:
            self.exhaustive_search(mr, orderings)
        return orderings
        
        
    
    def execute_search(self) -> List[List[MetamorphicRelation]]:
        """
        Runs the search strategy and returns the selected orderings of relations.
        """
        return self.generate_orderings(self.mrs, self.strategy, self.num_tests)
