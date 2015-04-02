#! /usr/bin/env python3.4
__author__ = 'ee364h05'

import sys
import os
import base64

#   Message Class
class Message:

    ###     Constructor


    def __init__( self, **kwargs ):
        numParameters = len( kwargs )

        self.XMLString = ""

        #   Check for type
        if numParameters == 1:
            #   Type 1: two parameters
            #   1.  filePath:       Path to load message file
            #   2.  messageType:    Type of message(Text, GrayImage, ColorImage)

            filePath = kwargs[0]
            messageType = kwargs[1]
            #   Check for argument type
            if ( filePath is str and messageType is str ):
                #   Check for messageType
                if messageType == "Text" or messageType == "GrayImage" or messageType == "ColorImage":
                    #   Get message
                    with open( filePath,'r' ) as inputFile:
                        message = inputFile.readlines()
                        self.message = message
                        self.messageType = messageType
                else:
                    #   Raise error
                    raise ValueError( "Message type is not acceptable" )
            else:
                #   Raise error
                raise ValueError( "Arguments are not of the correct type. Expected: string, string" )

        elif numParameters == 2:
            #   Type 2: one parameter
            #   1.  XmlString:      Input XML string
            #   Check for argument type
            XMLString = kwargs[0]
            if ( XMLString is str ):
                #   Get message from XML
                self.XMLString = XMLString
            else:
                #   Raise error
                raise ValueError( "Argument is not of the correct type. Expected: string" )

        else:
            #   Raise Error
            raise ValueError("Invalid number of arguments to constructor")

    ###     Member Functions

    #   Function to get message size of current XML representation
    #   Parameters: None
    def getMessageSize(self):
        length = len( self.XMLString )
        return length

    #   Function to save message to image
    #   Parameters: 1
    #   1.  targetImagePath: Target path to image file
    def saveToImage(self):
        pass

    #   Function to save message to text file
    #   Parameters: 1
    #   1.  targetTextFilePath: Target path to text file
    def saveToTextFile(self):
        pass

    #   Function to save message to target
    #   Parameters: 1
    #   1.  targetPath: Target path to target file
    def saveToTarget(self):
        pass

    #   Function to get XML string
    #   Parameters: 1None
    def getXmlString(self):
        pass

    ###     Helper Functions

#   Steganography Class
class Steganography:

    ###     Constructor

    #   Parameters: 2
    #   1.  imagePath:      Path to image file
    #   2.  direction:      Direction to use for medium
    def __init__(self, imagePath, direction='horizontal'):
        pass

    ###     Member Functions

    #   Function to embed message in image
    #   Parameters: 2
    #   1.  message:            Message to be embedded
    #   2.  targetImagePath:    Target path to image
    def embedMessageInMedium(self):
        pass

    #   Function to extract message from medium
    #   Parameters: None
    def extractMessageFromMedium(self):
        pass

    ###     Helper Functions




#   Main Block
def main():
    pass

if __name__ == "__main__":
    main()