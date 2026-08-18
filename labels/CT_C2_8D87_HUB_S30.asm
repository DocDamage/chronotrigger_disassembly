; C2:8D87-C2:8DDA - ct_c2_8d87_service_s30
; Score: 9
; Size: 83 bytes
; Session: 30
;
; C2:8000-9000 hub region expansion
; 4 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Call-rich handler

ct_c2_8d87_service_s30:
    ; Function entry point
    .addr $8D87

ct_c2_8d87_service_s30_end:
    ; Function boundary end
    .addr $8DD9
