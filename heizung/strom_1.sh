    #!/bin/bash
    # read and evaluate SML output received from EMH eHZ

    # set serial device
    INPUT_DEV="/dev/ttyUSB0"

    #set $INPUT_DEV to 9600 8N1
    stty -F $INPUT_DEV 1:0:8bd:0:3:1c:7f:15:4:5:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0

    SML_START_SEQUENCE="1B1B1B1B0101010176"
    METER_OUTPUT__START_SEQUENCE=""

    while [ "$METER_OUTPUT__START_SEQUENCE" != "$SML_START_SEQUENCE" ]
    do
            METER_OUTPUT=`cat $INPUT_DEV 2>/dev/null | xxd -p -u -l 460`
            METER_OUTPUT__START_SEQUENCE=$(echo "${METER_OUTPUT:0:18}")
            if [ $METER_OUTPUT__START_SEQUENCE != $SML_START_SEQUENCE ];
            then
                    echo "missed start and trying again..."
                    #exit 1
            fi
    done

    let METER_180=0x${METER_OUTPUT:390:10}
    VALUE=$(echo "scale=2; $METER_180 / 10000" |bc)
    echo "Meter 1.8.0 (from plant):    " $VALUE "kWh"

    let METER_180=0x${METER_OUTPUT:347:10}
    VALUE=$(echo "scale=2; $METER_180 / 10000" |bc)
    echo "Meter 2.8.0 (to plant):      " $VALUE "kWh"

    let METER_180=0x${METER_OUTPUT:518:8}
    VALUE=$(echo "scale=2; $METER_180 / 10" |bc)
    echo "Total effective power (+/-): " $VALUE "W"
