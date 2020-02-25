class FDFA:
    def __init__(self, fdfa_string):
        P, S = fdfa_string.split('#')
        self.accepted_states = S.split(',')

        self.states = {}
        for src, t0, t1, action in [e.split(',') for e in P.split(';')]:
            self.states[src] = (t0, t1, action)

    def _get_state_stack(self, input_string):
        current_state = '0'
        stack = [current_state]
        for char in input_string:
            t0, t1, action = self.states[current_state]
            current_state = t0 if char == '0' else t1
            stack.append(current_state)
        return stack

    def run(self, input_string):
        result = ''
        while True:
            # Create a stack from the -remaining- input
            stack = self._get_state_stack(input_string)
            _, _, top_action = self.states[stack[-1]]  # Used whenever an error occurs (aka string not accepted).

            while True:
                current_state = stack.pop()
                if not stack:
                    return result + top_action  # String not accepted

                if current_state in self.accepted_states:
                    result += self.states[current_state][2]
                    # Update the input_string, basically mocking the L&R pointers
                    input_string = input_string[(len(stack)):]
                    if not input_string:
                        # If the input is exhausted, then the string is accepted with the accumulated action
                        return result
                    break

        return result


FDFA_STRING = '0,0,1,00;1,2,1,01;2,0,3,10;3,3,3,11#0,1,2'
test_cases = [
    ('100', '00'),
    ('101', '1001'),
    ('110', '10'),
    ('10110', '1010'),
    ('011', '01'),
]

# FDFA_STRING = '0,1,0,00;1,1,2,01;2,3,2,10;3,3,3,11#1,2'
# test_cases = [
#     ('011', '10'),
#     ('110', '01'),
#     ('00101', '1010'),
#     ('100100', '1001'),
#     ('100', '01'),
# ]


# FDFA_STRING = "0,1,0,00;1,1,2,01;2,1,3,10;3,1,0,11#3"
# test_cases = [
#     ("0100", "01"),
#     ("10011", "11"),
#     ("100011011", "11"),
#     ("011001", "1110"),
#     ("1001111010", "1101")
# ]

# FDFA_STRING = "0,1,0,00;1,0,2,01;2,0,2,11#1"
# test_cases = [
#     ("011110",  "0101"),
#     ("110110",  "0101"),
#     ("010011",  "0100"),
#     ("01111",  "0100"),
#     ("1011011",  "010100"),
# ]

fdfa = FDFA(FDFA_STRING)
for i, o in test_cases:
    print(fdfa.run(i), o, fdfa.run(i) == o)
