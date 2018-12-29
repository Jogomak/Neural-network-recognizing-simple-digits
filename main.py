# -*- coding: utf-8 -*-
import random
import numpy as np
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GdkPixbuf


class MainWindow():
    #pixels = np.zeros(46, dtype=int)
    pixels = np.array([-1] * 46)
    pixels[45] = 1

    def __init__(self):


        self.get_learning_sample()
        self.initialize_perceptrons()
        self.initialize_window()


    def get_learning_sample(self):
        self.pictures_pixels = np.zeros((121, 46), dtype=int)

        for i in xrange(11):
            for j in xrange(11):
                picture_pixels = np.zeros(46, dtype=int)
                picture_pixbuf = GdkPixbuf.Pixbuf.new_from_file('./images/' + str(i) + str(j) + '.png')

                for k in xrange(45):
                    if ord(picture_pixbuf.get_pixels()[k * 4]) > 0:
                        picture_pixels[k] = -1
                    else:
                        picture_pixels[k] = 1

                picture_pixels[45] = 1

                self.pictures_pixels[i * 10 + j + i] = picture_pixels


    def initialize_perceptrons(self):
        self.perceptrons = []
        for i in xrange(10):
            self.perceptrons += [Perceptron(i)]
        self.perceptrons = np.array(self.perceptrons)

        for i in xrange(10):
            self.perceptrons[i].learn(self.pictures_pixels)


    def initialize_window(self):
        self.pressed_button = 0
        main_window = Gtk.Window()
        event_box_image = Gtk.EventBox()
        table_pixels = Gtk.Table(9, 5)
        main_vbox = Gtk.VBox()
        buttons_hbox = Gtk.HBox()
        self.label_result = Gtk.Label('?')

        self.pixbuf_pixel_white = GdkPixbuf.Pixbuf.new_from_file('./images/blank.png')
        self.pixbuf_pixel_black = GdkPixbuf.Pixbuf.new_from_file('./images/blank.png')
        self.pixbuf_pixel_black.fill(0x000000ff)

        for i in xrange(45):
            table_pixels.attach(Gtk.Image.new_from_pixbuf(self.pixbuf_pixel_white.scale_simple(40, 40, 3)), i % 5,
                                i % 5 + 1, i / 5, i / 5 + 1, Gtk.AttachOptions(2))

        self.pixels = np.array(table_pixels.get_children())

        button = Gtk.Button.new_with_label('baton')
        main_vbox.set_halign(3)
        main_window.set_default_size(300, 400)

        main_window.add(main_vbox)
        event_box_image.add(table_pixels)
        main_vbox.pack_start(event_box_image, False, False, 0)
        main_vbox.pack_start(self.label_result, False, False, 0)
        main_vbox.pack_start(buttons_hbox, False, False, 0)
        buttons_hbox.pack_start(button, False, False, 0)

        main_window.connect("delete-event", Gtk.main_quit)
        event_box_image.connect('button-press-event', self.image_pressed)
        event_box_image.connect('motion-notify-event', self.image_move)

        main_window.show_all()
        Gtk.main()


    def image_pressed(self, event_box, event):
        self.pressed_button = event.button

        self.fill_pixel(event)


    def image_move(self, event_box, event):
        self.fill_pixel(event)


    def fill_pixel(self, position):
        x, y = int(position.x), int(position.y)

        if x > 0 and y > 0 and x < 200 and y < 360:
            if self.pressed_button == 1:
                self.pixels[44 - x / 40 - y / 40 * 5].set_from_pixbuf(self.pixbuf_pixel_black.scale_simple(40, 40, 3))
                MainWindow.pixels[x / 40 + y / 40 * 5] = 1
            else:
                self.pixels[44 - x / 40 - y / 40 * 5].set_from_pixbuf(self.pixbuf_pixel_white.scale_simple(40, 40, 3))
                MainWindow.pixels[x / 40 + y / 40 * 5] = -1

        self.check()


    def check(self):
        answer = ''
        for i in xrange(10):
            if self.perceptrons[i].check(MainWindow.pixels):
                answer += str(i) + ' '

        if answer == '':
            answer = '?'

        self.label_result.set_text(answer)


class Perceptron():
    def __init__(self, recognize):
        self.recognize = recognize
        self.learning_rate = 0.03
        data = []

        for i in xrange(46):
            data += [(random.random() * 2 - 1)]

        self.weights = np.matrix(data, float).transpose()


    def check(self, data_input):
        return (data_input * self.weights) > 0

    def learn(self, pictures_pixels):
        for i in xrange(1500):
            if i % 7 == 0:
                picture_number_first = self.recognize
                picture_number_second = random.randint(0, 10)
            else:
                picture_number_first = random.randint(0, 10)
                picture_number_second = random.randint(0, 10)

            picture_number = picture_number_first * 10 + picture_number_first + picture_number_second

            if picture_number_first == self.recognize:
                correct_answer = 1
            else:
                correct_answer = -1

            if pictures_pixels[picture_number] * self.weights > 0:
                perceptron_answer = 1
            else:
                perceptron_answer = -1

            error = correct_answer - perceptron_answer

            for j in xrange(45):
                self.weights[j] += self.learning_rate * error * pictures_pixels[picture_number][j]
            self.weights[45] += self.learning_rate * error

        errors = 0
        for i in xrange(11):
            for j in xrange(11):
                picture_number = i * 10 + i + j

                if i == self.recognize:
                    correct_answer = 1
                else:
                    correct_answer = -1

                if pictures_pixels[picture_number] * self.weights > 0:
                    perceptron_answer = 1
                else:
                    perceptron_answer = -1

                error = correct_answer - perceptron_answer

                if error != 0:
                    errors += 1

        if errors:
            print self.recognize, errors
            self.learn(pictures_pixels)


if __name__ == '__main__':
    MainWindow()