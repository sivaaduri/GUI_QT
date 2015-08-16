/*
 * 5012.c
 *
 *  Created on: Jul 14, 2014
 *      Author: aduri
 */



#include "Scu/Std/IfxScuWdt.h"
#include "h5012.h"
#include "_Reg/IfxQspi_regdef.h"
#include "_Reg/IfxQspi_bf.h"
#include "_Reg/IfxSrc_reg.h"
#include "_Reg/IfxSent_reg.h"
#include "_Reg/IfxSrc_regdef.h"
#include "Qspi/SpiMaster/IfxQspi_SPiMaster.h"
#include "Src/Std/IfxSrc.h"
#include "Qspi/Std/IfxQspi.h"
#include "_Reg/IfxQspi_reg.h"
#include "Cpu/Std/Ifx_types.h"
#include "SpiIf.h"


IfxQspi_SpiMaster spi_1;
IfxQspi_SpiMaster_Channel spiChannel_1;
static uint16 tle5012_register[TLE5012_REGISTER_LAST];
float angle16;
uint16 Rx[3],r1,r2,r3;

IFX_INTERRUPT(qspi1TxISR, 0, IFX_INTPRIO_QSPI1_TX)
{
    IfxQspi_SpiMaster_isrTransmit(&spi_1);
}

IFX_INTERRUPT(qspi1RxISR, 0, IFX_INTPRIO_QSPI1_RX)
{
    IfxQspi_SpiMaster_isrReceive(&spi_1);
}
IFX_INTERRUPT(qspi1ErISR, 0, IFX_INTPRIO_QSPI1_ER)
{
    IfxQspi_SpiMaster_isrError(&spi_1);
}


void init_5012 (void)
{
	// create module config
			IfxQspi_SpiMaster_Config spiMasterConfig1;
			IfxQspi_SpiMaster_initModuleConfig(&spiMasterConfig1, &MODULE_QSPI1);
			// set the desired mode and maximum baudrate
			spiMasterConfig1.base.mode             = SpiIf_Mode_master;
			spiMasterConfig1.base.maximumBaudrate  = 10000000;
			// ISR priorities and interrupt target
			spiMasterConfig1.base.txPriority       = IFX_INTPRIO_QSPI1_TX;
			spiMasterConfig1.base.rxPriority       = IFX_INTPRIO_QSPI1_RX;
			spiMasterConfig1.base.erPriority       = IFX_INTPRIO_QSPI1_ER;
			spiMasterConfig1.base.isrProvider      = IfxSrc_Tos_cpu0;
			// pin configuration
			const IfxQspi_SpiMaster_Pins pins = {
				&IfxQspi1_SCLK_P11_6_OUT, IfxPort_OutputMode_pushPull, // SCLK
				&IfxQspi1_MTSR_P10_3_OUT, IfxPort_OutputMode_openDrain, // MTSR
				//&IfxQspi1_MTSR_P10_3_OUT, IfxPort_OutputMode_pushPull, // 9180 check
				&IfxQspi1_MRSTA_P10_1_IN, IfxPort_InputMode_noPullDevice,  // MRST
				IfxPort_PadDriver_cmosAutomotiveSpeed1 // pad driver mode
			};
			spiMasterConfig1.pins = &pins;
			// initialize module
			//IfxQspi_SpiMaster spi; // defined globally
			IfxQspi_SpiMaster_initModule(&spi_1, &spiMasterConfig1);

			// create channel config
			IfxQspi_SpiMaster_ChannelConfig spiMasterChannelConfig1;
			IfxQspi_SpiMaster_initChannelConfig(&spiMasterChannelConfig1, &spi_1);
			// set the baudrate for this channel
			spiMasterChannelConfig1.base.baudrate = 125000;
			//spiMasterChannelConfig1.base.mode.dataHeading=SpiIf_DataHeading_msbFirst;
			// select pin configuration
			const IfxQspi_SpiMaster_Output slsOutput1 = {
			    &IfxQspi1_SLSO4_P11_11_OUT,
			    IfxPort_OutputMode_pushPull,
			    IfxPort_PadDriver_cmosAutomotiveSpeed1
			};
			spiMasterChannelConfig1.sls.output = slsOutput1;
			//spiMasterChannelConfig1.base.mode.dataWidth=8;

			// initialize channel
			spiMasterChannelConfig1.base.mode.shiftClock=SpiIf_ShiftClock_shiftTransmitDataOnLeadingEdge;
			IfxQspi_SpiMaster_initChannel(&spiChannel_1, &spiMasterChannelConfig1);
			P15_IOCR4.B.PC7=0x10;
			P15_OMCR.B.PCL7=1;

}

uint16 TLE5012_WriteGeneral(uint16 Tx, uint16 val)
{
	spiTxBuffer1_5012[0]=Tx;
	spiTxBuffer1_5012[1]=val;
	spiTxBuffer1_5012[2]=0xFFFF;
	while( IfxQspi_SpiMaster_getStatus(&spiChannel_1) == SpiIf_Status_busy );
			// receive new stream
	IfxQspi_SpiMaster_exchange(&spiChannel_1,&spiTxBuffer1_5012,&spiRxBuffer1_5012,3);
	return spiRxBuffer1_5012[0];
}





/*void TLE9180_Status(void)
{

	while( IfxQspi_SpiMaster_getStatus(&spiChannel_1) == SpiIf_Status_busy );// receive new stream
	{
		IfxQspi_SpiMaster_exchange(&spiChannel_1,&TLE_9180_InitData1,&TLE9180_Recdata1,6);
		IfxQspi_SpiMaster_exchange(&spiChannel_1,NULL_PTR,&TLE9180_Recdata1,3);
	}

}*/





uint16 TLE5012_Read(uint16 Tx)
{
	spiTxBuffer1_5012[0]=Tx;
	spiTxBuffer1_5012[1]=0xFFFF;
	spiTxBuffer1_5012[2]=0xFFFF;
	while( IfxQspi_SpiMaster_getStatus(&spiChannel_1) == SpiIf_Status_busy );
			// receive new stream
	IfxQspi_SpiMaster_exchange(&spiChannel_1,&spiTxBuffer1_5012,&spiRxBuffer1_5012,3);
	return spiRxBuffer1_5012[1];
}
uint16 spi_angle(void)
{
	uint16 Tx[3];
	volatile uint16 Safety_Word;
	uint32 angle_safe;
	volatile float angle;
	Tx[0]=0x8021;
	Tx[1]=0xFFFF;
	Tx[2]=0xFFFF;
	while( IfxQspi_SpiMaster_getStatus(&spiChannel_1) == SpiIf_Status_busy );
				// receive new stream
		IfxQspi_SpiMaster_exchange(&spiChannel_1,&Tx,&Rx,3);
	 angle =(float)(Rx[1] & 0x7FFF)/32768*360;
	 //angle_safe= ((uint32) (Angle_TLE5012 & 0x7FFF))<<16 +  (uint32)(Safety_Word & 0xFFFF);
	 angle_safe = ((uint32) (Rx[1] & 0x7FFF))<<16;
	 angle_safe +=  ((uint32)Rx[2]) & 0xFFFF;
	 r1=Rx[1];
return angle;
}


static uint8 CRC8(uint8 *message, uint8 Bytelength)
  //“message” is the data transfer for which a CRC has to be calculated.
  //A typical “message” consists of 2 bytes for the command word plus 2 bytes for the
  //data word plus 2 bytes for the safety word.
  //“Bytelength” is the number of bytes in the “message”. A typical “message” has 6
  //bytes.
{
  //Look-up table (LUT) for the TLE5012B with generator polynomial 100011101 (0x11D).
  //As this table will be checked byte by byte, each byte has 256 possible values (2^8)
  //for its CRC calculation with the given generator polynomial.
  const uint8 TableCRC[256] =
  {
    //The “crc” of the position [1] (result from operation [crc ^*(message+Byteidx)])
    //is 0x00 -> 0x00 XOR 0x11D = 0x00 (1 byte).
    0x00,
    //The “crc” of the position [2] is 0x1D -> 0x01 XOR 0x11D = 0x1D (1 byte).
    0x1D,
    //The “crc” of the position [3] is 0x3A -> 0x02 XOR 0x11D = 0x3A (1 byte).
    0x3A,
    //For all the rest of the cases.
    0x27, 0x74, 0x69, 0x4E, 0x53, 0xE8, 0xF5, 0xD2, 0xCF, 0x9C, 0x81, 0xA6, 0xBB, 0xCD,
    0xD0, 0xF7, 0xEA, 0xB9, 0xA4, 0x83, 0x9E, 0x25, 0x38, 0x1F, 0x02, 0x51, 0x4C, 0x6B,
    0x76, 0x87, 0x9A, 0xBD, 0xA0, 0xF3, 0xEE, 0xC9, 0xD4, 0x6F, 0x72, 0x55, 0x48, 0x1B,
    0x06, 0x21, 0x3C, 0x4A, 0x57, 0x70, 0x6D, 0x3E, 0x23, 0x04, 0x19, 0xA2, 0xBF, 0x98,
    0x85, 0xD6, 0xCB, 0xEC, 0xF1, 0x13, 0x0E, 0x29, 0x34, 0x67, 0x7A, 0x5D, 0x40, 0xFB,
    0xE6, 0xC1, 0xDC, 0x8F, 0x92, 0xB5, 0xA8, 0xDE, 0xC3, 0xE4, 0xF9, 0xAA, 0xB7, 0x90,
    0x8D, 0x36, 0x2B, 0x0C, 0x11, 0x42, 0x5F, 0x78, 0x65, 0x94, 0x89, 0xAE, 0xB3, 0xE0,
    0xFD, 0xDA, 0xC7, 0x7C, 0x61, 0x46, 0x5B, 0x08, 0x15, 0x32, 0x2F, 0x59, 0x44, 0x63,
    0x7E, 0x2D, 0x30, 0x17, 0x0A, 0xB1, 0xAC, 0x8B, 0x96, 0xC5, 0xD8, 0xFF, 0xE2, 0x26,
    0x3B, 0x1C, 0x01, 0x52, 0x4F, 0x68, 0x75, 0xCE, 0xD3, 0xF4, 0xE9, 0xBA, 0xA7, 0x80,
    0x9D, 0xEB, 0xF6, 0xD1, 0xCC, 0x9F, 0x82, 0xA5, 0xB8, 0x03, 0x1E, 0x39, 0x24, 0x77,
    0x6A, 0x4D, 0x50, 0xA1, 0xBC, 0x9B, 0x86, 0xD5, 0xC8, 0xEF, 0xF2, 0x49, 0x54, 0x73,
    0x6E, 0x3D, 0x20, 0x07, 0x1A, 0x6C, 0x71, 0x56, 0x4B, 0x18, 0x05, 0x22, 0x3F, 0x84,
    0x99, 0xBE, 0xA3, 0xF0, 0xED, 0xCA, 0xD7, 0x35, 0x28, 0x0F, 0x12, 0x41, 0x5C, 0x7B,
    0x66, 0xDD, 0xC0, 0xE7, 0xFA, 0xA9, 0xB4, 0x93, 0x8E, 0xF8, 0xE5, 0xC2, 0xDF, 0x8C,
    0x91, 0xB6, 0xAB, 0x10, 0x0D, 0x2A, 0x37, 0x64, 0x79, 0x5E, 0x43, 0xB2, 0xAF, 0x88,
    0x95, 0xC6, 0xDB, 0xFC, 0xE1, 0x5A, 0x47, 0x60, 0x7D, 0x2E, 0x33, 0x14, 0x09, 0x7F,
    0x62, 0x45, 0x58, 0x0B, 0x16, 0x31, 0x2C, 0x97, 0x8A, 0xAD, 0xB0, 0xE3, 0xFe,
    //The “crc” of the position [255] is 0xD9 -> 0xFE XOR 0x11D = 0xD9 (1 byte).
    0xD9,
    //The “crc” of the position [256] is 0xC4 -> 0xFF XOR 0x11D = 0xC4 (1 byte).
    0xC4
  };

  //“crc” defined as the 8-bits that will be generated through the message till the
  //final crc is generated. In the example above this are the blue lines out of the
  //XOR operation.
  unsigned char crc;
  //“Byteidx” is a counter to compare the bytes used for the CRC calculation and “Bytelength”.
  unsigned char Byteidx;
  //Initially the CRC remainder has to be set with the original seed (0xFF for the TLE5012B).
  crc = 0xFF;
  //For all the bytes of the message.
  for(Byteidx=0; Byteidx<Bytelength; Byteidx++)
  {
    //“crc” is the value in the look-up table TableCRC[x] at the position “x”.
    //The position “x” is determined as the XOR operation between the previous “crc” and
    //the next byte of the “message”.
    //“^” is the XOR operator.
    crc = TableCRC[crc ^ *(message+Byteidx)];
  }
  //Return the inverted “crc” remainder(“~” is the invertion operator). An alternative
  //to the “~” operator would be a XOR operation between “crc” and a 0xFF polynomial.
  return(~crc);
}

static uint8 tle5012_crc( void )
{
	uint8 *ch;
	static uint8 crc;
    uint8 crcbuf[16];
    uint8 i;

  ch = crcbuf;
  for( i=0x08; i<=0x0F; i++ )
  {
    *ch++ = (uint8) (tle5012_register[i] >> 8);
    *ch++ = (uint8) (tle5012_register[i] & 0xFF);
  }

	crc = CRC8( crcbuf, 15 );

	return( crc );
}







void TLE5012_Sent_Init(void)
{
	Sent_Init();
	/*r2=TLE5012_Read(0xD0E1);
	r2=r2&&0xff4f;*/
	r3= TLE5012_WriteGeneral(0x50E1, 0x1c83);
	IfxPort_setPinMode (&MODULE_P02, 7, IfxPort_Mode_outputOpenDrainAlt6);
}


uint16 TLE5012_SentAngle(void)
{


	SPC_MODE1Trigger();
	angle16 = Sent_Read()/(float)4095*360;	// !*!*!* TODO: this doesn't handle more than 32 bits of data

	return angle16;
}


