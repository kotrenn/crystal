class FunctionCall(object):
    def __init__(self, code):
        self.name = ''
        self.args = []

        self.parse_code(code)

    def __str__(self):
        ret = self.name + '('
        ret += ', '.join([str(arg) for arg in self.args])
        ret += ')'
        return ret

    def parse_code(self, code):
        pos = code.index('(')
        name = code[:pos]
        body = code[pos:]
        self.name = name
        if body[-1] != ')':
            print 'Missing `)` at end of function call `' + code + '`'
            return None
        body = body[1:-1]
        args = self.split_args(body)
        for arg in args:
            if len(arg) == 0:
                continue
            val = None
            if arg[0] == '@':
                val = FunctionCall(arg)
            else:
                val = arg
            self.args.append(val)

    def split_args(self, args):
        lhs = 0
        rhs = 0
        ret = []
        depth = 0
        while rhs < len(args):
            x = args[rhs]
            if x == '(':
                depth += 1
            elif x == ')':
                depth -= 1
                if depth < 0:
                    print 'Error: too many `)` in argument list `' + args + '`'
            elif x == ',' and depth == 0:
                cur = args[lhs:rhs]
                ret.append(cur)
                lhs = rhs + 1
                rhs += 1
            rhs += 1
        cur = args[lhs:]
        ret.append(cur)
        return ret
