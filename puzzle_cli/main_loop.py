import keyboard
from constants import INITIAL_CURSOR_POSITION, INITIAL_KEYBOARD_LAYOUT
from utils import print_keyboard, clear_screen, show_fireworks
from game_logic import shuffle_layout, swap_with_empty, check_win

def main():
    # 初始化游戏状态
    cursor_position = INITIAL_CURSOR_POSITION
    keyboard_layout = [row.copy() for row in INITIAL_KEYBOARD_LAYOUT]  # 深拷贝初始布局
    step_count = 0

    # 打乱键盘布局
    keyboard_layout = shuffle_layout()

    # 打印初始键盘布局
    print_keyboard(keyboard_layout, cursor_position, step_count)

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key == 'q':
                print("退出程序")
                break
            elif key == 'r':
                keyboard_layout = shuffle_layout()  # 打乱键盘布局
                step_count = 0  # 重置步数
                cursor_position = INITIAL_CURSOR_POSITION  # 重置光标位置
                print_keyboard(keyboard_layout, cursor_position, step_count)
            elif key == 'space':
                keyboard_layout, cursor_position, swapped = swap_with_empty(keyboard_layout, cursor_position)
                if swapped:
                    step_count += 1  # 增加步数
                print_keyboard(keyboard_layout, cursor_position, step_count)
                # 检查是否胜利
                if check_win(keyboard_layout):
                    print("恭喜你，胜利了！")
                    show_fireworks()  # 显示烟花动画
                    # 回到开始状态
                    keyboard_layout = shuffle_layout()  # 重新打乱布局
                    step_count = 0  # 重置步数
                    cursor_position = INITIAL_CURSOR_POSITION  # 重置光标位置
                    print_keyboard(keyboard_layout, cursor_position, step_count)
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
                print_keyboard(keyboard_layout, cursor_position, step_count)

if __name__ == "__main__":
    main()