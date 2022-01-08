***`Design`***: Captures attributes of an LWC hardware implementation. 
- ***`name`*** *(string)*: A unique identifier for the design. It can consist of English letters, digits, dashes, and underscores and must start with a letter. 
- ***`description`*** *(string)*: A short description of the design. 
- ***`author`*** *(string or array of string)*: The name(s) of the developer(s) of this implementation. 
- ***`url`*** *(string)*: Uniform Resource Locator pointing to a webpage or source repository associated with this design or its author(s). 
- ***`license`*** *(string or array of string)*: License or licenses covering this design's use and distribution. Use SPDX (ISO/IEC 5962:2021) short identifiers when applicable. 
    _Examples:_
        `"SHL-2.1"`
- **`version`** *(string)*: Design version. 
    _Examples:_
        `"0.0.1"`
- ***`rtl`***: Details of the synthesizable RTL code. 
    - ***`sources`*** *(array of string)*: Non-empty list of HDL source file paths in correct compilation order. All paths must be relative to the location of the configuration file. Path separator is `/` (slash) on all platforms. Paths are case-sensitive and should not contain whitespaces. HDL language is inferred from the file extension. 
    - **`includes`** *(array of string)*: Non-empty list of HDL include file paths, such as Verilog headers. Include files are not directly compiled but need to be present for elaboration of design. Order is arbitrary. All paths must be relative to the location of the configuration file. Path separator is `/` (slash) on all platforms. Paths are case-sensitive and should not contain whitespaces.    _Default:_ `[]` 
    - ***`top`*** *(string)*: Name of top-level RTL entity/module.    _Default:_ `LWC` 
    - **`clock`**: Top level RTL clock signal. Only a single clock is supported by LWC API. 
        - **`pin`** *(string)*: Name of the top-level clock input.    _Default:_ `clk` 
    - **`reset`**: Top level reset signal. Only a single reset is supported by LWC API. 
        - **`pin`** *(string)*: Name of top-level reset input.    _Default:_ `reset` 
        - **`active_high`** *(boolean)*: Polarity of the reset signal. Active-high (positive) if true, otherwise active-low.    _Default:_ `true` 
        - **`asynchronous`** *(boolean)*: Whether reset is asynchronous with respect to `rtl.clock`.    _Default:_ `false` 
    - **`parameters`**: Top-level design parameters or generics specified as a key-value map. The default value of each parameter is overridden by synthesis tool, simulator, testbench, or wrapper. For the best tool compatibility, we only support integer and string values.    _Default:_ `{}` 
        _Examples:_
                `{"G_NUM_SHARES": 2, "G_PARALLEL": 8}`
- **`tb`**: Details of test-bench used for verification of top-level design. [Optional]. 
    - **`sources`** *(array of string)*: Source files used only for verification. Should _not_ contain any of the files included in 'rtl.sources'. 
    - **`includes`** *(array of string)*: HDL include file paths.    _Default:_ `[]` 
    - **`top`** *(string)*: Name of top-level test entity or module. 
    - **`parameters`**: Testbench parameter or generics specified as a key-value map. The default value of each parameter is overridden by the simulator. For the best tool compatibility, we only support integer and string values.    _Default:_ `{}` 
        _Examples:_
                `{"G_TEST_MODE": 0}`
- **`language`**: Information about Hardware Description/Design Language(s) used. 
    - **`vhdl`**: Common VHDL features supported by all VHDL source files. VHDL files must have a `.vhd` or `.vhdl` extension. 
        - **`version`** *(string)*: VHDL language standard.    _Supported values:_ `1993`, `2000`, `2002`, `2008`    _Default:_ `1993` 
        - **`synopsys`** *(boolean)*: Use of non-standard Synopsys packages which were placed in the IEEE namespace, e.g. 'std_logic_arith'. Dependence on such packages is _strongly_ discouraged.    _Default:_ `false` 
    - **`verilog`**: Common Verilog (pre-SystemVerilog) language features supported by all Verilog source files. Verilog files must have a `.v` extension. 
        - **`version`** *(string)*: Verilog language standard.    _Supported values:_ `1995`, `2001`    _Default:_ `2001` 
    - **`systemverilog`**: SystemVerilog (IEEE 1800-2005 and onwards) language features supported by all SystemVerilog source files. SystemVerilog files must have a `.sv` extension. 
        - **`version`** *(string)*: SystemVerilog language standard.    _Supported values:_ `2005`, `2009`    _Default:_ `2009` 
- ***`lwc`***: LWC-specific meta-data. 
    - **`aead`**: Details about the AEAD scheme and its implementation. 
        - **`algorithm`** *(string)*: Name of the implemented AEAD algorithm based on [SUPERCOP](https://bench.cr.yp.to/primitives-aead.html) convention. 
            _Examples:_
                        `"giftcofb128v1"`, `"romulusn1v12"`, `"gimli24v1"`
        - **`input_sequence`**: Order in which different input segment types should be fed to PDI. 
            - **`encrypt`** *(array of string)*: Sequence of inputs during encryption.    _Default:_ `['npub', 'ad', 'pt', 'tag']` 
            - **`decrypt`** *(array of string)*: Sequence of inputs during decryption.    _Default:_ `['npub', 'ad', 'ct', 'tag']` 
    - **`hash`**
        - **`algorithm`** *(string)*: Name of the hashing algorithm based on [SUPERCOP](https://bench.cr.yp.to/primitives-aead.html) convention. Empty string if hashing is not supported.    _Default:_ `` 
            _Examples:_
                        `""`, `"gimli24v1"`
        - **`digest_bits`** *(integer)*: Size of hash digest (output) in bits.    _Default:_ `128` 
    - ***`ports`***: Description of LWC ports. 
        - ***`pdi`***: Public Data Input port. 
            - **`bit_width`** *(integer)*: Width of each word of PDI data in bits (`w`). The width of 'pdi_data' signal would be `pdi.bit_width × pdi.num_shares` (`w × n`) bits.    _Minimum:_ `8`    _Maximum:_ `32`    _Default:_ `32` 
            - ***`num_shares`*** *(integer)*: Number of PDI shares (`n`). 
        - ***`sdi`***: Secret Data Input port. 
            - **`bit_width`** *(integer)*: Width of each word of SDI data in bits (`sw`). The width of `sdi_data` signal would be `sdi.bit_width × sdi.num_shares` (`sw × sn`) bits.    _Minimum:_ `8`    _Maximum:_ `32`    _Default:_ `32` 
            - ***`num_shares`*** *(integer)*: Number of SDI shares (`sn`). 
        - ***`rdi`***: Random Data Input port. 
            - ***`bit_width`*** *(integer)*:   _Minimum:_ `0`    _Maximum:_ `2048` 
    - ***`sca_protection`***: Implemented countermeasures against side-channel attacks. 
        - **`target`** *(array of string)*: Type of side-channel analysis attack(s) against which this design is assumed to be secure. 
            _Examples:_
                        `["spa", "dpa", "cpa", "timing"]`, `["dpa", "sifa", "dfia"]`
        - **`masking_schemes`** *(array of string)*: Masking scheme(s) applied in this implementation. Could be name/abbreviation of established schemes (e.g., "DOM", "TI") or reference to a publication.    _Default:_ `[]` 
            _Examples:_
                        `["TI"]`, `["DOM", "https://eprint.iacr.org/2022/000.pdf"]`
        - ***`order`*** *(integer)*: Claimed order of protectcion. 0 means unprotected.    _Default:_ `0` 
