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
        self.imagePath = imagePath

    # ------------- Member Functions -------------
    #   Function to erase embedded message in medium
    #   Parameters: None
    def wipeMedium(self):
        #   Get image parameters
        imageWidth, imageHeight = self.image.size
        numPixels = imageWidth * imageHeight
        pixelList = list( self.image.getdata() )

        #   Bit manipulation:   Setting LSB to 0
        for i in range( numPixels ):

            if pixelList[i] % 2 == 1:
                pixelList[i] -= 1;

        #   Save image
        image = Image.frombuffer( 'L', ( imageWidth, imageHeight ), bytearray( pixelList ), 'raw', 'L', 0, 1 )
        image.putdata( pixelList )
        image.save( self.imagePath )
        print( "Wiped Message" )

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
        self.btnWipeMedium.clicked.connect( lambda : self.wipeMessage() )
        self.btnExtract.clicked.connect( lambda : self.getMessageInMedium() )

    def disableAll(self):
        #   Set other views to disabled
        self.viewMedium.setDisabled( True )
        self.stackMessage.setDisabled( True )
        self.btnExtract.setDisabled( True )
        self.btnWipeMedium.setDisabled( True )

    def clearMessageMedium(self):
        self.viewMessage.setScene( None )

    # ------------- Initial State -------------
    def initialize(self, folderPath):
        self.disableAll()

        #   Get files in folder
        filesInFolder = glob.glob( "{0}/*".format( folderPath ) )

        #   Go over every file in folder
        for file in filesInFolder:

            #   Get three widget item
            item = self.createTreeItem( file )

            #   Add item to parent
            self.fileTreeWidget.addTopLevelItem( item )
            item.setExpanded( True )

    def createTreeItem(self, file):

        filename = re.findall( r'.*\\(.*)', file )[0]

        item = QTreeWidgetItem()
        item.setText( 0, filename )
        font = QFont()
        font.setBold( True )

        #   Check if image has message
        img = NewSteganography( file, "horizontal" )
        res = img.checkIfMessageExists()

        if res[0]:
            #   Set font and color to item
            item.setFont(0, font)
            self.changeColor( item, 'red', 0 )

            #   Create child widget item
            imageTypeItem = QTreeWidgetItem()
            #   Set color to green
            self.changeColor( imageTypeItem, 'green', 0 )
            imageTypeItem.setText( 0, res[1] )
            item.addChild( imageTypeItem )

        else:
            #   Set color to blue
            self.changeColor( item, 'blue', 0 )

        return item



    def changeColor(self, item, color, column):
        brush = QBrush()
        brush.setColor(QColor(color))
        item.setForeground(column,brush)

    def getMessage(self):
        print( "Item Clicked!!" )
        self.clearMessageMedium()
        item = self.fileTreeWidget.currentItem()
        #   Check if sub child is clicked
        if item.parent():
            itemParent = item.parent()
        else:
            itemParent = item

        self.selectedItem = itemParent

        #   Check if item has message
        imgPath = self.folderPath + "\\" + itemParent.text(0)
        self.image = NewSteganography( imagePath=imgPath )

        result = self.image.checkIfMessageExists()
        if result[0]:
            #   Message Exists
            self.embeddedMedium( imgPath )
        else:
            #   Message Doesn't exist
            self.displayImage( imgPath )

    def embeddedMedium(self, imagePath ):
        #   Enable options
        self.btnExtract.setEnabled( True )
        self.btnWipeMedium.setEnabled( True )
        self.stackMessage.setEnabled( True )

        #   Check message type for stack Message
        child = self.selectedItem.child(0)
        messageType = child.text(0)

        if messageType == "Text":
            #   Change to Text View
            self.stackMessage.setCurrentIndex(1)

        else:
            #   Change to graphics View
            self.stackMessage.setCurrentIndex(0)

        #   Display chosen image
        self.viewMedium.setEnabled( True )
        self.showImage( self.viewMedium, imagePath )

    def displayImage(self, imagePath ):
        #   Set other views to disabled
        self.stackMessage.setDisabled( True )
        self.btnExtract.setDisabled( True )
        self.btnWipeMedium.setDisabled( True )
        #   Display the chosen image
        self.viewMedium.setEnabled( True )
        self.showImage( self.viewMedium, imagePath )

    def showImage(self, view, imagePath):
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(imagePath))
        view.setScene( scene )
        view.show()

    def wipeMessage(self):

        #   Confirm irreversible action
        box = self.createMessageBox()
        ret = box.exec_()
        print( str( ret ))
        if ret == 16384:
            self.btnWipeMedium.setDisabled( True )
            self.clearMessageMedium()
            self.txtMessage.setPlainText("")
            self.stackMessage.setDisabled( True )
            self.image.wipeMedium()

    def createMessageBox(self):
        dialogBox = QMessageBox()
        dialogBox.setText( "Are you sure you want to wipe the medium?" )
        dialogBox.setStandardButtons( QMessageBox.Yes | QMessageBox.Cancel )
        return dialogBox

    def getMessageInMedium(self):
        self.btnExtract.setDisabled( True )
        #   Get message from image
        message = self.image.extractMessageFromMedium()
        messageType = message.getMessageTypeFromXML()

        if messageType == "Text":
            #   Extract text
            textMessage = message.getTextMessage()
            messageString = str( textMessage )[2:-1]
            self.txtMessage.setPlainText( messageString )
        else:
            #   Extract image
            message.saveToTarget("out.png")
            self.showImage( self.viewMessage, "out.png" )
            pass

def main():
    browserApp = QApplication(sys.argv)
    browserForm = SteganographyBrowser()

    browserForm.show()
    browserApp.exec_()
    pass

if __name__ == "__main__":
    main()