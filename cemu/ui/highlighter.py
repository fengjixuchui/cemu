import time

from PyQt5.QtGui import(
    QFont,
    QTextCharFormat,
    QColor,
    QSyntaxHighlighter
)

from pygments import highlight
from pygments.formatter import Formatter
from pygments.lexers import get_lexer_by_name


class QFormatter(Formatter):
    def __init__(self, *args, **kwargs):
        Formatter.__init__(self)
        self.data=[]
        self.styles={}
        for token, style in self.style:
            qtf=QTextCharFormat()
            if style['color']:
                qtf.setForeground(self.hex2QColor(style['color']))
            if style['bgcolor']:
                qtf.setBackground(self.hex2QColor(style['bgcolor']))
            if style['bold']:
                qtf.setFontWeight(QFont.Bold)
            if style['italic']:
                qtf.setFontItalic(True)
            if style['underline']:
                qtf.setFontUnderline(True)
            self.styles[str(token)]=qtf
        return


    def hex2QColor(self, c):
        red = int(c[0:2], 16)
        green = int(c[2:4], 16)
        blue = int(c[4:6], 16)
        return QColor(red, green, blue)


    def format(self, tokensource, outfile):
        self.data=[]
        for ttype, value in tokensource:
            l=len(value)
            t=str(ttype)
            self.data.extend([self.styles[t],]*l)
        return


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent, mode):
        QSyntaxHighlighter.__init__(self, parent)
        self.tstamp=time.time()
        self.formatter=QFormatter()
        self.lexer=get_lexer_by_name(mode)
        return


    def highlightBlock(self, text):
        cb = self.currentBlock()
        p = cb.position()
        text = self.document().toPlainText() +'\n'
        highlight(text,self.lexer,self.formatter)
        for i in range(len(text)):
            try:
                self.setFormat(i,1,self.formatter.data[p+i])
            except IndexError:
                pass
        self.tstamp = time.time()
        return