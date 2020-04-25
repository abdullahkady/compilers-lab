# T15_37_16401_Abdullah_Elkady
class LRE:
    def __init__(self, input_string):
        self.original_rules = self._parse_input(input_string)

    def _parse_input(self, input_string: str):
        rules = [r.split(',') for r in input_string.split(';')]
        return [(rule[0], rule[1:]) for rule in rules]

    def _serialize_output(self, rules):
        output = ''
        for var, p_rules in rules:
            output += '{},{};'.format(var, ','.join(p_rules))
        return output[:-1]

    def _substitute(self, rule, preceding_rule):
        var, production_rules = rule
        new_production_rules = []
        pre_variable, pre_production_rules = preceding_rule
        for prod_rule in production_rules:
            if prod_rule[0] == pre_variable:
                new_production_rules += [p+prod_rule[1:] for p in pre_production_rules]
            else:
                new_production_rules += [prod_rule]
        return (var, new_production_rules)

    def _eliminate_left_recursion(self, rule):
        alpha = []
        beta = []
        has_recursion = False
        var, prod_rules = rule

        for prod_rule in prod_rules:
            if prod_rule[0] == var:
                alpha.append(prod_rule[1:])
                has_recursion = True
            else:
                beta.append(prod_rule)

        if not has_recursion:
            # Hack around to avoid checking in the caller
            return [rule]

        return [
            (var, ["{}{}'".format(b, var) for b in beta]),
            (var + "'", [*["{}{}'".format(a, var) for a in alpha], ''])
        ]

    def eliminate_lre(self):
        output = []
        for idx, rule in enumerate(self.original_rules):
            for preceding_rule in self.original_rules[:idx]:
                rule = self._substitute(rule, preceding_rule)
                self.original_rules[idx] = rule

            refined_rules = self._eliminate_left_recursion(rule)
            self.original_rules[idx] = refined_rules[0]
            output += refined_rules
        return self._serialize_output(output)


if __name__ == "__main__":
    input_string = "S,ScT,T;T,aSb,iaLb,i;L,SdL,S"
    output = LRE(input_string).eliminate_lre()
    print(output)
    # UNCOMMENT THE BELOW CODE TO RUN ALL THE TEST CASES WITH THE EXPECTED OUTPUTS

    # test_cases = [
    #     (
    #         "S,ScT,T;T,aSb,iaLb,i;L,SdL,S",
    #         "S,TS';S',cTS',;T,aSb,iaLb,i;L,aSbS'dL,iaLbS'dL,iS'dL,aSbS',iaLbS',iS'"
    #     ),
    #     (
    #         "S,Sa,b",
    #         "S,bS';S',aS',"
    #     ),
    #     (
    #         "S,Sab,cd",
    #         "S,cdS';S',abS',"
    #     ),
    #     (
    #         "S,SuS,SS,Ss,lSr,a",
    #         "S,lSrS',aS';S',uSS',SS',sS',"
    #     ),
    #     (
    #         "S,SuT,T;T,TF,F;F,Fs,P;P,a,b",
    #         "S,TS';S',uTS',;T,FT';T',FT',;F,PF';F',sF',;P,a,b"
    #     ),
    #     (
    #         "S,z,To;T,o,Sz",
    #         "S,z,To;T,oT',zzT';T',ozT',"
    #     ),
    #     (
    #         "S,lLr,a;L,LbS,S",
    #         "S,lLr,a;L,lLrL',aL';L',bSL',"
    #     ),
    #     (
    #         "S,BC,C;B,Bb,b;C,SC,a",
    #         "S,BC,C;B,bB';B',bB',;C,bB'CCC',aC';C',CC',"
    #     ),
    # ]
    # for i, o in test_cases:
    #     print(LRE(i).eliminate_lre() == o)
