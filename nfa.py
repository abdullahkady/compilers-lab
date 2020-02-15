class NFA:
    dfa_states = {}

    def __init__(self, nfa_string):

        trans_z, trans_o, trans_e, accepted = nfa_string.split('#')
        accepted_states = accepted.split(',')
        self.trans_z = [t.split(',') for t in trans_z.split(';') if t]
        self.trans_o = [t.split(',') for t in trans_o.split(';') if t]
        self.trans_e = [t.split(',') for t in trans_e.split(';') if t]
        dfa = self._construct_dfa(accepted_states)

    def _construct_dfa(self, accepted_states):
        # {
        #     'STATE_TUPLE': ('STATE_TUPLE_ZERO', 'STATE_TUPLE_ONE')
        # }
        queue = [('0', )]
        while queue:
            current_states = queue.pop(0)
            current_states = self._find_null_closure_set(current_states)
            state_key = tuple(sorted(current_states))
            if state_key not in self.dfa_states:
                zeros = tuple(sorted(target for src, target in self.trans_z if src in current_states))
                ones = tuple(sorted(target for src, target in self.trans_o if src in current_states))
                queue.append(self._find_null_closure_set(zeros))
                queue.append(self._find_null_closure_set(ones))
                print(self._find_null_closure_set(ones))
                self.dfa_states[state_key] = (
                    self._find_null_closure_set(zeros),
                    self._find_null_closure_set(ones)
                )
        print(self.dfa_states)

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


if __name__ == '__main__':
    # NFA_STRING = '0,0;1,2;3,3#0,0;0,1;2,3;3,3#1,2#3'

    # NFA_STRING = "0,0;0,1;0,4;4,4#0,0;1,2;2,3;4,5##3,5"
    NFA_STRING = "0,2;1,0;2,1#2,1;2,2#0,1#1"

    NFA(NFA_STRING)
