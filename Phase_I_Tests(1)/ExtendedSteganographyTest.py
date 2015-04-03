__author__ = 'Classifier'

import os
import uuid
import unittest
from PIL import Image

from Steganography import Message, Steganography
from ExtendedSteganography import AesMessage, ColorSteganography

def loadTwoTextFiles(path1, path2):
    """
    Load two text files and return them to allow for assertion of their content. A more elegant way to do that is to
    create a custom assertion function: assertTextEqual
    """
    with open(path1, 'r') as firstFile:
        first = firstFile.read()

    with open(path2, 'r') as secondFile:
        second = secondFile.read()

    return first, second

def loadTwoImageFiles(path1, path2):
    """
    Load two image files and return them to allow for assertion of their content. A more elegant way to do that is to
    create a custom assertion function: assertImageEqual
    """
    first = Image.open(path1)
    second = Image.open(path2)
    # first = list(Image.open(path1).getdata())
    # second = list(Image.open(path2).getdata())

    return first, second

class ExtendedSteganographyTestSuite(unittest.TestCase):

    testFileNames = []
    password = 'Bold & Beautiful'

    ext = '.png'

    def setUp(self):
        """
        Create a new file name to use if a test needs so.
        """
        self.targetTextFilePath = 'files/' + str(uuid.uuid4()) + '.txt'
        self.targetImageFilePath = 'files/' + str(uuid.uuid4()) + self.ext

        self.testFileNames.append(self.targetTextFilePath)
        self.testFileNames.append(self.targetImageFilePath)

    def test_embedEncryptedText(self):
        """
        Test the embedding of an encrypted text file in a medium.
        """
        sourcePath = 'files/full.txt'
        expectedPath = 'files/lena_full_enc' + self.ext
        mediumPath = 'files/lena' + self.ext

        message = Message(filePath=sourcePath, messageType='Text')
        encryptedMessage = AesMessage(message, self.password)

        medium = Steganography(mediumPath)
        medium.embedMessageInMedium(encryptedMessage, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedEncryptedGrayImage(self):
        """
        Test the embedding of an encrypted gray-scale image in a medium.
        """
        sourcePath = 'files/mona' + self.ext
        expectedPath = 'files/bridge_mona_enc' + self.ext
        mediumPath = 'files/bridge' + self.ext

        message = Message(filePath=sourcePath, messageType='GrayImage')
        encryptedMessage = AesMessage(message, self.password)

        medium = Steganography(mediumPath)
        medium.embedMessageInMedium(encryptedMessage, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedEncryptedColorImage(self):
        """
        Test the embedding of an encrypted color image in a medium.
        """
        sourcePath = 'files/color_mona' + self.ext
        expectedPath = 'files/bridge_color_mona_enc' + self.ext
        mediumPath = 'files/bridge' + self.ext

        message = Message(filePath=sourcePath, messageType='ColorImage')
        encryptedMessage = AesMessage(message, self.password)

        medium = Steganography(mediumPath)
        medium.embedMessageInMedium(encryptedMessage, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractEncryptedText(self):
        """
        Test the extraction of an encrypted text file in a medium.
        """
        sourcePath = 'files/lena_full_enc' + self.ext
        expectedPath = 'files/full.txt'

        medium = Steganography(sourcePath)
        extractedMessage = medium.extractMessageFromMedium()

        encryptedMessage = AesMessage(extractedMessage, self.password)
        encryptedMessage.saveToTarget(self.targetTextFilePath)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_extractEncryptedGrayImage(self):
        """
        Test the extraction of an encrypted gray-scale Image in a medium.
        """
        sourcePath = 'files/bridge_mona_enc' + self.ext
        expectedPath = 'files/mona' + self.ext

        medium = Steganography(sourcePath)
        extractedMessage = medium.extractMessageFromMedium()

        encryptedMessage = AesMessage(extractedMessage, self.password)
        encryptedMessage.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractEncryptedColorImage(self):
        """
        Test the extraction of an encrypted color image `in a medium.
        """
        sourcePath = 'files/bridge_color_mona_enc' + self.ext
        expectedPath = 'files/color_mona' + self.ext

        medium = Steganography(sourcePath)
        extractedMessage = medium.extractMessageFromMedium()

        encryptedMessage = AesMessage(extractedMessage, self.password)
        encryptedMessage.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_encryptedTextXml(self):
        """
        Test the XML representation of an encrypted text file to match the reference.
        """
        sourcePath = 'files/full.txt'
        expectedPath = 'files/full_enc.xml'

        message = Message(filePath=sourcePath, messageType='Text')
        encryptedMessage = AesMessage(message, self.password)

        with open(self.targetTextFilePath, 'w') as xmlFile:
            xmlString = encryptedMessage.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_encryptedGrayImageXml(self):
        """
        Test the XML representation of an encrypted gray-scale image to match the reference.
        """
        sourcePath = 'files/mona' + self.ext
        expectedPath = 'files/mona_enc.xml'

        message = Message(filePath=sourcePath, messageType='GrayImage')
        encryptedMessage = AesMessage(message, self.password)

        with open(self.targetTextFilePath, 'w') as xmlFile:
            xmlString = encryptedMessage.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_colorImageXml(self):
        """
        Test the XML representation of an encrypted color image to match the reference.
        """
        sourcePath = 'files/color_mona' + self.ext
        expectedPath = 'files/color_mona_enc.xml'

        message = Message(filePath=sourcePath, messageType='ColorImage')
        encryptedMessage = AesMessage(message, self.password)

        with open(self.targetTextFilePath, 'w') as xmlFile:
            xmlString = encryptedMessage.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_badMessageInitializerWithEmptyPassword(self):
        """
        Test that creating an 'AesMessage' instance with an empty password raises an exception.
        """
        sourcePath = 'files/full.txt'
        message = Message(filePath=sourcePath, messageType='Text')

        self.assertRaises(ValueError, AesMessage, message, password='')

    def test_badMessageInitializerWithEmptyMessageArgument(self):
        """
        Test that creating an 'AesMessage' instance with an improper first argument causes an exception.
        """
        self.assertRaises(ValueError, AesMessage, None, password='Something')

    def test_badMediumInitializerWithGrayImage(self):
        """
        Test that trying to create a 'ColorSteganography' instance using a gray-scale image, produces an exception.
        """
        imagePath = 'files/dog' + self.ext
        self.assertRaises(TypeError, ColorSteganography, imagePath)

    def test_embedTextHorizontal(self):
        """
        Test the embedding of a text file in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/full.txt'
        expectedPath = 'files/sunflower_full_h' + self.ext
        mediumPath = 'files/sunflower' + self.ext

        message = Message(filePath=sourcePath, messageType='Text')
        medium = ColorSteganography(mediumPath)
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedTextVertical(self):
        """
        Test the embedding of a text file in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/full.txt'
        expectedPath = 'files/sunflower_full_v' + self.ext
        mediumPath = 'files/sunflower' + self.ext

        message = Message(filePath=sourcePath, messageType='Text')
        medium = ColorSteganography(mediumPath, direction='vertical')
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedGrayImageHorizontal(self):
        """
        Test the embedding of a gray-scale image in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/lena' + self.ext
        expectedPath = 'files/tiger_lena_h' + self.ext
        mediumPath = 'files/tiger' + self.ext

        message = Message(filePath=sourcePath, messageType='GrayImage')
        medium = ColorSteganography(mediumPath)
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedGrayImageVertical(self):
        """
        Test the embedding of a gray-scale image in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/lena' + self.ext
        expectedPath = 'files/tiger_lena_v' + self.ext
        mediumPath = 'files/tiger' + self.ext

        message = Message(filePath=sourcePath, messageType='GrayImage')
        medium = ColorSteganography(mediumPath, direction='vertical')
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedColorImageHorizontal(self):
        """
        Test the embedding of a color image in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/sunflower' + self.ext
        expectedPath = 'files/lake_sunflower_h' + self.ext
        mediumPath = 'files/lake' + self.ext

        message = Message(filePath=sourcePath, messageType='ColorImage')
        medium = ColorSteganography(mediumPath)
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedColorImageVertical(self):
        """
        Test the embedding of a color image in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/sunflower' + self.ext
        expectedPath = 'files/lake_sunflower_v' + self.ext
        mediumPath = 'files/lake' + self.ext

        message = Message(filePath=sourcePath, messageType='ColorImage')
        medium = ColorSteganography(mediumPath, direction='vertical')
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractTextHorizontal(self):
        """
        Test the extraction of a text file in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/sunflower_full_h' + self.ext
        expectedPath = 'files/full.txt'

        medium = ColorSteganography(sourcePath)
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetTextFilePath)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_extractTextVertical(self):
        """
        Test the extraction of a text file in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/sunflower_full_v' + self.ext
        expectedPath = 'files/full.txt'

        medium = ColorSteganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetTextFilePath)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_extractGrayImageHorizontal(self):
        """
        Test the extraction of a gray-scale in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/tiger_lena_h' + self.ext
        expectedPath = 'files/lena' + self.ext

        medium = ColorSteganography(sourcePath)
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractGrayImageVertical(self):
        """
        Test the extraction of a gray-scale in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/tiger_lena_v' + self.ext
        expectedPath = 'files/lena' + self.ext

        medium = ColorSteganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractColorImageHorizontal(self):
        """
        Test the extraction of a color in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/lake_sunflower_h' + self.ext
        expectedPath = 'files/sunflower' + self.ext

        medium = ColorSteganography(sourcePath)
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractColorImageVertical(self):
        """
        Test the extraction of a color in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/lake_sunflower_v' + self.ext
        expectedPath = 'files/sunflower' + self.ext

        medium = ColorSteganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the created files, as unit tests are not supposed to change the environment.
        """
        for filePath in cls.testFileNames:

            if os.path.exists(filePath):
                os.remove(filePath)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
