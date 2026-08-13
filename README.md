# primeg2-sat

# **please read the [disclaimer](DISCLAIMER.md) before using this project.**

this is my first repository. i wanted to make a program that makes solving and understanding sat questions easier for students.

this is a portable sat math solver, built for graphing calculators and your devices. running it on a regular pc with python is possible through your terminal. 

i have been using the hp prime virtual calculator to test this. the physical hp prime g2 should work the same, but other python‑capable graphing calculators (ti‑84 evo, numworks, casio fx‑cg50) may run into small quirks because i haven't tested them personally. please let me know if you find any issues.

## launching on the hp prime (virtual or physical)

shift + program,
click SAT

## what's inside

- step‑by‑step solvers for over 60 sat math topics
- a built‑in sat formula reference with examples
- text guides for tricky conceptual topics like surveys, data visualization, circle theorems, and more
- calculator utilities like fraction simplifier, gcf, prime factorization, and others

## why the hp prime g2?

simply because it has better hardware.

## will you make a ti version?

maybe... we will see.

## installation (windows) (mac not tested, should work)

1. install the hp connectivity kit and the hp prime virtual calculator (unless you already have one)
2. open connectivity kit, locate your calculator, then double click
3. click application library
4. click python
5. right‑click files, then add file, then add this program
6. scroll down to programs
7. right click, name it "SAT"
8. paste this script:
###
#PYTHON launcher
exec(open("sat.py").read())
#END

EXPORT SAT()
BEGIN
  PYTHON(launcher);
END;   
###
9. make sure to save everything to calculator

## installation (linux)
> sorry linux users (including me, i use cachy btw), there is no official hp prime virtual calculator for linux, but you can still run the sat solver in the terminal safely.

1. install python from your package manager:
   - ubuntu/debian: `sudo apt install python`
   - fedora: `sudo dnf install python`
   - arch: `sudo pacman -S python`
2. open your file manager and navigate to where `sat.py` is saved, and use the full path
3. run: python /path/of/sat.py *(replace `/path/of/` with the real location)* or if you're comfortable, `cd` into where `sat.py` is saved, then run: python `sat.py`

## license (gnu gpl 3.0)

this project uses the gnu general public license version 3.0.

**you can:**
- use this sat solver for anything you like
- study the code and change it however you want
- share it with friends, classmates, or the whole internet
- include it in your own projects (even paid ones)

**you must:**
- keep the same gpl 3.0 license if you distribute your version
- make your changes open‑source too
- keep the original copyright notice and license text

**the catch:**
there's no warranty — if something breaks, i'm not responsible.
but that's standard for open‑source software.

**why gpl 3.0?**
i chose this license so that any improvements to the solver stay free and open for everyone. nobody can take this tool, tweak it, and lock it behind a paywall. the math help stays free — forever.

## contributing

found a bug? have an idea? open an issue or a pull request. i'm learning too, so i'd love the help.

## thanks

built for students who want to truly understand the math. hope it helps!
