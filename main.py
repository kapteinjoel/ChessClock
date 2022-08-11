import subprocess

import kivy
import time
from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('1.9.0')

class RoundedButton(Button):
    pass

class Settings_Window(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_audio()
        self.controls = []
        with open('Settings.txt', 'r') as file:
            Lines = file.readlines()
            file.close()
            pass
        for line in Lines:
            self.controls.append(line.strip())
        print(self.controls)
        self.buttons = []
        self.current_selection = None
        Clock.schedule_interval(self.keep_window_updated, 1/30)

    def on_enter(self):
        self.current_selection = None
        self.ids.time_controls.clear_widgets()
        self.buttons = []
        self.controls = []
        with open('Settings.txt', 'r') as file:
            Lines = file.readlines()
            file.close()
            pass
        for line in Lines:
            self.controls.append(line.strip())
        for item in self.controls:
            self.buttons.append(RoundedButton(text=item, size_hint=(1, 1), font_size = 45, bold = True, on_press = self.on_option_press, on_release = self.on_option_release))
            self.ids.time_controls.add_widget(self.buttons[self.controls.index(item)])
        height =  190*len(self.buttons)
        self.ids.time_controls.height = height

    def on_leave(self):
        if self.current_selection != None:
            self.current_selection.color = [1, 1, 1, 1]

    def init_audio(self):
        self.pop = SoundLoader.load('pop.wav')
        self.pop.volume = .15

    def add_press(self):
        if self.current_selection is not None:
            self.current_selection.color = [1, 1, 1, 1]
        self.current_selection = None
        self.pop.play()

    def on_use(self):
        if self.current_selection is not None:
            self.current_selection.color = [1, 1, 1, 1]
        self.pop.play()
        with open('Current.txt', 'r') as file:
            lines = file.readlines()

        before, sep, after = self.current_selection.text.partition('|')

        lines[0] = str(sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(before.split(":")))))
        with open('Current.txt', 'w') as file:
            file.writelines(lines)
        file.close()

        if after == '':
            after = '0'

        with open('current_inc.txt', 'w') as file:
            file.writelines(after)
        file.close()

        self.current_selection = None

    def back_press(self):
        if self.current_selection is not None:
            self.current_selection.color = [1,1,1,1]
        self.current_selection = None
        self.pop.play()

    def remove_button(self):
        self.pop.play()
        self.controls.pop(self.controls.index(self.current_selection.text))
        with open('Settings.txt', 'r') as fr:
            lines = fr.readlines()
            with open('Settings.txt', 'w') as fw:
                for line in lines:
                    if line.strip('\n') != str(self.current_selection.text):
                        fw.write(line)
        fr.close()
        fw.close()
        if self.current_selection != None:
            self.buttons.remove(self.current_selection)
            self.current_selection = None
        height = 190*len(self.buttons)
        self.ids.time_controls.height = height
        self.ids.time_controls.clear_widgets()
        for button in self.buttons:
            self.ids.time_controls.add_widget(button)

    def on_option_press(self, *args):
        self.pop.play()
        if self.current_selection != None:
            self.current_selection.color = [1,1,1,1]
        if self.current_selection == args[0]:
            self.current_selection.color = [1, 1, 1, 1]
            self.current_selection = None
        else:
            self.current_selection = args[0]
            args[0].color = [202/255, 173/255, 150/255, 1]

    def on_option_release(self, *args):
        pass

    def keep_window_updated(self, dt):
        if self.current_selection == None:
            self.ids.remove_button.opacity = 0
            self.ids.add_button.opacity = 0
            self.ids.remove_button.disabled = True
            self.ids.add_button.disabled = True
        else:
            self.ids.remove_button.opacity = 1
            self.ids.add_button.opacity = 1
            self.ids.remove_button.disabled = False
            self.ids.add_button.disabled = False

class Time_Control(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mins = 0
        self.secs = 0
        self.inc = 0
        Clock.schedule_interval(self.update, 1 / 30)

    def on_enter(self):
        self.mins = 0
        self.secs = 0
        self.inc = 0
        self.ids.slider1.value = 0
        self.ids.slider2.value = 0
        self.ids.slider3.value = 0

    def back(self):
        self.ids.slider1.value = 0
        self.ids.slider2.value = 0
        self.ids.slider3.value = 0

    def minutes(self, *args):
        self.ids.minute_slider.text = 'Minute(s): {}'.format(int(args[1]))
        self.mins = int(args[1])

    def seconds(self, *args):
        self.ids.second_slider.text = 'Second(s): {}'.format(int(args[1]))
        self.secs = int(args[1])

    def increment(self, *args):
        self.ids.increment_slider.text = 'Increment: {}'.format(int(args[1]))
        self.inc = int(args[1])

    def create_time_control(self):
        value = (self.mins*60)+self.secs

        if (time.strftime('%M:%S', time.gmtime(value)))[0] == '0':
            stime = (time.strftime('%M:%S', time.gmtime(value)))[1:]
        else:
            stime = (time.strftime('%M:%S', time.gmtime(value)))
        controls = []
        with open('Settings.txt', 'r') as file:
            Lines = file.readlines()
            file.close()
            pass
        for line in Lines:
            controls.append(line.strip())

        if stime not in controls:
            with open("Settings.txt", "a") as file:
                if self.inc == 0:
                    file.write(stime+'\n')
                else:
                    file.write(stime+'|'+str(self.inc)+'\n')
                file.close()

            self.ids.slider1.value = 0
            self.ids.slider2.value = 0
            self.ids.slider3.value = 0


    def update(self, dt):
        if self.mins > 0 or self.secs>0:
            self.ids.create_button.disabled = False
            self.ids.create_button.opacity = 1
        else:
            self.ids.create_button.disabled = True
            self.ids.create_button.opacity = 0


class WindowManager(ScreenManager):
    pass

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.click = None
        self.init_audio()
        with open('Current.txt', 'r') as file:
            self.Line = file.readline()
            file.close()
            pass
        with open('current_inc.txt', 'r') as file:
            inc = file.readline()
            file.close()
            pass
        self.increment = int(inc)

        self.turn = None
        self.last_turn = 0
        self.current_selection = self.Line
        self.time_clock_1 = int(self.Line)
        self.time_clock_2 = int(self.Line)
        if (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[0] == '0':
            self.top_label = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[1:]
        else:
            self.top_label = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))
        Clock.schedule_interval(self.update, 1)

    def on_enter(self):
        with open('current_inc.txt', 'r') as file:
            inc = file.readline()
            file.close()
            pass
        self.increment = int(inc)
        with open('Current.txt', 'r') as file:
            Lines = file.readlines()
            file.close()
        if self.current_selection != Lines[0]:
            self.turn = None
            self.ids.pause.text = 'PAUSE'
            self.ids.top_button.disabled = False
            self.ids.lower_button.disabled = False
            self.current_selection = Lines[0]
            self.time_clock_1 = int(Lines[0])
            self.time_clock_2 = int(Lines[0])
            if (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[0] == '0':
                self.top_label = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[1:]
            else:
                self.top_label = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))
            self.ids.top_button.text = self.top_label
            self.ids.lower_button.text = self.top_label

    def init_audio(self):
        self.click = SoundLoader.load('click.wav')
        self.click.volume = 1
        self.pop = SoundLoader.load('pop.wav')
        self.pop.volume = .15

    def settings_press(self):
        if self.turn != 0:
            self.pause()

    def toggle_click_1(self):
        self.click.play()
        if self.turn == 1 or self.turn == None:
            self.time_clock_1 += self.increment
            if (time.strftime('%M:%S', time.gmtime(self.time_clock_1)))[0] == '0':
                self.ids.lower_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_1)))[1:]
            else:
                self.ids.lower_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_1)))
            self.ids.top_button.disabled = False
            self.ids.lower_button.disabled = True
            self.turn = 2

    def toggle_click_2(self):
        self.click.play()
        if self.turn == 2 or self.turn == None:
            self.time_clock_2 += self.increment
            if (time.strftime('%M:%S', time.gmtime(self.time_clock_1)))[0] == '0':
                self.ids.top_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[1:]
            else:
                self.ids.top_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))
            self.ids.top_button.disabled = True
            self.ids.lower_button.disabled = False
            self.turn = 1

    def pause_press(self):
        self.ids.pause.bold = False

    def pause_release(self):
        self.ids.pause.bold = True

    def reset_press(self):
        with open('Current.txt', 'r') as file:
            Lines = file.readlines()
            file.close()

        self.turn = None
        self.ids.top_button.disabled = False
        self.ids.lower_button.disabled = False
        self.current_selection = Lines[0]
        self.time_clock_1 = int(Lines[0])
        self.time_clock_2 = int(Lines[0])
        if (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[0] == '0':
            self.top_label = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[1:]
        else:
            self.top_label = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))
        self.ids.top_button.text = self.top_label
        self.ids.lower_button.text = self.top_label
        self.ids.reset.bold = False
        self.ids.pause.text = 'PAUSE'
        self.pop.play()

    def reset_release(self):
        self.ids.reset.bold = True

    def pause(self):
        if self.turn != 0:
            self.last_turn = self.turn
            if self.turn == 1:
                self.ids.lower_button.disabled = True
                self.ids.pause.text = 'RESUME'
            elif self.turn == 2:
                self.ids.top_button.disabled = True
                self.ids.pause.text = 'RESUME'
            self.pop.play()
        if self.turn == 0:
            self.turn = self.last_turn
            if self.turn == 1:
                self.ids.lower_button.disabled = False
            elif self.turn == 2:
                self.ids.top_button.disabled = False
            self.ids.pause.text = 'PAUSE'
            self.pop.play()
        else:
            if self.turn != None:
                self.pop.play()
                self.turn = 0

    def update(self, dt):
        if self.turn == 1:
            if self.time_clock_1 > 0:
                self.time_clock_1 = self.time_clock_1 - 1
            if (time.strftime('%M:%S', time.gmtime(self.time_clock_1)))[0] == '0':
                self.ids.lower_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_1)))[1:]
            else:
                self.ids.lower_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_1)))
        if self.turn == 2:
            if self.time_clock_2 > 0:
                self.time_clock_2 = self.time_clock_2 - 1
            if (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[0] == '0':
                self.ids.top_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))[1:]
            else:
                self.ids.top_button.text = (time.strftime('%M:%S', time.gmtime(self.time_clock_2)))

class ChessClock(App):
    def build(self):
        Window.clearcolor = (240/255, 240/255, 240/255, 1)
        return Builder.load_file('mainmenu.kv')

if __name__ == '__main__':
    ChessClock().run()