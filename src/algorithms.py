import DFA
from typing import List, Tuple
import copy
import itertools

def run(dfa: DFA, word: str, verbose : bool = False) -> bool:
    """
    Runs the specified DFA on a word and returns True if the word is
        accepted.

    :param dfa: the DFA to be executed.
    :type dfa: DFA
    :param word: the word to be tested.
    :type word: str
    :param verbose: if True, more information are displayed about the
            execution, defaults to False
    :type verbose: bool, optional
    :return: True if the word is accepted, False otherwise.
    :rtype: bool
    """
    if dfa.init == None:
        print("error : the automaton does not have any initial symbol.")
        return False

    current_state = dfa.init

    i = 0
    for symbol in word:
        if verbose : print("configuration : (" + current_state + ", " + word[i:] + ")")
        if not dfa.valid_symbol(symbol):
            print("error : the symbol '" + symbol + "' is not part of the alphabet. Abord.")

        next_state = dfa.dst_state(current_state, symbol)
        if next_state is None:
            if verbose: print("no transition available for (" + current_state + ", " + symbol + ").")
            return False;

        current_state = next_state
        i = i+1

    if current_state in dfa.finals:
        if verbose: print("ending on final state '" + current_state + "'.")
        return True
    if verbose: print("ending on non accepting state '" + current_state + "'")
    return False

def successors(dfa: DFA, state: str) -> List[str]:    
    """ 
    Returns the list of the successors of the specified state in the DFA.

    :param dfa: the considered automaton.
    :type dfa: DFA
    :param state: the considered state.
    :type state: str
    :return: the list of the successors of the state.
    :rtype: List[str]
    """
    if state not in dfa.states:
        print("error : the specified state '" + state + "' is not part of the automaton.")
        return

    ret = []
    for (symbol, dst_state) in dfa.transitions[state]:
        if dst_state not in ret:
            ret.append(dst_state)

    return ret

def predecessors(dfa: DFA, state: str) -> List[str]:    
    """ 
    Returns the list of the predecessors of the specified state in the DFA.

    :param dfa: the considered automaton.
    :type dfa: DFA
    :param state: the considered state.
    :type state: str
    :return: the list of the predecessors of the state.
    :rtype: List[str]
    """
    if state not in dfa.states:
        print("error : the specified state '" + state + "' is not part of the automaton.")
        return

    ret = []
    for src_state in dfa.states:
        for (symbol, dst_state) in dfa.transitions[src_state]:
            if dst_state == state and src_state not in ret:
                ret.append(src_state)

    return ret

def is_complete(dfa: DFA) -> bool:
    """
    Returns True if the automaton is complete, False otherwise.

    :param dfa: the automaton to test.
    :type dfa: DFA
    :return: a boolean corresponding to the completion of the automaton.
    :rtype: bool
    """
    for state in dfa.states:
        for symbol in dfa.alphabet:
            if dfa.dst_state(state, symbol) == None:
                return False
    return True

def complete(dfa: DFA) -> DFA:
    """
    Completes the specified automaton.

    :param dfa: the automaton to complete.
    :type dfa: DFA
    :return: the automaton.
    :rtype: DFA
    """
    if is_complete(dfa): return
    # Find a name for Qp
    qp = "Qp"
    i = 0
    while qp in dfa.states:
        qp = "Qp" + str(i)
        i += 1

    # Complete
    dfa.add_state(qp)
    for state in dfa.states:
        for symbol in dfa.alphabet:
            if dfa.dst_state(state, symbol) == None:
                dfa.add_transition(state, symbol, qp)

    return dfa

def accessible_states(dfa: DFA) -> List[str]:
    """ 
    Returns the list of all accessible states in the specified automaton.

    :param dfa: the automaton considered.
    :type dfa: DFA
    :return: the list of the accessible states.
    :rtype: List[str]
    """
    visited = []
    to_visit = [dfa.init]

    while len(to_visit) > 0:
        state = to_visit.pop()
        visited.append(state)
        for succ in successors(dfa, state):
            if succ not in visited and succ not in to_visit:
                to_visit.append(succ)

    return visited

def accessible(dfa: DFA, state: str) -> bool:
    """ 
    Returns True if the specified state is accessible in the automaton, returns
        False otherwise.

    :param dfa: the considered automaton.
    :type dfa: DFA
    :param state: the state to be tested.
    :type state: str
    :return: True if the state is accessible, False otherwise.
    :rtype: bool
    """
    if state not in dfa.states:
        print("error : the state '" + state + "' is not part of the automaton.")
        return

    return state in accessible_states(dfa)

def accessible(dfa: DFA) -> bool:
    """
    Returns True if the specified DFA is accessible (if all it's states are,
     accessible), False otherwise.

    :param dfa: the considered automaton.
    :type dfa: DFA
    :return: True if the DFA is accessible, False otherwise.
    :rtype: bool
    """
    return len(dfa.states) == len(accessible_states(dfa))

def coaccessible_states(dfa: DFA) -> List[str]:
    """ 
    Returns the list of all coaccessible states in the specified automaton.

    :param dfa: the automaton considered.
    :type dfa: DFA
    :return: the list of the coaccessible states.
    :rtype: List[str]
    """
    visited = []
    to_visit = dfa.finals.copy()

    while len(to_visit) > 0:
        state = to_visit.pop()
        visited.append(state)
        for pred in predecessors(dfa, state):
            if pred not in visited and pred not in to_visit:
                to_visit.append(pred)

    return visited

def coaccessible(dfa: DFA, state: str) -> bool:
    """ 
    Returns True if the specified state is coaccessible in the automaton, returns
        False otherwise.

    :param dfa: the considered automaton.
    :type dfa: DFA
    :param state: the state to be tested.
    :type state: str
    :return: True if the state is coaccessible, False otherwise.
    :rtype: bool
    """
    if state not in dfa.states:
        print("error : the state '" + state + "' is not part of the automaton.")
        return

    return state in coaccessible_states(dfa)

def coaccessible(dfa: DFA) -> bool:
    """
    Returns True if the specified DFA is coaccessible (if all it's states are,
     coaccessible), False otherwise.

    :param dfa: the considered automaton.
    :type dfa: DFA
    :return: True if the DFA is coaccessible, False otherwise.
    :rtype: bool
    """
    return len(dfa.states) == len(coaccessible_states(dfa))

def trim(dfa: DFA) -> bool:
    """
    Returns True if the specified automaton is trim (accessible and coaccessible),
     False otherwise.

    :param dfa: the considered automaton.
    :type dfa: DFA
    :return: True is the DFA is trim, False otherwise.
    :rtype: bool
    """
    return accessible(dfa) and coaccessible(dfa)

def negate(dfa: DFA) -> DFA:
    """ Negates the specfied automaton, which now recognizes the complementary
        language of the original DFA.
        @param dfa the input automaton.
        @returns the modified DFA."""
    if not is_complete(dfa):
        print("error : negation requires a complete DFA.")
        return None
    oldfinals = dfa.finals.copy()
    dfa.finals.clear()

    for state in dfa.states:
        if state not in oldfinals:
            dfa.finals.append(state)

    return dfa

def product(dfa1: DFA, dfa2: DFA) -> DFA:
    """
    Returns a new automaton which is the product of the two specified DFAs.

    :param dfa1: the first operand of the product.
    :type dfa1: DFA
    :param dfa2: the second operand of the product.
    :type dfa2: DFA
    :return: the product of the two DFAs.
    :rtype: DFA
    """
    
    
    alphabet = set.union(set(list(dfa1.alphabet)), set(list(dfa2.alphabet)))
    ret = DFA.DFA(alphabet)
    to_visit = []

    def get_superstate(state1: str, state2: str) -> str:
        """
         Returns the superstate corresponding to the specified states and add it
        to the product DFA if it doesn't exist.

        :param state1: state in DFA1.
        :type state1: str
        :param state2: state in DFA2.
        :type state2: str
        :return: the corresponding superstate.
        :rtype: str
        """
        sstate = "{" + state1 + "," + state2 + "}"

        if sstate not in ret.states:
            is_final = state1 in dfa1.finals and state2 in dfa2.finals
            ret.add_state(sstate, is_final)
            to_visit.append((sstate, state1, state2))

        return sstate

    ret.init = get_superstate(dfa1.init, dfa2.init) # Add init state.

    while len(to_visit) > 0:
        (sstate, state1, state2) = to_visit.pop()

        # Add transitions.
        for symbol in ret.alphabet:
            dst_state1 = dfa1.dst_state(state1, symbol)
            dst_state2 = dfa2.dst_state(state2, symbol)

            if dst_state1 is None or dst_state2 is None:
                continue

            dst_sstate = get_superstate(dst_state1, dst_state2)

            ret.add_transition(sstate, symbol, dst_sstate)

    return ret

def distinguish(dfa: DFA, partitions: List[List[str]], partition: List[str]) -> List[List[str]]:
    """
    Try to distinguish a state partition, returning the new partition generated by the step.

    :param dfa: the DFA containing the states.
    :type dfa: DFA
    :param partitions: the list of state partitions.
    :type partitions: List[List[str]]
    :param partition: the partitions to be distinguished.
    :type partition: List[str]
    :return: the list of new
    :rtype: List[List[str]]
    """
    new_partitions = dict()

    def partition_index(state: str) -> int:
        """
        Returns the partition id (in the partition list) for the specified state.

        :param state: the state
        :type state: str
        :return: the index of the partition of the state
        :rtype: int
        """
        id = 0
        for partition in partitions:
            if state in partition:
                return id
            id = id + 1
        return -1        

    def dst_partition(state: str, symbol: str) -> int:
        """
        Returns the index of the partition targeted by the transition for the specified state and symbol.

        :param state: the source state. 
        :type state: str
        :param symbol: the symbol of the transition.
        :type symbol: str
        :return: the index of the targeted partition.
        :rtype: int
        """
        dst = dfa.dst_state(state, symbol)
        return partition_index(dst)
    
    for state in partition:
        coloration = []
        for symbol in dfa.alphabet:
            pid = dst_partition(state, symbol)
            coloration.append(pid)
        
        coloration = tuple(coloration)
        if coloration in new_partitions:
            new_partitions[coloration].append(state)
        else:
            new_partitions[coloration] = [state]

    return list(new_partitions.values())

def equivalent_states(dfa: DFA) -> List[List[str]]:
    """
     Returns a list containing each group of equivalent states.

    :param dfa: the DFA to search for equivalent states.
    :type dfa: DFA
    :return: a list of equivalent states lists.
    :rtype: List[List[str]]
    """

    # Spread finals and non-final states.
    partitions : List[List[str]] = [[], []]
    for state in dfa.states:
        if state in dfa.finals:
            partitions[0].append(state)
        else:
            partitions[1].append(state)

    changes = True # Determines if a change occured between two generations.

    step_counter = 0
    while changes:
        #print(f"step {step_counter}")

        n_p = []
        for part in partitions:
            part_d = distinguish(dfa, partitions, part)
            #print(f"part = [{','.join(part)}] n_p: [{','.join(list(itertools.chain.from_iterable(part_d)))}]")
            n_p.extend(part_d)
        
        if len(n_p) == len(partitions):
            changes = False

        partitions = n_p 
        #print(f"ended step {step_counter} : \n")
        #for part in partitions:
            #print(f"   - {part}")

        step_counter = step_counter + 1

    return partitions

def minimize(dfa: DFA) -> DFA:
    """
    Minimizes the specified automaton (returns a copy).

    :param dfa: the DFA to be minimized.
    :type dfa: DFA
    :return: the minimized DFA.
    :rtype: DFA
    """

    if len(dfa.states) < 2:
        return copy.deepcopy(dfa) # sure ? 
    
    ret = DFA.DFA(dfa.alphabet)
    eq_states = equivalent_states(dfa)

    def group_of(state: str) -> List[str]:
        """
        Returns the state group corresponding to the specified state.

        :param state: the state.
        :type state: str
        :return: the corresponding state group.
        :rtype: List[str]
        """
        for state_group in eq_states:
            if state in state_group:
                return state_group
        return None

    to_visit = [] # List of pair (super_state, state_group)

    def get_superstate(state_group: List[str]) -> str:
        """
        Returns the superstate corresponding to the specified state_group.
        If the superstate doesn't exists in the ret DFA, add it and add the pair (super_state, state_group) to the list of pair to visit.

        :param state_group: the group of state (partition) to be merged in a superstate.
        :type state_group: List[str]
        :return: the superstate corresponding to the partition.
        :rtype: str
        """
        sstate = "{" + ",".join(state_group) + "}"

        if sstate not in ret.states:
            is_final =  state_group[0] in dfa.finals # If one is final, all are final.
            ret.add_state(sstate, is_final)
            to_visit.append((sstate, state_group)) # remember relation

        return sstate
    

    # Construct minimal automaton
    ret.init = get_superstate(group_of(dfa.init)) # Add init state.

    while len(to_visit) > 0:
        #print("constructing: " + str(ret))
        (sstate, sg) = to_visit.pop()

        # Add transitions.
        for state in sg:
            for symbol in ret.alphabet:
                dst_state = dfa.dst_state(state, symbol)

                if dst_state is None:
                    continue

                dst_sstate = get_superstate(group_of(dst_state))

                ret.add_transition(sstate, symbol, dst_sstate)

    return ret
