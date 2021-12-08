***`Design`***: Captures attributes of an LWC hardware implementations to enable automated benchmarking and validation.  Cannot contain additional properties.
- ***`name`*** *(string)*: A unique identifier for the design. It can consist of English letters, digits, dashes, and underscores and must start with a letter. 
- **`description`** *(string)*: A short description of the design. 
- **`author`** *(string or array of string)*: Author or list of authors and developers who have contributed to this implementation. 
- **`url`** *(string)*: Uniform Resource Locator pointing to a webpage or source repository associated with this design or its author(s). 
- **`license`** *(string or array of string)*: License or licenses covering this design's use and distribution. Use SPDX (ISO/IEC 5962:2021) short identifiers when applicable. 
    _Examples:_
        `"SHL-2.1"`
- **`version`** *(string)*: Design version. 
    _Examples:_
        `"0.0.1"`
- ***`rtl`***: Details of the synthesizable RTL design.  Cannot contain additional properties.
    - ***`sources`*** *(array of string)*: Non-empty list of HDL source file paths in correct compilation order. All paths must be relative to the location of the configuration file. Path separator is `/` (slash) on all platforms. Paths are case-sensitive and should not contain whitespaces. HDL language is inferred from the file extension. 
    - **`includes`** *(array of string)*: Non-empty list of HDL include file paths, such as Verilog headers. Include files are not directly compiled but need to be present for elaboration of design. Order is arbitrary. All paths must be relative to the location of the configuration file. Path separator is `/` (slash) on all platforms. Paths are case-sensitive and should not contain whitespaces.    _Default:_ `[]` 
    - ***`top`*** *(string)*: Name of top-level RTL entity/module.    _Default:_ `LWC` 
    - **`clock`**: Top level RTL clock signal. Only a single clock is supported by LWC API. 
        - **`port`** *(string)*: Name of the top-level RTL clock input.    _Default:_ `clk` 
    - **`reset`**: Top level reset signal. Only a single reset is supported by LWC API. 
        - **`port`** *(string)*: Name of top-level RTL reset input.    _Default:_ `reset` 
        - **`active_high`** *(boolean)*: Polarity of the reset signal. Active-high (positive) if true, otherwise active-low.    _Default:_ `true` 
        - **`asynchronous`** *(boolean)*: Whether reset is asynchronous with respect to `rtl.clock`.    _Default:_ `false` 
    - **`parameters`**: Top-level design parameters or generics specified as a key-value map. The default value of each parameter is overridden by synthesis tool, simulator, testbench, or wrapper. For the best tool compatibility, we only support integer and string values. 
        _Examples:_
                `{"G_NUM_SHARES": 2, "G_BACKDOOR": 0}`
    - **`language`**: Information about Hardware Description/Design Language(s). 
        - **`vhdl`**: Common VHDL features supported by all VHDL source files. VHDL files must have a `.vhd` or `.vhdl` extension. 
            - **`version`** *(string)*: VHDL language standard.    _Supported values:_ `1993`, `2000`, `2002`, `2008`    _Default:_ `1993` 
            - **`synopsys`** *(boolean)*: Use of non-standard Synopsys packages which were placed in the IEEE namespace, e.g. 'std_logic_arith'. Dependence on such packages is _strongly_ discouraged.    _Default:_ `false` 
        - **`verilog`**: Common Verilog (pre-SystemVerilog) language features supported by all Verilog source files. Verilog files must have a `.v` extension. 
            - **`version`** *(string)*: Verilog language standard.    _Supported values:_ `1995`, `2001`    _Default:_ `2001` 
        - **`systemverilog`**: SystemVerilog (IEEE 1800-2005 and onwards) language features supported by all SystemVerilog source files. SystemVerilog files must have a `.sv` extension. 
            - **`version`** *(string)*: SystemVerilog language standard.    _Supported values:_ `2005`, `2009`    _Default:_ `2009` 
- **`tb`**: Details of test-bench used for verification of top-level design. [Optional].  Cannot contain additional properties.
    - **`sources`** *(array of string)*: Source files used only for verification. Should _not_ contain any of the files included in 'rtl.sources'. 
    - **`includes`** *(array of string)*: HDL include file paths.    _Default:_ `[]` 
    - **`top`** *(string)*: Name of top-level test entity or module. 
    - **`parameters`**: Testbench parameter or generics specified as a key-value map. The default value of each parameter is overridden by the simulator. For the best tool compatibility, we only support integer and string values. 
        _Examples:_
                `{"G_TEST_MODE": 0}`
    - **`language`**: Information about HDL or programming languages used in the testbench. 
        - **`vhdl`**: Common VHDL features supported by all VHDL source files. VHDL files must have a `.vhd` or `.vhdl` extension. 
            - **`version`** *(string)*: VHDL language standard.    _Supported values:_ `1993`, `2000`, `2002`, `2008`    _Default:_ `1993` 
            - **`synopsys`** *(boolean)*: Use of non-standard Synopsys packages which were placed in the IEEE namespace, e.g. 'std_logic_arith'. Dependence on such packages is _strongly_ discouraged.    _Default:_ `false` 
        - **`verilog`**: Common Verilog (pre-SystemVerilog) language features supported by all Verilog source files. Verilog files must have a `.v` extension. 
            - **`version`** *(string)*: Verilog language standard.    _Supported values:_ `1995`, `2001`    _Default:_ `2001` 
        - **`systemverilog`**: SystemVerilog (IEEE 1800-2005 and onwards) language features supported by all SystemVerilog source files. SystemVerilog files must have a `.sv` extension. 
            - **`version`** *(string)*: SystemVerilog language standard.    _Supported values:_ `2005`, `2009`    _Default:_ `2009` 
        - **`python`**
            - **`version`** *(string)*
            - **`framework`** *(string)*:   _Supported values:_ `cocotb`    _Default:_ `cocotb` 
- ***`lwc`***: LWC-specific meta-data. 
    - ***`algorithm`*** *(string or array of string)*: LWC AEAD/Hash algorithm(s) supported by this design. Should follow [SUPERCOP](https://bench.cr.yp.to/primitives-aead.html) naming conventions and uniquely identify the scheme's variant and version. In case of duplicates, the second instance indicates support for AEAD and Hash algorithms with the same name. 
        _Examples:_
                `["giftcofb128v1"]`, `["romulusn1v12"]`, `["gimli24v1", "gimli24v1"]`
    - **`input_sequence`**: Order in which different input segment types should be fed to PDI. 
        - **`encrypt`** *(array of string)*:   _Default:_ `['npub', 'ad', 'pt', 'tag']` 
        - **`decrypt`** *(array of string)*:   _Default:_ `['npub', 'ad', 'ct', 'tag']` 
    - ***`pt_block_bits`*** *(integer)*: Algorithm's size of plaintext/ciphertext 'blocks' in bits. This is the number of bits that the algorithm operates upon during its basic operations. Potentially used for the evaluation of some performance metrics. 
    - ***`ad_block_bits`*** *(integer)*: Algorithm's size of associated-data 'blocks' in bits. This is the number of bits that the algorithm operates upon during its basic operations. Potentially used for the evaluation of some performance metrics. 
    - **`key_bits`** *(integer)*:   _Default:_ `128` 
    - **`npub_bits`** *(integer)*:   _Default:_ `128` 
    - **`tag_bits`** *(integer)*:   _Default:_ `128` 
    - **`hash`**
        - **`supported`** *(boolean)*: Whether this implementation supports hashing.    _Default:_ `false` 
        - **`digest_bits`** *(integer)*: Size of hash digest (output) in bits.    _Default:_ `128` 
    - ***`ports`***: Description of LWC ports. 
        - ***`pdi`***: Public Data Input port. 
            - **`bit_width`** *(integer)*: Width of each share of PDI data (bits). Width of 'pdi_data' signal would be `pdi.bit_width × pdi.num_shares` bits.    _Minimum:_ `8`    _Maximum:_ `32`    _Default:_ `32` 
            - **`num_shares`** *(integer)*: Number of PDI shares. Default is 1 (unprotected).    _Default:_ `1` 
        - **`sdi`**: Secret Data Input port. 
            - **`bit_width`** *(integer)*: Width of each share of SDI data (bits). Width of `sdi_data` signal would be `sdi.bit_width × sdi.num_shares` bits.    _Minimum:_ `8`    _Maximum:_ `32`    _Default:_ `32` 
            - **`num_shares`** *(integer)*: Number of SDI shares. Default is the same as `pdi.num_shares`.    _Minimum:_ `1`    _Default:_ `1` 
        - **`rdi`**: Random Data Input port. 
            - **`bit_width`** *(integer)*:   _Minimum:_ `0`    _Maximum:_ `2048`    _Default:_ `0` 
    - ***`sca_protection`***: Implemented countermeasures against side-channel attacks.  Cannot contain additional properties.
        - **`target`** *(array of string)*: Type of side-channel analysis attack(s) against which this design is assumed to be secure. 
            _Examples:_
                        `["spa", "dpa", "cpa", "timing"]`, `["dpa", "sifa", "dfia"]`
        - **`masking_schemes`** *(array of string)*: Masking scheme(s) applied in this implementation. Could be name/abbreviation of established schemes (e.g., "DOM", "TI") or reference to a publication.    _Default:_ `[]` 
            _Examples:_
                        `["TI"]`, `["DOM", "https://eprint.iacr.org/2022/000.pdf"]`
        - ***`order`*** *(integer)*: Claimed order of protectcion. 0 means unprotected.    _Default:_ `0` 
