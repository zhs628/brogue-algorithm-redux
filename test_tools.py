
# 测试用工具

from array2d import array2d


def print_grid(grid, symbols:str = '.+#', message='------------------------'):
        symbols = list(symbols)
        frequency_dict = {}
        
        for x in range(grid.width):
            for y in range(grid.height):
                element = grid[x,y]
                if element in frequency_dict:
                    frequency_dict[element] += 1
                else:
                    frequency_dict[element] = 1
        
        sorted_elements = sorted(frequency_dict, key=lambda x: frequency_dict[x], reverse=True)
        symbol_tuples = [(sorted_elements[i] if i < len(sorted_elements) else None, symbols[i] if i < len(symbols) else sorted_elements[i]) for i in range(max(len(sorted_elements), len(symbols)))]


        symbol_dict = {}  # {element: symbol}
        for key, value in symbol_tuples:
            symbol_dict[key] = value
        def replace_element_with_symbol(_, __, element):
            return symbol_dict[element]
        print(message)
        grid.copy().map2d(replace_element_with_symbol).draw(width=2)