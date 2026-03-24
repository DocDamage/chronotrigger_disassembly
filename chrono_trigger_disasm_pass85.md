# Chrono Trigger Disassembly — Pass 85

## Scope of this pass
Pass 84 mapped the exact `CFFF` writers and left one explicit cleanup seam open:

- keep freezing the late auxiliary token cluster around `0xE3..0xE8`
- do **not** guess at the final gameplay-facing nouns too early
- only return to the wider `CDC8 / CE0F` reader hunt after the local token family is tighter

This pass follows that instruction directly.

The result is real and exact:

> the late auxiliary token cluster at `0xE0..0xE8` is now mostly frozen as **exact handlers**, not vague placeholders.
>
> `0xE1 / 0xE2 / 0xE4 / 0xE6` are direct immediate staging/store helpers.
> `0xE3` is an exact six-byte indexed snapshot/copy helper.
> `0xE5` is an indexed increment helper.
> `0xE7 / 0xE8 / 0xE0` are exact wrappers into already-isolated D1 helpers.

This does **not** finish the final higher-level noun of the whole family.
But it does collapse a fuzzy tail of the auxiliary VM into concrete behavior.

---

## 1. exact pointer-table decode for tokens `0xE0..0xE8`
The auxiliary token table at `CD:16B5` continues to decode cleanly as:

- `0xE8 -> CD:1874`
- `0xE7 -> CD:1879`
- `0xE6 -> CD:18C2`  *(already frozen in pass 84)*
- `0xE5 -> CD:18C8`
- `0xE4 -> CD:18CF`
- `0xE3 -> CD:18DF`
- `0xE2 -> CD:1907`
- `0xE1 -> CD:190D`
- `0xE0 -> CD:1913`

So this is not a random late-token scatter.
It is a real contiguous control family inside the auxiliary VM.

---

## 2. exact wrappers at `0xE8`, `0xE7`, and `0xE0`
Three members of the family are exact tiny wrappers.

### 2a. token `0xE8` = exact wrapper to `D1:FB72`
At `CD:1874..1878` the exact body is:

```text
JSL D1:FB72
RTS
```

### 2b. token `0xE7` = exact wrapper to `D1:FB68`
At `CD:1879..187D` the exact body is:

```text
JSL D1:FB68
RTS
```

### 2c. token `0xE0` = exact wrapper to `D1:F47C`
At `CD:1913..1917` the exact body is:

```text
JSL D1:F47C
RTS
```

### strongest safe reading
The strongest safe reading is:

> `0xE8`, `0xE7`, and `0xE0` are not local arithmetic helpers.
> They are exact bridge tokens into already-separated D1-side logic.

I am intentionally **not** forcing the final nouns of `D1:FB72`, `D1:FB68`, or `D1:F47C` in this pass.
The wrapper identities themselves are exact enough to freeze now.

---

## 3. token `0xE5` is an exact indexed increment helper
At `CD:18C8..18CE` the exact body is:

```text
LDA [$40]
TAX
INC $5D80,X
RTS
```

That means this token consumes one immediate byte from the auxiliary stream,
uses it as an index,
and increments one byte inside the `5D80 + index` strip.

### strongest safe reading
The strongest safe reading is:

> token `0xE5` is an **indexed byte-strip increment helper** over the `5D80` family.

I am still not freezing the final gameplay-facing noun of the `5D80` strip itself.
But the local operation is exact.

---

## 4. token `0xE4` stages one immediate byte and snapshots the current `5DA0` index
At `CD:18CF..18DE` the exact body is:

```text
LDA [$40]
STA $CD24
LDA $5DA0
TAX
STX $CD25
INC $CD23
RTS
```

This is structurally clean:

- one immediate stream byte is stored to `CD24`
- the current byte at `5DA0` is copied into X
- that same value is mirrored into `CD25`
- `CD23` is incremented

### strongest safe reading
The strongest safe reading is:

> token `0xE4` is a **small staging helper** that stores one immediate selector/control byte,
> snapshots the current `5DA0` index byte,
> and bumps a local count/state byte.

The exact final noun of the `CD23 / CD24 / CD25` trio still wants more context,
but their immediate local behavior is now exact.

---

## 5. token `0xE3` is an exact six-byte indexed snapshot/copy helper
At `CD:18DF..1906` the exact body copies six bytes from the live `5DA0..5DA5` vector family
into one indexed record rooted at `CAEA`.

The exact write pattern is:

```text
LDA [$40]
TAX
LDA $5DA0  -> STA $CAEA,X
LDA $5DA2  -> STA $CAEE,X
LDA $5DA4  -> STA $CAF2,X
LDA $5DA1  -> STA $CAEC,X
LDA $5DA3  -> STA $CAF0,X
LDA $5DA5  -> STA $CAF4,X
RTS
```

So this is not a vague “copy some scratch somewhere” helper.
It is an exact indexed snapshot of the current `5DA0..5DA5` six-byte live vector,
written into an interleaved six-byte destination record family rooted at `CAEA`.

### strongest safe reading
The strongest safe reading is:

> token `0xE3` copies the current `5DA0..5DA5` six-byte live vector
> into one indexed destination record in the `CAEA..CAF5` family.

I am still not claiming the final gameplay-facing noun of either family.
But the structural ownership is now exact.

---

## 6. tokens `0xE2` and `0xE1` are exact immediate staging writes
These two siblings are tiny and exact.

### 6a. token `0xE2`
At `CD:1907..190C`:

```text
LDA [$40]
STA $CD2E
RTS
```

### 6b. token `0xE1`
At `CD:190D..1912`:

```text
LDA [$40]
STA $CD2D
RTS
```

### strongest safe reading
The strongest safe reading is:

> `0xE2` and `0xE1` are direct immediate staging/store tokens
> for the neighboring control bytes `CD2E` and `CD2D`.

The final nouns of those bytes remain open,
but these are no longer unresolved handlers.

---

## 7. this tightens the meaning of the whole `0xE0..0xE8` tail cluster
With pass 84 and this pass combined, the late auxiliary cluster now reads much more cleanly:

- `0xE8` -> exact wrapper to `D1:FB72`
- `0xE7` -> exact wrapper to `D1:FB68`
- `0xE6` -> exact immediate write to `CFFF`
- `0xE5` -> indexed increment into `5D80 + index`
- `0xE4` -> stage one immediate byte and snapshot current `5DA0` index into `CD25`, incrementing `CD23`
- `0xE3` -> copy current `5DA0..5DA5` six-byte live vector into indexed `CAEA..CAF5` record space
- `0xE2` -> immediate write to `CD2E`
- `0xE1` -> immediate write to `CD2D`
- `0xE0` -> exact wrapper to `D1:F47C`

That means the family is no longer “a few known tokens plus a foggy tail.”
It is now mostly concrete.

---

## 8. strongest keepable conclusions from pass 85
1. The auxiliary VM late tail `0xE0..0xE8` is a real contiguous control family.
2. `0xE1`, `0xE2`, `0xE4`, and `0xE6` are direct immediate-state staging/store helpers.
3. `0xE3` is an exact indexed six-byte snapshot helper from the live `5DA0..5DA5` vector family.
4. `0xE5` is an exact indexed increment helper over the `5D80` byte strip.
5. `0xE7`, `0xE8`, and `0xE0` are exact D1 wrappers.
6. This pass materially shrinks the unresolved auxiliary tail before the project goes back to the wider `CDC8 / CE0F` reader hunt.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the `5D80` byte strip.
- I have **not** frozen the final noun of the `5DA0..5DA5` six-byte live vector family.
- I have **not** frozen the final noun of the indexed destination record family at `CAEA..CAF5`.
- I have **not** yet pinned the first exact external reader(s) of `CDC8` and `CE0F`.
- I have **not** proven whether auxiliary token `0xE6` uses only `00/01` in real content or multiple meaningful nonzero values.

---

## Next recommended target
The cleanest next move is:

1. keep the same local-control mindset and find the first exact reader(s) of `CD23 / CD24 / CD25 / CD2D / CD2E`
2. then return to the external-reader hunt for `CDC8` and `CE0F`
3. only after that, go back to the remaining wider unresolved auxiliary families

That keeps the project on the high-value path of converting exact VM/control seams into durable labels instead of guessing presentation nouns too early.
