__author__ = 'Classifier'

import os
import uuid
import unittest
from PIL import Image
from Steganography import Message, Steganography

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

class SteganographyTestSuite(unittest.TestCase):

    testFileNames = []
    ext = '.png'

    def setUp(self):
        """
        Create a new file name to use if a test needs so.
        """
        self.targetTextFilePath = 'files/' + str(uuid.uuid4()) + '.txt'
        self.targetImageFilePath = 'files/' + str(uuid.uuid4()) + self.ext

        self.testFileNames.append(self.targetTextFilePath)
        self.testFileNames.append(self.targetImageFilePath)

    def test_embedShortTextHorizontal(self):
        """
        Test the embedding of a short text file in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/small.txt'
        expectedPath = 'files/mona_small_h' + self.ext
        mediumPath = 'files/mona' + self.ext

        message = Message(filePath=sourcePath, messageType='Text')
        medium = Steganography(mediumPath)
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedShortTextVertical(self):
        """
        Test the embedding of a short text file in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/small.txt'
        expectedPath = 'files/mona_small_v' + self.ext
        mediumPath = 'files/mona' + self.ext

        message = Message(filePath=sourcePath, messageType='Text')
        medium = Steganography(mediumPath, direction='vertical')
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedLongTextHorizontal(self):
        """
        Test the embedding of a long text file in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/full.txt'
        expectedPath = 'files/lena_full_h' + self.ext
        mediumPath = 'files/lena' + self.ext

        message = Message(filePath=sourcePath, messageType='Text')
        medium = Steganography(mediumPath)
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedLongTextVertical(self):
        """
        Test the embedding of a long text file in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/full.txt'
        expectedPath = 'files/lena_full_v' + self.ext
        mediumPath = 'files/lena' + self.ext

        message = Message(filePath=sourcePath, messageType='Text')
        medium = Steganography(mediumPath, direction='vertical')
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedGrayImageHorizontal(self):
        """
        Test the embedding of a gray-scale image in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/dog' + self.ext
        expectedPath = 'files/bridge_dog_h' + self.ext
        mediumPath = 'files/bridge' + self.ext

        message = Message(filePath=sourcePath, messageType='GrayImage')
        medium = Steganography(mediumPath)
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedGrayImageVertical(self):
        """
        Test the embedding of a gray-scale image in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/dog' + self.ext
        expectedPath = 'files/bridge_dog_v' + self.ext
        mediumPath = 'files/bridge' + self.ext

        message = Message(filePath=sourcePath, messageType='GrayImage')
        medium = Steganography(mediumPath, direction='vertical')
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedColorImageHorizontal(self):
        """
        Test the embedding of a color image in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/sunflower' + self.ext
        expectedPath = 'files/nature_sunflower_h' + self.ext
        mediumPath = 'files/nature' + self.ext

        message = Message(filePath=sourcePath, messageType='ColorImage')
        medium = Steganography(mediumPath)
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_embedColorImageVertical(self):
        """
        Test the embedding of a color image in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/sunflower' + self.ext
        expectedPath = 'files/nature_sunflower_v' + self.ext
        mediumPath = 'files/nature' + self.ext

        message = Message(filePath=sourcePath, messageType='ColorImage')
        medium = Steganography(mediumPath, direction='vertical')
        medium.embedMessageInMedium(message, self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractShortTextHorizontal(self):
        """
        Test the extraction of a short text file in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/mona_small_h' + self.ext
        expectedPath = 'files/small.txt'

        medium = Steganography(sourcePath)
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetTextFilePath)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_extractShortTextVertical(self):
        """
        Test the extraction of a short text file in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/mona_small_v' + self.ext
        expectedPath = 'files/small.txt'

        medium = Steganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetTextFilePath)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_extractLongTextHorizontal(self):
        """
        Test the extraction of a long text file in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/lena_full_h' + self.ext
        expectedPath = 'files/full.txt'

        medium = Steganography(sourcePath)
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetTextFilePath)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_extractLongTextVertical(self):
        """
        Test the extraction of a long text file in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/lena_full_v' + self.ext
        expectedPath = 'files/full.txt'

        medium = Steganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetTextFilePath)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_extractGrayImageHorizontal(self):
        """
        Test the extraction of a gray-scale in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/bridge_dog_h' + self.ext
        expectedPath = 'files/dog' + self.ext

        medium = Steganography(sourcePath)
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractGrayImageVertical(self):
        """
        Test the extraction of a gray-scale in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/bridge_dog_v' + self.ext
        expectedPath = 'files/dog' + self.ext

        medium = Steganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractColorImageHorizontal(self):
        """
        Test the extraction of a color in a medium, using a horizontal raster scan.
        """
        sourcePath = 'files/nature_sunflower_h' + self.ext
        expectedPath = 'files/sunflower' + self.ext

        medium = Steganography(sourcePath)
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_extractColorImageVertical(self):
        """
        Test the extraction of a color in a medium, using a vertical raster scan.
        """
        sourcePath = 'files/nature_sunflower_v' + self.ext
        expectedPath = 'files/sunflower' + self.ext

        medium = Steganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()
        message.saveToTarget(self.targetImageFilePath)

        actualImage, expectedImage = loadTwoImageFiles(self.targetImageFilePath, expectedPath)

        self.assertEqual(actualImage, expectedImage)

    def test_shortTextXml(self):
        """
        Test the XML representation of a short text file to match the reference.
        """
        sourcePath = 'files/small.txt'
        expectedPath = 'files/small.xml'

        message = Message(filePath=sourcePath, messageType='Text')

        with open(self.targetTextFilePath, 'w') as xmlFile:
            xmlString = message.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_longTextXml(self):
        """
        Test the XML representation of a long text file to match the reference.
        """
        sourcePath = 'files/full.txt'
        expectedPath = 'files/full.xml'

        message = Message(filePath=sourcePath, messageType='Text')

        with open(self.targetTextFilePath, 'w') as xmlFile:
            xmlString = message.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_grayImageXml(self):
        """
        Test the XML representation of a gray-scale image to match the reference.
        """
        sourcePath = 'files/dog' + self.ext
        expectedPath = 'files/dog.xml'

        message = Message(filePath=sourcePath, messageType='GrayImage')

        with open(self.targetTextFilePath, 'w') as xmlFile:
            xmlString = message.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_colorImageXml(self):
        """
        Test the XML representation of a color image to match the reference.
        """
        sourcePath = 'files/sunflower' + self.ext
        expectedPath = 'files/sunflower.xml'

        message = Message(filePath=sourcePath, messageType='ColorImage')

        with open(self.targetTextFilePath, 'w') as xmlFile:
            xmlString = message.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles(self.targetTextFilePath, expectedPath)

        self.assertEqual(actualTextFile, expectedTextFile)

    def test_badMessageInitializerWithMissingArgument(self):
        """
        Test that creating a 'Message' instance with a missing argument produces an exception.
        """
        sourcePath = 'files/small.txt'
        self.assertRaises(ValueError, Message, filePath=sourcePath)

    def test_badMessageInitializerWithWrongMessageType(self):
        """
        Test that creating a 'Message' instance with an invalid 'messageType' produces an exception.
        """
        self.assertRaises(ValueError, Message, messageType='Video')

    def test_badMessageInitializerWithEmptyMessageType(self):
        """
        Test that creating a 'Message' instance with an empty 'messageType' produces an exception.
        """
        sourcePath = 'files/small.txt'
        self.assertRaises(ValueError, Message, filePath=sourcePath, messageType='')

    def test_badMessageInitializerWithEmptyFilePath(self):
        """
        Test that creating a 'Message' instance with an empty 'fileName' produces an exception.
        """
        self.assertRaises(ValueError, Message, filePath='', messageType='Text')

    def test_badMessageInitializerWithEmptyXmlString(self):
        """
        Test that creating a 'Message' instance with an empty 'XmlString' produces an exception.
        """
        self.assertRaises(ValueError, Message, xmlString='')

    def test_badSavingGrayImageToText(self):
        """
        Test that trying to save a gray-scale image as a text produces an exception.
        """
        sourcePath = 'files/bridge_dog_h' + self.ext

        medium = Steganography(sourcePath)
        message = medium.extractMessageFromMedium()

        self.assertRaises(TypeError, message.saveToTextFile, self.targetImageFilePath)

    def test_badSavingColorImageToText(self):
        """
        Test that trying to save a color image as a text produces an exception.
        """
        sourcePath = 'files/nature_sunflower_v' + self.ext

        medium = Steganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()

        self.assertRaises(TypeError, message.saveToTextFile, self.targetImageFilePath)

    def test_badSavingTextToGrayImage(self):
        """
        Test that trying to save a text file as an image produces an exception.
        """
        sourcePath = 'files/mona_small_h' + self.ext

        medium = Steganography(sourcePath)
        message = medium.extractMessageFromMedium()

        self.assertRaises(TypeError, message.saveToImage, self.targetTextFilePath)

    def test_badMediumInitializerWithInvalidDirection(self):
        """
        Test that trying to create a 'Steganography' instance with an invalid scanning direction, produces an exception.
        """
        imagePath = 'nature' + self.ext
        self.assertRaises(ValueError, Steganography, imagePath, 'serpentine')

    def test_badMediumInitializerWithColorImage(self):
        """
        Test that trying to create a 'Steganography' instance using a color image, produces an exception.
        """
        imagePath = 'files/sunflower' + self.ext
        self.assertRaises(TypeError, Steganography, imagePath)

    def test_embedLargeMessageInSmallMedium(self):
        """
        Test that trying to embed a large message in medium, produces an exception.
        """
        sourcePath = 'files/sunflower' + self.ext
        mediumPath = 'files/mona' + self.ext

        message = Message(filePath=sourcePath, messageType='ColorImage')
        medium = Steganography(mediumPath)

        self.assertRaises(ValueError, medium.embedMessageInMedium, message, self.targetImageFilePath)

    def test_embedHorizontalExtractVertical(self):
        """
        Test that trying to extract a horizontal message using a vertical scan, produces an exception.
        """
        sourcePath = 'files/lena_full_h' + self.ext

        medium = Steganography(sourcePath, direction='vertical')
        message = medium.extractMessageFromMedium()

        self.assertEqual(message, None)

    def test_embedVerticalExtractHorizontal(self):
        """
        Test that trying to extract a vertical message using a horizontal scan, produces an exception.
        """
        sourcePath = 'files/mona_small_v' + self.ext

        medium = Steganography(sourcePath)
        message = medium.extractMessageFromMedium()

        self.assertEqual(message, None)

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
