; C2:8CAB-C2:8D11 - ct_c2_8cab_handler_s30
; Score: 9
; Size: 102 bytes
; Session: 30
;
; C2:8000-9000 hub region expansion
; 7 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Call-rich handler

ct_c2_8cab_handler_s30:
    ; Function entry point
    .addr $8CAB

ct_c2_8cab_handler_s30_end:
    ; Function boundary end
    .addr $8D10
