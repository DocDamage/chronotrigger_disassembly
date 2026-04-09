; C2:86F0-C2:875B - ct_c2_86f0_handler_s30
; Score: 7
; Size: 107 bytes
; Session: 30
;
; C2:8000-9000 hub region expansion
; 9 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Call-rich handler

ct_c2_86f0_handler_s30:
    ; Function entry point
    .addr $86F0

ct_c2_86f0_handler_s30_end:
    ; Function boundary end
    .addr $875A
