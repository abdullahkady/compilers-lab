"SRC,TARGET_ZERO,TARGET_ONE;ANOTHER#ACCEPTED,STATES"


class DFA:
    def __init__(self, dfa_string):
        transitions, accepted = dfa_string.split('#')
        self.accepted_states = accepted.split(',')
        self.transitions = [t.split(',') for t in transitions.split(';')]

    def get_transitions(self):
        return {src: (z, o) for src, z, o in self.transitions}

    def get_accepted_states(self):
        return self.accepted_states

    def _transition(self, char, current_state):
        if char == '0':
            return self.get_transitions()[current_state][0]
        return self.get_transitions()[current_state][1]
        #    return next(
        #         next_state for state, next_state, _ in
        #         self.get_transitions() if state == current_state
        #     )
        # return next(
        #     next_state for state, _, next_state in
        #     self.get_transitions() if state == current_state
        # )

    def get_initial_state(self):
        return '0'

    def run(self, input_string):
        state = self.get_initial_state()
        for char in input_string:
            state = self._transition(char, state)
        return state in self.get_accepted_states()


if __name__ == '__main__':
    # DFA_STRING = '0,3,1;1,2,1;2,3,3;3,3,3#3'
    DFA_STRING = '0,0,1;1,2,3;2,3,2;3,3,3#0,3'
    dfa = DFA(DFA_STRING)
    TESTS = (
        '000',
        '101111',
        '101010',
        '001001',
        '00010111',
    )
    for test in TESTS:
        print(dfa.run(test))
