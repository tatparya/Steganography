__author__ = 'ee364h05'
import Steganography

def main():
    #   Testing message class
    mes = Steganography.Message( filePath="testtxt.txt", messageType="Text" )
    #print( mes.getXmlString() )
    #print( mes.getTextMessage() )
    #mes.saveToTarget( "testingTxtSave.txt" )

    #   Testing steg class
    image = Steganography.Steganography( "testing.png", "vertical" )
    image.embedMessageInMedium( mes, "testingEmbed.png" )
    pass

if __name__ == "__main__":
    main()