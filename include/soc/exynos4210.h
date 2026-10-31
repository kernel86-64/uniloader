/* SPDX-License-Identifier: GPL-2.0 */
/*
 * Copyright (c) 2026, Exynos 4210 support for uniLoader
 * Samsung Galaxy S2 (GT-I9100) family SoC.
 */

#ifndef EXYNOS4210_H_
#define EXYNOS4210_H_

/* Debug UARTs: S3C-style 32-bit registers */
#define EXYNOS4210_UART0_BASE		0x13800000	/* QEMU default / internal */
#define EXYNOS4210_UART1_BASE		0x13810000
#define EXYNOS4210_UART2_BASE		0x13820000	/* Micro-USB FSA9280 / MAX8997 */
#define EXYNOS4210_UART3_BASE		0x13830000

#define EXYNOS4210_ULCON		0x00
#define EXYNOS4210_UCON			0x04
#define EXYNOS4210_UFCON		0x08
#define EXYNOS4210_UTRSTAT		0x10
#define EXYNOS4210_UTXH			0x20
#define EXYNOS4210_URXH			0x24

#define EXYNOS4210_UTRSTAT_TX_EMPTY	(1 << 1)
#define EXYNOS4210_UTRSTAT_RX_READY	(1 << 0)

/* FIMD (Fully Interactive Mobile Display controller v5.1) */
#define EXYNOS4210_FIMD_BASE		0x11C00000
#define EXYNOS4210_FIMD_VIDCON0		0x00
#define EXYNOS4210_FIMD_VIDCON1		0x04
#define EXYNOS4210_FIMD_VIDW00ADD0B0	0xA0	/* Window 0 buffer start address */
#define EXYNOS4210_FIMD_VIDW00ADD1B0	0xD0	/* Window 0 buffer end address */
#define EXYNOS4210_FIMD_VIDW00ADD2	0x100

/* Interrupt Controller (ARM GIC) */
#define EXYNOS4210_GIC_DIST_BASE	0x10490000
#define EXYNOS4210_GIC_CPU_BASE		0x10480000

/* Multi-Core Timer (MCT) */
#define EXYNOS4210_MCT_BASE		0x10050000

#endif // EXYNOS4210_H_
