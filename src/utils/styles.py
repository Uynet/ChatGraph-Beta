import re

from PyQt5.QtGui import QColor

from utils.util import Console, Util


def extract_css_string(css_file_content, class_name):
    regex = r"(\." + re.escape(class_name) + r"[^}]*\{[^}]*\}(?:\s*\." + re.escape(class_name) + r"::[a-zA-Z0-9-_:]*\s*\{[^}]*\})*)"
    matches = re.findall(regex, css_file_content, re.MULTILINE)

    return "\n".join(matches)

customStyleFileName = "customStyle.scss"
colorFileName = "colors.scss"
nodeWindowFilaName = "nodeWindow.scss"


class Styles:
    cashe = {}
    def getCustomStyle(filename , value):
        with open(filename  , "r" , encoding="utf-8") as file:
            scss_content = file.read()

        scss_content = re.sub(r'//.*', '', scss_content)
        pattern = r'\$' + re.escape(value) + r':\s*([^;]+);'
        match = re.search(pattern, scss_content)

        if match:
            color_code = match.group(1).strip()
            return (color_code)
        else:
            Console.error(f"style '{value}' not found in SCSS file '{filename}'")
            return "#000000"

    def getNodeWindowStyle(value):
        path = Util.getCustomStylePath(nodeWindowFilaName) 
        return Styles.getCustomStyle(path, value)

    def getColor(color_name):
        scss_file_path = Util.getCustomStylePath(colorFileName ) 
        return Styles.getCustomStyle(scss_file_path , color_name)
    def getQColor(color_name):
        scss_file_path = Util.getCustomStylePath(colorFileName ) 
        colorCode:str = Styles.getCustomStyle(scss_file_path , color_name)
        return QColor(colorCode)

    def replace_variables(css_str, variables):
        def replacer(match):
            var_name = match.group(1)
            return str(variables.get(var_name, match.group(0)))

        regex = r"\$\{([a-zA-Z0-9_]+)\}"
        return re.sub(regex, replacer, css_str)


    def qClass(className , QElem , file = customStyleFileName):
        filename = Util.getCustomStylePath(file)
        # cache
        if className in Styles.cashe:
            return Styles.cashe[className]

        with open(filename, "r") as file:
            css_str = file.read()
        s = extract_css_string(css_str, className)
        
        # pyQtの仕様に合わせて変換
        # .className -> QMenu など
        s = s.replace("." + className , QElem)
        # cache
        Styles.cashe[className] = s
        return s


    def className(className , cssFile = customStyleFileName):
        # cache
        if className in Styles.cashe:
            return Styles.cashe[className]

        filename = Util.getCustomStylePath(cssFile)
        with open(filename, "r") as file:
            css_str = file.read()
            pattern = r'\.' + className + r'\s*{([^}]*)}'
            match = re.search(pattern, css_str)
            if match:
                s = match.group(1)
            else:
                s = "" 
                Console.error(f"style '{className}' not found in SCSS file '{filename}'")
            Styles.cashe[className] = s
            return s 