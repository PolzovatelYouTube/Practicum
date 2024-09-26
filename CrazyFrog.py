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
        self.setZValue(10)
    '''
    def getPos(self):
        return QGraphicsEllipseItem.pos(self)

    def setPos(self, pos):
        QGraphicsEllipseItem.setPos(self, pos)
    '''

    def crazy_jump(self, where):
        self.setPos(where.x(), where.y())  # Устанавливаем как x, так и y

    #pos = pyqtProperty(QPointF, getPos, setPos)

class LilyPad(QGraphicsEllipseItem):
    def __init__(self, x, y, strength):
        super().__init__(0, 0, 30, 30)  # размеры кувшинки
        self.setPos(x, y)  # Устанавливаем координаты (x, y)
        self.strength = strength
        self.setBrush(QBrush(QColor("green")))

    def fall(self, speed):
        # Смещаем кувшинку вниз на `speed` пикселей
        current_pos = self.pos()
        self.setPos(current_pos.x(), current_pos.y() + speed)
    
    def getPos(self):
        return self.pos()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.scene = QGraphicsScene(0, 0, 800, 600) 
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCentralWidget(self.view)
        
        #след
        self.lines = []

        # Берега
        self.left_shore = 0
        self.right_shore = self.width() - 50
        self.current_shore = 'left'

        # Логика движения
        self.direction = 'right'  # Лягушка начинает с левого берега

        # Создание списка кувшинок
        self.lilies = []

        # Создание лягушки
        self.frog = Frog(0, 300, weight=5, max_jump_distance=300)
        self.scene.addItem(self.frog)

        # Таймер для прыжков лягушки
        self.timer_frog = QTimer()
        self.timer_frog.timeout.connect(self.update_frog_position)
        self.timer_frog.start(100)  # Обновление каждые 0.1 секунды

        # Таймер для падения кувшинок
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lily_pads_position)
        self.timer.start(20)  # Обновление каждые n мс для плавного падения

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
                x = random.randint(0, self.scene.width() - 30)  # 30 - ширина кувшинки
                if all(abs(x - pos_x) > 40 for pos_x in positions):  # 40 пикселей - минимальное расстояние
                    positions.append(x)
                    break
            
            y = 0  # Начальное положение по оси Y (сверху)
            # Добавляем кувшинку в сцену с позицией (x, y)
            strength = random.randint(5, 5)  # Случайная прочность
            lily = LilyPad(x, y, strength) 
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
        current_pos = self.frog.scenePos()

        # Определяем расстояние до левого и правого берегов
        distance_to_left_shore = abs(current_pos.x() - self.left_shore)
        distance_to_right_shore = abs(current_pos.x() - self.right_shore)

        # Проверка на возможность прыжка на берег
        if self.direction == 'right' and distance_to_right_shore <= self.frog.max_jump_distance:
            return QPointF(self.right_shore, current_pos.y())  # Повернуть в сторону правого берега

        if self.direction == 'left' and distance_to_left_shore <= self.frog.max_jump_distance:
            return QPointF(self.left_shore, current_pos.y())  # Повернуть в сторону левого берега

        # Обычный поиск кувшинок
        for lily in self.lilies:
            distance_x = abs(lily.scenePos().x() - current_pos.x())
            distance_y = abs(lily.scenePos().y() - current_pos.y())
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance <= self.frog.max_jump_distance and self.frog.weight <= lily.strength and distance >= 2:
                possible_lilies.append(lily)

        if possible_lilies:
            if self.direction == 'right':
                next_lily = min(possible_lilies, key=lambda l: l.scenePos().x())  # Ближайшая вправо
            else:
                next_lily = max(possible_lilies, key=lambda l: l.scenePos().x())  # Ближайшая влево

            return next_lily.scenePos()
        
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
            self.draw_path(self.frog.pos(), next_position)
            self.frog.crazy_jump(next_position)

            # Уменьшение прочности кувшинки после прыжка
            if jumped_lily:
                jumped_lily.strength -= self.frog.weight  # Снимаем прочность на вес лягушки
                if jumped_lily.strength <= 0:
                    # Если прочность кувшинки достигла нуля, удаляем её из сцены
                    self.scene.removeItem(jumped_lily)
                    self.lilies.remove(jumped_lily)
        else:
            # Если нет доступных кувшинок для прыжка, лягушка следует за кувшинкой вниз
            current_pos = self.frog.scenePos()
            for lily in self.lilies:
                if abs(lily.scenePos().x() - current_pos.x()) < 1:  # Если лягушка находится на кувшинке
                    # Следуем за кувшинкой вниз
                    self.frog.setPos(lily.scenePos().x(), lily.scenePos().y())


        # Проверка, достигла ли лягушка берега, чтобы сменить направление
        if self.direction == 'right' and self.frog.pos().x() >= self.right_shore:
            self.direction = 'left'  # Лягушка меняет направление на левое
        elif self.direction == 'left' and self.frog.pos().x() <= self.left_shore:
            self.direction = 'right'  # Лягушка меняет направление на правое
        
    def draw_path(self, start_pos, end_pos):
        pen = QPen(QColor("blue"))
        pen.setWidth(2)
        line = self.scene.addLine(start_pos.x()+10, start_pos.y()+10, end_pos.x()+10, end_pos.y()+10, pen)
        self.lines.append(line)

        if len(self.lines) > 2:
            old_line = self.lines.pop(0)
            self.scene.removeItem(old_line)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
