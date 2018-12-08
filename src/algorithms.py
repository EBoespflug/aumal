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
