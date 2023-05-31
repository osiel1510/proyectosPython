import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QRectF,QPropertyAnimation,QAbstractAnimation,QPointF,QEasingCurve,QVariantAnimation
from PyQt5.QtGui import QBrush, QColor, QPen


class Bead(QGraphicsEllipseItem):
    def __init__(self, rect, bead_color, is_above_line):
        super().__init__(rect)
        self.setBrush(QBrush(bead_color))
        self.setAcceptHoverEvents(True)
        self.is_above_line = is_above_line

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            start_pos = self.pos()

            if self.is_above_line:
                target_y = self.y() - 60
            else:
                target_y = self.y() + 60

            # Create animation
            self.animation = QVariantAnimation()
            self.animation.setDuration(200)
            self.animation.setStartValue(start_pos)
            self.animation.setEndValue(QPointF(self.x(), target_y))
            self.animation.setEasingCurve(QEasingCurve.InOutCubic)
            self.animation.valueChanged.connect(self.on_value_changed)
            self.animation.start()

            # Update the bead's position state
            self.is_above_line = not self.is_above_line

    def on_value_changed(self, value):
        self.setPos(value)




class AbacusApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.setWindowTitle("Abacus Child Learning App")
        self.setGeometry(100, 100, 800, 600)

        # Add a combo box for selecting abacus type
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Regular (4 and 1)")
        self.comboBox.addItem("Aztec (4 and 3)")
        self.comboBox.currentIndexChanged.connect(self.change_abacus)
        self.comboBox.move(10, 10)

        # Add a QGraphicsView
        self.view = QGraphicsView(self)
        self.view.setGeometry(10, 50, 780, 540)

        self.abacus_config = {
            "Regular": (4, 1),
            "Aztec": (4, 3)
        }

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.change_abacus()

    def change_abacus(self):
        self.scene.clear()
        abacus_type = self.comboBox.currentText().split(" ")[0]

        beads_above, beads_below = self.abacus_config[abacus_type]
        self.draw_abacus(beads_above, beads_below)

    def draw_abacus(self, beads_above, beads_below):
        gap = 60
        radius = 25
        bead_color_earth = QColor("blue")
        bead_color_heaven = QColor("red")

        for i in range(10):
            # Draw vertical lines
            line = QGraphicsLineItem(i * gap, -30, i * gap, (beads_above + beads_below) * gap + 40)
            self.scene.addItem(line)

            for j in range(beads_above + beads_below):
                # Draw beads
                if j < beads_below:  # Change the condition here
                    brush = QBrush(bead_color_heaven)
                    bead = Bead(QRectF(i * gap - radius,j * gap-60, 2 * radius, 2 * radius), brush,False)
                    self.scene.addItem(bead)
                else:
                    brush = QBrush(bead_color_earth)
                    bead = Bead(QRectF(i * gap - radius, j * gap +59, 2 * radius, 2 * radius), brush,True)
                    self.scene.addItem(bead)


        # Draw horizontal line
        line = QGraphicsLineItem(-30, beads_below * gap-4,  10 * gap - 30 , beads_below * gap -4)  # Modify this line as well
        line.setPen(QPen(Qt.black, 3))
        self.scene.addItem(line)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    abacus_app = AbacusApp()
    abacus_app.show()
    sys.exit(app.exec_())
