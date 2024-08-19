from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QInputDialog, QFormLayout, QLineEdit
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import cv2
from pathlib import Path
import funcoes as fc


class Janela_Principal(QWidget):
    def __init__(self, caminho_imagem=None, imagem=None):
        super().__init__()

        self.caminho_imagem = caminho_imagem
        self.imagem = imagem

        self.setWindowTitle("CONVOLUÇÕES EM IMAGENS")
        self.setFixedSize(800, 600)

        self.layout = QVBoxLayout()

        self.label = QLabel("Selecione uma imagem e clique em Confirmar", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(60)
        self.layout.addWidget(self.label)

        self.image_container = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_container.addWidget(self.image_label)
        self.layout.addLayout(self.image_container)

        self.btn = QPushButton('Selecionar Imagem', self)
        self.btn.clicked.connect(self.showDialog)
        self.btn.setFixedHeight(60)
        self.layout.addWidget(self.btn)

        self.confirm_btn = QPushButton('Confirmar', self)
        self.confirm_btn.clicked.connect(self.confirmaracao)
        self.confirm_btn.setFixedHeight(60)
        self.layout.addWidget(self.confirm_btn)

        self.setLayout(self.layout)

        self.show()

        if self.caminho_imagem:
            self.updateImageLabel(QPixmap(str(self.caminho_imagem)))
        elif self.imagem is not None:
            self.updateImageLabel(QPixmap.fromImage(self.imagem))

    def showDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecionar Imagem', '', 'Images (*.png *.xpm *.jpg *.jpeg)')
        if file_path:
            self.caminho_imagem = Path(file_path)
            pixmap = QPixmap(file_path)
            self.updateImageLabel(pixmap)
            self.label.setText("Imagem Selecionada:")

    def updateImageLabel(self, pixmap):
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.repaint()

    def resizeEvent(self, event):
        if self.caminho_imagem:
            pixmap = QPixmap(str(self.caminho_imagem))
            self.updateImageLabel(pixmap)
        elif self.imagem is not None:
            self.updateImageLabel(QPixmap.fromImage(self.imagem))
        super().resizeEvent(event)

    def confirmaracao(self):  
        if self.caminho_imagem:
            self.Janela_Secundaria = Janela_Secundaria(self.caminho_imagem)
            self.Janela_Secundaria.show()
            self.close()
        else:
            self.label.setText("Nenhuma imagem foi selecionada!")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.confirmaracao()


class Janela_Secundaria(QWidget):
    def __init__(self, path):
        super().__init__()
        
        self.caminho_imagem = path
        
        self.setWindowTitle("TRATAR A IMAGEM")
        self.setFixedSize(600, 400)
        
        layout = QVBoxLayout()
        
        botao_inver = QPushButton("Aplicar Inversão de Cores")
        layout.addWidget(botao_inver)
        botao_inver.clicked.connect(self.inverter_cor)
        botao_inver.setFixedHeight(60)
        
        botao_contr = QPushButton("Aplicar Convolução")
        layout.addWidget(botao_contr)
        botao_contr.clicked.connect(self.conv)
        botao_contr.setFixedHeight(60)
        
        botao_blur = QPushButton("Aplicar BLUR")
        layout.addWidget(botao_blur)
        botao_blur.clicked.connect(self.blur)
        botao_blur.setFixedHeight(60)
        
        botao_voltar = QPushButton("Voltar")
        layout.addWidget(botao_voltar)
        botao_voltar.clicked.connect(self.voltar)
        botao_voltar.setFixedHeight(60)
        
        self.setLayout(layout)
        
    def voltar(self):
        self.Janela_Principal = Janela_Principal(self.caminho_imagem)
        self.Janela_Principal.show()
        self.close()
    
    def blur(self):
        self.janela_blur = Valor_BLUR(self.caminho_imagem)
        self.janela_blur.show()
        self.close()
    
    def inverter_cor(self):
        self.imagem_invertida, self.hist_orig, self.hist_inver = fc.inverter_cor(self.caminho_imagem)
        self.Janela_Imagem = Janela_Imagem_Inv(self.imagem_invertida, self.hist_orig, self.hist_inver)
        self.Janela_Imagem.show()
    
    def conv(self):
        self.janela_conv = Valor_Conv(self.caminho_imagem)
        self.janela_conv.show()
        self.close()


class Janela_Imagem_Inv(QWidget):
    def __init__(self, imagem_invertida, hist_orig, hist_inver):
        super().__init__()
        
        self.setWindowTitle("Imagem Invertida")
        
        main_layout = QVBoxLayout()
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)
        
        hist_layout = QHBoxLayout()
        
        before_layout = QVBoxLayout()
        before_title = QLabel("Antes")
        before_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hist_ori_label = QLabel(self)
        self.hist_ori_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        before_layout.addWidget(before_title)
        before_layout.addWidget(self.hist_ori_label)
        
        after_layout = QVBoxLayout()
        after_title = QLabel("Depois")
        after_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hist_inv_label = QLabel(self)
        self.hist_inv_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        after_layout.addWidget(after_title)
        after_layout.addWidget(self.hist_inv_label)
        
        hist_layout.addLayout(before_layout)
        hist_layout.addLayout(after_layout)
        
        main_layout.addLayout(hist_layout)
        self.setLayout(main_layout)
        
        # Convertendo a imagem BGR para RGB
        imagem_invertida = cv2.cvtColor(imagem_invertida, cv2.COLOR_BGR2RGB)
        
        height_imv, width_imv, _ = imagem_invertida.shape
        
        bytes_per_line = 3 * width_imv
        
        q_img = QImage(imagem_invertida.data, width_imv, height_imv, bytes_per_line, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_img)
        
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width() * 10, self.image_label.height() * 10, Qt.AspectRatioMode.KeepAspectRatio))

        # Exibindo histogramas
        self.conversao_histogram(self.hist_ori_label, hist_orig)
        self.conversao_histogram(self.hist_inv_label, hist_inver)

    def conversao_histogram(self, label, hist_img):
        height_hist, width_hist, _ = hist_img.shape
        bytes_per_line = 3 * width_hist
        q_hist = QImage(hist_img.data, width_hist, height_hist, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap_hist = QPixmap.fromImage(q_hist)
        
        # Atualizando o QLabel com o histograma
        label.setPixmap(pixmap_hist.scaled(label.width() * 10, label.height() * 10, Qt.AspectRatioMode.KeepAspectRatio))
        label.repaint()

class Valor_Conv(QWidget):
    def __init__(self, caminho):
        super().__init__()
        
        self.caminho_imagem = caminho
        
        self.setWindowTitle("Valor da Convolução")
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.label = QLabel("Aceita-se valores positivos e negativos.\nUse 0 para retornar a imagem sem convolução.", self)
        layout.addWidget(self.label)
        
        self.caixa_valor_conv = QLineEdit(self)
        self.text_valor_conv = 'Intensidade da Convolução:'
        
        formlayout.addRow(self.text_valor_conv, self.caixa_valor_conv)
        
        botao_confirmar = QPushButton('Confirmar')
        botao_confirmar.clicked.connect(self.enviar_dados)
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.enviar_dados()
    
    def enviar_dados(self):
        imagem = fc.convolucao(self.caminho_imagem, int(self.caixa_valor_conv.text()))
        self.Janela_Conv = Janela_Conv(imagem, self.caminho_imagem)
        self.Janela_Conv.show()
        self.close()
    

class Janela_Conv(QWidget):
    def __init__(self, imagem, caminho):
        super().__init__()
        
        self.caminho_imagem = caminho
        
        self.imagem = imagem
        
        self.setWindowTitle("Imagem com convolução aplicada")
        
        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        
        botao_voltar = QPushButton("Voltar")
        layout.addWidget(botao_voltar)
        botao_voltar.clicked.connect(self.voltar)
        
        self.setLayout(layout)
        
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        
        height_imv, width_imv, _ = imagem.shape
        
        bytes_per_line = 3 * width_imv
        
        q_img = QImage(imagem.data, width_imv, height_imv, bytes_per_line, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_img)
        
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width() * 10, self.image_label.height() * 10, Qt.AspectRatioMode.KeepAspectRatio))
    
    def voltar(self):
        self.menu_principal = Janela_Secundaria(self.caminho_imagem)
        self.menu_principal.show()
        self.close()

class Valor_BLUR(QWidget):
    def __init__(self, caminho):
        super().__init__()
        
        self.caminho_imagem = caminho
        
        self.setWindowTitle("Valor do BLUR")
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.label = QLabel("Deve ser um valor maior que 0.", self)
        layout.addWidget(self.label)
        
        self.caixa_valor_blur = QLineEdit(self)
        self.text_valor_blur = 'Intensiade do BLUR:'
        
        formlayout.addRow(self.text_valor_blur, self.caixa_valor_blur)
        
        botao_confirmar = QPushButton('Confirmar')
        botao_confirmar.clicked.connect(self.enviar_dados)
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.enviar_dados()
    
    def enviar_dados(self):
        imagem = fc.blur(self.caminho_imagem, int(self.caixa_valor_blur.text()))
        self.Janela_Blur = Janela_Blur(imagem, self.caminho_imagem)
        self.Janela_Blur.show()
        self.close()
    
class Janela_Blur(QWidget):
    def __init__(self, imagem, caminho):
        super().__init__()
        
        self.caminho_imagem = caminho
        
        self.imagem = imagem
        
        self.setWindowTitle("Imagem com Blur")
        
        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        
        botao_voltar = QPushButton("Voltar")
        layout.addWidget(botao_voltar)
        botao_voltar.clicked.connect(self.voltar)
        
        self.setLayout(layout)
        
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        
        height_imv, width_imv, _ = imagem.shape
        
        bytes_per_line = 3 * width_imv
        
        q_img = QImage(imagem.data, width_imv, height_imv, bytes_per_line, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_img)
        
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width() * 10, self.image_label.height() * 10, Qt.AspectRatioMode.KeepAspectRatio))
    
    def voltar(self):
        self.menu_principal = Janela_Secundaria(self.caminho_imagem)
        self.menu_principal.show()
        self.close()