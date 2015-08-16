/*
 * h4998.h
 *
 *  Created on: Aug 5, 2014
 *      Author: aduri
 */

#ifndef H4998_H_
#define H4998_H_
#include <Sent/Sent/IfxSent_Sent.h>
#define IFX_INTPRIO_SENT_CHANNEL 21

void SentInterruptHandler(IfxSent_Sent_Channel *channel);
#define CMU_CLK0 0
#define CMU_CLK1 1
#define CMU_CLK2 2
#define CMU_CLK3 3
#define CMU_CLK4 4
#define CMU_CLK5 5
#define CMU_CLK6 6
#define CMU_CLK7 7


/*Set global clock divider to a 1:1 ratio - i.e. 100MHz for fSPB = 100MHz */
#define IFX_GTM_GCLK_NUM			0xFFF
#define IFX_GTM_GCLK_DEN			0xFFF

/* Enable for FXCLK systen for TOM modules */
#define IFX_GTM_CMU_FXCLK_ENABLE	1

/* Enable for clock source 0 .. 7 for TIMs */
#define IFX_GTM_CMU_CLK0_ENABLE		1
#define IFX_GTM_CMU_CLK1_ENABLE		1
#define IFX_GTM_CMU_CLK2_ENABLE		1
#define IFX_GTM_CMU_CLK3_ENABLE		1
#define IFX_GTM_CMU_CLK4_ENABLE		1
#define IFX_GTM_CMU_CLK5_ENABLE		1
#define IFX_GTM_CMU_CLK6_ENABLE		1
#define IFX_GTM_CMU_CLK7_ENABLE		1

#define IFX_GTM_CMU_CLK0_DIVIDE_FACTOR	1
#define IFX_GTM_CMU_CLK1_DIVIDE_FACTOR	2
#define IFX_GTM_CMU_CLK2_DIVIDE_FACTOR	3
#define IFX_GTM_CMU_CLK3_DIVIDE_FACTOR	4
#define IFX_GTM_CMU_CLK4_DIVIDE_FACTOR	8
#define IFX_GTM_CMU_CLK5_DIVIDE_FACTOR	16
#define IFX_GTM_CMU_CLK6_DIVIDE_FACTOR	32
#define IFX_GTM_CMU_CLK7_DIVIDE_FACTOR	64

#define IFX_GTM_TBU0_ENABLE	1
#define IFX_GTM_TBU1_ENABLE	1
#define IFX_GTM_TBU2_ENABLE	1

#define IFX_GTM_TBU0_CLKSEL	CMU_CLK0
#define IFX_GTM_TBU1_CLKSEL	CMU_CLK1
#define IFX_GTM_TBU2_CLKSEL	CMU_CLK2

#endif /* H4998_H_ */
