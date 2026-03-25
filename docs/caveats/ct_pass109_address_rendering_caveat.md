# Pass 109 address-rendering caveat

While continuing the C0 low-bank seam, pass 109 found that the current toolkit workflow can present bank-C0 address windows in a way that is good enough for continuity but not always safe enough for byte-perfect proof if trusted blindly.

Practical rule used in pass 109:
- continuity wording from older handoffs was preserved where useful
- but every new closure was checked against the raw ROM bytes directly before being promoted

This is why pass 109 reframed the old `AE2B/AE33` seam:
the byte-level body proves a forced-blank shutdown loop there, not a general nonzero `0128` ownership path.

Recommended next-session behavior:
- keep using pass 109 as the source of truth for the low-bank seam
- verify any new C0 closure against the raw bytes, especially around the old `AE..` and `EC..` continuity windows
