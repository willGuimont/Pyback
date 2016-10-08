from pyxHook import HookManager
import time as pytime


def _record_event(event):
    try:
        key = event.Key
        if Composer._exit_key_enabled and key == Composer._exit_key:
            Composer.stop = True
            return
    except:
        pass

    # TODO handle specials keys --> pass key name too?
    event_name = event.MessageName
    if "mouse left down" in event_name:
        Composer._file.write("lmd,")
    elif "mouse left up" in event_name:
        Composer._file.write("lmu,")
    elif "mouse right down" in event_name:
        Composer._file.write("rmd,")
    elif "mouse right up" in event_name:
        Composer._file.write("rmu,")
    elif "key down" in event_name:
        Composer._file.write("kd,")
    elif "key up" in event_name:
        Composer._file.write("ku,")

    try:
        pos = event.Position
        Composer._file.write(str(pos[0]) + "," + str(pos[1]) + '\n')
    except:
        pass

    try:
        ascii = event.Ascii
        key = event.Key
        # To be consistent with pos information
        Composer._file.write(str(ascii) + "," + str(key) + '\n')
    except:
        pass


class Composer:
    _file = None
    _exit_key = None
    _instanced = False
    _stop = False
    _exit_key_enabled = True

    def __init__(self, actions_files, exit_key='q', time=None):
        if time is not None:
            Composer._exit_key_enabled = False

        if Composer._instanced:
            print("Cannot create more than one Composer at the time")
            return
        Composer.instanced = True
        Composer.exit_key = exit_key
        self.__action_file = actions_files
        Composer._file = open(self.__action_file, 'w')
        self.__hm = HookManager()
        self.__hm.HookMouse()
        self.__hm.HookKeyboard()
        self.__hm.KeyDown = _record_event
        self.__hm.KeyUp = _record_event
        self.__hm.MouseAllButtonsDown = _record_event
        self.__hm.MouseAllButtonsUp = _record_event

        self.__time = time
        self.__stop_time = 0
        self.__running = False

    def __del__(self):
        self.stop()
        pytime.sleep(0.5)
        Composer._file.close()
        Composer._instanced = False

    def is_running(self):
        return self.__running

    def record(self, time=None):
        Composer._stop = False
        if time is not None:
            self.__time = time
        self.__running = True
        self.__hm.start()
        if self.__time is not None:
            self.__stop_time = pytime.time() + self.__time

    def stop(self):
        Composer._file.close()
        self.__running = False
        self.__hm.cancel()
        self.__time = None

    @staticmethod
    def should_stop():
        return Composer._stop

    def update(self):
        if self.__time is not None:
            if pytime.time() >= self.__stop_time:
                Composer._stop = True

        if self.should_stop():
            self.stop()
