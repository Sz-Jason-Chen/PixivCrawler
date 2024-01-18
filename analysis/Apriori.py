import math
import threading
import time
# 定义一个函数，接受一个列表和一个分组数量作为参数


def split_list(lst, num_groups):
    # 计算每个分组应该包含的元素个数和余数
    group_size = len(lst) // num_groups # 整除
    remainder = len(lst) % num_groups # 取余
    # 创建一个空列表，用于存放分组后的结果
    result = []
    # 使用一个循环，从原始列表中切片出相应的元素，添加到结果列表中
    start = 0 # 起始索引
    for i in range(num_groups):
        # 如果还有余数，就多分配一个元素
        if remainder > 0:
            end = start + group_size + 1 # 结束索引
            remainder -= 1 # 余数减一
        else:
            end = start + group_size # 结束索引
        # 切片出元素，添加到结果列表中
        result.append(lst[start:end])
        # 更新起始索引
        start = end
    # 返回结果列表
    return result

def get_item_set(data):
    '''
    获取项的字典
    :param data: 数据集
    :return: 项的字典
    '''
    item_set = set()
    for d in data:
        item_set = item_set | set(d)
    return item_set

def get_last_set(list_set):
    result = set()
    for s in list_set:
        result = result.union(s)
    return result
def apriori(item_set, data, min_support=0.50):
    '''
    获取频繁项集
    :param item_set: 项的字典
    :param data: 数据集
    :param min_support: 最小支持度，默认为0.50
    :return: None
    '''
    # 初始化存储非频繁项集的列表
    infrequent_list = []
    # 初始化存储频繁项集的列表
    frequent_list = []
    # 初始化存储频繁项集的支持度的列表
    frequent_support_list = []
    # 遍历获取 n-项集
    for n in range(1, len(item_set) + 1):
        c = []
        supports = []
        if len(frequent_list) == 0:
            # 计算 1-项集
            for item in item_set:
                items = {item}
                support = calc_support(data, items)
                # 如果支持度大于等于最小支持度就为频繁项集
                if support >= min_support:
                    c.append(items)
                    supports.append(support)
                else:
                    infrequent_list.append(items)
        else:
            # 计算 n-项集，n > 1
            for last_items in frequent_list[-1]:
                last_set = get_last_set(frequent_list[-1])
                for item in item_set:
                    if item in last_set and item not in last_items:
                        items = last_items.copy()
                        items.add(item)
                        # 如果items的子集没有非频繁项集才计算支持度
                        if is_infrequent(infrequent_list, items) is False:
                            support = calc_support(data, items)
                            # 如果支持度大于等于最小支持度就为频繁项集
                            if support >= min_support:
                                c.append(items)
                                supports.append(support)
                            else:
                                infrequent_list.append(items)
        c = [set(item) for item in set(frozenset(item) for item in c)]
        frequent_list.append(c)
        frequent_support_list.append(supports)
        print(f"{n}-项集: {c} , 支持度分别为: {supports}")
    return infrequent_list, frequent_list, frequent_support_list



def muti_thread_apriori(item_set, data, min_support=0.50):
    '''
    获取频繁项集
    :param item_set: 项的字典
    :param data: 数据集
    :param min_support: 最小支持度，默认为0.50
    :return: None
    '''
    #使用互斥锁机制保证线程间对共享变量访问互斥
    c_lock = threading.Lock()
    sup_lock = threading.Lock()
    inf_lock = threading.Lock()
    # 初始化存储非频繁项集的列表
    infrequent_list = []
    # 初始化存储频繁项集的列表
    frequent_list = []
    # 初始化存储频繁项集的支持度的列表
    frequent_support_list = []
    # 遍历获取 n-项集
    for n in range(1, len(item_set) + 1):
        c = []
        supports = []

        def thread_apriori(item_set, last_list, last_set, data, min_support):
            nonlocal c
            nonlocal supports
            nonlocal infrequent_list
            for last_items in last_list:
                for item in item_set:
                    if item in last_set and item not in last_items:
                        items = last_items.copy()
                        items.add(item)
                        # 如果items的子集没有非频繁项集才计算支持度
                        if is_infrequent(infrequent_list, items) is False:
                            support = calc_support(data, items)
                            # 如果支持度大于等于最小支持度就为频繁项集
                            if support >= min_support:
                                c_lock.acquire()
                                sup_lock.acquire()

                                c.append(items)
                                supports.append(support)

                                c_lock.release()
                                sup_lock.release()
                            else:
                                inf_lock.acquire()
                                infrequent_list.append(items)
                                inf_lock.release()


        if len(frequent_list) == 0:
            # 计算 1-项集
            for item in item_set:
                items = {item}
                support = calc_support(data, items)
                # 如果支持度大于等于最小支持度就为频繁项集
                if support >= min_support:
                    c.append(items)
                    supports.append(support)
                else:
                    infrequent_list.append(items)
        else:
            last_set = get_last_set(frequent_list[-1])
            # 计算 n-项集，n > 1
            thread_pool = []
            thread_list = split_list(frequent_list[-1],8)
            for thread in thread_list:
                t = threading.Thread(target=thread_apriori,kwargs={"item_set":item_set,"last_list":thread,"data":data,"min_support":min_support,"last_set":last_set})
                thread_pool.append(t)
                t.start()
            for t in thread_pool:
                t.join()

        c = [set(item) for item in set(frozenset(item) for item in c)]
        frequent_list.append(c)
        frequent_support_list.append(supports)
        print(f"{n}-项集: {c} , 支持度分别为: {supports}")
    return infrequent_list, frequent_list, frequent_support_list


def is_infrequent(infrequent_list, items):
    '''
    判断是否属于非频繁项集的超集
    :param infrequent_list: 非频繁项集列表
    :param items: 项集
    :return: 是否属于非频繁项集的超集
    '''
    for infrequent in infrequent_list:
        if infrequent.issubset(items):
            return True
    return False


def calc_support(data, items):
    '''
    计算 support
    :param data: 数据集
    :param items: 项集
    :return: 计算好的支持度
    '''
    cnt = 0
    for d in data:
        if items.issubset(d):
            cnt += 1
    return cnt / len(data)


def generate_rules(frequent_list, data, min_confidence=0.60):
    '''
    根据频繁项集和最小置信度生成规则
    :param frequent_list: 存储频繁项集的列表
    :param data: 数据集
    :param min_confidence: 最小置信度
    :return: 规则
    '''
    rule_key_set = set()
    rules = []
    for frequent in frequent_list:
        for items in frequent:
            if len(items) > 1:
                for n in range(1, math.ceil(len(items) / 2) + 1):
                    front_set_list = get_all_combine(list(items), n)
                    for front_set in front_set_list:
                        back_set = items - front_set
                        confidence = calc_confidence(front_set, items, data)
                        if confidence >= min_confidence:
                            rule = (front_set, back_set, confidence)
                            key = f'{front_set} ==> {back_set} , confidence: {confidence}'
                            if key not in rule_key_set:
                                rule_key_set.add(key)
                                rules.append(rule)
                                print(f"规则{len(rules)}: {key}")
    return rules


def get_all_combine(data_set, length):
    '''
    在指定数据集种获取指定长度的所有组合
    :param data_set: 数据集
    :param length: 指定的长度
    :return: 所有符合约束的组合
    '''

    def dfs(cur_index, cur_arr):
        if cur_index < len(data_set):
            cur_arr.append(data_set[cur_index])
            if len(cur_arr) == length:
                combine_list.append(set(cur_arr))
            else:
                for index in range(cur_index + 1, len(data_set)):
                    dfs(index, cur_arr.copy())

    combine_list = []

    for start_index in range(len(data_set)):
        dfs(start_index, [])

    return combine_list


def calc_confidence(front_set, total_set, data):
    '''
    计算规则 X==>Y 的置信度
    :param front_set: X
    :param total_set: X ∪ Y
    :param data: 数据集
    :return: 返回规则 X==>Y 的置信度
    '''
    front_cnt = 0
    total_cnt = 0
    for d in data:
        if front_set.issubset(d):
            front_cnt += 1
        if total_set.issubset(d):
            total_cnt += 1
    return total_cnt / front_cnt

'''
if __name__ == '__main__':
    # 记录开始时间
    s = time.time()

    # 数据集
    data = [
        ['1', '3', '4'],
        ['2', '3', '5'],
        ['1', '2', '3', '5'],
        ['2', '5']
    ]
    # 获取项的字典
    item_set = get_item_set(data)
    print("项的字典:", item_set)

    # 根据 Apriori算法 获取 n-频繁项集
    infrequent_list, frequent_list, frequent_support_list =  muti_thread_apriori(item_set, data, min_support=0.50)
    #print(frequent_list)
    # 生成规则
    rule_set = generate_rules(frequent_list, data, min_confidence=0.60)

    # 输出总用时
    print("总用时:", (time.time() - s), "s")
'''