import DFA

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
        @param dfa the DFA to complete."""
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

def complement(dfa):
    """ Returns a complementary automaton from the specified automaton (which
        remains inchanged).
        @param dfa the input automaton.
        @return a complementary automaton recognizing the reversal language."""
    ret = dfa.clone()

    oldfinals = dfa.finals.copy()
    dfa.finals.clear()

    for state in dfa.states:
        if state not in oldfinals:
            dfa.finals.append(state)

    return ret

def accessible_states(dfa):
    """ Returns the list of all accessible states in the specified automaton.
        @param dfa  the automaton considered."""

    accessibles = []

    visited = []
    to_visit = [dfa.init]

    while len(to_visit) != 0:
        state = to_visit.pop()

        visited.append(state)

def accessible(dfa, state):
    """ Returns true if the specified state is accessible in the automaton, returns
        false otherwise.
        @param dfa      the considered automaton.
        @param state    the state to be tested.
        @return true if the state is accessible, false otherwise."""
    if state not in dfa.states:
        print("error : the state '" + state + "' is not part of the automaton.")
        return

    return state in accessibles_states(dfa)

def product(dfa1, dfa2):

    return ""
