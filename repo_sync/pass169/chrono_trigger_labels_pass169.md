# Chrono Trigger Labels — Pass 169 (Audit)

## Labels audited and kept
- `C3:09E9..C3:0A8F` — `ct_c3_wram_runtime_code_emitter_writing_generated_stub_bytes_through_2180`
- `C3:0B03..C3:0C91` — `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`
- `C3:0CB1..C3:0CB7` — `ct_c3_stream_word_fetch_helper_advancing_20_and_caching_fetched_word`

## Audit notes
- exact `09E9..0A8F` remains a real shared top-level runtime-code emitter with confirmed long-call hits
- exact `0B03..0C91` remains one interpreter owner, not several public entries
- exact `0CB1..0CB7` remains correctly split because same-bank external caller evidence holds
