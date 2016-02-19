# bitparse
small interpreter to parse bitstreams based on their spec

This is a small utility that defines a simple language which corresponds almost exactly with the format of MPEG specifications and related protocol definitions (eg DVB subs, teletext, PSI/SI). I built it since I was frustrated doing hand-decodes of small sections of data, especially when an analyser is in question or not available.

The aim is to make it simple to quickly generate a parser that can read a blob of binary data and interpret it as specified, displaying the result in a human-readable format. I have tried to keep the syntax of the mini-language as close as possible to the common specification format so that it is easy to copy-and-paste straight from the spec.

Here is an example of the mini-language which defines the multiple_operation_message structure from ANSI SCTE 104:

multiple_operation_message {
    Reserved                16 uimsbf
    messageSize             16 uimsbf
    protocol_version        8  uimsbf
    AS_index                8  uimsbf
    message_number          8  uimsbf
    DPI_PID_index           16 uimsbf
    SCTE35_protocol_version 8  uimsbf
    timestamp()
    num_ops                 8  uimsbf
    for ( num_ops ) {
        opID                16 uimsbf
        data_length         16 uimsbf
        data       data_length stuff
    }
}

This is an almost exact copy of the spec, with a few adjustments in the for-loop syntax. Note that the field names can be re-used once parsed, so the value of num_ops is used to specify the number of iterations of the for-loop.

TODO add more examples to demo the IF-syntax, comparison operators etc, as well as demoing the nesting of structures.

The mini-language is sepcified in the files bitparse.py and bitlex.py, and uses python lex/yacc to define the language. The library bitparse is used to read the binary data bit by bit.

At the moment, the result of the parse is a s-expression tree representing the parsed structures. This is reasonably readable if pretty-printed, but the next step will be to make a nicer environment for editing and running the mini-language against different data sources and viewing the output.
