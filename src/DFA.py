import copy
from typing import List, Dict, Tuple

class DFA:
    """
    This class represent any type of deterministic finite automaton.
    """
    def __init__(self, alphabet: str):
        """
        Initialise the finite automaton.

        :param alphabet: the alphabet of the automaton.
        :type alphabet: str
        """

        self.states : List[str] = []
        """ List of string corresponding to states name.
            States are always identificated by name."""
        self.transitions : Dict[str, List[Typle[str, str]]] = {}
        """ Dict[str, List[Typle[str, str]]]: Dictionary mapping src state to a list of
            pairs (dest_state, symbol)."""
        self.init : str = None
        """ str: The initial state of the automaton."""
        self.finals = []
        """ List[str]: A list containing the name of the final states."""
        self.alphabet = ""
        """ str: A string containing all symbols in the alphabet."""
        for s in alphabet:
            if s not in self.alphabet:
                self.alphabet += s

    def add_state(self, state: str, final : bool = False):
        """
        Add a new state. Print error if the state already exists.

        :param state: the name of the new state.
        :type state: str
        :param final: a boolean determining if the state is
                final, defaults to False
        :type final: bool, optional
        """
        if state in self.states:
            print("error : state '" + state + "' already exists.")
            return
        self.transitions[state] = []
        self.states.append(state)
        if final:
            self.finals.append(state)

    def valid_symbol(self, symbol: str) -> bool:
        """
        Returns true if the symbol is part of the alphabet,
            false otherwise.

        :param symbol: the symbol to be tested.
        :type symbol: str
        :return: _description_
        :rtype: bool
        """
        if symbol not in self.alphabet: return False
        return True

    def dst_state(self, src_state: str, symbol: str) -> str:
        """
        Search the transition corresponding to the specified source state
            and symbol and returns the destination state. If the transition does
            not exists, return None.

        :param src_state: the source state of the transition.
        :type src_state: str
        :param symbol: the symbol of the transition.
        :type symbol: str
        :return: the destination state.
        :rtype: str
        """
        if src_state not in self.states:
            print("error : the state '" + str(src_state) + "' is not an existing state.")
            return
        for (s, dst_state) in self.transitions[src_state]:
            if s == symbol:
                return dst_state
        return None

    def add_transition(self, src_state: str, symbol: str, dst_state: str):
        """
        Add a transition to the FA. Print error if the automaton already have a
            transition for the specified source state and symbol.

        :param src_state: the name of the source state.
        :type src_state: str
        :param symbol: the symbol of the transition.
        :type symbol: str
        :param dst_state: the name of the destination state.
        :type dst_state: str
        """
        if not self.valid_symbol(symbol):
            print("error : the symbol '" + symbol + "' is not part of the alphabet.")
            return
        if src_state not in self.states:
            print("error : the state '" + src_state + "' is not an existing state.")
            return
        if dst_state not in self.states:
            print("error : the state '" + dst_state + "' is not an existing state.")
            return

        if self.dst_state(src_state, symbol) != None:
            print("error : the transition (" + src_state + ", " + symbol + ", ...) already exists.")
            return

        self.transitions[src_state].append((symbol, dst_state))
        return

    def clone(self):
        """
        Clones the DFA.

        :return: the cloned automaton.
        :rtype: DFA
        """
        a = DFA(self.alphabet)
        a.states = self.states.copy()
        a.init = self.init
        a.finals = self.finals
        a.transitions = copy.deepcopy(self.transitions)
        return a

    def __str__(self) -> str:
        """
        :return: Returns the string representation of the automaton.
        :rtype: str
        """
        ret = "FA :\n"
        ret += "   - alphabet   : '" + self.alphabet + "'\n"
        ret += "   - init       : " + str(self.init) + "\n"
        ret += "   - finals     : " + str(self.finals) + "\n"
        ret += "   - states (%d) :\n" % (len(self.states))
        for state in self.states:
            ret += "       - (%s)" % (state)
            if len(self.transitions[state]) == 0:
                ret += ".\n"
            else:
                ret += ":\n"
                for (sym, dest) in self.transitions[state]:
                    ret += "          --(%s)--> (%s)\n" % (sym, dest)
        return ret
