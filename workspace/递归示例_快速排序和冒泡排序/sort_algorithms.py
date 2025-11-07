# -*- coding: utf-8 -*-

def merge_sort(arr):
    """
    归并排序算法实现
    """
    # 基本情况：数组长度为0或1时已经有序
    if len(arr) <= 1:
        return arr
    
    # 分解：找到中间点
    mid = len(arr) // 2
    
    # 递归解决：对左右两半分别排序
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # 合并：将两个有序数组合并
    return merge(left_half, right_half)

def merge(left, right):
    """
    合并两个有序数组
    """
    result = []
    i = j = 0
    
    # 比较两个数组的元素，将较小的加入结果
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # 将剩余元素加入结果
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def quick_sort(arr):
    """
    快速排序算法实现
    """
    # 基本情况：数组长度为0或1时已经有序
    if len(arr) <= 1:
        return arr
    
    # 选择基准（这里选择第一个元素）
    pivot = arr[0]
    
    # 分区：将数组分为小于基准、等于基准、大于基准三部分
    left = [x for x in arr[1:] if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr[1:] if x > pivot]
    
    # 递归解决：对左右两部分分别排序
    return quick_sort(left) + middle + quick_sort(right)

def quick_sort_in_place(arr, low=0, high=None):
    """
    原地快速排序（更节省空间）
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # 分区并获取基准位置
        pivot_index = partition(arr, low, high)
        
        # 递归排序左右部分
        quick_sort_in_place(arr, low, pivot_index - 1)
        quick_sort_in_place(arr, pivot_index + 1, high)

def partition(arr, low, high):
    """
    分区函数：将数组重新排列，返回基准的最终位置
    """
    # 选择最后一个元素作为基准
    pivot = arr[high]
    
    # i 指向小于基准的区域的边界
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # 将基准放到正确位置
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# 调试版本的归并排序
def merge_sort_debug(arr, depth=0, side="root"):
    """
    带调试信息的归并排序
    """
    indent = "  " * depth
    print("{}[深度{} {}] 输入数组: {}".format(indent, depth, side, arr))
    
    # 基本情况
    if len(arr) <= 1:
        print("{}[深度{} {}] 基本情况返回: {}".format(indent, depth, side, arr))
        return arr
    
    # 分解
    mid = len(arr) // 2
    print("{}[深度{} {}] 分解为左右两半，中间点索引: {}".format(indent, depth, side, mid))
    
    # 递归解决
    print("{}[深度{} {}] 递归排序左半部分...".format(indent, depth, side))
    left_half = merge_sort_debug(arr[:mid], depth + 1, "left")
    
    print("{}[深度{} {}] 递归排序右半部分...".format(indent, depth, side))
    right_half = merge_sort_debug(arr[mid:], depth + 1, "right")
    
    # 合并
    print("{}[深度{} {}] 合并左右两部分: {} + {}".format(indent, depth, side, left_half, right_half))
    result = merge_debug(left_half, right_half, depth, side)
    print("{}[深度{} {}] 合并结果: {}".format(indent, depth, side, result))
    
    return result

def merge_debug(left, right, depth=0, side=""):
    """
    带调试信息的合并函数
    """
    indent = "  " * depth
    result = []
    i = j = 0
    step = 1
    
    print("{}[合并{}] 开始合并: left={}, right={}".format(indent, side, left, right))
    
    while i < len(left) and j < len(right):
        print("{}[合并{} 步骤{}] 比较 left[{}]={} 和 right[{}]={}".format(indent, side, step, i, left[i], j, right[j]))
        
        if left[i] <= right[j]:
            result.append(left[i])
            print("{}[合并{} 步骤{}] 选择 left[{}]={}，结果: {}".format(indent, side, step, i, left[i], result))
            i += 1
        else:
            result.append(right[j])
            print("{}[合并{} 步骤{}] 选择 right[{}]={}，结果: {}".format(indent, side, step, j, right[j], result))
            j += 1
        step += 1
    
    # 处理剩余元素
    if i < len(left):
        print("{}[合并{}] 添加左半剩余元素: {}".format(indent, side, left[i:]))
        result.extend(left[i:])
    if j < len(right):
        print("{}[合并{}] 添加右半剩余元素: {}".format(indent, side, right[j:]))
        result.extend(right[j:])
    
    print("{}[合并{}] 最终合并结果: {}".format(indent, side, result))
    return result

# 调试版本的快速排序
def quick_sort_debug(arr, depth=0, side="root"):
    """
    带调试信息的快速排序
    """
    indent = "  " * depth
    print("{}[快速排序 深度{} {}] 输入数组: {}".format(indent, depth, side, arr))
    
    # 基本情况
    if len(arr) <= 1:
        print("{}[快速排序 深度{} {}] 基本情况返回: {}".format(indent, depth, side, arr))
        return arr
    
    # 选择基准
    pivot = arr[0]
    print("{}[快速排序 深度{} {}] 选择基准: {}".format(indent, depth, side, pivot))
    
    # 分区
    left = [x for x in arr[1:] if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr[1:] if x > pivot]
    
    print("{}[快速排序 深度{} {}] 分区结果:".format(indent, depth, side))
    print("{} 小于基准: {}".format(indent, left))
    print("{} 等于基准: {}".format(indent, middle))
    print("{} 大于基准: {}".format(indent, right))
    
    # 递归解决
    print("{}[快速排序 深度{} {}] 递归排序左半部分...".format(indent, depth, side))
    sorted_left = quick_sort_debug(left, depth + 1, "left")
    
    print("{}[快速排序 深度{} {}] 递归排序右半部分...".format(indent, depth, side))
    sorted_right = quick_sort_debug(right, depth + 1, "right")
    
    # 合并结果
    result = sorted_left + middle + sorted_right
    print("{}[快速排序 深度{} {}] 合并结果: {} + {} + {} = {}".format(indent, depth, side, sorted_left, middle, sorted_right, result))
    
    return result

# 测试代码
def test_sorts():
    # 测试数据 - 使用不规律排序的9元素数组
    test_arr = [64, 8, 51, 32, 91, 17, 45, 78, 3]
    print("原始数组 (9个不规律元素):", test_arr)
    
    # 测试归并排序
    sorted_merge = merge_sort(test_arr[:])
    print("归并排序结果:", sorted_merge)
    
    # 测试快速排序
    sorted_quick = quick_sort(test_arr[:])
    print("快速排序结果:", sorted_quick)
    
    # 测试原地快速排序
    arr_in_place = test_arr[:]
    quick_sort_in_place(arr_in_place)
    print("原地快速排序结果:", arr_in_place)
    
    # 测试边界情况
    print("\n=== 边界情况测试 ===")
    
    # 空数组
    empty_arr = []
    print("空数组测试:", merge_sort(empty_arr[:]))
    
    # 单元素数组
    single_arr = [42]
    print("单元素数组测试:", merge_sort(single_arr[:]))
    
    # 已排序数组
    sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("已排序数组测试:", merge_sort(sorted_arr[:]))
    
    # 逆序数组
    reverse_arr = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("逆序数组测试:", merge_sort(reverse_arr[:]))

# 调试测试函数
def debug_demo():
    """
    调试演示函数
    """
    print("\n" + "="*60)
    print("归并排序详细调试演示")
    print("="*60)
    
    # 使用不规律排序的数组进行调试演示
    test_arr = [38, 27, 43, 3, 15, 92, 7, 61, 24]  # 9个不规律元素
    print("测试数组 (9个不规律元素): {}".format(test_arr))
    print("\n开始归并排序调试...\n")
    
    result = merge_sort_debug(test_arr)
    print("\n最终排序结果: {}".format(result))
    
    print("\n" + "="*60)
    print("快速排序详细调试演示")
    print("="*60)
    
    # 使用不同的不规律数组
    test_arr2 = [64, 8, 51, 32, 91, 17, 45, 78, 3]  # 9个不规律元素
    print("测试数组 (9个不规律元素): {}".format(test_arr2))
    print("\n开始快速排序调试...\n")
    
    result2 = quick_sort_debug(test_arr2)
    print("\n最终排序结果: {}".format(result2))

# 递归调用过程演示
def demonstrate_recursion():
    print("\n=== 归并排序递归过程演示 ===")
    arr = [38, 27, 43, 3, 9, 82, 10]
    print("排序过程:")
    print("原始数组: {}".format(arr))
    
    # 模拟递归调用层级
    print("分解为: [38, 27, 43] 和 [3, 9, 82, 10]")
    print("继续分解左半部分: [38] [27, 43]")
    print("继续分解: [27] [43]")
    print("合并: [27, 43]")
    print("合并: [27, 38, 43]")
    print("分解右半部分: [3, 9] [82, 10]")
    print("继续分解: [3] [9] 和 [82] [10]")
    print("合并: [3, 9] 和 [10, 82]")
    print("合并: [3, 9, 10, 82]")
    print("最终合并: [3, 9, 10, 27, 38, 43, 82]")

if __name__ == "__main__":
    # 基本测试
    test_sorts()
    
    # 调试演示
    debug_demo()
    
    # 递归过程演示
    demonstrate_recursion()