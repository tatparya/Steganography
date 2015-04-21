__author__ = 'ee364h05'

import os
import sys
import glob

from PySide.QtCore import *
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
            sys.exit()

        self.folderPath = folderPath
        #   Initialize to initial state
        self.initialize( folderPath )

        #   Connect Signals
        self.fileTreeWidget.itemClicked.connect( lambda : self.getSelectedImage() )
        self.btnWipeMedium.clicked.connect( lambda : self.wipeMessage() )
        self.btnExtract.clicked.connect( lambda : self.getMessageInMedium() )

    # ------------- Member Functions -------------

    #   Function to disable all elements on widget
    #   Parameters: None
    def disableAll(self):
        #   Set other views to disabled
        self.viewMedium.setDisabled( True )
        self.stackMessage.setDisabled( True )
        self.btnExtract.setDisabled( True )
        self.btnWipeMedium.setDisabled( True )

    #   Function to disable all elements on widget
    #   Parameters: None
    def clearMessageMedium(self):
        self.viewMessage.setScene( None )

    #   Function to initialize app to initial state
    #   Parameters: 1
    #   1. folderPath: Path of the folder to be opened
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

    #   Function to create and return a tree widget item
    #   Parameters: 1
    #   1. file:    name of the file
    def createTreeItem(self, file):

        filename = re.findall( r'.*\\(.*)', file )[0]

        item = QTreeWidgetItem()
        item.setText( 0, filename )

        #   Check if image has message
        img = NewSteganography( file, "horizontal" )
        res = img.checkIfMessageExists()

        if res[0]:
            #   Set font and color to item
            self.setBold( item, True )
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

    #   Function to set the fond to bold
    #   Parameters: 2
    #   1. item:    Item to set bold on
    #   2. bool:    True / False
    def setBold( self, item, bool ):
        font = QFont()
        font.setBold( bool )
        item.setFont( 0, font )

    #   Function to set the color of text for an item
    #   Parameters: 3
    #   1. item:    Item to set color on
    #   2. color:   Color to set
    #   3. column:  Column in item
    def changeColor(self, item, color, column):
        brush = QBrush()
        brush.setColor(QColor(color))
        item.setForeground(column,brush)

    #   Function to open selected image in the View Medium
    #   Parameters: None
    def getSelectedImage(self):
        print( "Item Clicked!!" )
        self.clearMessageMedium()

        self.selectedItem = self.currentItem()

        #   Check if item has message
        imgPath = self.folderPath + "\\" + self.selectedItem.text(0)
        self.image = NewSteganography( imagePath=imgPath )

        result = self.image.checkIfMessageExists()
        if result[0]:
            #   Message Exists
            self.embeddedMedium( imgPath )
        else:
            #   Message Doesn't exist
            self.displayImage( imgPath )

    #   Function to get selected item in tree view
    #   Parameters: None
    def currentItem(self):
        item = self.fileTreeWidget.currentItem()
        #   Check if sub child is clicked
        if item.parent():
            itemParent = item.parent()
        else:
            itemParent = item

        selectedItem = itemParent
        return selectedItem

    #   Function to show selected medium and enable options
    #   Parameters: 1
    #   1. imagePath:   Path to the image to be opened
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

    #   Function to display image in the viewMedium
    #   Parameters: 1
    #   1. imagePath:   Path to the image
    def displayImage(self, imagePath ):
        #   Set other views to disabled
        self.stackMessage.setDisabled( True )
        self.btnExtract.setDisabled( True )
        self.btnWipeMedium.setDisabled( True )
        #   Display the chosen image
        self.viewMedium.setEnabled( True )
        self.showImage( self.viewMedium, imagePath )

    #   Function to show image in given view
    #   Parameters: 2
    #   1. view:        View where the image will be shown
    #   2. imagePath:   Path to the image
    def showImage(self, view, imagePath):
        scene = QGraphicsScene()
        image = QPixmap( imagePath )
        image2 = image.scaled(270, 250, Qt.KeepAspectRatio )
        scene.addPixmap(image2)
        view.setScene( scene )
        view.show()

    #   Function to wipe embedded message in medium
    #   Parameters: None
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
            #   Update current item in tree
            item = self.currentItem()
            item.removeChild( item.child(0) )
            self.changeColor( item, 'blue', 0 )
            self.setBold( item, False )

    #   Function to create and return a message box
    #   Parameters: None
    def createMessageBox(self):
        dialogBox = QMessageBox()
        dialogBox.setText( "Are you sure you want to wipe the medium?" )
        dialogBox.setStandardButtons( QMessageBox.Yes | QMessageBox.Cancel )
        return dialogBox

    #   Function to show message from medium    
    #   Parameters: None
    def getMessageInMedium(self):
        self.btnExtract.setDisabled( True )
        #   Get message from image
        message = self.image.extractMessageFromMedium()
        if not message:
            self.image.direction = "vertical"
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

    sys.exit(browserApp.exec_())

if __name__ == "__main__":
    main()