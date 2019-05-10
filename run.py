from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QComboBox, QCompleter, QLabel, QShortcut
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeySequence
from PyQt5 import QtCore
import sys, os
import win32api, win32con, win32gui
import threading
import PyHook3

class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('运行')
        self.setWindowIcon(QIcon('shell32.ico'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.resize(625,280)
        self.move(0,QApplication.desktop().height()-370)
        self.setFont(QFont('微软雅黑'))
        self.initUI()
        QShortcut(QKeySequence(QtCore.Qt.Key_Return), self, self.Enter.click)
        QShortcut(QKeySequence("ALT+O"), self, self.combobox.setFocus)
        QShortcut(QKeySequence("ALT+B"), self, self.Browser.click)
        QShortcut(QKeySequence("Esc"), self, self.hide)

    def show(self):
        self.enable_Enter()
        self.combobox.setFocus()
        super().show()
        win32gui.SetWindowPos(win32gui.FindWindow(None,'运行'), win32con.HWND_TOP, 0,0,0,0, win32con.SWP_NOMOVE| win32con.SWP_NOSIZE|win32con.SWP_SHOWWINDOW)
        win32api.SendMessage(win32gui.FindWindow(None,'运行'), win32con.WM_INPUTLANGCHANGEREQUEST, 0, 0x0804)
        
    
    def initUI(self):
        self.label0 = QLabel(self)
        self.label0.resize(625, 180)
        self.label0.move(0, 1)
        self.label0.setStyleSheet("background-color:white")
        
        self.label1 = QLabel(self)
        self.label1.setText('打开(<u>O</u>):')
        self.label1.resize(600, 35)
        self.label1.move(20, 110)
        
        self.label2 = QLabel(self)
        self.label2.setPixmap(QPixmap('shell32.ico'))
        self.label2.setScaledContents (True)
        self.label2.resize(50, 50)
        self.label2.move(20, 35)
        
        self.label3 = QLabel(self)
        self.label3.setText('Windows 将根据你所输入的名称，为你打开相应的程序、文件夹、文档或 Internet 资源')
        self.label3.setWordWrap(True)
        self.label3.resize(500, 50)
        self.label3.move(100, 35)
        
        self.Enter=QPushButton("确定", self)
        self.Enter.move(175, 210)
        self.Enter.resize(135,45)
        self.Enter.clicked.connect(shell)
        self.Enter.setDefault(True)
        
        self.Cancel=QPushButton("取消", self)
        self.Cancel.move(320, 210)
        self.Cancel.resize(135,45)
        self.Cancel.clicked.connect(self.hide)
        
        self.Browser=QPushButton("浏览(B)...", self)
        self.Browser.move(470, 210)
        self.Browser.resize(135,45)
        self.Browser.clicked.connect(file_browser)
        
        self.combobox = QComboBox(self, width=400)
        self.combobox.resize(500,35)
        self.combobox.move(100,110)
        self.combobox.setEditable(True)
        self.combobox.editTextChanged.connect(self.enable_Enter)
        self.combobox.editTextChanged.connect(self.Flash_completer)
        self.combobox.completer = QCompleter(cookie.keys())
        self.combobox.completer.setFilterMode(QtCore.Qt.MatchStartsWith or QtCore.Qt.MatchContains)
        self.combobox.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.combobox.setCompleter(self.combobox.completer)

    def Flash_completer(self):
        files_path=[]
        if os.path.isdir(self.combobox.currentText()):
            for file in os.listdir(self.combobox.currentText()):
                file_path = os.path.join(self.combobox.currentText(), file)
                if os.path.isdir(file_path):
                    file_path=file_path+ ('\\' if self.combobox.currentText().find('/')==-1 else '/')
                else:
                    file_path=os.path.splitext(file_path)[0]
                files_path.append(file_path)
            self.combobox.completer = QCompleter(files_path)
    
    def enable_Enter(self):
        if self.combobox.currentText()=='':
            self.Enter.setEnabled(False)
        else:
            self.Enter.setEnabled(True)

    def closeEvent(self,event):
        self.hide()
        event.ignore()

    def hideEvent(self,event):
        self.combobox.clear()
        items=sorted(cookie,key=lambda key:cookie[key])
        self.combobox.addItem(recent)
        #items.remove('')
        self.combobox.addItems(items)
        self.combobox.removeItem(0)
        self.combobox.completer = QCompleter(list(set(list(cookie.keys())+get_basic_path())))
        self.combobox.setCompleter(self.combobox.completer)
        self.combobox.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)


def shell():
    filename= w.combobox.currentText()
    w.hide()
    try:
        win32api.ShellExecute(0, 'open',filename , None, '', 1)
        global cookie, recent
        recent= filename
        try:
            cookie[recent]=cookie[recent]+1
        except KeyError:
            cookie[recent]=1
        with open("cookie.dat",'w')as f:
            f.write(str(cookie))
    except Exception as e:
        print(e.strerror)
        #QMessageBox.critical(w,"Windows 找不到文件'{}'。请确定文件名是否正确后，再试一次。".format(w.combobox.currentText()))
        '''
        ret=e[0]
        if ret==0:
            print("内存不足")
        elif ret==2:
            
            print("Windows 找不到文件'{}'。请确定文件名是否正确后，再试一次。")
        elif ret==3:
            print("路径名错误")
        elif ret==11:
            print("EXE 文件无效")
        elif ret==26:
            print("发生共享错误")
        elif ret==27:
            print("文件名不完全或无效")
        elif ret==28:
            print("DDE 事务失败")
        elif ret==30:
            print("正在处理其他 DDE 事务而不能完成该 DDE 事务")
        elif ret==31:
            print("没有相关联的应用程序")
        '''
        
def file_browser():
    filepath, _ = QFileDialog.getOpenFileName(w,
                                    "浏览",
                                    os.path.expandvars('$HOME'),
                                    "程序(*.exe;*.pif;*.com;*.bat;*.cmd);;所有文件(*.*)")
    w.combobox.setEditText(filepath)
    
def keyboard_hook(event):
    global win,run
    if event.MessageName=='key down' and event.KeyID==(91 or 92):
        win=True
    elif event.MessageName=='key up' and event.KeyID==(91 or 92):
        win=False
        if run:
            run=False
            win32api.keybd_event(27,0,0,0)
            win32api.keybd_event(27,0,win32con.KEYEVENTF_KEYUP,0)
    elif win and event.KeyID==82:
        run=True
        w.show()
        return False
    return True

def on_close(sig):
    try:
        hm.UnhookKeyboard()
    except:
        pass

def get_basic_path():
    basic_path=[]
    for path in os.environ['PATH'].split(';'):
        try:
            for file in os.listdir(path):
                if os.path.isdir(os.path.join(path, file)) or os.path.splitext(file)[1]=='.dll': continue
                if os.path.splitext(file)[1]=='.lnk':
                    basic_path.append(os.path.splitext(file)[0])
                else:
                    basic_path.append(file)
        except:
            continue
    return basic_path
    
if __name__ == '__main__':
    try:
        with open("cookie.dat",'r')as f:
            cookie=eval(f.read())
    except FileNotFoundError:
        cookie={}
    except:
        exit()
    recent=''
    t1 = threading.Thread(target=keyboard_hook)
    t1.setDaemon(True)
    global run,  win
    win=False
    run=False
    hm = PyHook3.HookManager()
    hm.KeyAll = keyboard_hook
    win32api.SetConsoleCtrlHandler(on_close, True)
    global w
    app = QApplication(sys.argv)
    w=Main_window()
    hm.HookKeyboard()
    sys.exit(app.exec_())
    
