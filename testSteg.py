__author__ = 'ee364h05'
import Steganography

def main():
    #   Testing message class
    #mes = Steganography.Message( filePath="files/small.txt", messageType="Text" )
    #message2 = Steganography.Message( filePath="dog.png", messageType="GrayImage" )
    #print( mes.getXmlString() )
    #print( mes.getTextMessage() )
    #print( mes.getXmlString() )
    #fp = open( "files/small_out.xml", "w" )
    #fp.write( mes.getXmlString() )

    medium = Steganography.Steganography( "files/nature.png", "vertical" )
    #message = Steganography.Message( filePath="files/small.txt", messageType="Text" )
    #medium = Steganography.Steganography( "files/mona.png", "horizontal" )
    #medium.embedMessageInMedium( message, "mona_out.png")
    #medium.extractMessageFromMedium()
    message = Steganography.Message( filePath="files/sunflower.png", messageType="ColorImage" )
    print( message )
    medium.embedMessageInMedium( message, "files/nature_sunflower_v_out.png")

    #   Testing steg class
    #bridge = Steganography.Steganography( "bridge.png", "horizontal" )
    #bridge.embedMessageInMedium( mes, "bridge_out.png" )
    #image = Steganography.Steganography( "bridge_dog_v.png", "vertical" )
    #image.embedMessageInMedium( mes, "mona_test.png" )
    #image.embedCustomMessage( "TS", "mona_test.png" )
    #image.extractMessageFromMedium()
    #print( image.image.getpixel( (700,670)) )
    #image.message.saveToTarget( "out.txt" )

    #newimg = Steganography.Steganography( "testingEmbed.png", "horizontal" )
    #newimg.extractMessageFromMedium()
    pass

if __name__ == "__main__":
    main()