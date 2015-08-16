/*
 * 4998.c
 *
 *  Created on: Aug 5, 2014
 *      Author: aduri
 */

#include "h4998.h"
#include "IfxGtm_reg.h"
#include "IfxGtm_Prev.h"
uint32 duty1,duty2;
uint32 period1,period2;
volatile uint8 dutycycle1,dutycycle2;
void Torquesensor_init()
{
	uint16 passwd = IfxScuWdt_getCpuWatchdogPassword();
	    IfxScuWdt_clearCpuEndinit(passwd);

		/* set fSTM = fFPI */
		GTM_CLC.U = 0x00000000 ; /* enable GTM module */
	    while ((GTM_CLC.U & 0x00000002) == 0x2) { }

		/* re-enable endinit protection */
	    IfxScuWdt_setCpuEndinit(passwd);
	    GTM_CMU_CLK_EN.U |= 2 << 22 ;
	    GTM_CMU_CLK_EN.U |= 1 << 0 ;
	    GTM_CMU_CLK_0_CTRL.B.CLK_CNT = IFX_GTM_CMU_CLK0_DIVIDE_FACTOR - 1  ;
	    GTM_CMU_CLK_EN.U |= 2 << 0 ;
	P33_IOCR4.B.PC5=2;
	GTM_TIM1_CH1_CTRL.B.TIM_EN=1;
	GTM_TIM1_CH1_CTRL.B.TIM_MODE=0;
	GTM_TIM1_CH1_CTRL.B.OSM=1;
	GTM_TIM1_CH1_CTRL.B.ARU_EN=1;
	GTM_TIM1_CH1_CTRL.B.CICTRL=0;
	GTM_TIM1_CH1_CTRL.B.DSL=1;
	GTM_TIM1_CH1_CTRL.B.ECNT_RESET=0;
	GTM_TIM1_CH1_CTRL.B.FLT_EN=1;
	GTM_TIM1_CH1_CTRL.B.CLK_SEL=0;
	GTM_TIM1_CH1_CTRL.B.GPR0_SEL=11;
	GTM_TIM1_CH1_CTRL.B.GPR1_SEL=11;
	GTM_TIM1_IN_SRC.B.MODE_1=00;
	GTM_TIM1_IN_SRC.B.VAL_1=0;
	GTM_TIM1INSEL.B.CH1SEL=8;
	IfxGtm_SetTimChannel(&TIM1, 1, CMU_Clk0, TPWM, RisingEdgeStart, OneShot) ;
	IfxGtm_EnableTimChannel(&TIM1, 1, Enable) ;

	P11_IOCR8.B.PC9=2;
	GTM_TIM1_CH2_CTRL.B.TIM_EN=1;
		GTM_TIM1_CH2_CTRL.B.TIM_MODE=0;
		GTM_TIM1_CH2_CTRL.B.OSM=1;
		GTM_TIM1_CH2_CTRL.B.ARU_EN=1;
		GTM_TIM1_CH2_CTRL.B.CICTRL=0;
		GTM_TIM1_CH2_CTRL.B.DSL=1;
		GTM_TIM1_CH2_CTRL.B.ECNT_RESET=0;
		GTM_TIM1_CH2_CTRL.B.FLT_EN=1;
		GTM_TIM1_CH2_CTRL.B.CLK_SEL=0;
		GTM_TIM1_CH2_CTRL.B.GPR0_SEL=11;
		GTM_TIM1_CH2_CTRL.B.GPR1_SEL=11;
		GTM_TIM2_IN_SRC.B.MODE_1=00;
		GTM_TIM2_IN_SRC.B.VAL_1=0;
		GTM_TIM2INSEL.B.CH1SEL=8;
		IfxGtm_SetTimChannel(&TIM2, 5, CMU_Clk0, TPWM, RisingEdgeStart, OneShot) ;
		IfxGtm_EnableTimChannel(&TIM2, 5, Enable) ;
}


uint8 GetDutyCycle1(void)
{
	duty1 = (uint32)(GTM_TIM1_CH1_GPR0.B.GPR0 & 0xFFFFFF);
	period1 = (uint32)(GTM_TIM1_CH1_GPR1.B.GPR1 & 0xFFFFFF);
	dutycycle1= duty1/(float)period1*100;
	GTM_TIM1_CH1_CTRL.B.TIM_EN=1;
	return dutycycle1;
}

uint8 GetDutyCycle2(void)
{
	duty2 = (uint32)(GTM_TIM2_CH5_GPR0.B.GPR0 & 0xFFFFFF);
	period2 = (uint32)(GTM_TIM2_CH5_GPR1.B.GPR1 & 0xFFFFFF);
	dutycycle2= duty1/(float)period1*100;
	GTM_TIM2_CH5_CTRL.B.TIM_EN=1;
	return dutycycle2;
}
