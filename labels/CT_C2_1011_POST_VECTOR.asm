; C2:1011-10A8 - Post-Vector Handler
; Score: 6
; Size: 151 bytes
; Session: 29
;
; Handler function in C2:1000-2000 region
; Just after vector table area
;
; Characteristics:
; - 5 internal calls (call-rich)
; - REP prologue pattern
; - Multi-branch control flow
; - Extension of vector table functionality

ct_c2_1011_post_vector_handler_s29:
    ; Post-vector handler entry
    .addr $1011
    
ct_c2_1011_handler_end:
    ; Function boundary end
    .addr $10A8
