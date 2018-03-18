# `Pretty Universal Home Automation` hardware specification

## Design goals

Create an embedded device that is:

* controllable via wifi or USB,
* controls things such as lighting,
* provides measurements (e.g. temperature, humidity)
* remotely upgradeable

## Components

### Core Components

* STM32F103C8T6 Evaluation Board
* ESP-01 wifi module
* 5V power supply

### Optional/Supported Components

* WS2812B programmable RGB LED strip
* HTU21D Temperature & Humidity sensor
* HC-SR501 PIR motion sensor
* Knightbright KPS-3227SP1C ambient light photo sensor

## Features

### Remote firmware upgrade

#### STM32F1

The embedded bootloader (DFU) can be used. USART1, BOOT0 and NRST must be connected to the ESP module. Bootloader is activated by "Pattern 1".

| Pin function (for STM32) | STM32 Pin | ESP-01 Pin           |
|--------------------------|-----------|----------------------|
| USART1 RX                | PA10      | TXD                  |
| USART1 TX                | PA9       | RXD                  |
| BOOT0 (=1)               | -         | controlled via GPIO2 |
| BOOT1 (=0)               | -         | _GND_                |
| NRST                     | -         | GPIO0                |

BOOT0 must not be pulled high by default, NRST pull-up is O.K.
Series resistors should be included between STM and ESP pins.

##### Boot configuration

| BOOT1 | BOOT0 | Mode              |
|:-----:|:-----:|:------------------|
| x     | 0     | Main Flash memory |
| 0     | 1     | System memory     |
| 1     | 1     | Embedded SRAM     |

##### Notes
* 512 byte starting from address 0x20000000 are used by the bootloader firmware.
* 2 Kbyte starting from address 0x1FFFF000 contain the bootloader firmware.

##### See also
* [AN2606: STM32 microcontroller system memory boot mode](http://www.st.com/content/ccc/resource/technical/document/application_note/b9/9b/16/3a/12/1e/40/0c/CD00167594.pdf/files/CD00167594.pdf/jcr:content/translations/en.CD00167594.pdf)

#### ESP-01

Using the [esp-link firmware](https://github.com/jeelabs/esp-link) on the device makes remote firmware upgrade possible from the web interface. Unfortunately that only works on the ESP-12, with the large flash, and not on the ESP-01.

##### Boot configuration

GPIO0 and GPIO2 weak pull-up required. CH_PD must be pulled high to operate.

### Ambient light sensor feature

According to [wikipedia](https://en.wikipedia.org/wiki/Lux), illuminance in the kitchen should always be under `80 lx`, the living room should be around `300-400 lx`.

The KPS's maximal collector current is `20 mA`, which would be 20 000 lx. That can be achieved on a bright day, or on direct sunlight (collector current must be limited). V_CE saturation voltage is `0.4 V` at 10 000 lx.

#### Implementation

The STM32's ADC can be configured in many ways. The input impedance depends on sampling time, max 50 kOhm for 4 us sampling. Voltage range depends on `VDDA`, which is connected to **3V3** on the Evaluation Board.

Connect C to 3.3 V power supply, connect E to a series resistor that is connected to GND. The voltage measured on E will be a function of R value and illuminance.

The resistor value should be above 165 Ohm (allows 20 mA at 3.3 V) and under 3.3 kOhm (allows 1 mA ~ 1000 lx). `3.3 k << 50 k` (input impedance can be ignored).
