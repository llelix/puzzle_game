import os
from constants import RED, RESET
import time

def clear_screen():
    """清屏函数"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')

def print_keyboard(keyboard_layout, cursor_pos, step_count):
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


def show_fireworks():
    """显示烟花动画"""
    fireworks = [
        r"""
           \ | /
         '-.;;;.-'
          -=====-
           / | \
        """,
        r"""
           \ | /
         '-.@@@.-'
          -=====-
           / | \
        """,
        r"""
           \ | /
         '-.+++.-'
          -=====-
           / | \
        """
    ]
    for _ in range(5):  # 重复 5 次烟花动画
        for firework in fireworks:
            clear_screen()
            print(firework)
            time.sleep(0.3)