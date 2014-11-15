#!/usr/bin/env python3.4
#-*- coding: UTF-8 -*-

from PyQt4 import QtCore, QtGui, uic

import sys
import os
import pickle
import time

import enchant as en
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter

text = None
savedText = None
recentPath = None
words = None
text_dic = None
en_dic = None

count = 1

autosaveTime = 5 * 60

checkerCount = 1



class AutoSave(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
      try:
        global count
        while True:
            time.sleep(autosaveTime)
            if window.editor.toPlainText() and window.editor.toPlainText() != savedText:
                saveFile(os.path.expanduser('~/.ExPy/autosave-{}.txt'.format(count)))
                print('[DEBUG] Autosaved')
                if count == 20:
                    count = 1
                else:
                    count += 1
      except Exception:
        pass
            
        

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        uic.loadUi('writer.ui', self)
    def closeEvent(self, event):
        if quit_p() == 'cancel':
            event.ignore() 
        else:
            event.accept()
    def resizeEvent(self, event):
            event.accept()
            self.editor.setFixedHeight(self.height()-45)
            self.editor.setFixedWidth(self.width())
            
            
            
class Checker(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        uic.loadUi('writer_o.ui', self)
    
            
            
            
def checkErrors():
    global text, checkerCount,  words, text_dic
    words = []
    text = window.editor.toPlainText()
    text_dic.set_text(text)
    checker.setWindowModality(QtCore.Qt.ApplicationModal)
    for err in text_dic:
        words.append(err.word)
    if words:
        checkErrorsOb()
        checker.show()
    else:
         window.statusbar.showMessage('Ошибок не обнаружено', msecs =5000)
         
def checkErrorsOb():
    global words, text
    if words:
        cur = words[0]
        items = tuple(en_dic.suggest(cur))
        checker.text.setText('Возможно, допущена ошибка в слове "{}" '.format(cur))
        checker.variants.clear()
        checker.variants.addItems(items)
        checker.variants.setCurrentRow(0)
    else:
        checker.hide()
        window.editor.setText(text)

        
                
def checkerReplaceAction():
    global text, words
    text = text.replace(words[0], checker.variants.currentItem().text())
    del words[0]
    window.editor.setText(text)
    checkErrorsOb()

def checkerNext():
    global words
    del words[0]
    checkErrorsOb()
    
def checkerAdd():
    global words
    if os.path.exists(os.path.expanduser('~/.ExPy/dict.txt')):
        reg = 'a'
    else:
        reg = 'w'
    with open(os.path.expanduser('~/.ExPy/dict.txt'),  reg) as f:
        f.write(words[0] + '\n')
    del words[0]
    checkErrorsOb()

def checkerCancel():
    global words
    words = None
    checkErrorsOb()
    

               

def getCharsCount():
    cursor = window.editor.textCursor()
    text = cursor.selectedText()
    
    stats_t = (len(text.strip()), 
    len(text.strip().replace(' ','').replace('\n',
    '').replace('\t','')), 
    len(text.strip().split()))
    
    stats = (len(window.editor.toPlainText().strip()), 
    len(window.editor.toPlainText().strip().replace(' ','').replace('\n',
    '').replace('\t','')), 
    len(window.editor.toPlainText().strip().split()))
    reply = QtGui.QMessageBox.information(None,
                "Статистика", """
\t\tДокумент:\tВыделение:
Знаков:\t\t{0}\t{3}
Знаков (б/п):\t{1}\t{4}
Слов:\t\t{2}\t{5}

""".format(str(stats[0]),str(stats[1]),str(stats[2]), str(stats_t[0]),str(stats_t[1]),str(stats_t[2])))

def getAutosaveTime():
    global autosaveTime
    i = QtGui.QInputDialog.getInteger(None,"Настройка автосохранения", 
    "Укажите интервал между автосохранениями (в секундах):", autosaveTime,
     60, 10800, 60)
    if i:
        autosaveTime = i[0]
        print('[DEBUG] Autosave interval set to ', i[0])



def openFile(path=None):
    if savedText != window.editor.toPlainText() and window.editor.toPlainText():
        reply = QtGui.QMessageBox.question(None, 'Файл не сохранен',
                "Текущий файл не сохранен. Сохранить?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            saveFile(recentPath)

        elif reply == QtGui.QMessageBox.Cancel:
            return None
            
    if not path:
        if recentPath:
            home_path = os.path.split(recentPath)[0] + '/'
        else:
            home_path = ''
        path = QtGui.QFileDialog.getOpenFileName(None, "Открыть файл", 
                                            home_path, 'Текстовые файлы (*.txt)')
    if path:
        inFile = QtCore.QFile(path)
        if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            text = inFile.readAll()            
            try:
                # Python v3
                try:
                    text = str(text, encoding='utf-8')
                except UnicodeDecodeError:
                    text = str(text, encoding='windows-1251')
            except TypeError:
                # Python v2
                text = str(text)   
            global savedText, recentPath
            savedText = text    
            recentPath = path
            window.editor.setPlainText(text)
            with open('style.qss') as f:
                window.editor.setStyleSheet(f.read())
    print('[DEBUG] Cursor position: ', cursor.position())
    
def saveFile(path=None):
    if not path:
        if recentPath:
            path = QtGui.QFileDialog.getSaveFileName(None, 'Сохранить файл', os.path.split(recentPath)[1], '.txt')
        else:
            path = QtGui.QFileDialog.getSaveFileName(None, 'Сохранить файл', '.txt')
        
    if path:
        inFile = open(path, 'w')
        inFile.write(window.editor.toPlainText())
        inFile.close()
        global savedText, recentFilePath 
        saved = True
        recentFilePath = path
        savedText = window.editor.toPlainText() 
        window.statusbar.showMessage('Сохранено', msecs =5000)

def saveFileAs():
    path = QtGui.QFileDialog.getSaveFileName(None, 'Сохранить файл', '.txt')
    if path:
        inFile = open(path, 'w')
        inFile.write(window.textarea.toPlaitText())
        inFile.close()
        global savedText, recentFilePath 
        saved = True
        recentFilePath = path
        savedText = window.editor.toPlainText() 
        
def newFile():
    global recentPath
    if savedText != window.editor.toPlainText() and window.editor.toPlainText():
        reply = QtGui.QMessageBox.question(None, 'Файл не сохранен',
                "Текущий файл не сохранен. Сохранить?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            saveFile(recentPath)

        elif reply == QtGui.QMessageBox.Cancel:
            return None
    window.editor.clear()
    recentPath = None
    window.statusbar.showMessage('Текстовое поле очищено', msecs = 5000)


def loadDicts():
    global text_dic, en_dic
    en_dic = en.Dict("ru_RU")
    if  en.dict_exists("ru_RU"):
        if os.path.exists(os.path.expanduser('~/.ExPy/dict.txt')):
            buf_dic = en.DictWithPWL("ru_RU",os.path.expanduser('~/.ExPy/dict.txt'))
            text_dic = SpellChecker(buf_dic, filters=[EmailFilter,URLFilter])
        else:
            text_dic = SpellChecker("ru_RU", filters=[EmailFilter,URLFilter])
    else:
        QtGui.QMessageBox.information(None,
                "Не обнаружен словарь", "Не обнаружен русский словарь Hunspell, проверка орфографии невозможна")
        
        
        


def textChanged():
    selection = QtGui.QTextEdit.ExtraSelection()
    selection.format.setBackground(QtGui.QColor('#555753'))
    selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
    selection.cursor = window.editor.textCursor()
    selection.cursor.clearSelection()
    selections = [selection]
    window.editor.setExtraSelections(selections)
    cursor = window.editor.textCursor()
    cursor_pos = cursor.position()

        
            
    print('[DEBUG] cursor position: ', cursor.position())
    
def auto_replace():
    auto_replace = {'--': '—', '<<':'«', '>>': '»'}
    cursor = window.editor.textCursor()
    cursor_pos = cursor.position()
    if window.editor.toPlainText()[cursor.position()-2:cursor.position()] in auto_replace and window.auto_replace.isChecked():
        
        text = window.editor.toPlainText()
        print(text[cursor_pos-2:cursor_pos])
        text = text.replace(text[cursor_pos-2:cursor_pos], auto_replace[text[cursor_pos-2:cursor_pos]])
        print(text)
        window.editor.setPlainText(text)
        cursor.setPosition(cursor_pos-1)
        window.editor.setTextCursor(cursor)
        
def openAutosaveDir():
    print('[DEBUG] Открытие паки с автосохранениями.')
    p = sys.platform

    if p == 'linux' or p == 'darwin':
        os.system('xdg-open ~/.ExPy')
    elif p == 'win32':
        os.system('start "" "{}"'.format(os.path.expanduser('~/.ExPy/')))
        
    
    
##############################################################################################################################################


def quit_p():
    print()
    cursor = window.editor.textCursor()
    data = {'recPath': recentPath, 'curPos': cursor.position(), 'cnt': count, 'ast': autosaveTime, 'w': window.width(), 'h': window.height() }
    with open(os.path.expanduser('~/.ExPy/settings'), 'wb') as f:
        pickle.dump(data, f)
    if savedText != window.editor.toPlainText() and window.editor.toPlainText():
        reply = QtGui.QMessageBox.question(None, 'Файл не сохранен',
                            "Текущий файл не сохранен. Сохранить?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            saveFile(recentPath)
        elif reply == QtGui.QMessageBox.Cancel:
            return 'cancel'
        
        
    sys.exit()






##############################################################################################################################################
##                                                               START
##                                                               START
##############################################################################################################################################
app = QtGui.QApplication(sys.argv)
window = MainWindow()
checker = Checker()


clipboard = app.clipboard()
cursor = window.editor.textCursor() 
textChanged()

##############################################################################################################################################
QtCore.QObject.connect(window.open_f, QtCore.SIGNAL('triggered()'), openFile)
QtCore.QObject.connect(window.save_f, QtCore.SIGNAL('triggered()'), saveFile)
QtCore.QObject.connect(window.save_as, QtCore.SIGNAL('triggered()'), saveFileAs)
QtCore.QObject.connect(window.new_f, QtCore.SIGNAL('triggered()'), newFile)
QtCore.QObject.connect(window.autosave_s, QtCore.SIGNAL('triggered()'), getAutosaveTime)
QtCore.QObject.connect(window.open_autosave, QtCore.SIGNAL('triggered()'), openAutosaveDir)
QtCore.QObject.connect(window.quit_p, QtCore.SIGNAL('triggered()'), quit_p)

QtCore.QObject.connect(window.get_stats, QtCore.SIGNAL('triggered()'), getCharsCount)
QtCore.QObject.connect(window.check_o, QtCore.SIGNAL('triggered()'), checkErrors)

QtCore.QObject.connect(window.editor, QtCore.SIGNAL('cursorPositionChanged()'), textChanged)
QtCore.QObject.connect(window.editor, QtCore.SIGNAL('textChanged()'), auto_replace)
##############################################################################################################################################
QtCore.QObject.connect(checker.replace, QtCore.SIGNAL('clicked()'), checkerReplaceAction)
QtCore.QObject.connect(checker.add, QtCore.SIGNAL('clicked()'), checkerAdd)
QtCore.QObject.connect(checker.next, QtCore.SIGNAL('clicked()'), checkerNext)
QtCore.QObject.connect(checker.quit_c, QtCore.SIGNAL('clicked()'), checkerCancel)
QtCore.QObject.connect(checker.variants, QtCore.SIGNAL('itemDoubleClicked()'), checkerReplaceAction)


##############################################################################################################################################
##                                                               ON START
##                                                               ON START
##############################################################################################################################################
try:
    os.mkdir(os.path.expanduser('~/.ExPy'))
    if sys.platform == 'win32':
        os.system('attrib +H "" "{}"'.format(os.path.expanduser('~/.ExPy/')))
except OSError as e:
    print(e)

if os.path.exists(os.path.expanduser('~/.ExPy/settings')):
    with open(os.path.expanduser('~/.ExPy/settings'), 'rb') as f:
        try:
            data = pickle.load(f)
            print(data)
        except pickle.PickleError:
            print('[DEBUG] PickleError')
            data = {'recPath': None, 'curPos': None, 'cnt': None, 'ast': 300, 'w': 700, 'h': 750}
else:
     data = {'recPath': None, 'curPos': None, 'cnt': None, 'ast': 300, 'w': 700, 'h': 750}
     
recentPath = data['recPath']
if recentPath:
    openFile(recentPath)
    if data['curPos']:
        print('[DEBUG] Cursor position loaded', data['curPos'])
        cursor.setPosition(data['curPos'])
        window.editor.setTextCursor(cursor)
else:
    newFile()
if data.get('cnt'):
    count = data['cnt']
if data.get('ast'):
    autosaveTime = data['ast']
if not data.get('w'):
    data['w'] = 700; data['h'] = 750
window.resize(data['w'], data['h'])
window.editor.setFixedHeight(window.height()-45)
window.editor.setFixedWidth(window.width())
del data

with open('style.qss') as f:
    window.editor.setStyleSheet(f.read())

en.set_param("enchant.hunspell.dictionary.path", '')

##############################################################################################################################################

loadDicts()
window.show()

autosave = AutoSave()
autosave.start()
sys.exit(app.exec_())
