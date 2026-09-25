---
title: Problem set — the second law and heat engines
short_title: 07 · Problems
---

# Problem set: the second law and heat engines

Exam-style problems. Work them with a pen before touching a computer; the last one is meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ throughout, and give every temperature
in kelvin before doing anything else with it.

## Problem 1 — the two statements

<!-- objectives: OBJ-07-1, OBJ-07-2 -->

(a) State the Kelvin and Clausius forms of the second law, and explain what the words
*cyclic* and *sole result* are doing in each. Give an example of a real process that converts
heat entirely into work, and say why it does not violate the Kelvin statement.

(b) A device is claimed to draw $500\ \mathrm{J}$ per cycle from a single reservoir at
$400\ \mathrm{K}$ and deliver $500\ \mathrm{J}$ of work, returning to its initial state each
cycle. Construct, in words and with an energy diagram, a machine that combines this device
with an ordinary refrigerator to violate the Clausius statement.

(c) Explain why a gas undergoing a single quasistatic isothermal expansion is not a
counterexample to (a), even though $\Delta U = 0$ and all the heat absorbed becomes work.

## Problem 2 — bounds on a real plant

<!-- objectives: OBJ-07-4 -->

A steam turbine takes heat from a boiler at $811\ \mathrm{K}$ and rejects it to a condenser at
$311\ \mathrm{K}$. It absorbs $2.40\ \mathrm{GJ}$ of heat per second.

(a) Compute the maximum possible efficiency and the maximum possible power output.

(b) The plant actually delivers $0.95\ \mathrm{GW}$. Compute its efficiency, and the rate at
which it dumps heat into the condenser.

(c) An engineer proposes raising the output by cooling the condenser to $280\ \mathrm{K}$ with
a refrigeration unit, which would itself reject its heat to the surroundings at
$311\ \mathrm{K}$. Without computing anything, give the argument for why this cannot pay for
itself. Then estimate the minimum work the refrigeration unit would need — assume it must
move the full condenser load — and compare that with the extra output the colder condenser
would buy.

(d) Compute $1 - \sqrt{T_c/T_h}$ for this plant and compare it with your answer to (b).
Comment on what this does and does not tell you.

## Problem 3 — Carnot's theorem as a tool

<!-- objectives: OBJ-07-3, OBJ-07-6 -->

(a) An inventor claims an engine running between $500\ \mathrm{K}$ and $300\ \mathrm{K}$ that
absorbs $1000\ \mathrm{J}$ and delivers $450\ \mathrm{J}$ per cycle. Is the claim possible?
Show your reasoning, and state which law is violated if it is not.

(b) A second inventor claims $380\ \mathrm{J}$ from the same $1000\ \mathrm{J}$ between the
same reservoirs. Is this possible? Is it necessarily *achievable*?

(c) Two reversible engines run between the same reservoirs, one using helium and one using
steam. Prove, using only Carnot's theorem and without evaluating anything, that they have
identical efficiencies. Where exactly would a proof that depended on the working substance
break down?

(d) Explain how a reversible engine could be used to construct a temperature scale, and state
one practical reason this is not how thermometers are actually built.

## Problem 4 — the refrigerator and the kitchen

<!-- objectives: OBJ-07-5 -->

A refrigerator maintains its interior at $275\ \mathrm{K}$ in a kitchen at $298\ \mathrm{K}$.

(a) Compute the maximum possible coefficient of performance. The unit actually achieves 3.2;
compute the electrical power it needs to remove heat at $150\ \mathrm{W}$.

(b) Compute the rate at which the refrigerator delivers heat into the kitchen. A student
suggests cooling the kitchen on a hot day by leaving the refrigerator door open. Say exactly
what happens to the kitchen's temperature, and why.

(c) The same hardware is used as a heat pump to warm a house at $295\ \mathrm{K}$ from outside
air at $273\ \mathrm{K}$. Compute the maximum COP. Compare the electricity needed to deliver
$5\ \mathrm{kW}$ of heating this way with the electricity a resistive heater would need, and
explain in one sentence where the difference comes from.

(d) The outside temperature drops to $258\ \mathrm{K}$. Recompute the maximum COP and comment
on why heat pumps are harder to justify in very cold climates.

## Problem 5 — where the work went

<!-- objectives: OBJ-07-7 -->

An engine runs between reservoirs at $600\ \mathrm{K}$ and $300\ \mathrm{K}$, but its heat
exchangers are imperfect: the working gas sits at $560\ \mathrm{K}$ while absorbing heat and
at $340\ \mathrm{K}$ while rejecting it. Internally every stroke is reversible.

(a) Compute the engine's efficiency and compare it with the Carnot bound for the reservoirs.

(b) Per $1000\ \mathrm{J}$ absorbed from the hot reservoir, compute the work delivered, the
heat rejected, and the value of $\oint \dbar Q / T_{\text{res}}$, being careful about which
temperature belongs in each denominator.

(c) Show that the work lost, compared with a perfect Carnot engine drawing the same
$1000\ \mathrm{J}$, equals $T_c$ times the quantity you computed in (b). Interpret this
result.

(d) Explain why closing the temperature gaps to zero is not a design improvement anyone can
adopt, and what is actually being traded away.

## Problem 6 — computational

<!-- objectives: OBJ-07-3, OBJ-07-4, OBJ-07-7 -->

Using the module's laboratory notebook and the `thermolab.engines` module:

(a) Build Carnot cycles between $600\ \mathrm{K}$ and $300\ \mathrm{K}$ for at least four
combinations of working gas ($f = 3, 5, 6$) and expansion ratio, and tabulate the
efficiencies. Report how many figures they agree to, and say what that is evidence for.

(b) Using `endoreversible_cycle`, plot the efficiency against the temperature gap for gaps
from $0$ to $100\ \mathrm{K}$, with the Carnot bound drawn as a horizontal line. At what gap
has the engine lost a quarter of its available efficiency?

(c) On the same axes plot the entropy produced per cycle against the gap. Fit its behaviour
at small gap and state the power law you find.

(d) Attempt to construct any cycle from the library that exceeds $1 - T_c/T_h$. Report what
you tried. Then state precisely why failing to find one is *not* a proof of Carnot's theorem,
and what it is evidence of instead.

## Problem 7 — the cost of irreversibility

<!-- objectives: OBJ-07-8, OBJ-07-9, OBJ-07-7 -->

(a) A block sliding across a table at $300\ \mathrm{K}$ is brought to rest by friction,
converting $50\ \mathrm{J}$ of kinetic energy into heat that ends up in the table. Show that
undoing this process without trace would violate the Kelvin statement, and compute the entropy
produced.

(b) On a winter day, $500\ \mathrm{J}$ of heat leaks through a window from a room at
$293\ \mathrm{K}$ to the outside air at $263\ \mathrm{K}$. Compute the entropy produced, and
the work that an ideal engine placed across the window could have delivered from the same
heat. Show that the two answers are related as the lost-work theorem says they must be.

(c) One mole of ideal gas ($N = 6.022 \times 10^{23}$) at $300\ \mathrm{K}$ expands freely into
a vacuum, doubling its volume inside an insulated box. Compute its entropy change by choosing a
suitable reversible process between the same end states, and explain why that is legitimate
although the real process is nothing like it. How much work would the reversible process have
delivered, and how is that number related to the entropy produced?

(d) Two identical blocks, each of heat capacity $C = 500\ \mathrm{J\,K^{-1}}$, one at
$400\ \mathrm{K}$ and the other at $200\ \mathrm{K}$, are put in thermal contact inside an
insulated box. Find the final temperature and the total entropy change. Then show, for any
starting temperatures $T_1$ and $T_2$, that

$$
\Delta S = C \ln \frac{(T_1 + T_2)^2}{4\, T_1 T_2} \ge 0 ,
$$

with equality only when $T_1 = T_2$.

(e) Suppose instead that a reversible engine runs between the two blocks of (d) until they
reach a common temperature. Find that temperature and the total work delivered, and explain in
one sentence why the final temperature is lower than in (d).

## Problem 8 — the Otto engine

<!-- objectives: OBJ-07-4, OBJ-07-9 -->

An idealised petrol engine takes in air at $T_1 = 300\ \mathrm{K}$ and compresses it
adiabatically by a factor $r = 10$; treat air as an ideal gas with $\gamma = 7/5$. Burning the
fuel then heats it at constant volume to $T_3 = 2200\ \mathrm{K}$, it expands adiabatically
back to its original volume, and it gives up its remaining heat at constant volume.

(a) Show that the efficiency is $\eta = 1 - r^{1-\gamma}$, independent of $T_3$, and evaluate
it.

(b) Find the temperatures $T_2$ after compression and $T_4$ after expansion. Compare the
efficiency with the Carnot bound between the coldest and hottest temperatures the air reaches.

(c) Every stroke of this cycle is reversible, yet it falls short of that bound. Explain why,
by dividing the cycle into thin slices with adiabats.

(d) Compute the entropy change of the air on the heating stroke and on the cooling stroke.
Dividing each stroke's heat by its entropy change defines an average temperature for that
stroke; compute both, and show that the engine's efficiency is that of a Carnot engine between
them.

(e) The efficiency grows with $r$. What stops petrol engines from using much higher
compression ratios, and how does the diesel engine of module 06 get around it?
