/*
 * h5012.h
 *
 *  Created on: Jul 14, 2014
 *      Author: aduri
 */

#ifndef H5012_H_
#define H5012_H_

#define SPI_BUFFER_SIZE1 10
#define IFX_INTPRIO_QSPI1_TX  16
#define IFX_INTPRIO_QSPI1_RX  17
#define IFX_INTPRIO_QSPI1_ER  18


uint16  spiTxBuffer1_5012[SPI_BUFFER_SIZE1];
uint16  spiRxBuffer1_5012[SPI_BUFFER_SIZE1];

uint16 spiTxBuffer1_5012[10] = {0x8001, 0xFFFF, 0xFFFF, 0x8625, 0x8D27, 0x8811, 0x87BE,0x8668, 0x877D, 0x8795 };              // initial the TLF35584 to disable the WD
uint8 TLE_9180_InitData1[8] = {0x01,0x00,0x04,0x02,0x00,0x03};
uint8 TLE9180_Recdata1[12];
typedef enum
{
	TLE5012_REGISTER_STAT 		= 0x00,
	TLE5012_REGISTER_ACSTAT 	= 0x01,
	TLE5012_REGISTER_AVAL 		= 0x02,
	TLE5012_REGISTER_ASPD		= 0x03,
	TLE5012_REGISTER_AREV		= 0x04,
	TLE5012_REGISTER_FSYNC		= 0x05,
	TLE5012_REGISTER_MOD_1		= 0x06,
	TLE5012_REGISTER_SIL		= 0x07,
	TLE5012_REGISTER_MOD_2		= 0x08,
	TLE5012_REGISTER_MOD_3		= 0x09,
	TLE5012_REGISTER_OFFX		= 0x0A,
	TLE5012_REGISTER_OFFY		= 0x0B,
	TLE5012_REGISTER_SYNCH		= 0x0C,
	TLE5012_REGISTER_IFAB		= 0x0D,
	TLE5012_REGISTER_MOD_4		= 0x0E,
	TLE5012_REGISTER_TCO_Y		= 0x0F,
	TLE5012_REGISTER_ADC_X		= 0x10,
	TLE5012_REGISTER_ADC_Y		= 0x11,
	TLE5012_REGISTER_D_MAG		= 0x14,
	TLE5012_REGISTER_T_RAW		= 0x15,
	TLE5012_REGISTER_IIF_CNT	= 0x20,
	TLE5012_REGISTER_T25O		= 0x30,
	TLE5012_REGISTER_LAST
};

#endif /* H5012_H_ IFX_CFG_CPU_TRAP_TSR_HOOK*/