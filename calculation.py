# coding=utf-8


class FNode(object):
    """
    数学表达式的树节点
    """
    methods = '+-*/'

    TYPE_NUM = 1
    TYPE_MED = 2

    with_bracket = False
    is_root = False
    node_type = None
    method = None
    parent = None
    left_child = None
    right_child = None
    value = None

    def __init__(self, formula, parent=None):
        if not isinstance(formula, str):
            print('表达式错误')
            return
        if not formula.count('(') == formula.count(')'):
            print('表达式错误')
            return
        for ch in formula:
            if ch not in ' +-*/0123456789.()':
                print('非法字符:{}'.format(ch))

        if not parent:
            self.is_root = True
        else:
            self.parent = parent

        if formula == '':
            self.value = 0
            self.node_type = self.TYPE_NUM
            return

        # 对 formula 去最外层的括号
        formula = formula.strip()

        if formula[0] == '(' and formula[-1] == ')':
            test_formula = formula[1:-1]
            bracket_level = 0
            self.with_bracket = True
            for ch in test_formula:
                if ch == '(':
                    bracket_level += 1
                elif ch == ')':
                    bracket_level -= 1

                if bracket_level < 0:
                    # 不能去掉最外层的括号
                    test_formula = formula
                    self.with_bracket = False
                    break
            formula = test_formula

        # 如果 formula 中不含有 methods， 则尝试转换为数字，返回
        if not ('+' in formula or
                '-' in formula or
                '*' in formula or
                '/' in formula):

            try:
                if '.' in formula:
                    self.value = float(formula)
                else:
                    self.value = int(formula)
                self.node_type = self.TYPE_NUM
            except Exception as e:
                print(e)
                return
            # print(self.value)
            return

        # 从最右边开始遍历字符
        # 如果找到 (， 括号层数 + 1，继续向左
        # 如果找到 )，括号层数 - 1 ，继续向左
        # 在括号层数为 0 的时候，如果找到 +- 则进行折断
        # 如果整个字符串找不到 +- ，则寻找第一个括号层数为 0 的*/，折断
        bracket_level = 0
        offset = 0
        # for ch in formula:
        for i in range(len(formula)-1, -1, -1):
            ch = formula[i]
            if ch == '(':
                bracket_level += 1
            elif ch == ')':
                bracket_level -= 1
            else:
                if bracket_level == 0 and (ch == '+' or ch == '-'):
                    left_str = formula[:i].strip()
                    right_str = formula[i + 1:].strip()
                    self.method = ch
                    self.node_type = self.TYPE_MED
                    break
            # offset += 1

        if self.method is None:
            bracket_level = 0
            offset = 0
            # for ch in formula:
            for i in range(len(formula) - 1, -1, -1):
                ch = formula[i]
                if ch == '(':
                    bracket_level += 1
                elif ch == ')':
                    bracket_level -= 1
                else:
                    if bracket_level == 0 and \
                            (ch == '*' or ch == '/'):
                        left_str = formula[:i].strip()
                        right_str = formula[i + 1:].strip()
                        self.method = ch
                        self.node_type = self.TYPE_MED
                        break
                # offset += 1

        self.left_child = FNode(left_str, self)
        self.right_child = FNode(right_str, self)

    def restore_formula(self):
        left_str = ''
        right_str = ''
        if self.left_child:
            left_str = self.left_child.restore_formula()
        if self.right_child:
            right_str = self.right_child.restore_formula()
        if self.node_type == self.TYPE_MED:
            new_formula = left_str + ' ' + self.method + ' ' + right_str
        else:
            new_formula = str(self.value)

        if self.with_bracket:
            new_formula = '(' + new_formula + ')'
        return new_formula

    def traverse(self):
        print(self)
        if self.left_child:
            self.left_child.traverse()
        if self.right_child:
            self.right_child.traverse()

    def cal(self):
        # if self.is_root:
        #     self.traverse()
        result = 0
        if self.node_type == self.TYPE_MED:
            if self.method == '+':
                result = self.left_child.cal() + self.right_child.cal()
            elif self.method == '-':
                result = self.left_child.cal() - self.right_child.cal()
            elif self.method == '*':
                result = self.left_child.cal() * self.right_child.cal()
            elif self.method == '/':
                result = self.left_child.cal() / self.right_child.cal()
        else:
            result = self.value

        if self.is_root:
            if result == int(result):
                result = int(result)
        return result

    def __repr__(self):
        if self.node_type == self.TYPE_NUM:
            return '<FNode type=NUM value={}>'.format(self.value)
        else:
            return '<FNode type=MED method={}>'.format(self.method)


if __name__ == '__main__':
    form_str = '(123 + 2422) * 23 + 24 / (4 - 2) + 0.5'
    formu = FNode(form_str)
    formu.traverse()
    print(formu.restore_formula())
    print(formu.cal())
