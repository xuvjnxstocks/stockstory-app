# Draven Multi-Agent Research Contracts

These contracts define what each agent may produce, what it may not infer, and the rejection criteria applied at each handoff.

## 1. Orchestrator and compliance gate

**Inputs:** ticker, proposed event, intended holding period, evidence cutoff, known conflicts.  
**Outputs:** official security, event definition, dated or windowed timing, source plan, conflict status, required agents.  
**Reject when:** the event cannot be verified from a primary source; the security or rights economics are ambiguous; the evidence cutoff is missing; a personal-trading or employer-coverage conflict is unresolved.

## 2. Evidence-dossier agent

Create atomic evidence records before writing prose.

Each record must include:

- claim;
- exact source;
- publication and effective dates;
- source tier;
- confidence;
- entity and asset resolution;
- whether it is observed, calculated, or inferred;
- conflicts with other records.

**Prohibited:** merging conflicting claims, silently selecting a preferred source, or converting guidance windows into exact dates.

## 3. Clinical and biology agent

For each material endpoint, capture population, line of therapy, intervention, comparator, dose, analysis population, denominator, estimand, effect estimate, confidence interval, P value, analysis timing, missingness, censoring, and relevant subgroup behavior.

**Required output:** mechanistic crux, translational chain, same-modality comparator, efficacy table, safety table, and clinical-adoption constraints.

**Reject when:** the analysis compares non-comparable populations without a comparability grade or treats response rate, PFS, and OS as interchangeable evidence.

## 4. Biostatistics agent

Reconstruct the statistical architecture using only disclosed information.

Evaluate:

- primary and secondary hypotheses;
- multiplicity and hierarchy;
- interim looks and alpha spending;
- information fraction when disclosed;
- proportional-hazards assumptions;
- censoring and follow-up maturity;
- sensitivity to event count and effect attenuation.

**Required:** distinguish nominal P values from prespecified success boundaries. Present probability ranges when confidential design inputs are unavailable.

## 5. Regulatory and CMC agent

Decompose regulatory probability into efficacy, safety, CMC, inspection, labeling, confirmatory-obligation, and procedural risk. Prior approval of the molecule may reduce specific risks but may never be described as eliminating CMC or inspection risk.

**Required scenarios:** broad approval, narrower approval, delay, extension, CRL, and approval with material post-marketing obligations.

## 6. Commercial and competitive agent

Assess addressable population, biomarker prevalence, line of therapy, treatment duration, regimen complexity, payer and physician constraints, partner rights, royalties, milestone economics, launch responsibilities, and same-indication competitors.

**Reject when:** market size is calculated from prevalence without diagnosis, treatment, eligibility, penetration, duration, and net-price adjustments.

## 7. Capital structure and valuation engine

All scenario prices must reconcile through a disclosed bridge:

```text
equity value
= unrestricted cash
+ probability-adjusted milestone value
+ royalty or product value
+ acquired-asset value
+ pipeline residual
- debt
- royalty financing
- transaction obligations
- expected dilution
```

The engine, not the prose agent, calculates probability-weighted value and expected return.

## 8. Ownership and positioning agent

Ownership informs likely stock behavior, not clinical probability. Separate stale 13F data, current beneficial-ownership filings, passive holdings, specialist concentration, short interest, days to cover, borrow conditions, and recent flow.

**Prohibited:** treating institutional ownership as proof of clinical success.

## 9. Options and instrument-selection agent

Use a synchronized chain. For each candidate structure, calculate executable debit or credit, maximum loss, maximum gain, breakeven, expiry coverage, spread width as a fraction of structure width, open interest, volume, implied volatility, and expected payoff under the fundamental scenarios.

**Automatic rejection:**

- expiry does not cover the event window;
- quoted spread exceeds 15% of vertical width unless explicitly approved;
- expected value is negative using executable prices;
- timing guidance can slip beyond expiration;
- short-premium exposure creates unbounded or insufficiently bounded regulatory gap risk.

## 10. Red-team agent

Attack every load-bearing claim. Produce the strongest alternative explanation, identify correlated downside, expose circular valuation, test stale sources, and state the single new fact that would most change the recommendation.

## 11. Investment committee editor

The final report must contain:

1. conclusion and instrument;
2. evidence cutoff and version hash;
3. catalyst map;
4. clinical and statistical crux;
5. regulatory decomposition;
6. commercial and rights economics;
7. valuation bridge and scenario table;
8. ownership and positioning;
9. instrument gate;
10. falsifiers, kill criteria, and post-event rules;
11. source ledger and disclosures.

No probability, terminal value, or market statistic may appear without a source or disclosed assumption.

## 12. Post-event scorecard

After the event, freeze the pre-event report and score:

- event timing accuracy;
- outcome classification;
- endpoint forecast error;
- regulatory forecast calibration;
- terminal-price error at one day, two days, and ten trading days;
- instrument-selection result;
- thesis elements that were right for the wrong reason;
- process changes required.

Backtests must use archived evidence snapshots and must not permit revised publications or later registry updates to leak into the historical dossier.
