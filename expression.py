class expression_count:
    def __init__(self, numbers):
        self.numbers = numbers
        self.expression_map = {}

    def count_expressions(self, target):
        if len(self.numbers) <= 0:
            return 0
        if len(self.numbers) == 1:
            if self.numbers[0] == target:
                return 1
            else:
                return 0

        return self.__expression_for(len(self.numbers) - 1,target)

    def __expression_for(self, index, target):
        if index < 0:
            return 0
        if index == 0:
            if self.numbers[0] == target:
                self.expression_map[(index, target)] = 1
                return 1
            else:
                self.expression_map[(index, target)] = 0
                return 0

        # 先查看是否已经有答案
        if (index, target) in self.expression_map:
            return self.expression_map[(index, target)]

        '''
        对于最后一个元素e，如果使用+,那么就需要前n-1个元素的组合得到结果target - e，
        如果使用-,那么需要前n - 1 个元素的组合实现target + e
        '''
        last_element = self.numbers[index]
        result_plus = self.__expression_for(index - 1, target - last_element)
        result_minus = self.__expression_for(index - 1, target + last_element)
        result = result_minus + result_plus
        self.expression_map[(index, target)] = result

        return result

    def count_expressions_topdown(self, target):
        index = 1
        cache_map1 = {}
        cache_map2 = {}
        cache_map1[self.numbers[0]] = 1
        while index < len(self.numbers):
            number = self.numbers[index]
            for previous_result in cache_map1:
                result_add = previous_result + number
                if result_add in cache_map2:
                    cache_map2[result_add] += cache_map1[previous_result]
                else:
                    cache_map2[result_add] = cache_map1[previous_result]

                result_sub = previous_result - number
                if result_sub in cache_map2:
                    cache_map2[result_sub] += cache_map1[previous_result]
                else:
                    cache_map2[result_sub] = cache_map1[previous_result]

            index += 1
            cache_map1 = cache_map2
            cache_map2 = {}

        if target in cache_map1:
            return cache_map1[target]

        return 0



target = 3
expressions = expression_count([1, 2, 2, 3, 1])
expression_ways = expressions.count_expressions(target)

print(f"there are {expression_ways} ways to express target: {target}")

print(expressions.count_expressions_topdown(target))

