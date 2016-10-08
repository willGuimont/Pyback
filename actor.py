import pyautogui


class Actor:
    def __init__(self, actions_file, pause=0, duration=0.5, tween=pyautogui.easeInCubic, fail_safe=False):
        pyautogui.PAUSE = pause
        pyautogui.FAILSAFE = fail_safe

        self.__action_file = actions_file
        self.__duration = duration
        self.__tween = tween
        self.__lines = None
        self.__param = None

    def act(self):
        # Parse info before running to reduce latency between actions
        with open(self.__action_file, 'r') as file:
            self.__lines = file.readlines()
            self.__param = list()
            for l in self.__lines:
                self.__param.append(l.split(','))
        for cmd, arg1, arg2 in self.__param:
            if "m" in cmd:
                x = int(arg1)
                y = int(arg2)

                pyautogui.moveTo(x, y, duration=self.__duration, tween=self.__tween)

                if "l" in cmd:
                    if 'd' in cmd:
                        pyautogui.mouseDown(button='left')
                    elif 'u' in cmd:
                        pyautogui.mouseUp(button='left')
                elif "r" in cmd:
                    if 'd' in cmd:
                        pyautogui.mouseDown(button='right')
                    elif 'u' in cmd:
                        pyautogui.mouseUp(button='right')
            elif 'k' in cmd:
                if arg1 == "0":
                    # TODO parse arg2 to find real key (see http://pyautogui.readthedocs.io/en/latest/keyboard.html)
                    key = int(arg1)
                else:
                    key = int(arg1)

                if 'd' in cmd:
                    pyautogui.keyDown(chr(key))
                elif 'u' in cmd:
                    pyautogui.keyUp(chr(key))
