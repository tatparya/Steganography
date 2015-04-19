#! /usr/bin/env python3.4
__author__ = 'ee364h05'

import sys
import os
import base64
import re
from PIL import Image

#-------------------   Message Class    ------------------
class Message:

    #-------------------   Function Overloads    ------------------

    def __init__( self, **kwargs ):
        numParameters = len( kwargs )

        self.XMLString = ""
        self.message = ""
        self.messageType = ""

        #   Check for type
        if numParameters == 2:
            #   Type 1: two parameters
            #   1.  filePath:       Path to load message file
            #   2.  messageType:    Type of message(Text, GrayImage, ColorImage)

            #   Get arguments
            filePath = kwargs["filePath"]
            messageType = kwargs["messageType"]
            self.messageType = messageType

            #   Check for messageType
            if messageType == "Text":
                message = ""
                #   Get text message
                try:
                    fp = open( filePath, 'r' )
                except:
                    raise ValueError( "File path invalid" )
                message = fp.read()
                x = bytes( message, 'UTF-8' )
                #   Encode message
                self.encodedMessage = base64.b64encode( x )
                #   Create XML String
                self.XMLString = self.getXmlString()

            elif messageType == "GrayImage" or messageType == "ColorImage":
                #   Open image
                im = Image.open( filePath )
                #   Get pixel list
                if messageType == "GrayImage":
                    pixelList = self.rasterScanGray( im )
                else:
                    pixelList = self.rasterScanColor( im )
                #   Encode message
                self.encodedMessage = self.encodePixelList( pixelList )
                #   Get image size
                self.imgSize = im.size
                #   Create XML String
                self.XMLString = self.getXmlString()

            else:
                #   Raise error
                raise ValueError( "Message type is invalid" )

        elif numParameters == 1:
            #   Type 2: one parameter
            #   1.  XmlString:      Input XML string
            #   Check for argument type
            try:
                XMLString = kwargs["XmlString"]
            except KeyError:



                raise ValueError( "Missing or invalid arguments" )
            #   Get message from XML
            self.XMLString = XMLString
            #   Get encoded message
            self.encodedMessage = self.getMessageFromXML()
            #   Get message type
            self.messageType = self.getMessageTypeFromXML()
            #   Check for messageType
            if self.messageType not in [ "Text", "GrayImage", "ColorImage" ]:
                #   Raise error
                raise ValueError( "Invalid message type" )

        else:
            #   Raise Error
            raise ValueError("Invalid number of arguments to constructor")

    def __str__(self):
        string = "Encoded Message: {0}\nMessage Type: {1}\nMessage Size: {2}\nXML String: {3}".format( self.encodedMessage, self.messageType, self.getSizeFromXML(), self.XMLString )
        return string

    #-------------------   Member Functions    ------------------

    #   Function to get message size of current XML representation
    #   Parameters: None
    def getMessageSize(self):
        if self.XMLString:
            string = self.XMLString
            length = len( string )
            return length
        else:
            #   Raise exception
            raise Exception( "No data exists in instance" )

    #   Function to save message to image
    #   Parameters: 1
    #   1.  targetImagePath: Target path to image file
    def saveToImage(self, targetImagePath):
        if not self.XMLString:
            #   Raise error
            raise Exception( "No data exists in instance" )

        #   Get image size
        size = self.getSizeFromXML()

        #   Check message type
        if self.messageType == "GrayImage":
            image = Image.new( 'L', size, "black" )
        elif self.messageType == "ColorImage":
            image = Image.new( 'RGB', size, "black" )
        else:
            #   Raise error
            raise TypeError( "Message is not text type" )

        self.createImageFromMessage( image )

        #   Save image
        image.save( targetImagePath )

    #   Function to save message to text file
    #   Parameters: 1
    #   1.  targetTextFilePath: Target path to text file
    def saveToTextFile(self, targetTextFilePath):
        #   Check message type
        if not self.messageType == "Text":
            #   Raise error
            raise TypeError( "Message is not text type" )
        #   Get message string from encoded message
        message = self.getTextMessage()
        if message:
            #   Write to file
            fp = open( targetTextFilePath, 'wb' )
            fp.write( message )
            fp.close()
            pass
        else:
            #   Raise error
            raise Exception( "No data exists in instance")

    #   Function to call save message to target based on target type
    #   Parameters: 1
    #   1.  targetPath: Target path to target file
    def saveToTarget(self, targetPath):
        #   Find message type
        if self.messageType == "Text":
            #   Text message
            self.saveToTextFile( targetPath )
        elif self.messageType == "GrayImage" or self.messageType == "ColorImage":
            #   Image message
            self.saveToImage( targetPath )

    #   Function returns serialized XML String
    #   Parameters: None
    def getXmlString(self ):
        messageType = self.messageType
        encodedMessage = self.encodedMessage
        if messageType == "Text":
            size = len( base64.b64decode( encodedMessage ) )
        else:
            size = "{0},{1}".format( self.imgSize[0], self.imgSize[1] )
        if encodedMessage:
            retString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<message type=\"{0}\" size=\"{1}\" encrypted=\"False\">\n{2}\n</message>".format( messageType, size, str(encodedMessage)[2:-1] )
            return retString
        else:
            raise Exception( "No data exists in instance" )

    #-------------------   Helper Functions    ------------------

    #   Function to create pixel map from message
    def createImageFromMessage(self, image):
        #   Get message
        encodedMessage = self.getMessageFromXML()   #    Gives encoded message
        messageBinaryArray = base64.b64decode( encodedMessage ) #    Gives bytearray

        pixelMap = image.load()

        #   Modify pixels
        if self.messageType == "GrayImage":
            image.putdata( messageBinaryArray )
         #   for row in range( image.size[1] ):
          #      for col in range( image.size[0] ):
           #         pixelMap[ col,row ] = messageBinaryArray[ row * image.size[1] + col ]

        if self.messageType == "ColorImage":
            #   Create sequences for rgb
            sequence = []
            size = ( image.size[0] * image.size[1] )
            for row in range( image.size[1] ):
                for col in range( image.size[0] ):
                    red = messageBinaryArray[ row * image.size[1] + col ]
                    green = messageBinaryArray[ size + row * image.size[1] + col ]
                    blue = messageBinaryArray[ size * 2 + row * image.size[1] + col ]
                    sequence.append( (red, green, blue) )
            image.putdata( sequence )
        #    size = ( image.size[0] * image.size[1] )
         #   for row in range( image.size[1] ):
          #      for col in range( image.size[0] ):
           #         pixelMap[ col,row ] = ( messageBinaryArray[ row * image.size[1] + col ], messageBinaryArray[ size + row * image.size[1] + col ], messageBinaryArray[ size * 2 + row * image.size[1] + col ] )


    #   Function to return decoded text message string
    #   Parameters: None
    def getTextMessage(self):
        if self.encodedMessage:
            message = base64.b64decode( self.encodedMessage )
            return message
        else:
            return None

    #   Function to get message from the xmlString
    #   Parameters: None
    def getMessageFromXML(self):
        string = self.XMLString
        match = re.findall( r"<message.*>\n(.*)\n</message>", string )
        if match:
            encodedMessage = match[0]
            return encodedMessage
        else:
            return None

    #   Function to get message type from the xmlString
    #   Parameters: None
    def getMessageTypeFromXML(self):
        string = self.XMLString
        match = re.findall( r"message type=\"(.*)\" size", string )
        if match:
            messageType = match[0]
            return messageType
        else:
            return None

    #   Function to get message size from the xmlString
    #   Parameters: None
    def getSizeFromXML(self):
        string = self.XMLString
        match = re.findall( r"size=\"(.*)\" encrypted", string )
        if match:
            if self.messageType == "Text":
                size = match[0]
            else:
                numbers = re.findall( r"(.*),(.*)", match[0] )
                if numbers:
                    size = ( int(numbers[0][0]), int(numbers[0][1]) )
            return size
        else:
            return None

    #   Function to raster scan image and return serialized list of pixels
    #   Parameters: 1
    #   1.  image:          Image object to be scanned
    def rasterScanGray(self, image):
        pixelData = image.load()
        pixelList = []

        #   Make list from pixel map
        for row in range( image.size[1] ):
            for col in range( image.size[0] ):
                pixelList.append( pixelData[ col,row ] )

        return pixelList

    def rasterScanColor(self, image):
        pixelData = image.load()
        pixelList = []

        #   Make list from pixel map
        for row in range( image.size[1] ):
            for col in range( image.size[0] ):
                pixelList.append( pixelData[ col,row ][0] )

        for row in range( image.size[1] ):
            for col in range( image.size[0] ):
                pixelList.append( pixelData[ col,row ][1] )

        for row in range( image.size[1] ):
            for col in range( image.size[0] ):
                pixelList.append( pixelData[ col,row ][2] )

        return pixelList

    #   Function to return encoded image message
    #   Parameters: 1
    #   1.  pixelList:      List of pixels to be encoded
    def encodePixelList(self, pixelList):
        binaryPixelArray = bytearray( pixelList )
        encodedMessage = base64.b64encode( binaryPixelArray )

        return encodedMessage

#   Steganography Class
class Steganography:

    ###     Constructor

    #   Parameters: 2
    #   1.  imagePath:      Path to image file
    #   2.  direction:      Direction to use for medium
    def __init__(self, imagePath, direction='horizontal'):
        #   Try to open image
        try:
            self.image = Image.open( imagePath )
            self.size = self.image.size
            self.direction = direction
            #   Load pixelMap
            self.pixelMap = self.image.load()
        except:
            raise ValueError( "Invalid path to image file")

        #   Check image type
        if self.image.mode != "L":
            #   Raise error
            raise TypeError( "Image is not a GrayImage" )

        #   Get max message size that can be stored
        self.maxMessageSize = self.image.size[0] * self.image.size[1] / 8
        #print( int( self.maxMessageSize ) )

    ###     Member Functions

    #   Function to embed message in image
    #   Parameters: 2
    #   1.  message:            Message to be embedded
    #   2.  targetImagePath:    Target path to image
    def embedMessageInMedium(self, message, targetImagePath):
        
        size = message.getMessageSize()
        if size > self.maxMessageSize:
            raise ValueError( "Message is larger than what the medium can hold" )

        bitString = ""

        #   Create a steam of bits in the message
        for character in message.XMLString:
            bitString += self.getBitString(character)

        #   Get image parameters
        imageWitdh, imageHeight = self.image.size
        pixelList = list(self.image.getdata())

        #   Get direction
        if self.direction == "horizontal":
            pixCount = 0
            #   Bit manipulation: embedding bits into the medium
            for bit in bitString:
                if bit == '1':
                    if pixelList[ pixCount ] % 2 == 0:
                        pixelList[ pixCount ] += 1
                        #   Check overflow
                        if pixelList[ pixCount ] >= 256:
                            pixelList[ pixCount ] -=    2
                elif bit == '0':
                    if pixelList[ pixCount ] % 2 == 1:
                        pixelList[ pixCount ] -= 1
                        #   Check overflow
                        if pixelList[ pixCount ] < 0:
                            pixelList[ pixCount ] += 2
                pixCount += 1

        #   For vertical scan
        else:
            newMessageList = []

            #   Iterate through message list and create new list
            for row in range( imageWitdh ):
                for col in range( imageHeight ):
                    newMessageList.append( pixelList[ col * imageWitdh + row ] )

            pixelList = newMessageList

            pixCount = 0
            for i in bitString:
                #   Bit manipulation: embedding bits into the medium
                if i == '1':
                    if pixelList[ pixCount ] % 2 == 0:
                        pixelList[ pixCount ] += 1
                        #   Check overflow
                        if pixelList[ pixCount ] >= 256:
                            pixelList[ pixCount ] -= 2
                elif i == '0':
                    if pixelList[ pixCount ] % 2 == 1:
                        pixelList[ pixCount ] -= 1
                        #   Check overflow
                        if pixelList[ pixCount ] < 0:
                            pixelList[ pixCount ] += 2
                pixCount += 1

            newMessageList = []
            #   For vertical scan go through list again and create new to transpose

            for row in range(imageHeight):
                for col in range(imageWitdh):
                    newMessageList.append( pixelList[col*imageHeight + row] )

            pixelList = newMessageList

        image = Image.frombuffer( 'L', ( imageWitdh, imageHeight ), bytearray( pixelList ), "raw", 'L', 0, 1 )
        image.save( targetImagePath )

    #   Function to extract message from medium
    #   Parameters: None
    def extractMessageFromMedium(self):
        #   Read pixelData
        byteList = []
        byteString = ""

        #---------------------- HORIZONTAL SCAN   ----------------------

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

        #---------------------- VERTICAL SCAN   ----------------------

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

        #   ByteList gets all of the bytes
        #print( byteList )

        #   Get extracted String
        extractedString = ""
        for byte in byteList:

            character = chr( int(byte, 2) )
            extractedString += character

        #print( extractedString )

        #   Check if valid message
        match = re.findall( r"(<\?xml.*\n*.*\n.*\n.*</message>)", extractedString )
        #print( len(match) )
        if match:
            #   Message is valid
            self.message = Message( XmlString=match[0] )
            #print( "Extracted Message:")
            #print( self.message )
            return self.message

    ###     Helper Functions

    #   Function to get an 8-bit binary string representation of a char
    #   Parameters: char
    def getBitString(self, char):

        asciiChar = ord( char )
        binaryChar = str( bin( asciiChar ) )[2:]

        #   If binaryChar is not 8-bit, pad with 0's
        while len( binaryChar ) < 8:
            binaryChar = '0' + binaryChar

        return binaryChar

    def embedCustomMessage(self, messageStr, targetImagePath ):
        size = len( messageStr )
        #   Check if message can fit in medium
        if size > self.maxMessageSize:
            #raise ValueError( "Message is larget than what the medium can hold" )
            pass

        print( "Embedding: ", messageStr )

        pixelCount = 0
        #   Get each symbol in string
        for letter in messageStr:
            #print( letter, ": ", ord(letter ))
            for i in range(8):
                #   Gets each bit
                bit = ( ord(letter) >> 8-i-1 ) & 1
                #print( bit, ": ", 8-i-1 )
                #   Embed bit in message
                if bit == 0:
                    if self.pixelList[ pixelCount ] % 2 != 0:
                        self.pixelList[ pixelCount ] += 1
                elif bit == 1:
                    if self.pixelList[ pixelCount ] % 2 == 0:
                        self.pixelList[ pixelCount ] -= 1
                pixelCount += 1

        #   Save the iamge to target path
        self.modifyPixData()
        targetImage.save( targetImagePath )
        print( "Here!!")

    def modifyPixData(self, targetImage ):
        #   Get direction
        direction = self.direction
        pixelMap = targetImage.load()

        #if direction == "horizontal":
        #    targetImage.putdata( self.pixelList )
        #elif direction == "vertical":
        #    targetImage.putdata( self.pixelList )

        if direction == "horizontal":
            for row in range( self.image.size[1] ):
                for col in range( self.image.size[0] ):
                    pixelMap[ col,row ] = self.pixelList[ row * self.image.size[1] + col ]

        elif direction == "vertical":
            for col in range( self.image.size[0] ):
                for row in range( self.image.size[1] ):
                    pixelMap[ col,row ] = self.pixelList[ col * self.image.size[0] + row ]

#   Main Block
def main():

    #mes = Message( filePath="testing.png", messageType="GrayImage" )
    #print( mes )
    #print( mes.getMessageSize() )
    #print( mes.getXmlString() )
    #de = mes.saveToTarget( "testSave2.png" )
    pass

if __name__ == "__main__":
    main()