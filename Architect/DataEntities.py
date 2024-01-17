# 定义存储用的数据结构
from typing import Any, Callable
from array2d import array2d

class Grid(array2d):
    
    def __getitem__(self, indices):  # [x, y] [x1:x2, y1:y2] 
        error = TypeError("Invalid indexing type. Must use a tuple with two indices or slices.")
        
        if not len(indices) == 2:
            raise error
        
        if not isinstance(indices[0], (slice, int)) or not isinstance(indices[1], (slice, int)):
            raise error
        
        x_range = None
        x = indices[0] if isinstance(indices[0], int) else None
        if x is None:
            x_slice = indices[0]
            x_range = range(x_slice.start if x_slice.start is not None else 0, x_slice.stop if x_slice.stop is not None else self.n_cols, x_slice.step if x_slice.step is not None else 1)
            
        y_range = None
        y = indices[1] if isinstance(indices[1], int) else None
        if y is None:
            y_slice = indices[1]
            y_range = range(y_slice.start if y_slice.start is not None else 0, y_slice.stop if y_slice.stop is not None else self.n_rows, y_slice.step if y_slice.step is not None else 1)
        
        if x_range is not None and y_range is not None:
            sub_array = Grid(len(x_range), len(y_range))
            for new_y, self_y in enumerate(y_range):
                for new_x, self_x in enumerate(x_range):
                    sub_array.__setitem__((new_x, new_y), self.__getitem__((self_x,self_y)))
            return sub_array
        
        if x is not None and y is not None:
            return super(Grid, self).__getitem__((x, y))
        
        if x_range is not None and y is not None:
            sub_list = []
            for self_x in x_range:
                sub_list.append(super(Grid, self).__getitem__((self_x, y)))
            return sub_list
        
        if x is not None and y_range is not None:
            sub_list = []
            for self_y in y_range:
                sub_list.append(super(Grid, self).__getitem__((x, self_y)))
            return sub_list

    def map1d(self, f) -> 'Grid':
        new_a = Grid(self.n_cols, self.n_rows)
        for i in range(self.n_cols * self.n_rows):
            new_a.data[i] = f(i, self.data[i])
        return new_a
    
    def map2d(self, f) -> 'Grid':
        new_a = Grid(self.n_cols, self.n_rows)
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                new_a[col, row] = f(col, row, self[col, row])
        return new_a
    
    def copy(self) -> 'Grid':
        new_a= Grid(self.n_cols, self.n_rows)
        new_a.data = self.data.copy()
        return new_a
    
    def transpose(self) -> 'Grid':
        new_a = Grid(self.n_rows, self.n_cols)
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                new_a[row, col] = self[col, row]
        return new_a
    
    def shape(self) -> tuple: # (n_cols, n_rows)
        return (self.width, self.height)
    
    def element_frequency(self) -> dict:
        '''
        统计每个值出现的次数
        返回一个字典，字典的键是元素，键的值是该元素出现的次数
        '''
        frequency_dict = {}
        
        def append_to_dict(_, element):
            if element in frequency_dict:
                frequency_dict[element] += 1
            else:
                frequency_dict[element] = 1
        
        self.map1d(append_to_dict)
        
        return frequency_dict 
    
    
    def show(self, symbols:list = ['.', '+', '#']):
        frequency_dict = self.element_frequency()
        sorted_elements = sorted(frequency_dict, key=lambda x: frequency_dict[x], reverse=True)
        symbol_tuples = [(sorted_elements[i] if i < len(sorted_elements) else None, symbols[i] if i < len(symbols) else sorted_elements[i]) for i in range(max(len(sorted_elements), len(symbols)))]


        symbol_dict = {}  # {element: symbol}
        for key, value in symbol_tuples:
            symbol_dict[key] = value
        def replace_element_with_symbol(_, __, element):
            return symbol_dict[element]
        
        self.copy().map2d(replace_element_with_symbol).draw(width=2)