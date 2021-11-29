# Design

Captures attributes of an LWC hardware implementations to enable automated benchmarking and validation.

## Properties:
- **name** *(string)*: A unique identifier for the design. It can consist of English letters, digits, dashes, and underscores and must start with a letter.&ensp;
- **description** *(string)*: A short description of the design.&ensp;
- **authors** *(array of strings)*: A list of names of author(s) for this implementation.&ensp;
- **url** *(string)*: Uniform Resource Locator pointing to a webpage or source repository associated with this design or its author(s).&ensp;
- **version** *(string)*: Design version.&ensp;
    _Examples:_
        `"0.0.1"`
- **rtl**: Details of the synthesizable RTL design.&ensp; Cannot contain additional properties.
    - **sources** *(array of strings)*: Non-empty list of HDL source file paths in correct compilation order. All paths must be relative to the location of the configuration file. Path separator is `/` (slash) on all platforms. Paths are case-sensitive and should not contain whitespaces. HDL language is inferred from the file extension. NOTE: Xeda `sources` fields can be an `object` containing meta-data such as HDL type and version.&ensp;
    - **includes** *(array of strings)*: Non-empty list of HDL include file paths, such as Verilog headers. Include files are not directly compiled but need to be present for elaboration of design. Order is arbitrary. All paths must be relative to the location of the configuration file. Path separator is `/` (slash) on all platforms. Paths are case-sensitive and should not contain whitespaces.&ensp;
    - **top** *(string)*: Name of top-level RTL entity/module.&ensp;   _Default:_ `LWC`&nbsp;
    - **clock**: Top level RTL clock signal. Only a single clock is supported by LWC API.&ensp;
        - **port** *(string)*: Name of the top-level RTL clock input.&ensp;   _Default:_ `clk`&nbsp;
    - **reset**: Top level reset signal. Only a single reset is supported by LWC API.&ensp;
        - **port** *(string)*: Name of top-level RTL reset input.&ensp;   _Default:_ `reset`&nbsp;
        - **active\_high** *(boolean)*: Polarity of the reset signal. Active-high (positive) if true, otherwise active-low.&ensp;   _Default:_ `true`&nbsp;
        - **synchronous** *(boolean)*: Reset is synchronous (positive) if true, otherwise asynchronous.&ensp;   _Default:_ `true`&nbsp;
    - **parameters**: Top-level design parameters or generics specified as a key-value map. The default value of each parameter is overridden by synthesis tool, simulator, testbench, or wrapper. For the best tool compatibility, we only support integer and string values.&ensp;
    - **language**: Information about Hardware Description/Design Language(s) used.&ensp;
        - **vhdl**: VHDL language standard supported by all VHDL source files. VHDL files should have a `.vhd` or `.vhdl` extension.&ensp;
            - **version** *(string)*:   _Supported values:_ `1993`, `2000`, `2002`, `2008`&nbsp;   _Default:_ `2002`&nbsp;
            - **synopsys** *(boolean)*: Use of non-standard Synopsys packages in IEEE namespace. (NOTE: The use of non-standard `IEEE` libraries is _strongly_ discouraged!).&ensp;   _Default:_ `false`&nbsp;
        - **verilog**: Verilog language standard supported by all Verilog source files. Covers pre-SystemVerilog standards. Verilog files should have a `.v` extension.&ensp;
            - **version** *(string)*:   _Supported values:_ `1995`, `2001`&nbsp;   _Default:_ `2001`&nbsp;
        - **systemverilog**: SystemVerilog (IEEE 1800-2005 and onwards) language standard supported by all SystemVerilog files. Verilog files should have a `.sv` extension.&ensp;
            - **version** *(string)*:   _Supported values:_ `2005`, `2009`&nbsp;   _Default:_ `2009`&nbsp;
- **tb**: Details of test-bench used for verification of top-level design. [Optional].&ensp; Cannot contain additional properties.
    - **sources** *(array of strings)*: Source files used only for verification. Should _not_ contain any of the files included in 'rtl.sources'.&ensp;
    - **includes** *(array of strings)*: HDL include file paths.&ensp;
    - **top** *(string)*: Name of top-level test entity or module.&ensp;
    - **parameters**: Testbench parameter or generics specified as a key-value map. The default value of each parameter is overridden by the simulator. For the best tool compatibility, we only support integer and string values.&ensp;
    - **language**: Information about HDL or programming languages used in the testbench.&ensp;
        - **vhdl**: VHDL language standard supported by all VHDL source files. VHDL files should have a `.vhd` or `.vhdl` extension.&ensp;
            - **version** *(string)*:   _Supported values:_ `1993`, `2000`, `2002`, `2008`&nbsp;   _Default:_ `2002`&nbsp;
            - **synopsys** *(boolean)*: Use of non-standard Synopsys packages in IEEE namespace. (NOTE: The use of non-standard `IEEE` libraries is _strongly_ discouraged!).&ensp;   _Default:_ `false`&nbsp;
        - **verilog**: Verilog language standard supported by all Verilog source files. Covers pre-SystemVerilog standards. Verilog files should have a `.v` extension.&ensp;
            - **version** *(string)*:   _Supported values:_ `1995`, `2001`&nbsp;   _Default:_ `2001`&nbsp;
        - **systemverilog**: SystemVerilog (IEEE 1800-2005 and onwards) language standard supported by all SystemVerilog files. Verilog files should have a `.sv` extension.&ensp;
            - **version** *(string)*:   _Supported values:_ `2005`, `2009`&nbsp;   _Default:_ `2009`&nbsp;
        - **python**
            - **version** *(string)*
            - **framework** *(string)*:   _Supported values:_ `cocotb`&nbsp;
- **lwc**: LWC-specific meta-data.&ensp;
    - **algorithms** *(string or array of strings)*: LWC AEAD/Hash algorithm(s) supported by this design. Should follow [SUPERCOP](https://bench.cr.yp.to/primitives-aead.html) naming conventions and uniquely identify the scheme's variant and version. In case of duplicates, the second instance indicates support for AEAD and Hash algorithms with the same name.&ensp;
        _Examples:_
                `["giftcofb128v1"]`, `["romulusn1v12"]`, `["gimli24v1", "gimli24v1"]`
    - **input\_sequence**: Order in which different input segment types should be fed to PDI.&ensp;
        - **encrypt** *(array of strings)*:   _Default:_ `['npub', 'ad', 'pt', 'tag']`&nbsp;
        - **decrypt** *(array of strings)*:   _Default:_ `['npub', 'ad', 'ct', 'tag']`&nbsp;
    - **pt\_block\_bits** *(integer)*: Algorithm's size of plaintext/ciphertext 'blocks' in bits. This is the number of bits that the algorithm operates upon during its basic operations.&ensp;   _Minimum:_ `1`&nbsp;
    - **ad\_block\_bits** *(integer)*: Algorithm's size of associated-data 'blocks' in bits. This is the number of bits that the algorithm operates upon during its basic operations.&ensp;   _Minimum:_ `1`&nbsp;
    - **key\_bits** *(integer)*:   _Default:_ `128`&nbsp;
    - **npub\_bits** *(integer)*:   _Default:_ `128`&nbsp;
    - **tag\_bits** *(integer)*:   _Default:_ `128`&nbsp;
    - **hash\_bits** *(integer)*:   _Default:_ `128`&nbsp;
    - **ports**: Description of LWC ports.&ensp;
        - **pdi**: Public Data Input port.&ensp;
            - **bit\_width** *(integer)*: Width of each share of PDI data (bits). Width of 'pdi_data' port is 'pdi.bit_width * pdi.shares'.&ensp;   _Minimum:_ `8`&nbsp;   _Maximum:_ `32`&nbsp;
            - **num\_shares** *(integer)*: Number of PDI shares. Default is 1 (unprotected).&ensp;   _Minimum:_ `1`&nbsp;   _Maximum:_ `8`&nbsp;   _Default:_ `1`&nbsp;
        - **sdi**: Secret Data Input port.&ensp;
            - **bit\_width** *(integer)*: Width of each share of SDI data (bits). Width of `sdi_data` port is `sdi.bit_width * sdi.shares`. Default is the same value as `pdi.bit_width`.&ensp;   _Minimum:_ `8`&nbsp;   _Maximum:_ `32`&nbsp;
            - **num\_shares** *(integer)*: Number of SDI shares. Default is the same as `pdi.num_shares`.&ensp;   _Minimum:_ `1`&nbsp;   _Maximum:_ `8`&nbsp;
        - **do**: Data Output port. Width of each share is always the same as `pdi.bit_width`.&ensp;
            - **num\_shares** *(integer)*: Number of `DO` output shares. Default is the same as `pdi.num_shares`.&ensp;   _Minimum:_ `1`&nbsp;   _Maximum:_ `8`&nbsp;
        - **rdi**: Random Data Input port.&ensp;
            - **bit\_width** *(integer)*:   _Minimum:_ `0`&nbsp;   _Maximum:_ `2048`&nbsp;   _Default:_ `0`&nbsp;
    - **sca\_protection**: Implemented countermeasures against side-channel attacks.&ensp; Cannot contain additional properties.
        - **attacks** *(array of strings)*: Family and type of side-channel analysis attack(s) this design is claims to be secure against.&ensp;
            _Examples:_
                        `["spa", "dpa", "cpa", "timing"]`, `["dpa", "sifa", "dfia"]`
        - **dpa\_order** *(integer)*: Claimed order of protectcion against differential power analysis. 0 means unprotected.&ensp;   _Minimum:_ `0`&nbsp;   _Maximum:_ `7`&nbsp;   _Default:_ `0`&nbsp;
