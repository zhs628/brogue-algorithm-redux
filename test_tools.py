# 测试用工具

from array2d import array2d
import traceback
import random
import time
from collections import defaultdict

def _grid_draw_str(grid):
    line_list = []
    for row in range(grid.n_rows):
        char_list = []
        for col in range(grid.n_cols):
            c = str(grid[col, row])
            if len(c) < 2:
                c = ' ' * (2 - len(c)) + c
            char_list.append(c)
        line_list.append(''.join(char_list))
    return '\n'.join(line_list)

def _random_selection(original_list, ratio):
    num_elements = int(len(original_list) * ratio)
    selected_elements = set()
    while len(selected_elements) < num_elements:
        selected_element = random.choice(original_list)
        selected_elements.add(selected_element)
    return list(selected_elements)


def print_grid(grid: array2d[int], symbols=".+#@", message="------------------------"):
    counter = defaultdict(int)

    for x in range(grid.width):
        for y in range(grid.height):
            counter[grid[x, y]] += 1

    sorted_elements = sorted(
        counter, key=lambda x: counter[x], reverse=True
    )

    symbol_dict = {}  # {element: symbol}
    for i in range(max(len(sorted_elements), len(symbols))):
        key = sorted_elements[i] if i < len(sorted_elements) else None
        value = symbols[i] if i < len(symbols) else sorted_elements[i]
        symbol_dict[key] = value

    print(message)
    grid.map(symbol_dict.__getitem__).draw(width=2)



def _test(args):
    w,h, func, test_count, ignore_assertion_error, print_exception = args
    passed_set = True
    avg_time_count_add = 0
    avg_time_sum_add = 0
    all_scales_passed_set = True
    all_scales_failed_set = True
    for i in range(test_count):
        try:
            try:
                start_time = time.time()
                func(array2d(w, h))
                end_time = time.time()
                avg_time_count_add += 1
                avg_time_sum_add += end_time - start_time
                all_scales_failed_set = False
            except AssertionError:
                if not ignore_assertion_error:
                    raise Exception("AssertionError")
            all_scales_failed_set = False
        except Exception as e:
            if print_exception:
                traceback.print_exc()
            passed_set = False
            all_scales_passed_set = False
            break
    return passed_set, avg_time_count_add, avg_time_sum_add, all_scales_passed_set, all_scales_failed_set


def test_all_rooms(
    test_count=30,
    grid_width_range=None,
    grid_height_range=None,
    selection_ratio=0.1,
    print_exception=False,
    ignore_assertion_error=True,
    selected_func_name=None,
    mulity_process_count=None \
):
    # 为了保证算法的正确性, 可以使用本测试函数来覆盖所有可能的参数值
    # 待测函数的通过率视图的每个点(x,y)表示该次测试传入的grid是 array2d(x,y)
    # 只有待测试函数存在不通过的测试样例时, 才会展示通过率视图
    # 图例:
    # passed: "·"
    # failed: "×"
    # not tested: " "
    

    
    grid_width_range = grid_width_range or (15, 40)
    grid_height_range = grid_height_range or (15, 40)
    
    from Architect2 import Rooms

    print(f"---- Testing functions in Architect2.Rooms  (ignore_assertion_error={ignore_assertion_error})")

    selected_func_name = selected_func_name or ['brogue']
    
    function_list = [
        (name, obj) \
        for name, obj in Rooms.__dict__.items() \
        if "design" in name and not name.startswith('_') and (sum([int(sub_name in name) for sub_name in selected_func_name])) \
    ]
    
    print('\t Will test:')
    print('\t\t ' + '\n\t\t '.join([name for name, _ in function_list]))
    print()
    
    all_func_passed = True
    for i, func_tuple in enumerate(function_list):
        name, func = func_tuple
        

        
        print(f"\t---- Testing: {name} ({i+1}/{len(function_list)})")

        passing_scale = array2d(
            grid_width_range[1] + 1, grid_height_range[1] + 1, default=" "
        )


        args = []
        for w in range(grid_width_range[0], grid_width_range[1] + 1):
            for h in range(grid_height_range[0], grid_height_range[1] + 1):
                args.append((w, h, func, test_count, ignore_assertion_error, print_exception))

        
        args = _random_selection(args, selection_ratio)
        if mulity_process_count is not None:
            from tqdm import tqdm
            import multiprocessing
            with multiprocessing.Pool(mulity_process_count) as p:
                res_list = list(tqdm(p.imap(_test, args), total=len(args)))
            
        else:
            res_list = []
            for arg in args:
                res_list.append(_test(arg))

        avg_time_sum = 0
        avg_time_count = 0
        all_scales_passed = True
        all_scales_failed = True
        for i, arg in enumerate(args):
            w,h, func, test_count, ignore_assertion_error, print_exception = arg
            
            passed, avg_time_count_add, avg_time_sum_add, all_scales_passed_set, all_scales_failed_set = res_list[i]
            
            if passed:
                passing_scale[w, h] = "·"
            else:
                passing_scale[w, h] = "X"
            
            avg_time_count += avg_time_count_add
            avg_time_sum += avg_time_sum_add
            
            if all_scales_passed:
                all_scales_passed = all_scales_passed_set
            if all_scales_failed:
                all_scales_failed = all_scales_failed_set

        if avg_time_count > 0:
            avg_time = avg_time_sum / avg_time_count
            print(f"\t average: {avg_time:.6f} s")
        else:
            print(f"\t average: N/A")
        if all_scales_passed:
            print("\t passed")
        else:
            if all_scales_failed:
                print(f"\t\t All tests failed!")
            else:
                print(f"\t\t Some test cases failed!")
            s1 = (str(' '.join([str(num)[-1] for num in range(passing_scale.width)])) + '\n \n' + _grid_draw_str(passing_scale))
            s2 = '\n\t\t'.join([str(i-2 if i-2 >= 0 else ' ')[-1] + ' ' + line for i,line in enumerate(s1.split('\n'))])
            print('\t\t ' + s2)
    if all_func_passed:
        print("-------- All tests passed!")
    else:
        print("-------- Some tests failed!")