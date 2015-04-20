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

    ###     Constructor

    #   Parameters: 2
    #   1.  imagePath:      Path to image file
    #   2.  direction:      Direction to use for medium
    def __init__(self, imagePath, direction='horizontal'):
        Steganography.__init__( self, imagePath, direction )

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
        extractedString = ""
        result = ( False, None )

        bitCount = 0
        #   Horizontal Scan
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

                if bitCount > 800:
                    break

                bitCount += 1

        #   Extract string
        for byte in byteList:
            character = chr( int( byte, 2) )
            extractedString += character

        #   Check if valid message
        match = re.findall( r"(<\?xml.*\n.*)", extractedString )
        if match:
            messageType = re.findall( r"message type=\"(.*?)\"", match[0] )
            if messageType:
                result = ( True, messageType[0] )
                return result

        #   Reset for vertical scan
        byteList = []
        byteString = ""
        extractedString = ""
        bitCount = 0

        #   Vertical Scan
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

                if bitCount > 800:
                    break

                bitCount += 1

        #   Extract String
        extractedString = ""
        for byte in byteList:
            character = chr( int( byte, 2) )
            extractedString += character

        #   Check if valid message
        match = re.findall( r"(<\?xml.*\n.*)", extractedString )
        if match:
            messageType = re.findall( r"message type=\"(.*?)\"", match[0] )
            if messageType:
                result = ( True, messageType[0] )
                return result

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
            sys.exit(self.exec_())

        self.folderPath = folderPath
        #   Initialize to initial state
        self.initialize( folderPath )

        #   Connect Signals
        self.fileTreeWidget.itemClicked.connect( lambda : self.getMessage() )

    # ------------- Initial State -------------
    def initialize(self, folderPath):
        #   Set other views to disabled
        self.viewMedium.setDisabled( True )
        self.stackMessage.setDisabled( True )
        self.btnExtract.setDisabled( True )
        self.btnWipeMedium.setDisabled( True )

        #   Get files in folder
        filesInFolder = glob.glob( "{0}/*".format( folderPath ) )

        #   Go over every file in folder
        for file in filesInFolder:

            filename = re.findall( r'.*\\(.*)', file )[0]

            #   Create new Tree Widget Item
            item = QTreeWidgetItem()
            item.setText( 0, filename )
            brush = QBrush()
            font = QFont()
            font.setBold( True )

            #   Check if image has message
            img = NewSteganography( file, "horizontal" )
            res = img.checkIfMessageExists()
            if res[0]:
                #   Set brush to red
                brush.setColor(QColor( 'red' ))
                #   Set font and color to item
                item.setFont(0, font)
                item.setForeground(0, brush)

                #   Create child widget item
                imageTypeItem = QTreeWidgetItem()
                #   Set brush to green
                brush.setColor(QColor('green'))
                imageTypeItem.setForeground(0, brush)
                imageTypeItem.setText( 0, res[1] )
                item.addChild( imageTypeItem )

            else:
                #   Set brush to blue
                brush.setColor( QColor('blue') )
                item.setForeground(0, brush)

            #   Add Item to parent tree
            self.fileTreeWidget.addTopLevelItem( item )
            item.setExpanded( True )

    def getMessage(self):
        print( "Item Clicked!!" )
        item = self.fileTreeWidget.currentItem()
        #   Check if sub child is clicked
        if item.parent():
            itemParent = item.parent()
        else:
            itemParent = item

        #   Check if item has message
        imgPath = self.folderPath + "\\" + itemParent.text(0)
        image = NewSteganography( imagePath=imgPath )

        result = image.checkIfMessageExists()
        if result[0]:
            #   Message Exists
            self.embeddedMedium( imgPath, image )
        else:
            #   Message Doesn't exist
            self.displayImage( imgPath )

    def embeddedMedium(self, imagePath, image ):
        self.viewMedium.setEnabled( True )
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(imagePath))
        self.viewMedium.setScene( scene )
        self.viewMedium.show()
        pass

    def displayImage(self, imagePath ):
        self.viewMedium.setEnabled( True )
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(imagePath))
        self.viewMedium.setScene( scene )
        self.viewMedium.show()

def main():
    browserApp = QApplication(sys.argv)
    browserForm = SteganographyBrowser()

    browserForm.show()
    browserApp.exec_()
    pass

if __name__ == "__main__":
    main()