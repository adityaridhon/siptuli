import sys
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TaskReminderApp(QWidget):
    def __init__(self):
        super().__init__()
                
        self.setWindowTitle('SIPTULI')
        self.setGeometry(100, 100, 400, 300)

        self.tasks = []

        self.load_tasks_from_file()  # mengambil data tugas dari database .txt

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        title_label = QLabel('SIPTULI', self)

        title_gradient = 'QLabel { color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00BFFF, stop:1 #000080); background-color: transparent; }'
        title_label.setStyleSheet(title_gradient)

        font = QFont('Sacramento', 20, QFont.Bold)
        title_label.setFont(font)

        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)


        hbox_add = QHBoxLayout()
        label_add = QLabel('Tambah Tugas:')
        self.input_task = QLineEdit()
        btn_add = QPushButton('Tambah')
        btn_add.clicked.connect(self.add_task)
        hbox_add.addWidget(label_add)
        hbox_add.addWidget(self.input_task)
        hbox_add.addWidget(btn_add)

        layout.addLayout(hbox_add)

        self.list_tasks = QListWidget()
        layout.addWidget(self.list_tasks)

        hbox_mark = QHBoxLayout()
        btn_mark = QPushButton('Tandai Selesai')
        btn_mark.clicked.connect(self.mark_task)
        hbox_mark.addWidget(btn_mark)

        layout.addLayout(hbox_mark)

        self.setLayout(layout)

        # Update the task list on UI
        self.update_task_list()

    def add_task(self):
        task = self.input_task.text()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.input_task.clear()
            self.save_tasks_to_file()  # Save tasks after adding
        else:
            QMessageBox.warning(self, 'Peringatan', 'Mohon masukkan tugas terlebih dahulu')

    def update_task_list(self):
        self.list_tasks.clear()
        self.list_tasks.addItems(self.tasks)

    def mark_task(self):
        selected_task = self.list_tasks.currentItem()
        if selected_task:
            task_index = self.list_tasks.row(selected_task)
            del self.tasks[task_index]
            self.update_task_list()
            self.save_tasks_to_file()  # Save tasks after marking as done
        else:
            QMessageBox.warning(self, 'Peringatan', 'Mohon pilih tugas yang akan ditandai sebagai selesai')

    def load_tasks_from_file(self):
        try:
            with open('tasks.txt', 'r') as file:
                self.tasks = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            pass

    def save_tasks_to_file(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(task + '\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskReminderApp()
    window.show()
    sys.exit(app.exec_())
