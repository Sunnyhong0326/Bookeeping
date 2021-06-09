import sys


class Categories:
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']],
                            'income', ['salary', 'bonus']]

    def view(self):
        lst = []

        def view_cat(cate=None, level=-1):
            if cate is None:
                cate = self._categories
            if type(cate) in {list, tuple}:
                for rec in cate:
                    view_cat(rec, level + 1)
            else:
                s = ' ' * 4 * level
                s += '-' + cate
                lst.append(s)
        view_cat()
        return lst

    def is_category_valid(self, categor):
        def valid(test_category=categor, cate=None):
            if cate is None:
                cate = self._categories
            if type(cate) == list:
                for v in cate:
                    if valid(test_category, v):
                        return True
                return False
            else:
                if cate == test_category:
                    return True

        return valid()

    def find_subcategories(self, find_category):
        if self.is_category_valid(find_category):
            def find_subcategories_gen(l=self._categories, found=False):
                if type(l) in {list, tuple}:
                    for index, child in enumerate(l):
                        yield from find_subcategories_gen(child, found)
                        if child == find_category and index + 1 < len(l) and \
                                type(l[index + 1]) == list:
                            yield from find_subcategories_gen(l[index + 1], True)
                else:
                    if find_category == l or found == True:
                        yield l
            lst = [i for i in find_subcategories_gen()]
            return lst
        else:
            sys.stderr.write(f'No such category\n')

    def flatten(self):
        def flat(lst=self._categories):
            if type(lst) == list:
                result = []
                for val in lst:
                    result.extend(flat(val))
                return result
            else:
                return [lst]
        return flat()
