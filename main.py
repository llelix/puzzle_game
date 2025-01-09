import keyboard
import os
import random

# 初始化光标位置
cursor_position = 4  # 默认在数字 4 的位置

# 数字键盘布局（空位用 "_" 表示）
keyboard_layout = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "_"]
]

# 初始化步数计数器
step_count = 0

# ANSI 转义序列
RED = "\033[91m"  # 红色
RESET = "\033[0m"  # 重置颜色

def clear_screen():
    """清屏函数"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')

def print_keyboard(cursor_pos):
    """打印键盘布局，并标记光标位置"""
    clear_screen()  # 清屏
    print("*************")
    for i in range(3):
        row = ""
        for j in range(3):
            cell = keyboard_layout[i][j]
            if i * 3 + j + 1 == cursor_pos:
                row += f"[{RED}{cell}{RESET}]"  # 标记光标位置为红色
            else:
                row += f" {cell} "
        print(row)
    print("*************")
    print(f"步数: {step_count}")
    print("按下上下左右键移动光标，按下 'space' 选中数字与空格交换，按下 'r' 打乱排序，按下 'q' 退出")

def shuffle_layout():
    """打乱键盘布局"""
    global keyboard_layout, step_count
    # 将二维列表扁平化为一维列表
    flat_layout = [cell for row in keyboard_layout for cell in row]
    # 打乱顺序
    random.shuffle(flat_layout)
    # 重新填充二维列表
    keyboard_layout = [flat_layout[i*3:(i+1)*3] for i in range(3)]
    # 重置步数
    step_count = 0

def swap_with_empty():
    """将当前光标所在的数字与相邻的空格交换"""
    global cursor_position, keyboard_layout, step_count
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
        return  # 如果没有空位，直接返回

    # 找到光标的位置
    cursor_row = (cursor_position - 1) // 3
    cursor_col = (cursor_position - 1) % 3

    # 检查光标位置是否与空位相邻
    if (abs(cursor_row - empty_pos[0]) + abs(cursor_col - empty_pos[1])) == 1:
        # 交换内容
        keyboard_layout[cursor_row][cursor_col], keyboard_layout[empty_pos[0]][empty_pos[1]] = \
            keyboard_layout[empty_pos[0]][empty_pos[1]], keyboard_layout[cursor_row][cursor_col]
        # 增加步数
        step_count += 1

def main():
    global cursor_position, step_count
    print_keyboard(cursor_position)

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key == 'q':
                print("退出程序")
                break
            elif key == 'r':
                shuffle_layout()  # 打乱键盘布局
                print_keyboard(cursor_position)
            elif key == 'space':
                swap_with_empty()  # 选中数字与空格交换
                print_keyboard(cursor_position)
            elif key in ['up', 'down', 'left', 'right']:
                # 移动光标
                if key == 'up' and cursor_position > 3:
                    cursor_position -= 3
                elif key == 'down' and cursor_position < 7:
                    cursor_position += 3
                elif key == 'left' and cursor_position not in [1, 4, 7]:
                    cursor_position -= 1
                elif key == 'right' and cursor_position not in [3, 6, 9]:
                    cursor_position += 1
                print_keyboard(cursor_position)

if __name__ == "__main__":
    main()