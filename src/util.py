from subprocess import call
import DFA

def read(filename: str) -> DFA:
    """
    Read the specified dfa from a file. A DFA can be saved with the 'save' function.

    :param filename: the file in which the DFA is stored.
    :type filename: str
    :return: the DFA from the file.
    :rtype: DFA
    """
    local_dict = locals()
    with open(filename, "r") as file:
        exec(compile(open(filename).read(), filename, 'exec'), globals(), local_dict)

    return local_dict["a"]

def save(dfa: DFA, filename: str):
    """
    Save the specified dfa into a file. A DFA can be read with the 'read' function.

    :param dfa: the DFA to save
    :type dfa: DFA
    :param filename: the name of the file in which the automaton will be saved.
    :type filename: str
    """
    txt = "a = DFA.DFA(\"" + dfa.alphabet + "\")\n"
    for state in dfa.states:
        if state in dfa.finals:
            txt += "a.add_state(\"" + state + "\", True)\n"
        else:
            txt += "a.add_state(\"" + state + "\")\n"

    txt += "\na.init = \"" + dfa.init + "\"\n\n"

    for state in dfa.states:
        for (symbol, dst_state) in dfa.transitions[state]:
            txt += "a.add_transition(\"" + state + "\", \"" + symbol + "\", \"" + dst_state + "\")\n"

    with open(filename, "w") as file:
        file.write(txt)

def to_dot(dfa: DFA, **kwargs) -> str:
    """
    Returns a string corresponding to the specified DFA in DOT format.

    **Kwargs**:
         - `group` (`bool`): if True, the transition are regrouped when they
            have the same origin and destination states. *default*: `False`.
         - `name` (`str`): the name of the automaton for the DOT file. 
            *default*: `"Graph01"`.

    :param dfa: the DFA to be converted.
    :type dfa: DFA
    :return: the string DOT representation of the automaton.
    :rtype: str
    """
    # Args
    if "name" not in kwargs: kwargs["name"] = "Graph01"
    if "group" not in kwargs: kwargs["group"] = False

    # Header
    ret = "digraph " + kwargs["name"] + " {\n    bgcolor=\"transparent\";\nrankdir=\"LR\";\n\n"
    ret += "    // States (" + str(len(dfa.states)) + ")\n"

    state_name = lambda s : "Q_" + str(dfa.states.index(s))

    # States
    ret += "    node [shape = point ];     __Qi__ // Initial state\n" # Initial state
    for state in dfa.states:
        ret += "    "
        if state in dfa.finals:
            ret += "node [shape=doublecircle]; "
        else:
            ret += "node [shape=circle];       "
        ret += state_name(state) + " [label=\"" + state + "\"];\n"

    # Transitions
    ret += "\n    // Transitions\n"
    ret += "    __Qi__ -> " + state_name(dfa.init) + "; // Initial state arrow\n"
    for state in dfa.states:
        if kwargs["group"]:
            transition_dict = {}
            for (symbol, dst_state) in dfa.transitions[state]:
                if dst_state not in transition_dict:
                    transition_dict[dst_state] = []
                transition_dict[dst_state].append(symbol)
            for dst_state in transition_dict:
                transition_dict[dst_state].sort()
                ret += "    " + state_name(state) + " -> " + state_name(dst_state) + " [label=\"" + ", ".join(transition_dict[dst_state]) + "\"];\n"
        else:
            for (symbol, dst_state) in dfa.transitions[state]:
                ret += "    " + state_name(state) + " -> " + state_name(dst_state) + " [label=" + symbol + "];\n"
    return ret + "}\n"

def to_png(dfa: DFA, filename: str, **kwargs):
    """ 
    Create the PNG image corresponding to the representation of the
        specified DFA in a file.

    **Kwargs**: see `to_dot`.

    :param dfa: the DFA to convert in PNG.
    :type dfa: DFA
    :param filename: the name of the file.
    :type filename: str
    """

    tmp_file = filename + ".tmp"
    with open(tmp_file, "w") as file:
        file.write(to_dot(dfa, **kwargs))

    call(("dot -Tpng " + tmp_file + " -o " + filename).split(" "))
    call(("rm " + tmp_file).split(" "))


def to_pdf(dfa: DFA, filename: str, **kwargs):
    """ 
    Create the graphical PDF representation of the specified DFA in a file.
        The automaton is converted in DOT format and the command dot is called
        in order to generate the PDF.

    **Kwargs**: see `to_dot`.

    :param dfa: the DFA to convert in PNG.
    :type dfa: DFA
    :param filename: the name of the file.
    :type filename: str
    """

    tmp_file = filename + ".tmp"
    with open(tmp_file, "w") as file:
        file.write(to_dot(dfa, **kwargs))

    call(("dot -Tpdf " + tmp_file + " -o " + filename).split(" "))
    call(("rm " + tmp_file).split(" "))
