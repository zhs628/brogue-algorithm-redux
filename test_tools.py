# 测试用工具

from array2d import array2d
import traceback
import random
import time
from collections import defaultdict
import time

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
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# Color Name	    Foreground Color Code	Background Color Code
# Black	            30	                    40
# Red	            31	                    41
# Green	            32	                    42
# Yellow	        33	                    43
# Blue	            34	                    44
# Magenta	        35	                    45
# Cyan	            36	                    46
# White	            37	                    47
# Default	        39	                    49
# Reset	            0	                    0
# Bright Black	    90	                    100
# Bright Red	    91	                    101
# Bright Green	    92	                    102
# Bright Yellow	    93	                    103
# Bright Blue	    94	                    104
# Bright Magenta	95	                    105
# Bright Cyan	    96	                    106
# Bright White	    97	                    107
    
    # (symbol, fg, bg)
    palette = {
        0: (".", 30, 0),
        1: ("1", 0, 41),
        2: ("2", 0, 42),
        3: ("3", 0, 43),
    }

    print(message)
    for y in range(grid.height):
        for x in range(grid.width):
            symbol, fg, bg = palette[grid[x, y]]
            symbol = symbol + ' '
            if fg == 0:
                print(f"\x1b[0;{bg}m{symbol}\x1b[0m", end="")
            else:
                print(f"\x1b[0;{fg}m{symbol}\x1b[0m", end="")
        print()


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


from collections import defaultdict


class ExecutionProfiler:
    def __init__(self):
        self.records = {} 

    def record_start(self, layer: int, record_id: int, message: str):
        if layer not in self.records:
            self.records[layer] = {}
        if record_id not in self.records[layer]:
            self.records[layer][record_id] = {
                'message': message,
                'count': 0,
                'total_time': 0.0,
                'start_time': None
            }
        self.records[layer][record_id]['start_time'] = time.time()

    def record_end(self, layer: int, record_id: int):
        end_time = time.time()
        record = self.records[layer][record_id]
        start_time = record['start_time']
        elapsed_time = end_time - start_time
        record['total_time'] += elapsed_time
        record['count'] += 1
        record['start_time'] = None 

    def __str__(self):
        output = []
        for layer, layer_records in sorted(self.records.items()):
            indent = '  |  ' * (layer+1) 
            for record_id, record in sorted(layer_records.items()):
                output.append(
                    f"{indent[:-3]}-----Layer {layer}, Record {record_id}:\n"
                    f"{indent}  message:    {record['message']}\n"
                    f"{indent}  count:      {record['count']}\n"
                    f"{indent}  total_time: {record['total_time']:0.8f}\n"
                    f"{indent}  avg_time:   {record['total_time'] / record['count']:0.8f}\n"
                    f"{indent}"
                )
        return '\n'.join(output)



if __name__ == "__main__":

    profiler = ExecutionProfiler()
    def func():
        for i in range(1000):
            profiler.record_start(layer=1, record_id=0, message="外层循环")  # layer和record_id的组合能够唯一确定一个record, 每一层layer中的id都是相互独立的
            if i % 2 == 1:
                for j in range(1000):
                    profiler.record_start(layer=2, record_id=0, message="单数循环")
                    j + 1
                    profiler.record_end(layer=2, record_id=0)
            else:
                for j in range(1000):
                    profiler.record_start(layer=2, record_id=1, message="双数循环")
                    j + 1
                    profiler.record_end(layer=2, record_id=1)
            profiler.record_end(layer=1, record_id=0)

    profiler.record_start(layer=0, record_id=0, message="func")
    func()
    profiler.record_end(layer=0, record_id=0)


    print(profiler)
