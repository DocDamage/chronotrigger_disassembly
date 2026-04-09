; C2:81A2-C2:81EF - ct_c2_81a2_interrupt_s30
; Score: 7
; Size: 77 bytes
; Session: 30
;
; C2:8000-9000 hub region expansion
; 9 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Call-rich handler

ct_c2_81a2_interrupt_s30:
    ; Function entry point
    .addr $81A2

ct_c2_81a2_interrupt_s30_end:
    ; Function boundary end
    .addr $81EE
