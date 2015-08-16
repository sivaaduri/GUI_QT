/*
 * IfxASCLIN.c
 *
 *  Created on: Jul 24, 2014
 *      Author: aduri
 */


#include <Asclin/Asc/IfxAsclin_Asc.h>
#include "_Lib/DataHandling/Ifx_Fifo.h"
#include "_Reg/IfxAsclin_bf.h"
#include "_Reg/IfxAsclin_reg.h"
#include "_Reg/IfxAsclin_regdef.h"
#include "IfxAsclin.h"
#include "Cpu/Std/Ifx_types.h"

IfxAsclin_Asc asc;
// used globallystatic

#define ASC_TX_BUFFER_SIZE 64
uint8 ascTxBuffer[ASC_TX_BUFFER_SIZE + sizeof(Ifx_Fifo) + 16];
#define ASC_RX_BUFFER_SIZE 64
uint8 ascRxBuffer[ASC_RX_BUFFER_SIZE + sizeof(Ifx_Fifo) + 16];
//uint8 DATA[20],DATA1=0;
uint16 DATA[20],DATA1=0,status=0;
IfxAsclin_Asc_Config ascConfig;
IFX_INTERRUPT(asclin0TxISR, 0, IFX_INTPRIO_ASCLIN0_TX)
{
	IfxAsclin_Asc_isrTransmit(&asc);
}

IFX_INTERRUPT(asclin0RxISR, 0, IFX_INTPRIO_ASCLIN0_RX)
{
	IfxAsclin_Asc_isrReceive(&asc);
	uint8 data = IfxAsclin_Asc_blockingRead(&asc);
	//uint16 data = IfxAsclin_Asc_blockingRead(&asc);
	if(data==0xAA)
	serialupdate=1;
	else
		serialupdate=0;
}
IFX_INTERRUPT(asclin0ErISR, 0, IFX_INTPRIO_ASCLIN0_ER)
{
	IfxAsclin_Asc_isrError(&asc);
}

void Init_Asc(void)
{
	// create module config

	IfxAsclin_Asc_initModuleConfig(&ascConfig, &MODULE_ASCLIN0);

	// set the desired baudrate
	ascConfig.baudrate.prescaler = 3;
	ascConfig.baudrate.baudrate = 9600; // FDR values will be calculated in initModule
	// ISR priorities and interrupt target
	ascConfig.interrupt.txPriority = IFX_INTPRIO_ASCLIN0_TX;
	ascConfig.interrupt.rxPriority = IFX_INTPRIO_ASCLIN0_RX;
	ascConfig.interrupt.erPriority = IFX_INTPRIO_ASCLIN0_ER;
	ascConfig.interrupt.typeOfService = (IfxSrc_Tos)IfxCpu_getCoreId();
	// FIFO configuration
	ascConfig.txBuffer = &ascTxBuffer;
	ascConfig.txBufferSize = ASC_TX_BUFFER_SIZE;
	ascConfig.rxBuffer = &ascRxBuffer;
	ascConfig.rxBufferSize = ASC_RX_BUFFER_SIZE;
	//ascConfig.asclin->DATCON.B.DATLEN=16;

	// pin configuration
	const IfxAsclin_Asc_Pins pins = {
	    NULL_PTR,                           IfxPort_InputMode_pullUp,    // CTS pin not used
	    &IfxAsclin0_RXA_P14_1_IN,   IfxPort_InputMode_pullUp,    // Rx pin
	    NULL_PTR,                           IfxPort_OutputMode_pushPull, // RTS pin not used
	    &IfxAsclin0_TX_P14_0_OUT,   IfxPort_OutputMode_pushPull, // Tx pin
	    IfxPort_PadDriver_cmosAutomotiveSpeed1
	};
	ascConfig.pins = &pins;
	// initialize module
	//IfxAsclin_Asc asc; // defined globally
	IfxAsclin_Asc_initModule(&asc, &ascConfig);
	//ASCLIN0_DATCON.B.DATLEN=0xf;
	//ascConfig.asclin->DATCON.B.DATLEN=0xf;
}

void use_Asclin(uint8 and)
{
	// send 3 bytes
	//uint8 data1;
	// receive a byte
	IfxAsclin_Asc_blockingWrite(&asc, and);
	/*IfxAsclin_Asc_blockingWrite(&asc, ang2);
	IfxAsclin_Asc_blockingWrite(&asc, ang3);
	IfxAsclin_Asc_blockingWrite(&asc,0xFF);*/


	/*DATA=data;
	data=data-0x01;
	data1=ReadRegister(data);
	DATA1=data1;
	IfxAsclin_Asc_blockingWrite(&asc, data1);*/
}
