from dfa import DFA


class MDFA(DFA):
    "SRC,TARGET_ZERO,TARGET_ONE;ANOTHER#ACCEPTED,STATES"

    def __init__(self, dfa_dict, accepted_states, initial_state):
        # dfa_dict = {
        #     (S0, S1): ((S2, ), (S3, S1)),
        # }
        # accepted_states = (S1, S3)

        self.accepted_states = [s for s in dfa_dict.keys() if bool(set(s) & set(accepted_states))]
        self.transitions = dfa_dict
        self.initial_state = initial_state

    def get_initial_state(self):
        return self.initial_state

    def get_transitions(self):
        return self.transitions

    def get_accepted_states(self):
        return self.accepted_states


class NFA:

    def __init__(self, nfa_string):
        trans_z, trans_o, trans_e, accepted = nfa_string.split('#')
        self.accepted_states = accepted.split(',')
        self.trans_z = [t.split(',') for t in trans_z.split(';') if t]
        self.trans_o = [t.split(',') for t in trans_o.split(';') if t]
        self.trans_e = [t.split(',') for t in trans_e.split(';') if t]

    def construct_dfa_dict(self):
        # {
        #     'STATE_TUPLE': ('STATE_TUPLE_ZERO', 'STATE_TUPLE_ONE')
        # }
        dfa_states = {}
        queue = [('0', )]
        while queue:
            current_states = queue.pop(0)
            current_states = self._find_null_closure_set(current_states)
            state_key = tuple(sorted(current_states))
            if state_key not in dfa_states:
                zeros = tuple(sorted(target for src, target in self.trans_z if src in current_states))
                ones = tuple(sorted(target for src, target in self.trans_o if src in current_states))
                queue.append(self._find_null_closure_set(zeros))
                queue.append(self._find_null_closure_set(ones))
                dfa_states[state_key] = (
                    self._find_null_closure_set(zeros),
                    self._find_null_closure_set(ones)
                )
        return dfa_states

    def _find_null_closure_set(self, states):
        result = tuple()
        for s in states:
            result += self._find_null_closure(s)
        return tuple(sorted(set(result)))

    def _find_null_closure(self, state):
        result = (state, )
        targets = [target for src, target in self.trans_e if src == state]
        if not targets:
            return (state, )
        for target in targets:
            result += self._find_null_closure(target)
        return tuple(sorted(set(result)))

    def get_dfa(self):
        dfa_dict = self.construct_dfa_dict()
        print(dfa_dict)
        initial_state = self._find_null_closure('0')
        return MDFA(dfa_dict, self.accepted_states, initial_state)


if __name__ == '__main__':
    NFA_1_STRING = '0,0;0,1;1,3#0,1;1,2;2,3#1,2;3,2#3'
    NFA_1_TEST_CASES = [
        '000111',
        '10110',
        '00110',
        '101010',
        '1111'
    ]
    NFA_2_STRING = '0,1;1,2;2,3#1,3;3,4;4,2#0,2;3,1;2,4#2'
    NFA_2_TEST_CASES = [
        '0000',
        '011011',
        '01010',
        '101010',
        '11100'

    ]

    NFA_STRING = NFA_2_STRING
    TEST_CASES = NFA_2_TEST_CASES

    nfa = NFA(NFA_STRING)
    dfa = nfa.get_dfa()
    for case in TEST_CASES:
        print(dfa.run(case))
