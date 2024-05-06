import sys
from PyQt5.QtWidgets import QApplication, QDateEdit, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QLineEdit, QPushButton, QSpacerItem, QListWidget, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor

class TaskReminderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SIPTULI')
        self.setGeometry(100, 100, 600, 400)

        self.tasks = []

        self.load_tasks_from_file()  # mengambil data tugas dari database .txt

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        

        # Membuat judul aplikasi
        title_label = QLabel('SIPTULI', self)

        # Variasi warna dan font judul aplikasi
        title_gradient = 'QLabel { color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00BFFF, stop:1 #000080); background-color: transparent; }'
        title_label.setStyleSheet(title_gradient)
        font = QFont('Sacramento', 20, QFont.Bold)
        title_label.setFont(font)

        # Set agar judul berada di tengah
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Mengatur jarak space judul
        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)

        hbox_add = QHBoxLayout()

        # Variabel untuk membuat input judul tugas, matkul dan tenggat
        self.label_title = QLabel('Judul Tugas:')
        self.input_title = QLineEdit()
        self.label_subject = QLabel('Mata Kuliah:')
        self.input_subject = QLineEdit()
        self.label_deadline = QLabel('Tenggat Waktu:')
        self.input_deadline = QDateEdit(calendarPopup=True)
        self.input_deadline.setDate(QDate.currentDate())  # Mengatur default awal deadline yaitu tanggal saat app dibuka

        self.btn_add_task = QPushButton('Tambah Tugas')
        self.btn_add_task.clicked.connect(self.toggle_input_fields)  # Menghubungkan ke bagian input tugas

        self.btn_insert_task = QPushButton('Masukkan Tugas')
        self.btn_insert_task.clicked.connect(self.add_task)  # Menghubungkan ke function tambahkan tugas
        self.btn_insert_task.hide()  # Set default awal input tidak muncul kecuali tombol tambah tugas ditambahkan

        hbox_add.addWidget(self.label_title)
        hbox_add.addWidget(self.input_title)
        hbox_add.addWidget(self.label_subject)
        hbox_add.addWidget(self.input_subject)
        hbox_add.addWidget(self.label_deadline)
        hbox_add.addWidget(self.input_deadline)
        hbox_add.addWidget(self.btn_add_task)
        hbox_add.addWidget(self.btn_insert_task)  # Menambahkan tombol masukkan tugas untuk memunculkan ke daftar tugas setelah menginput tugas  

        layout.addLayout(hbox_add)

        # Menyembunyikan input saat awal program dan akan muncul hanya ketika tombol tambahkan tugas diklik
        self.label_title.hide()
        self.input_title.hide()
        self.label_subject.hide()
        self.input_subject.hide()
        self.label_deadline.hide()
        self.input_deadline.hide()

        # Membuat tabel dafftar tugas
        self.table_tasks = QTableWidget()
        self.table_tasks.setColumnCount(3)
        self.table_tasks.setHorizontalHeaderLabels(["Judul Tugas", "Mata Kuliah", "Tenggat Waktu"])
        self.table_tasks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_tasks)

        # Membuat tombol tandai selesai yang mengarah ke functon tandai tugas selesai
        hbox_mark = QHBoxLayout()
        btn_mark = QPushButton('Tandai Selesai')
        btn_mark.clicked.connect(self.mark_task)
        hbox_mark.addWidget(btn_mark)

        layout.addLayout(hbox_mark)

        self.setLayout(layout)

        self.update_task_list()

    def toggle_input_fields(self):
        # Logika unutuk memunculkan input tugas ketika tombol tambah tugas diklik dan menyembunyikannya ketika tombol tambah tugas belum diklik
        if self.btn_add_task.text() == 'Tambah Tugas':
            self.label_title.show()
            self.input_title.show()
            self.label_subject.show()
            self.input_subject.show()
            self.label_deadline.show()
            self.input_deadline.show()
            self.btn_add_task.setText('Batal')
            self.btn_insert_task.show()  # Menampilkn tombol masukkan tugas ketika input selesai
        else:
            self.label_title.hide()
            self.input_title.hide()
            self.label_subject.hide()
            self.input_subject.hide()
            self.label_deadline.hide()
            self.input_deadline.hide()
            self.btn_add_task.setText('Tambah Tugas')
            self.btn_insert_task.hide() 

    # Function untuk menjalankan kode dimana akan menambahkan tugas yang sudah di input dan akan di save di database 
    def add_task(self):
        title = self.input_title.text()
        subject = self.input_subject.text()
        deadline = self.input_deadline.date().toString(Qt.ISODate)
        if title and subject and deadline:
            task_info = [title, subject, deadline]
            self.tasks.append(task_info)
            self.update_task_list()
            self.clear_input_fields()
            self.save_tasks_to_file()  # Menyimpan tugas ke database setelah masukkan tugas
        else:
            QMessageBox.warning(self, 'Peringatan', 'Mohon lengkapi semua input untuk menambah tugas')

    # Function untuk mengosongkan input tugas
    def clear_input_fields(self):
        self.input_title.clear()
        self.input_subject.clear()
        self.input_deadline.setDate(QDate.currentDate())  

    # Function untuk update daftar tugas yang ada di tabel  
    def update_task_list(self):
        self.table_tasks.setRowCount(len(self.tasks))
        for row, task in enumerate(self.tasks):
            for col, data in enumerate(task):
                item = QTableWidgetItem(data)
                self.table_tasks.setItem(row, col, item)

    # Function untuk menandai tugas selesai
    def mark_task(self):
        selected_row = self.table_tasks.currentRow()
        if selected_row != -1:
            del self.tasks[selected_row]
            self.update_task_list()
            self.save_tasks_to_file()  # Save tasks after marking as done
            QMessageBox.information(self, 'Informasi', 'Tugas telah ditandai selesai!')
        else:
            QMessageBox.warning(self, 'Peringatan', 'Mohon pilih tugas yang akan ditandai sebagai selesai')

    # Function untuk mengambil data tugas yang ada di database
    def load_tasks_from_file(self):
        try:
            with open('tasks.txt', 'r') as file:
                self.tasks = [line.strip().split(',') for line in file.readlines()]
        except FileNotFoundError:
            pass

    # Function untuk menyimpan data tugas ke dalam database
    def save_tasks_to_file(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(','.join(task) + '\n')


# Main aplikasi
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskReminderApp()
    window.show()
    sys.exit(app.exec_())
