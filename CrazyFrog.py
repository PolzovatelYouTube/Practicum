import sys
import random
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class Frog(QGraphicsEllipseItem):
    def __init__(self, x, y, weight, max_jump_distance):
        super().__init__(0, 0, 20, 20)  # размеры лягушки
        self.setPos(QPointF(x, y))  # Начальная позиция лягушки
        self.weight = weight
        self.max_jump_distance = max_jump_distance
        self.setBrush(QBrush(QColor("red")))

    def getPos(self):
        return QGraphicsEllipseItem.pos(self)

    def setPos(self, pos):
        QGraphicsEllipseItem.setPos(self, pos)

    def crazy_jump(self, where):
        z = QPointF(where)
        self.setPos(z)

    #pos = pyqtProperty(QPointF, getPos, setPos)

class LilyPad(QGraphicsEllipseItem):
    def __init__(self, x, y, strength):
        super().__init__(x, y, 30, 30)  # размеры кувшинки
        self.strength = strength
        self.setBrush(QBrush(QColor("green")))

    def fall(self, speed):
        # Смещаем кувшинку вниз на `speed` пикселей
        current_pos = self.pos()
        self.setPos(current_pos.x(), current_pos.y() + speed)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.scene = QGraphicsScene(0, 0, 800, 600) 
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCentralWidget(self.view)

        # Берега
        self.left_shore = 0
        self.right_shore = self.width() - 50
        self.current_shore = 'left'

        # Логика движения
        self.direction = 'right'  # Лягушка начинает с левого берега

        # Создание списка кувшинок
        self.lilies = []

        # Создание лягушки
        self.frog = Frog(0, 300, weight=5, max_jump_distance=150)
        self.scene.addItem(self.frog)

        # Таймер для прыжков лягушки
        self.timer_frog = QTimer()
        self.timer_frog.timeout.connect(self.update_frog_position)
        self.timer_frog.start(500)  # Обновление каждые 0.5 секунды

        # Таймер для падения кувшинок
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lily_pads_position)
        self.timer.start(25)  # Обновление каждые n мс для плавного падения

        # Таймер для добавления новых кувшинок с задержкой
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_lily_pads)
        self.spawn_timer.start()

    def spawn_lily_pads(self):
        self.spawn_timer.start(random.randint(500, 1000))
        # Случайное количество кувшинок от 0 до n
        number_of_lilies = random.randint(1, 7)
        positions = []  # Список для хранения позиций, чтобы избежать пересечения

        for _ in range(number_of_lilies):
            # Случайное положение по оси X, с проверкой на расстояние между кувшинками
            while True:
                x = random.randint(0, self.scene.width() - 30)  # 50 - ширина кувшинки
                if all(abs(x - pos_x) > 40 for pos_x in positions):  # 40 пикселей - минимальное расстояние
                    positions.append(x)
                    break

            # Добавляем кувшинку в сцену на случайной позиции сверху
            strength = random.randint(5, 10)  # Случайная прочность
            lily = LilyPad(x, 0, strength) 
            self.scene.addItem(lily)
            self.lilies.append(lily)

    def update_lily_pads_position(self):
        # Определяем скорость падения
        fall_speed = 2  # Скорость падения кувшинок

        for lily in self.lilies:
            # Падаем с заданной скоростью
            lily.fall(fall_speed)

             # Если кувшинка вышла за пределы окна, удаляем её
            if lily.pos().y() > self.height():
                self.scene.removeItem(lily)
                self.lilies.remove(lily)  # Удаляем из списка кувшинок

    def find_next_lily_pad(self):
        possible_lilies = []
        current_pos = self.frog.getPos()  # Используем метод для получения текущей позиции

        for lily in self.lilies:
            distance = abs(lily.pos().x() - current_pos.x())
            if distance <= self.frog.max_jump_distance and self.frog.weight <= lily.strength:
                possible_lilies.append(lily)

        if possible_lilies:
            if self.direction == 'right':
                next_lily = min(possible_lilies, key=lambda l: l.pos().x())
            else:
                next_lily = max(possible_lilies, key=lambda l: l.pos().x())
            return next_lily.pos()
        return None
    
    def update_frog_position(self):
        next_position = self.find_next_lily_pad()

        if next_position:
            # Найти кувшинку, на которую прыгнула лягушка
            jumped_lily = None
            for lily in self.lilies:
                if lily.pos() == next_position:
                    jumped_lily = lily
                    break

            # Прыжок на следующую кувшинку
            self.frog.crazy_jump(next_position)
            self.draw_path(self.frog.getPos(), next_position)

            # Уменьшение прочности кувшинки после прыжка
            if jumped_lily:
                jumped_lily.strength -= self.frog.weight  # Снимаем прочность на вес лягушки
                if jumped_lily.strength <= 0:
                    # Если прочность кувшинки достигла нуля, удаляем её из сцены
                    self.scene.removeItem(jumped_lily)
                    self.lilies.remove(jumped_lily)
        '''
        else:
            # Если нет подходящих кувшинок, лягушка тонет
            self.frog.setPos(self.frog.getPos().x(), self.height())  # Сбросить лягушку вниз
        '''

        # Проверка, достигла ли лягушка берега
        if self.direction == 'right' and self.frog.getPos().x() >= self.right_shore:
            self.direction = 'left'
        elif self.direction == 'left' and self.frog.getPos().x() <= self.left_shore:
            self.direction = 'right'
        
    def draw_path(self, start_pos, end_pos):
        pen = QPen(QColor("blue"))
        pen.setWidth(2)
        self.scene.addLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y(), pen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
