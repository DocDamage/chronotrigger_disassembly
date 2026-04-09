; C2:8C71-C2:8CA2 - ct_c2_8c71_handler
; Score: 10
; Size: 49 bytes
; Session: 31
;
; C2:8C00-9000 hub region expansion
; 1 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Hub network connector

ct_c2_8c71_handler:
    ; Function entry point
    .addr $8C71

ct_c2_8c71_handler_end:
    ; Function boundary end
    .addr $8CA1
