__author__ = 'ee364h05'

import os
import sys
import SteganographyGUI
import glob

from PySide.QtGui import *
from SteganographyGUI import *
from Steganography import *

# ------------- New Steganography Class -------------
class NewSteganography( Steganography ):

    # ------------- Constructor -------------

    #   Parameters: 2
    #   1.  imagePath:      Path to image file
    #   2.  direction:      Direction to use for medium

    # ------------- Member Functions -------------
    #   Function to erase embedded message in medium
    #   Parameters: None
    def wipeMedium(self):
        #   Get image parameters
        imageWidth, imageHeight = self.image.size
        pixelList = list( self.image.getdata() )

        #   Bit manipulation:   Setting LSB to 0
        for pixel in pixelList:
            if pixel % 2 == 1:
                pixel -= 1;

        #   Save image
        image = Image.frombuffer( 'L', ( imageWidth, imageHeight ), bytearray( pixelList ), 'raw', 'L', 0, 1 )
        image.save()

    #   Function to check if message exists in medium
    #   Parameters: None
    def checkIfMessageExists(self):
        #   Read pixelData
        byteList = []
        byteString = ""

        #   Horizontal Scan
        if self.direction == "horizontal":
            for row in range( self.image.size[1] ):
                for col in range( self.image.size[0] ):
                    #   Get LSB
                    if self.pixelMap[ col, row ] % 2 == 0:
                        lsb = '0'
                    else:
                        lsb = '1'
                    byteString += lsb
                    if len( byteString ) == 8:
                        byteList.append( byteString )
                        byteString = ""

        #   Vertical Scan
        elif self.direction == "vertical":
            for col in range( self.image.size[0] ):
                for row in range( self.image.size[1] ):
                    #   Get LSB
                    if self.pixelMap[ col, row ] % 2 == 0:
                        lsb = '0'
                    else:
                        lsb = '1'
                    byteString += lsb
                    if len( byteString ) == 8:
                        byteList.append( byteString )
                        byteString = ""

        #   Extract string
        extractedString = ""
        for byte in byteList:
            character = chr( int( byte, 2) )
            extractedString += character

        result = ( False, None )

        #   Check if valid message
        match = re.findall( r"(<\?xml.*\n*.*\n.*\n.*</message>)", extractedString )
        if match:
            messageType = re.findall( r"message type=\"(.*?)\"", match[0] )
            if messageType:
                result = ( True, messageType[0] )

        return result

# ------------- SteganographyBrowser Class -------------
class SteganographyBrowser( QMainWindow, Ui_MainWindow ):

    # ------------- Constructor -------------
    def __init__(self, parent=None):

        super(SteganographyBrowser, self).__init__(parent)
        self.setupUi(self)

        #   Get folder browser to get folder path
        folderPath = QFileDialog.getExistingDirectory( self, caption="Open folder with images" )
        if not folderPath:
            return

        self.folderPath = folderPath

        #   Connect Buttons

        self.initialize( folderPath )

    # ------------- Initial State -------------
    def initialize(self, folderPath):
        #   Get files in folder
        filesInFolder = glob.glob( "{0}/*".format( folderPath ) )

        for file in filesInFolder:
            print( file )
            item = QTreeWidgetItem()
            filename = re.findall( r'.*\\(.*)', file )[0]
            item.setText( 0, filename )
            self.fileTreeWidget.addTopLevelItem( item )

def main():
    browswerApp = QApplication(sys.argv)
    browserForm = SteganographyBrowser()

    browserForm.show()
    browswerApp.exec_()
    pass

if __name__ == "__main__":
    main()