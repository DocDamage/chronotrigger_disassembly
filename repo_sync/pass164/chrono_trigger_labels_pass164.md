# Chrono Trigger Labels — Pass 164

## Strong labels

### C3:0307..C3:0528  ct_c3_7f_tile_strip_builder_with_regenerate_reuse_blank_fast_paths_and_sampled_byte_to_planar_4bpp_pack_core   [strong structural]

**Why this name**
- exact destination is exact WRAM bank `7F`
- exact routine iterates one exact strip/tile sequence
- exact fast paths prove exact regenerate / reuse / blank behavior
- exact core samples bytes and repacks them into exact planar 4bpp tile rows

## Notes
- exact `C3:034C` remains one internal re-entry point, **not** one separate strong helper label
- exact next unfrozen downstream seam starts at exact `C3:08A9`
