#! /usr/bin/env python3.4
__author__ = 'ee364h05'

import sys
import os
import base64

#   Message Class
class Message:

    ###     Constructor

    #   Type 1: two parameters
    #   1.  filePath:       Path to load message file
    #   2.  messageType:    Type of message(Text, GrayImage, ColorImage)
    def __init__(self, filePath, messageType):
        pass
    #   Type 2: one parameter
    #   1.  XmlString:      Input XML string
    def __init__(self, XmlString):
        pass

    ###     Member Functions

    #   Function to get message size
    #   Parameters: None
    def getMessageSize(self):
        pass

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