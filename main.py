from math import log2
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty

class MainGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        
        self.N = ""
        self.i = ""
        self.I = ""
        self.K = ""

        #Блокирует TextInput
        #При изменении TextInput через функция update_text_input вызывается функция (переменная)_input_update, что может вызвать бесконечную рекурсию
        self.block = False

        #Кол-во столбов и рядов MainGrid
        self.cols = 1
        self.rows = 3

        #GridLayout, на котором расположены все TextInput и все Label
        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.rows = 4

        #input_filter="float" - TextInput с таким атрибутом будет принимать только цифры и точка

        self.N_label = Label(text="Введите N:", color=(0,0,0,1), size_hint=(1, 0.3), font_size=40)
        self.inside.add_widget(self.N_label)
        self.N_input = TextInput(multiline=False,input_filter="float", size_hint=(1, 0.3), font_size=50)
        self.N_input.padding_y = [self.N_input.height / 2.0 - (self.N_input.line_height / 2.0) * len(self.N_input._lines) - 10, 0]

        #При изменении текста в N_input, будет вызываться функция N_input_update
        self.N_input.bind(text=self.N_input_update)
        self.inside.add_widget(self.N_input)


        self.i_label = Label(text="Введите i:", color=(0,0,0,1), size_hint=(1, 0.3), font_size = 40)
        self.inside.add_widget(self.i_label)
        self.i_input = TextInput(multiline=False,input_filter="float", size_hint=(1, 0.3), font_size = 40)
        self.i_input.padding_y = [self.i_input.height / 2.0 - (self.i_input.line_height / 2.0) * len(self.i_input._lines) - 10, 0]

        #При изменении текста в i_input, будет вызываться функция i_input_update
        self.i_input.bind(text=self.i_input_update)
        self.inside.add_widget(self.i_input)


        self.I_label = Label(text="Введите I:", color=(0,0,0,1), size_hint=(1, 0.3), font_size = 40)
        self.inside.add_widget(self.I_label)
        self.I_input = TextInput(multiline=False,input_filter="float", size_hint=(1, 0.3), font_size = 40)
        self.I_input.padding_y = [self.I_input.height / 2.0 - (self.I_input.line_height / 2.0) * len(self.I_input._lines) - 10, 0]

        #При изменении текста в I_input, будет вызываться функция I_input_update
        self.I_input.bind(text=self.I_input_update)
        self.inside.add_widget(self.I_input)


        self.K_label = Label(text="Введите K:", color=(0,0,0,1), size_hint=(1, 0.3), font_size = 40)
        self.inside.add_widget(self.K_label)
        self.K_input = TextInput(multiline=False,input_filter="float", size_hint=(1, 0.3), font_size = 40)
        self.K_input.padding_y = [self.K_input.height / 2.0 - (self.K_input.line_height / 2.0) * len(self.K_input._lines) - 10, 0]
        #При изменении текста в K_input, будет вызываться функция K_input_update
        self.K_input.bind(text=self.K_input_update)        
        self.inside.add_widget(self.K_input)

        self.add_widget(self.inside)

        #Лейбл с копирайтом, который находится на MainGrid
        self.add_widget(Label(text="Сделано Арсением Стариковы vk@sv_n_nr", color=(200, 200, 200, 1), size_hint_y= 0.1))

    #В функциях N_input, i_input, I_input, K_input, мы только блокируем для пользователя Text_input. Все вычисления проходят в функции update_variables. 
    #Благодаря блокировки TextInput, мы понимаем, какие переменные мы должны принять за исходные

    def N_input_update(self, instance, value):
        #Защита от рекурсии
        if not self.block:
            #Если мы ввели число
            if len(value) != 0:
                #Когда мы конвертируем "." в float, то мы получим 0.0
                #Защита от 0
                if value[0] == "." or value[0] == "0":
                    self.block = True
                    self.N_input.text = ""
                    self.block = False
                else:
                    self.N = float(value)

                    #Перменная i зависит только N, мы блокируем i_input
                    self.i_input.disabled = True
                    
                    #Если нам извества переменная K, то мы блокируем I_input
                    if self.K_input.text != "" and not self.K_input.disabled: self.I_input.disabled = True
                    #Если нам извества переменная I, то мы блокируем K_input
                    if self.I_input.text != "" and not self.I_input.disabled: self.K_input.disabled = True

                    self.block = True
                    self.update_variables()
                    self.block = False
            #Если мы стёрли число
            else:
                self.N = ""

                self.i = ""
                self.i_input.disabled = False

                #Если нам известная переменная K, и она была введена пользователем, то I мы можем стереть
                if self.K_input.text != "" and self.K_input.disabled:
                    self.I = ""
                    self.I_input.disabled = False
                #Если нам известная переменная I, и она была введена пользователем, то I мы можем стереть
                if self.I_input.text != "" and self.I_input.disabled:
                    self.K = ""
                    self.K_input.disabled = False

                self.update_text_input()             

    def i_input_update(self, instance, value):
        #Защита от рекурсии
        if not self.block:
            #Если мы ввели число
            if len(value) != 0:
                #Когда мы конвертируем "." в float, то мы получим 0.0
                #Защита от 0
                if value[0] == "." or value[0] == "0":
                    self.block = True
                    self.i_input.text = ""
                    self.block = False
                else:
                    self.i = float(value)

                    #Перменная N зависит только i, мы блокируем N_input
                    self.N_input.disabled = True
                    
                    #Если нам извества переменная K, то мы блокируем I_input
                    if self.K_input.text != "" and not self.K_input.disabled: self.I_input.disabled = True
                    #Если нам извества переменная I, то мы блокируем K_input
                    if self.I_input.text != "" and not self.I_input.disabled: self.K_input.disabled = True

                    self.block = True
                    self.update_variables()
                    self.block = False
            #Если мы стёрли число
            else:
                self.i = ""

                self.N = ""
                self.N_input.disabled = False

                #Если нам известная переменная K, и она была введена пользователем, то I мы можем стереть
                if self.K_input.text != "" and self.K_input.disabled:
                    self.I = ""
                    self.I_input.disabled = False
                #Если нам известная переменная I, и она была введена пользователем, то K мы можем стереть
                if self.I_input.text != "" and self.I_input.disabled:
                    self.K = ""
                    self.K_input.disabled = False

                self.update_text_input()    
    
    def I_input_update(self, instance, value):
        #Защита от рекурсии
        if not self.block:
            #Если мы ввели число
            if len(value) != 0:
                #Когда мы конвертируем "." в float, то мы получим 0.0
                #Защита от 0
                if value[0] == "." or value[0] == "0":
                    self.block = True
                    self.I_input.text = ""
                    self.block = False
                else:
                    self.I = float(value)

                    #Если нам известна переменная i, мы можем посчитать переменную K, поэтому мы блокируем поле K_input для пользователя
                    if self.i_input.text != "" and not self.K_input.disabled and self.K_input.text == "": 
                        self.K_input.disabled = True
                    #Если нам известна переменная K, мы можем посчитать переменную i и N, поэтому мы блокируем поля i_input и N_input для пользователя
                    if self.i_input.text == "" and not self.K_input.disabled and self.K_input.text != "":
                        self.i_input.disabled = True
                        self.N_input.disabled = True

                    self.block = True
                    self.update_variables()
                    self.block = False
            #Если мы стёрли
            else:
                self.I = ""

                if self.K_input.text != "":
                    #Если переменная K не была исходной(то есть польхователь её не вводил), мы её стираем
                    if self.K_input.disabled:
                        self.K = ""
                        self.K_input.disabled = False
                    #Если переменная K была исходной(то есть польхователь её не вводил), мы стираем N и i
                    else:
                        self.N = ""
                        self.i = ""
                        self.N_input.disabled = False
                        self.i_input.disabled = False
                
                self.update_text_input()
            
    def K_input_update(self, instance, value):
        #Защита от рекурсии
        if not self.block:
            #Если мы ввели число
            if len(value) != 0:
                #Когда мы конвертируем "." в float, то мы получим 0.0
                #Защита от 0
                if value[0] == "." or value[0] == "0":
                    self.block = True
                    self.K_input.text= ""
                    self.block = False
                else:
                    self.K = float(value)

                    #Если нам известна переменная i, мы можем посчитать переменную I, поэтому мы блокируем поле I_input для пользователя
                    if self.i_input.text != "" and not self.I_input.disabled and self.I_input.text == "": 
                        self.I_input.disabled = True
                    #Если нам известна переменная I, мы можем посчитать переменную i и N, поэтому мы блокируем поля i_input и N_input для пользователя
                    if self.i_input.text == "" and not self.I_input.disabled and self.I_input.text != "":
                        self.i_input.disabled = True
                        self.N_input.disabled = True

                    self.block = True
                    self.update_variables() 
                    self.block = False
            #Если мы стёрли
            else:
                self.K = ""

                if self.I_input.text != "":
                    #Если переменная I не была исходной(то есть польхователь её не вводил), мы её стираем
                    if self.I_input.disabled:
                        self.I = ""
                        self.I_input.disabled = False
                    #Если переменная I была исходной(то есть польхователь её не вводил), мы стираем N и i
                    else:
                        self.N = ""
                        self.i = ""
                        self.N_input.disabled = False
                        self.i_input.disabled = False
                
                self.update_text_input()

    def update_text_input(self):
        #Обновляем text в Text_Input
        #Важно: если данная переменная является исходной(её ввёл пользователь), то мы не должны обновлять TextInput.
        #Т.к может невохможно будет менять исходные переменные
        if self.N_input.disabled or self.N == '': self.N_input.text = str(self.N)
        if self.i_input.disabled or self.i == '': self.i_input.text = str(self.i)
        if self.I_input.disabled or self.I == '': self.I_input.text = str(self.I)
        if self.K_input.disabled or self.K == '': self.K_input.text = str(self.K)

    def update_variables(self):
        #Если N является исходной
        if self.N != "" and not self.N_input.disabled:
            #i всегда зависит от N, и наоборот
            self.i = log2(self.N)

            #log2(N) может равнятся 0, следовательно, i может быть 0, поэтому мы делаем проверку

            #Если I зависищая переменная или пуста, и K нам известна
            if (self.I == "" or self.I_input.disabled) and self.K != "" and self.i != 0.0:
                self.I = self.K * self.i
            #Если K зависищая переменная или пуста, и I нам известна
            if (self.K == "" or self.K_input.disabled) and self.I != "" and self.i != 0.0:
                self.K = self.I / self.i

        #Если i является исходной
        elif self.i != "" and not self.i_input.disabled:
            #i всегда зависит от N, и наоборот
            self.N = 2 ** self.i

            #log2(N) может равнятся 0, следовательно, i может быть 0, поэтому мы делаем проверку

            #Если I зависищая переменная или пуста, и K нам известна
            if (self.I == "" or self.I_input.disabled) and self.K != "" and self.i != 0.0:
                self.I = self.K * self.i
            #Если K зависищая переменная или пуста, и I нам известна
            if (self.K == "" or self.K_input.disabled) and self.I != "" and self.i != 0.0:
                self.K = self.I / self.i

        #Если I является исходной
        elif self.I != "" and not self.I_input.disabled:
            #Если K зависищая переменная или пуста, и i нам известна
            if self.K == "" or self.K_input.disabled:
                if self.i != "" and self.i != 0.0: self.K = self.I / self.i
            #Если K является исходной
            else:
                if self.i == "" or (self.i_input.disabled and self.N_input.disabled):
                    self.i = self.I / self.K
                    self.N = 2 ** self.i

        #Если K является исходной
        elif self.K != "" and not self.K_input.disabled:
            #Если I зависищая переменная или пуста, и i нам известна
            if self.I == "" or self.I_input.disabled:
                if self.i != "" and self.i != 0.0: self.I = self.K * self.i
            #Если I является исходной
            else:
                if self.i == "" or (self.i_input.disabled and self.N_input.disabled):
                    self.i = self.I / self.K
                    self.N = 2 ** self.i 
        
        self.update_text_input()

#Разобраться с kivy language и переделать приложение 
"""class MainGrid_(Widget):
    n_input = ObjectProperty(None)
    i_input = ObjectProperty(None)
    ii_input = ObjectProperty(None)
    k_input = ObjectProperty(None)"""

class infaApp(App):
    def build(self):
        #Установка цвета заднего фона
        Window.clearcolor = (1, 1, 1, 1)
        #Функция, которая создаёт все uix объекты
        return MainGrid()

if __name__ == '__main__':
    #Создаём объект приложения и запускаем его
    infaApp().run()
