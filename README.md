# DS28E38
**The DS28E38**is an ECDSA public key-based secure authenticator that incorporates Maxim’s patented 
ChipDNA™ PUF technology. ChipDNA technology involves a physically unclonable function (PUF) that 
enables the DS28E38 to deliver cost-effective protection against invasive physical attacks.

# Benefits and Features
- Robust Countermeasures Protect Against Security Attacks.
- Efficient Public-Key Authentication Solution to Authenticate Peripherals.
- Supplemental Features Enable Easy Integration into End Applications.


# Preview

### Relationships between the circuit elements of the DS28E38

![relationships between the circuit elements of the DS28E38](https://github.com/maltahan/DS28E38/raw/master/screenshot.jpg)

### How do you connect to DS28E38
![how do you connect to DS28E38](https://github.com/maltahan/DS28E38/raw/master/screenshot1.jpg)

### Basic
```import ds28e38
import onewire
import _onewire as _ow
ds = ds28e38.DS28E38(onewire)
```

### External dependencies
all the dependencies are exists by default in micropython.

### Software
Currently supported commands are:
- onewire_crc16
- read_status
- read_man_rom_Id
- sign_message
- read_page

### Hardware
We are working with the ESP32 WEMOS to connect to out DS28E38 chip.

## Changelog
#### V 1.0.0
Initial Release

## Authors
Mohammad Altahan(mohammad.tahan1992@gmail.com), Arnaud Durand(arnaud.durand@unifr.ch)


## License

this website is licensed under The MIT License (MIT). Which means that you can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the final products. 
But you always need to state that Mohammad Altahan, Arnaud Durand are the original authors of this library.
