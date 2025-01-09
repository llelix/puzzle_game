# 接收上下左右按键的控制器


class Controller:
    def on_key_press(self, key):
        if key == 'Up':
            print('Up')
        elif key == 'Down':
            print('Down')
        elif key == 'Left':
            print('Left')
        elif key == 'Right':
            print('Right')