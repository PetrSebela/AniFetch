import os


class frame:
    def __init__(self, screenSize=None, border=False, borderSpacingX=0, borderSpacingY=0) -> None:
        self.screenSize = screenSize
        self.border = border
        self.borderSpacingX = borderSpacingX
        self.borderSpacingY = borderSpacingY

        self.width, self.height = os.get_terminal_size()

        self.charMetrix = [
            [" " for _ in range(self.width)] for _ in range(self.height - 1)]

    def colorString(self, string, color) -> str:
        return f"\033[{color}m{string}\033[00m"

    def addString(self, text, x=0, y=0, color=0):
        for offset, char in enumerate(text):
            self.charMetrix[y][x+offset] = self.colorString(char, color)

    def addAsciiArt(self, image, x=0, y=0, style=""):
        for offsetY, line in enumerate(image):
            for offsetX, pixel in enumerate(line):
                self.charMetrix[y+offsetY][x +
                                           offsetX] = self.colorString(pixel, style)

    def show(self, clearOnStart, frameTag):
        if clearOnStart:
            os.system('clear')
        if self.screenSize == 'fit':
            maxWidth, maxHeight = 0, 0
            for lIndex, line in enumerate(self.charMetrix):
                tmpMax = 0
                emptyLine = True
                for pIndex, pixel in enumerate(line):
                    if not pixel == " ":
                        emptyLine = False
                        tmpMax = pIndex + 1
                if not emptyLine:
                    maxHeight = lIndex + 1
                if tmpMax > maxWidth:
                    maxWidth = tmpMax

            self.width, self.height = maxWidth, maxHeight

        renderMetrix = [["" for _ in range(self.width)]
                        for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                renderMetrix[y][x] = self.charMetrix[y][x]

        if self.border:
            print('╭─' + frameTag + '─' * (self.width +
                  self.borderSpacingX*2 - len(frameTag) - 1) + '╮')

        for _ in range(self.borderSpacingY):
            renderMetrix.insert(0, [" " for _ in range(self.width)])
            renderMetrix.append([" " for _ in range(self.width)])

        for line in renderMetrix:
            if self.border:
                construct = '│' + " " * self.borderSpacingX + \
                    "".join(line) + " " * self.borderSpacingX + '│'
            else:
                construct = "".join(line)
            print(construct)

        if self.border:
            print('╰' + '─' * (self.width + (2*self.borderSpacingX)) + '╯')


if __name__ == "__main__":
    frame = frame()
    frame.addText("Hello", 10, 10, 32)
