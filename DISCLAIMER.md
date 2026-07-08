## “this is not affiliated with or endorsed by the college board.”

## a quick note on cheating (don't do it)

this sat math solver is an educational study tool, not a way to cheat.

- it’s here to help you **learn, practice, and review** math concepts for the digital sat.
- it is **not** meant to be used during the actual exam — that breaks college board rules.
- use it for self‑checking, homework, tutoring sessions, or classroom demos.
- the whole point is to **understand the math**, not just copy what the calculator says.

---

## don't run this on a regular computer

this software was built just for **graphing calculators and their official emulators**.
running it on a pc or mac with a full python interpreter is a bad idea, mainly because:

1. **security** — the universal equation solver uses a locked‑down `eval()` that’s safe on a calculator. on a desktop, a sneaky input could break out of the whitelist and run nasty code.

**safe ways to run it:**
- on an actual hp prime g2 (or any supported calculator)
- on the official **hp prime virtual calculator** emulator (windows/macos)
- in a **micropython emulator** that acts like a calculator

*seriously, just don't run it in a regular python terminal unless you’re in a sandbox.*

---

## always be careful

always run code with the highest caution. you better know what you’re doing. :)
