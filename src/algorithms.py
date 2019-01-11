import DFA
import copy

def run(dfa, word, verbose = False):
    """ Runs the specified DFA on a word and returns True if the word is
        accepted.
        @param dfa      the DFA to be executed.
        @param word     the word to be tested.
        @param verbose  if True, more information are displayed about the
            execution.
        @return True if the word is accepted, False otherwise."""
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

def successors(dfa, state):
    """ Returns the list of the successors of the specified state in the DFA.
        @param dfa      the considered automaton.
        @param state    the considered state.
        @return the list of the successors of the state."""
    if state not in dfa.states:
        print("error : the specified state '" + state + "' is not part of the automaton.")
        return

    ret = []
    for (symbol, dst_state) in dfa.transitions[state]:
        if dst_state not in ret:
            ret.append(dst_state)

    return ret

def predecessors(dfa, state):
    """ Returns the list of the predecessors of the specified state in the DFA.
        @param dfa      the considered automaton.
        @param state    the considered state.
        @return the list of the predecessors of the state."""
    if state not in dfa.states:
        print("error : the specified state '" + state + "' is not part of the automaton.")
        return

    ret = []
    for src_state in dfa.states:
        for (symbol, dst_state) in dfa.transitions[src_state]:
            if dst_state == state and src_state not in ret:
                ret.append(src_state)

    return ret

def is_complete(dfa):
    """ Returns True if the automaton is complete, False otherwise.
        @param dfa the automaton to be tested."""
    for state in dfa.states:
        for symbol in dfa.alphabet:
            if dfa.dst_state(state, symbol) == None:
                return False
    return True

def complete(dfa):
    """ Completes the specified automaton.
        @param dfa the DFA to complete.
        @return the modified DFA."""
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

def accessible_states(dfa):
    """ Returns the list of all accessible states in the specified automaton.
        @param dfa  the automaton considered.
        @return the list of the accessible states."""
    visited = []
    to_visit = [dfa.init]

    while len(to_visit) > 0:
        state = to_visit.pop()
        visited.append(state)
        for succ in successors(dfa, state):
            if succ not in visited and succ not in to_visit:
                to_visit.append(succ)

    return visited

def accessible(dfa, state):
    """ Returns True if the specified state is accessible in the automaton, returns
        False otherwise.
        @param dfa      the considered automaton.
        @param state    the state to be tested.
        @return True if the state is accessible, False otherwise."""
    if state not in dfa.states:
        print("error : the state '" + state + "' is not part of the automaton.")
        return

    return state in accessible_states(dfa)

def accessible(dfa):
    """ Returns True if the specified DFA is accessible (if all it's states are,
     accessible), False otherwise.
        @param dfa      the considered automaton.
        @return True if the DFA is accessible, False otherwise."""
    return len(dfa.states) == len(accessible_states(dfa))

def coaccessible_states(dfa):
    """ Returns the list of all co-accessible states in the specified automaton.
        @param dfa  the automaton considered.
        @return the list of the co-accessible states."""
    visited = []
    to_visit = dfa.finals.copy()

    while len(to_visit) > 0:
        state = to_visit.pop()
        visited.append(state)
        for pred in predecessors(dfa, state):
            if pred not in visited and pred not in to_visit:
                to_visit.append(pred)

    return visited

def coaccessible(dfa, state):
    """ Returns True if the specified state is accessible in the automaton, returns
        False otherwise.
        @param dfa      the considered automaton.
        @param state    the state to be tested.
        @return True if the state is coaccessible, False otherwise."""
    if state not in dfa.states:
        print("error : the state '" + state + "' is not part of the automaton.")
        return

    return state in coaccessible_states(dfa)

def coaccessible(dfa):
    """ Returns True if the specified DFA is coaccessible (if all it's states are,
     accessible), False otherwise.
        @param dfa      the considered automaton.
        @return True if the DFA is coaccessible, False otherwise."""
    return len(dfa.states) == len(coaccessible_states(dfa))

def trim(dfa):
    """ Returns True if the specified DFA is trim (accessible and coaccessible),
        False otherwise.
        @param dfa      the considered automaton.
        @return True is the DFA is trim, False otherwise."""
    return accessible(dfa) and coaccessible(dfa)

def negate(dfa):
    """ Negates the specfied automaton, which now recognizes the complementary
        language of the original DFA.
        @param dfa the input automaton.
        @returns the modified DFA."""
    if not is_complete(dfa):
        print("error : negation requires a complete DFA.")
        return
    oldfinals = dfa.finals.copy()
    dfa.finals.clear()

    for state in dfa.states:
        if state not in oldfinals:
            dfa.finals.append(state)

    return dfa

def product(dfa1, dfa2):
    """ Returns a new automaton which is the product of the two specified DFAs.
    @param dfa1 the first operand of the product.
    @param dfa2 the second operand of the product.
    @return the product of the two DFAs."""

    alphabet = set.union(set(list(dfa1.alphabet)), set(list(dfa2.alphabet)))
    ret = DFA.DFA(alphabet)
    to_visit = []

    """ Returns the superstate corresponding to the specified states and add it
        to the product DFA if it doesn't exist. """
    def get_superstate(state1, state2):
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
