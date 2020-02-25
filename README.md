E-closure:

start at 0 >> Find all states reachable through nulls.

If e-closure found, subst.
else create closure and subst.

<!-- ============================================================================================ -->

Fallback DFA:

Run will return the output string.
Initially push the 0 on the stack
    1 0 0 0 1 0 1
    |
    RL

- Stack of states, keep pushing as you move pointer L (the moving one on the pointer string).
- Move L and push on the stack the corresponding stack according to the character move
- Once input is finished, start popping from the stack, and check whether or not stack is accepted, if not move L back
- Once a popped state is an accepted one, get the corresponding output and append it to the result. Then move the R all the way to the L (aka previous part of the input string is accepted.)
- Re-do it all again, by emptying the stack, and starting from the new position where R&L at.
- Stop when your R after an update (aka the R=L) are at the end of the string.

NOTE: If the input is not accepted (aka stack gets empty and you're trying to POP)::
    - Get the latest top of the stack (that was starting this stage), so basically we need to keep track of the top of the stack at the start of every stage/tokenization
    - Append it to the existing result (if any) and return it