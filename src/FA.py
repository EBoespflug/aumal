
class FA:
    """ This class represent any type of finite automaton."""
    def __init__(self, alphabet):
        """ Initialise the finite automaton.
            @param the alphabet of the automaton."""

        """ List of string corresponding to states name.
            States are always identificated by name."""
        self.states = []
        """ Dictionary using src state as key and mapping it to a list of
            pair (dest_state, symbol)."""
        self.transitions = {}
        """ The string corresponding to the name of the initial state."""
        self.init = None
        """ A list containing the name of the final states."""
        self.finals = []
        """ A string containing all symbol in the alphabet. The string "\e"
            is used to represent epsilon and is implicit"""
        self.alphabet = alphabet

    def add_state(self, state, final = False):
        """ Add a new state. Print error if the state already exists.
            @param state the name of the new state."""
        if state in self.states:
            print("error : state '" + state + "' already exists.")
            return
        self.transitions[state] = []
        self.states.append(state)
        if final:
            self.finals.append(state)

    def valid_symbol(self, symbol):
        if symbol is "\e": return True
        if symbol not in self.alphabet: return False
        return True

    def add_transition(self, src_state, symbol, dst_state):
        """ Add a transition to the FA. Print error if the exact
            transition already exists.
            @param src_state the name of the source state.
            @param symbol the symbol of the transition
            @param dst_state the name of the destination state."""
        if not self.valid_symbol(symbol):
            print("error : the symbol '" + symbol + "'is not part of the alphabet.")
            return
        if src_state not in self.states:
            print("error : the state '" + src_state + "' is not an existing state")
            return
        if dst_state not in self.states:
            print("error : the state '" + dst_state + "' is not an existing state")
            return

        if (symbol, dst_state) in self.transitions[dst_state]:
            print("error : the transition (" + src_state + ", " + symbol + ", " + dst_state + ") already exists")
            return

        self.transitions[src_state].append((symbol, dst_state))
        return

    def __str__(self):
        ret = "FA :\n"
        for state in self.states:
            ret = ret + "   - state '%s':\n" % (state)
            for (sym, dest) in self.transitions[state]:
                ret = ret + "        - (%s) --(%s)--> (%s)\n" % (state, sym, dest)
        ret = ret + "   - alphabet: " + self.alphabet + "\n"
        ret = ret + "   - init: " + str(self.init) + "\n"
        ret = ret + "   - final: " + str(self.finals) + "\n"
        return ret
