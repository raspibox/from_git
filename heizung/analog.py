import time
import RPi.GPIO as GPIO
import sys
try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    HIGH = True  # HIGH-Pegel
    LOW  = False # LOW-Pegel

    # Funktionsdefinition
    def readAnalogData(adcChannel, SCLKPin, MOSIPin, MISOPin, CSPin):
        # Pegel vorbereiten
        GPIO.output(CSPin,   HIGH)    
        GPIO.output(CSPin,   LOW)
        GPIO.output(SCLKPin, LOW)
        
        sendcmd = adcChannel
        sendcmd |= 0b00011000 # Entspricht 0x18 (1:Startbit, 1:Single/ended)

    # Senden der Bitkombination (Es finden nur 5 Bits Beruecksichtigung)
        for i in range(5):
            if (sendcmd & 0x10): # (Bit an Position 4 pruefen. Zaehlung beginnt bei 0)
                GPIO.output(MOSIPin, HIGH)
            else:
                GPIO.output(MOSIPin, LOW)
            # Negative Flanke des Clocksignals generieren    
            GPIO.output(SCLKPin, HIGH)
            GPIO.output(SCLKPin, LOW)
            sendcmd <<= 1 # Bitfolge eine Position nach links schieben
            
        # Empfangen der Daten des ADC
        adcvalue = 0 # Ruecksetzen des gelesenen Wertes
        for i in range(13):
            GPIO.output(SCLKPin, HIGH)
            GPIO.output(SCLKPin, LOW)
            # print GPIO.input(MISOPin)
            adcvalue <<= 1 # 1 Postition nach links schieben
            if(GPIO.input(MISOPin)):
                adcvalue |= 0x01
        time.sleep(0.1)
        # print convert(adcvalue)
        return adcvalue

    def convert(adcvalue):
        # Berechnung Wert je Grad Celsius unter der Annahme dass der Widderstandsverlauf Linear ist
        # Gemessen wurden dass bei 0 Grad C = 1000 Ohm ein Wert von 138 ankommt
        # Bei 253 C = 1950 Ohm sind es 3863
        # Differenz 3863 - 138 = 3725
        GradJeWert = 253.0/3725.0
        Grad = GradJeWert * (adcvalue - 138) # 138 muessen abgezogen werden da 0 Grad ja dden Wert 138 haben
        return Grad
    

    # Variablendefinition
    ADC_Channel = 0  # Analog/Digital-Channel
    SCLK        = 12 # Serial-Clock
    MOSI        = 18 # Master-Out-Slave-In
    MISO        = 16 # Master-In-Slave-Out
    CS          = 22 # Chip-Select
    TempRelais  = 24 # Um zwischen Solar und Abgas umzuschalten

    # Pin-Programmierung
    GPIO.setup(SCLK, GPIO.OUT)
    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(CS,   GPIO.OUT)
    GPIO.setup(TempRelais,   GPIO.OUT)
    GPIO.output(TempRelais, LOW)
#    print "warten auf LOW"

    if not sys.argv[1] == "solar": 
#        print "x hat den Wert 1" 
    #else: 
     #   print "x hat den Wert 2"
#    while True:
        time.sleep(0.5)
#        print "Abgas:" 
        dummy = readAnalogData(ADC_Channel, SCLK, MOSI, MISO, CS)   
#        print dummy
        new = convert(dummy)
        print new
    #Hier AEndern auf HIGH
#    sys.exit()
    else:
        GPIO.output(TempRelais, HIGH)
        time.sleep(0.1)
#        print "###############################"
#        print "Solar:" 
        dummy = readAnalogData(ADC_Channel, SCLK, MOSI, MISO, CS)   
#        print dummy
        new = convert(dummy)
        print new
        GPIO.output(TempRelais, LOW);
    



except KeyboardInterrupt:
    GPIO.cleanup()
