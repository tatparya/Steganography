__author__ = 'ee364h05'
import Steganography

def main():
    #   Testing message class
    mes = Steganography.Message( filePath="testtxt.txt", messageType="Text" )
    #print( mes.getXmlString() )
    #print( mes.getTextMessage() )
    #mes.saveToTarget( "testingTxtSave.txt" )

    #   Testing steg class
    image = Steganography.Steganography( "mona_test.png", "horizontal" )
    image.embedMessageInMedium( mes, "mona_test.png" )
    #image.embedCustomMessage( "TS", "mona_test.png" )
    image.extractMessageFromMedium()

    #newimg = Steganography.Steganography( "testingEmbed.png", "horizontal" )
    #newimg.extractMessageFromMedium()
    pass

if __name__ == "__main__":
    main()