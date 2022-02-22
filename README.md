给定一组数字L以及一个目标数值target，要求你找出如何在数字间设置+和-两种符号，使得数字的计算结果等于给定数值，例如给定数组[1, 2, 2, 3, 1]以及目标数值3，那么有3中表达式方式使得数组元素计算后得到目标数值：
1 + 2 + 2 - 3 + 1 = 3
1 + 2 - 2 + 3 - 1 = 3
1 - 2 + 2 + 3 - 1 = 3

现在需要我们设计算法，找出可行组合方式的数量，例如给定上面数据，算法给出3作为答案。这个问题可以直接使用动态规划的套路模板，对应最后一个元素，我们用e表示，如果在它前面的符号是+，那么问题就转换为对前n-1个元素，我们要计算它的组合方式数量，使得前n-1个元素组合后所得结果为 (target - e),你看这样我们就把问题的规模从n缩小到n-1，同理我们还可以考虑如果最后一个元素e对应的符号是-，那么前n-1个元素的组合就得满足结果为(target + e)。

将问题规模缩小然后递归的求解是动态规划的解法套路的重要步骤。接下来我们要记录”中间结果“，也就是每次我们递归的求解问题时，我们先在缓存或者”表“中查看针对当前问题是否已经有了结果，如果有了结果直接获取返回，如果没有在进行相应计算。由于我们递归时针对元素的个数，因此我们缓存的对象就是元素个数和给定目标数值，例如当我们要递归的查找前n-1个元素是否存在给定组合使得元素计算结果为(target-e)，那么我们就拿(n, target - e)作为目标在缓存中进行查找。

动态规划由于要使用递归，因此我们再实现时一定要先注意处理递归终止条件，不然递归无法停止的话就会导致栈溢出。针对这个问题，递归的终止条件就是当前元素只有1个的情况，在只有一个元素时，如果它的值正好等于目标值，那么我们就返回1，因此只有一种方式让当前元素的组合等于给定目标值，如果元素值不等于给定值，那么返回0，因为在只有当前元素的条件下，没有任何方法能让它等于给定目标值，由此我们给出实现方法：
```
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
```
我们运行上面代码看看：
```
target = 3
expressions = expression_count([1, 2, 2, 3, 1])
expression_ways = expressions.count_expressions(target)

print(f"there are {expression_ways} ways to express target: {target}")
```
代码运行后给出结果如下：
there are 3 ways to express target: 3
从输出看，结果与预期一致。这个问题有一个难点在于如何分析它的复杂度。我们每一次递归时都会有一个目标值，然后查找给定元素如何组合成目标值，我们无法确定具体的目标值，但却能确定其范围，由于我们给定用于组合的数值都是正整数，因此目标值最大不会超过所有元素加总之和，我们用S来表示这个和，另外如果一开始给定的元素有n个，那么我们就需要递归n次，因此算法复杂度的上界就是O(S * n)。

对于动态规划问题，最容易思考的方式是自底向上，也就是要解决规模为n的问题，那么先考虑如何解决规模为n-1的问题。这种思维方法好处在于容易掌握，易于理解，不好之处在于内存消耗，因为使用递归就得消耗堆栈。几乎任何能递归解决的问题都有自顶向下的方法，我们这个问题也不例外，这种思考方式有点类似于上一节我们看到的BFS方法。

为了方便讨论，假设给定的素组元素为[1,1,1,1]，首先我们选定第一个元素1，那么我们就得到在给定第一个元素的情况下，我们有1种方法得到数值1。接下来我们引入第二个元素1，由于我们可以使用+和-作用于它，使用+我们得到2，使用-我们得到0，于是我们就有1中方法然前两个元素组合得到数值2，1种方法得到数值0，我们使用{2:1, 0:1}来记录这个信息。

接下来我们引入第3个元素1，同样可以使用+和-作用到它身上，如果前两个元素所得结果为2，那么使用+我们就得到数值3，使用-，我们就得到数值1，于是给定前3个元素，我们目前可以实现一种组合得到数值3，一种组合得到数值1。如果前两个元素组合成数值0，那么使用+就得到数值1，使用-就得到数值-1，注意到数值1这里就有了两种组合方式，一种是前两个元素组合成2，然后使用-作用到第3个元素，另一种是前两个元素组合成0，然后使用+作用到第3个元素，于是我们有{3:1, 1:2, -1:1}，如此依次类推直到遍历完所有元素，最后我们使用目标数值target在给定的记录表中查看，如果有对应记录，那么就能查到组合方式，如果找不到那意味着不存在组合方式能让给定元素得到目标值，我们看看实现方法：
```
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
```
同学们可以运行上面代码试试看看结果是不是与前面我们实现的自底向上的方法一样。

