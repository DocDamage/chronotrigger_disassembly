# Toolkit Upgrade — Pass 143 / v6.4

- Toolkit version advanced to **v6.4**.
- Per-pass workflow now assumes toolkit refresh every pass.
- Added finalize lane (`scripts/ct_finalize_pass.py`) so pass closeout can refresh state/session/release metadata/seam candidates together.
- Fixed state sync so toolkit version persists instead of collapsing back to older generic values.
- Forced smoke/report freshness for pass 143 so stale pass-139 smoke metadata no longer ships inside the release zip.
- Remaining rough edge: the original `ct_smoke_test.py` wrapper is still flaky in this container, so pass 143 uses the documented manual smoke-refresh fallback instead of pretending the wrapper is reliable.
