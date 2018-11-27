import DFA

def run(dfa, word, verbose = False):
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
            if verbose: print("no transition available for (" + current_state + ", " + symbol + " ).")
            return False;

        current_state = next_state
        i = i+1

    if current_state in dfa.finals:
        if verbose: print("ending on final state '" + current_state + "'.")
        return True
    if verbose: print("ending on non accepting state '" + current_state + "'")
    return False

def isComplete(dfa):
    """ Returns true if the automaton is complete, false otherwise.
        @param dfa the automaton to be tested."""
    for state in dfa.states:
        for symbol in dfa.alphabet:
            if dfa.dst_state(state, symbol) == None:
                return False
    return True

def complete(dfa):
    """ Returns a complete automaton from the specified automaton (which remains
        inchanged).
        @param dfa the input automaton.
        @return the complete automaton."""
    completed = dfa.clone()

    # Find name for Qp.
    qp = "Qp"
    i = 0
    while qp is in completed.states:
        qp = "Qp" + i

    # Complete
    completed.states.append(qp)
    for state in completed.states:
        for symbol in completed.alphabet:
            if completed.dst_state(state, symbol) == None:
                return completed.add_transition(state, symbol, qp)

    return completed

def accessible(dfa, state):
    """ Returns true if the specified state is accessible in the automaton, returns
        false otherwise.
        @param dfa      the considered automaton.
        @param state    the state to be tested.
        @return true if the state is accessible, false otherwise."""
    if state not in dfa.states:
        print("error : the state '" + state + "' is not part of the automaton.")
        return

    
