from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat

green = "#899965"
pink = "#ad5e82"
blue = "#35a18f"
string = "#7d485e"
comment_color = "#555555"

chatGraph = "#D3E46B"

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(green))

        class_format = QTextCharFormat()
        class_format.setForeground(QColor(pink))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(blue))

        # 文字列の色
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string))

        chatGraph_format = QTextCharFormat()
        chatGraph_format.setForeground(QColor(chatGraph))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))

        keyword_patterns = [
            r'\bdef\b', r'\bclass\b', r'\bimport\b', r'\bfrom\b', r'\bif\b',
            r'\bwhile\b', r'\bfor\b', r'\belse\b', r'\belif\b', r'\breturn\b',
            r'\btry\b', r'\bexcept\b', r'\bfinally\b', r'\braise\b', r'\bwith\b',
            r'\bcontinue\b', r'\bpass\b', r'\bbreak\b', r'\bassert\b', r'\bprint\b'
        ]

        self.rules = [
            (QRegExp(pattern), keyword_format) for pattern in keyword_patterns
        ]

        self.rules += [
            (QRegExp(r'\bclass\b\s*(\w+)'), class_format, 1),
            (QRegExp(r'\bdef\s+(\w+)'), function_format, 1),
            (QRegExp(r'#.*'), comment_format),
            (QRegExp(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format),
            (QRegExp(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format),
            (QRegExp(r'\{(\w+)\}'), chatGraph_format, 1)
        ]

    def highlightBlock(self, text):
        for pattern, _format, *group in self.rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, _format)
                index = expression.indexIn(text, index + length)

                # if group:
                #     self.setFormat(index + expression.pos(group[0]), expression.cap(group[0]).length(), _format)

        self.setCurrentBlockState(0)