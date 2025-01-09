import random
from constants import INITIAL_KEYBOARD_LAYOUT, WINNING_LAYOUT

def count_inversions(flat_layout):
    """计算逆序数"""
    inversions = 0
    for i in range(len(flat_layout)):
        for j in range(i + 1, len(flat_layout)):
            if flat_layout[i] != "_" and flat_layout[j] != "_" and flat_layout[i] > flat_layout[j]:
                inversions += 1
    return inversions

def shuffle_layout():
    """打乱拼图并确保有解"""
    while True:
        # 生成一个随机排列
        flat_layout = ["1", "2", "3", "4", "5", "6", "7", "8", "_"]
        random.shuffle(flat_layout)

        # 计算逆序数
        inversions = count_inversions(flat_layout)

        # 如果逆序数是偶数，则返回打乱后的布局
        if inversions % 2 == 0:
            return [flat_layout[i*3:(i+1)*3] for i in range(3)]
        # 否则，交换两个非空格数字，使逆序数变为偶数
        else:
            # 找到前两个非空格数字并交换
            for i in range(len(flat_layout)):
                if flat_layout[i] != "_":
                    for j in range(i + 1, len(flat_layout)):
                        if flat_layout[j] != "_":
                            flat_layout[i], flat_layout[j] = flat_layout[j], flat_layout[i]
                            return [flat_layout[i*3:(i+1)*3] for i in range(3)]
                        
                        

def swap_with_empty(keyboard_layout, cursor_position):
    """将当前光标所在的数字与相邻的空格交换"""
    # 找到空位的位置
    empty_pos = None
    for i in range(3):
        for j in range(3):
            if keyboard_layout[i][j] == "_":
                empty_pos = (i, j)
                break
        if empty_pos:
            break
    if not empty_pos:
        return keyboard_layout, cursor_position, False  # 如果没有空位，直接返回

    # 找到光标的位置
    cursor_row = (cursor_position - 1) // 3
    cursor_col = (cursor_position - 1) % 3

    # 检查光标位置是否与空位相邻
    if (abs(cursor_row - empty_pos[0]) + abs(cursor_col - empty_pos[1])) == 1:
        # 交换内容
        keyboard_layout[cursor_row][cursor_col], keyboard_layout[empty_pos[0]][empty_pos[1]] = \
            keyboard_layout[empty_pos[0]][empty_pos[1]], keyboard_layout[cursor_row][cursor_col]
        # 更新光标位置到空位
        cursor_position = empty_pos[0] * 3 + empty_pos[1] + 1
        return keyboard_layout, cursor_position, True
    return keyboard_layout, cursor_position, False

def check_win(keyboard_layout):
    """检查是否胜利"""
    return keyboard_layout == WINNING_LAYOUT