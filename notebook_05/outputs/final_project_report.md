# Fair and Constraint-Aware Pharmacy Shift Scheduling

## Abstract

This project investigates pharmacy duty scheduling as a constrained allocation of workload. The sole empirical input is the supplied TURNI CSV. The Bologna city-area calendar contains 53 weekly blocks, 123 rotating pharmacies and 931 assignments, organized into 42 recurring patterns and seven dominant rotation groups. A mixed-integer linear program preserves a historical staffing floor, H24 duty count, primary-group eligibility, a horizon workload ceiling and a policy of balanced H24 cycle counts. It compares efficiency-first, fairness-aware and full-group scenarios using lexicographic priorities.

The selected fairness-aware schedule has 923 assignments, total workload range 1 and H24 range 1, compared with 931, 2 and 3 historically. Total Jain improves slightly, but total Gini increases slightly; fairness improvement is metric-specific. 11 complete nT patterns change, including 2 with H24-only changes.

The robustness experiment tests 738 eligible pharmacy-pattern cases, of which 730 affect scheduled pharmacies. 424 (58.1%) have a materialized, model-feasible same-group response. All 306 remaining cases (41.9%) require human intervention. 17 have a historically evidenced candidate; these are not automatically authorized. These are completed results of a dataset-only computational case study; unrecorded real-world variables are excluded by design.

## 1. Research question and ethical framing

The research question is: how can the observed rotation be retained while reducing selected workload disparities, testing single-pharmacy pattern unavailability and explaining the resulting decisions?

### Dataset-only scope and completion criterion

The project uses only the CSV supplied in the original archive as empirical input. No geographic, actual-availability, demand, preference or external legal/contractual dataset is added. Those subjects are outside the agreed project scope and are not unfinished submission requirements. The analysis is complete when the reconstructed data, explicitly justified model, optimized schedules, simulated robustness results and report agree and can be reproduced from that input.

The distinction between observation and modeling is maintained throughout. Counts, dates, identifiers, H24/STANDARD labels, P/C labels and historical co-occurrences are observations or deterministic derivations. Workload equality, scenario priorities, historical continuity and the choice to simulate one absence at a time are analytical design choices. They are justified explicitly rather than attributed to information absent from the file. References support mathematical methods and the ethics discussion; they provide no additional pharmacy data.

Duty scheduling affects pharmacy organizations, workers, citizens and scheduling authorities. Fewer assignments can reduce measured workload but also remove redundancy, income opportunities or service availability. Equal pharmacy counts do not establish equal public access. The model's preferred outcome therefore depends on the objective chosen by the scheduling authority.

The European Commission's Trustworthy AI guidelines identify human oversight, technical robustness, privacy and data governance, transparency, fairness and accountability among their requirements. These provide an ethical framing for this case study; passing the computational checks is not certification against those guidelines. [1]

No protected-attribute, ownership, workforce, revenue or preference data are included. The project measures count-based allocation fairness among modeled pharmacies. It does not establish demographic parity, equal opportunity, legal compliance or absence of discrimination. Pseudonymizing names also does not remove inequities potentially embedded in historical group membership.

## 2. Dataset, reconstruction and privacy

The supplied CSV is a semi-structured spreadsheet export with date blocks, shift-section headers and pharmacy assignment rows. Notebook 00 checks the expected column layout, normalizes Unicode and whitespace, accepts assignment rows with access mode P or C and excludes two rows explicitly marked as outside the duty rotation. Names and addresses are replaced by pharmacy and location identifiers; source-row positions are retained for traceability.

The source distinguishes H24 from STANDARD service, and P (open-door) from C (call/closed-door) access. The source headers describe H24 as Monday 08:30 to the following Monday 08:30, and STANDARD duty as 08:30-12:30 and 15:30-19:30, Monday through Sunday. These labels describe the source; the model counts weekly assignments rather than simulating actual opening hours. One assignment is a pharmacy-week duty block, not an employee shift, working-hour total or full-time-equivalent measure.

| Property | Value |
| --- | --- |
| Weekly blocks | 53 |
| Distinct nT patterns | 42 |
| Rotating pharmacies | 123 |
| Historical assignment rows | 931 |
| Historical H24 assignments | 159 |
| Historical STANDARD assignments | 772 |
| Weekly historical staffing | 17-18 |
| H24 pharmacies in each block | 3 |
| Maximum assignments per pharmacy in the horizon | 8 |
| Excluded non-rotation facilities | 2 |
| Group sizes, in group order | 17, 18, 18, 17, 18, 18, 17 |

The first block begins on 29 December 2025 and ends on 5 January 2026. The final block begins on 28 December 2026 and is recorded as ending on 3 January 2027. That final end date is Sunday, six elapsed days after Monday start, inconsistent with a uniform Monday-to-Monday handover. Counting seven inclusive calendar dates does not resolve that timing inconsistency. The pipeline preserves the original boundary and records it as a source-data limitation; it does not guess a corrected date or require a second dataset to complete the analysis. Throughout this report, horizon workload means counts over all 53 source blocks, including the boundary anomaly, rather than hours or a strict 365-day total.

Sequential pseudonyms are not anonymization. Source-row positions, rare schedule features and the public calendar can enable linkage. The raw CSV and private mapping files contain the identifying information supplied with the project and are retained for reproducibility. They are excluded by the supplied version-control ignore rules. Analytical outputs use pseudonyms, but are not claimed to be irreversibly anonymous. Existing mappings are validated and new IDs start above the largest existing identifier, preventing collisions when a later dataset adds pharmacies or locations.

### Access modes, locations and source fidelity

The reconstructed calendar has 124 distinct pharmacy-location identifiers for 123 pharmacies. 118 pharmacies have mode P and 5 have mode C; no pharmacy changes P/C label across its observed rows. One pharmacy has two observed locations. Locations are retained as identifiers and are not converted into a geographic coverage model. Every accepted row preserves its source-row reference, and all accepted rows occur exactly once in the canonical output.

## 3. Computational pipeline and rotation evidence

The six notebooks execute in order: cleaning and canonicalization; descriptive baseline; constraint specification; MILP optimization; pattern-level robustness; final comparison and reporting. They exchange explicit CSV and JSON artifacts rather than relying on notebook memory. All three optimized schedules are exported, allowing every scenario's reported metrics to be checked against its actual rows.

The canonicalizer reconstructs dates, nT labels, groups, rounds, shift types and access modes. It verifies row counts, unique pharmacy-week assignments, consecutive weekly starts, adjacent boundaries, nT progression and consistent week metadata. The baseline checks repeated patterns and the constant H24 count. Identical nT values reuse the same pharmacy, location, shift and access signature across their calendar occurrences; there are 11 matching repeated-pattern comparisons out of 11.

For candidate periods 2 through 41, membership purity is the sum, across pharmacies, of the largest assignment count in any nT residue class, divided by all assignment rows. The leading period is 7 with purity 0.998926. One historical cross-group row means purity is not perfect. Dominant historical membership determines each pharmacy's primary modeled group; this is an inference from observations, not an externally supplied authorization list.

The revised permutation sensitivity test randomizes the 42 nT labels as intact pattern blocks, preserving each pattern's pharmacy membership and repeated-week multiplicity. Each randomization repeats the entire candidate-period search. It uses B=500 permutations and finds b=0 null maxima at least as extreme as the observed maximum. The corrected Monte Carlo p-value is (b+1)/(B+1) = 0.001996. Randomly sampled permutation p-values should not be reported as zero. [2]

This result supports the period under an exchangeable-pattern-label null. It is exploratory evidence, not proof of an administrative rule or stability in another year. The original row-level label shuffle disrupted within-pattern structure and repeated blocks; the revised procedure retains those dependencies. The significance claim is limited to this explicit randomization null.

Each stage records hashes of relevant inputs, outputs and implementation modules; downstream stages check those manifests before use. Notebook 05 additionally checks the explicit canonical, applied-specification, optimized-schedule and robustness links. Hashes detect accidental stale or altered artifacts relative to recorded manifests; they are not authentication, external validation or proof that a formula is correct.

### Numerical settings for the exploratory test

Candidate periods are 2 through 41, inclusive. The random seed is 0. The mean of the null best-purity values is 0.665429, and their maximum is 0.794844. The number of permutations controls Monte Carlo resolution; it is a computational precision setting, not a pharmacy-data value or a fairness threshold. A 0.01 significance cutoff is an explicit screening choice used to stop the pipeline if this exploratory structural evidence is weak, rather than a requirement inferred from pharmacy data. The complete search is repeated for each draw, so the null comparison accounts for selection of the leading candidate.

## 4. Fairness definition and parameter provenance

For N nonnegative pharmacy workloads w_i, range is max(w_i)-min(w_i), and population variance is the mean squared deviation from the mean workload. Range is understandable and easy to model linearly, but ignores changes between the extremes.

Jain's index is J(w) = (sum w_i)^2 / (N * sum w_i^2). For a nonzero nonnegative allocation its range is 1/N to 1, with 1 representing equality. [3] The project computes it descriptively; it is not a MILP objective. Gini is G(w) = sum over i,j of |w_i-w_j| / (2*N*sum w_i). Higher Gini indicates more inequality. Both metrics are evaluated across all 123 pharmacies, including any zero H24 counts. The code's all-zero convention is Jain=1 and Gini undefined; no reported schedule has zero aggregate workload. For a finite nonnegative N-pharmacy allocation, the maximum uncorrected Gini is (N-1)/N; no finite-sample correction is applied.

| Parameter or choice | Value / policy | Evidence status |
| --- | --- | --- |
| Weekly staffing floor | 17 | Historical minimum used as an unvalidated proxy |
| Horizon workload ceiling | 8 | Historical maximum used as an unvalidated proxy |
| Weekly H24 count | Exactly 3 | Observed constant retained by modeling policy |
| Primary-group eligibility | Dominant historical group | Observed association converted into an eligibility assumption |
| Shared nT decisions | All occurrences identical | Observed recurrence retained as policy |
| H24 cycle counts per pharmacy | 1-2 in 17-member groups; exactly 1 in 18-member groups | Normative equal-count allocation derived from 18 cycle slots |
| Recommended objective | Total range, H24 range, assignment count | Normative priority |
| Historical changes | Lower-priority tie-breakers | Normative continuity preference |

The cycle bounds deserve particular emphasis: six patterns per group times three H24 duties gives 18 H24 slots. Allocating those as evenly as possible yields floor(18/group size) and ceiling(18/group size). This is a hard equal-count fairness policy. Arithmetic derives its values, but does not make the policy an observed fact. Because the CSV has no capability variable, service type is modeled as reassignable among the primary-group members. This is an explicit symmetry assumption used for count-based optimization, not an additional capability observation.

Counts also omit differences in holidays, call duty, demand, staff size, costs, income and actual duration. A burden-adjusted objective would need weights unsupported by this dataset. Accordingly, no such weights are invented; total and H24 counts are analyzed separately.

## 5. Mathematical model

Let I be the pharmacy set, T the 42 patterns, g(t) the structural group of a pattern, g_i the dominant group of pharmacy i, and m_t the number of calendar occurrences of pattern t. Eligible decisions are E = {(i,t): g_i=g(t)}. For each eligible pair, binary y_it indicates active duty and binary h_it indicates H24 duty. Noneligible pairs are absent from the variable set.

Define total workload W_i = sum_t m_t*y_it and H24 workload H_i = sum_t m_t*h_it. H24 cycle workload C_i = sum_t h_it counts distinct patterns, with no occurrence weight. The implemented hard constraints are:

1. For every pattern t, sum_i y_it >= 17.
2. For every pattern t, sum_i h_it = 3.
3. For every eligible pair, h_it <= y_it.
4. For every pharmacy i, W_i <= 8 over the 53-block horizon.
5. For every pharmacy i in group g, floor(18/size_g) <= C_i <= ceiling(18/size_g).
6. Auxiliary extrema satisfy W_min <= W_i <= W_max and H_min <= H_i <= H_max; their differences define the two range objectives.

The variables y and h are binary. The four auxiliary extrema are continuous and bounded between zero and the horizon ceiling. Pattern-level variables enforce identical repeated nT assignments by construction. Location and access mode are carried from observed pharmacy metadata and checked in the materialized rows; neither is optimized.

The mixed-integer problem is solved through SciPy's milp interface to HiGHS. Each lexicographic stage must terminate successfully at zero reported relative MIP gap; bounds, integrality and linear-constraint residuals are checked before the objective is locked. Solver objectives and dual bounds are exported in solver_evidence.json. SciPy documents the MILP status and gap fields used for these checks. [4]

The scenario priority orders are:

- Efficiency-first: assignments, total range, H24 range, active changes, H24 changes.
- Fairness-aware: total range, H24 range, assignments, active changes, H24 changes.
- Full-group: fix every eligible y_it to one, then minimize H24 range and H24 changes.

Changes are weighted by calendar occurrences. Their linear coefficient is m_t minus twice the number of historical occurrences of that decision; a constant can be omitted without changing the minimizing solution. The unavoidable removal of an ineligible historical cross-group row is another constant. These tie-breakers minimize changed active/H24 decisions, not the number of distinct changed patterns. Equal objective values can therefore allow different detailed schedules across solver versions.

The historical schedule is a descriptive comparator. It contains a cross-group exception and need not satisfy the revised eligibility and cycle-balance policy; it is not presented as a feasible point of the same model.

## 6. Fairness and efficiency results

| Scenario | Assignments | Total range | H24 range | Nondominated* | Selected |
| --- | --- | --- | --- | --- | --- |
| Fairness-aware | 923 | 1 | 1 | True | True |
| Full-group | 931 | 1 | 1 | False | False |
| Historical | 931 | 2 | 3 | False | False |
| Efficiency-first | 901 | 3 | 1 | True | False |

*The table's nondominance labels compare the four displayed candidates over assignments, total range and H24 range. They do not enumerate the full feasible frontier. For the lexicographically optimized scenarios, optimality is separately supported by the solver evidence. Dominance uses only the declared comparison metrics and is not a claim about every ethical consideration.

The fairness-aware schedule removes 8 assignments (0.86% of history) and uses 22 more assignments than efficiency-first. It narrows total workload from 6-8 to 7-8 assignments and H24 workload from 0-3 to 1-2 assignments per pharmacy. Full-group matches those ranges but uses eight more assignments. It is dominated under the selected three metrics, yet has better total Jain and Gini than fairness-aware. Thus the preferred scenario depends on the specific fairness objective, not on a universal ordering of fairness.

| Measure | Historical | Fairness-aware |
| --- | --- | --- |
| Assignments | 931 | 923 |
| Total workload range | 2 | 1 |
| H24 workload range | 3 | 1 |
| Total Jain | 0.995456618 | 0.995580284 |
| Total Gini | 0.033306262 | 0.033313074 |
| Total population variance | 0.261484566 | 0.249983475 |
| H24 Jain | 0.867242976 | 0.889768768 |
| H24 Gini | 0.176100629 | 0.160147262 |

Total Jain increases slightly. Total Gini increases from 0.033306262 to 0.033313074, a small worsening of 0.000006812; both round to 0.0333 at four decimals. It would be incorrect to say that all fairness indices improve. The strongest positive results are the reduced total and H24 ranges and the improved H24 distribution.

There are 11 changed full patterns and 31 unchanged patterns in this executed solution. 9 patterns change active membership and 3 change H24 membership; 2 have H24-only changes. nt_change_explanation.csv records both types, including added and removed H24 IDs. A count based only on active pharmacies misses the H24-only changes. Patterns should not be called overstaffed merely because they exceed the historical-minimum proxy.

### All scenario fairness statistics

| Scenario | Total min | Total max | H24 min | H24 max | Total Jain | Total Gini | H24 Jain | H24 Gini |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Historical | 6 | 8 | 0 | 3 | 0.995457 | 0.033306 | 0.867243 | 0.176101 |
| Efficiency-first | 5 | 8 | 1 | 2 | 0.988469 | 0.054050 | 0.889769 | 0.160147 |
| Fairness-aware | 7 | 8 | 1 | 2 | 0.995580 | 0.033313 | 0.889769 | 0.160147 |
| Full-group | 7 | 8 | 1 | 2 | 0.995738 | 0.032398 | 0.889769 | 0.160147 |

### Workload distributions

| Schedule | Workload type | Assignments per pharmacy | Pharmacies |
| --- | --- | --- | --- |
| Historical | Total | 6 | 1 |
| Historical | Total | 7 | 51 |
| Historical | Total | 8 | 71 |
| Historical | H24 | 0 | 1 |
| Historical | H24 | 1 | 87 |
| Historical | H24 | 2 | 33 |
| Historical | H24 | 3 | 2 |
| Fairness-aware | Total | 7 | 61 |
| Fairness-aware | Total | 8 | 62 |
| Fairness-aware | H24 | 1 | 87 |
| Fairness-aware | H24 | 2 | 36 |

These distributions make the range and inequality calculations auditable from counts of pharmacies rather than only aggregate indices. All N pharmacies enter each distribution; zeros are included for historical H24.

### Changes measured at calendar level

| Scenario | Active decision changes | H24 decision changes |
| --- | --- | --- |
| Historical | 0 | 0 |
| Efficiency-first | 32 | 6 |
| Fairness-aware | 10 | 6 |
| Full-group | 2 | 6 |

A changed active or H24 decision means an added or removed pharmacy-week binary decision. Replacing one pharmacy with another counts as two changes, and recurring nT patterns contribute once for each affected calendar occurrence. These counts therefore differ from the number of distinct changed patterns.

## 7. Structural limits of the groups

Under the current membership, groups 1, 4 and 7 have 17 members. With a staffing floor of 17, removing any member leaves only 16 available pharmacies, so same-group recovery cannot meet staffing. The other four groups have 18 members. A spare member alone is not sufficient proof of recovery: annual limits and H24 constraints must also pass, as checked experimentally.

The counting proof requires precise assumptions. Making every one of seven groups robust to one absence under the floor requires at least 7*18=126 pharmacies, more than the available 123. If every group must first contain at least 17 pharmacies, allocating that minimum uses 7*17=119 pharmacies and leaves four. Those four can provide a spare to at most four groups; at least three groups therefore have exactly 17 members. The observed 17/18 distribution attains that bound and is maximally balanced by group size.

The identities 1, 4 and 7 are not fixed by mathematics. A repartition can move which groups are fragile. If groups below the staffing floor were allowed, even the claim of at least three small groups would fail: six groups of 18 and one of 15 also total 123, but the 15-member group cannot staff an ordinary week. The proof excludes that infeasible repartition by its explicit minimum-size assumption.

The proof does not establish that observed membership minimizes affected calendar weeks, weighted absence risk, geographic harm or workload disruption. Those are different optimization objectives. In particular, nT patterns occur with different multiplicities over the 53-block horizon.

## 8. Pattern-level robustness and substitutions

The experiment considers 738 eligible pharmacy-pattern pairs: each of 123 pharmacies has six primary-group patterns. 8 cases involve an inactive pharmacy and require no response; they are excluded from the recovery-rate denominator. The 730 scheduled cases are evaluated one at a time from the same base schedule, not cumulatively.

An absence removes a pharmacy from every calendar occurrence of its nT. When staffing falls below the floor, the policy considers a same-group spare without exceeding the horizon workload ceiling. If the absent pharmacy was H24, a small MILP reassigns H24 across all six patterns in that group. It preserves the H24 cycle bounds and the base schedule's annual H24 minimum and maximum. The optimal total-workload range is not locked during recovery, so disruptions can worsen total-count fairness.

Every reported successful response is expanded to calendar rows and checked for week metadata, absence compliance, unique pharmacy-week assignments, group eligibility, staffing, H24 totals, cycle bounds, horizon ceiling and repeated-pattern identity. The exported response CSV contains H24 changes, and recovery_pattern_plans.json records H24 sets across the affected group. A recovery can require changes at patterns other than the absent one, so it is not a simple last-minute one-week substitution and may be unsuitable once earlier duties have already occurred.

| Group | Size | Scheduled cases | Within group | Candidate / approval | No candidate |
| --- | --- | --- | --- | --- | --- |
| 1 | 17 | 102 | 0 | 0 | 102 |
| 2 | 18 | 104 | 104 | 0 | 0 |
| 3 | 18 | 104 | 104 | 0 | 0 |
| 4 | 17 | 102 | 0 | 0 | 102 |
| 5 | 18 | 108 | 108 | 0 | 0 |
| 6 | 18 | 108 | 108 | 0 | 0 |
| 7 | 17 | 102 | 0 | 17 | 85 |

The same-group modeled recovery rate is 424/730 = 58.1%. All 306 remaining cases (41.9%) require human intervention. Of these, 17 have a historical candidate and 289 have no pre-filled candidate. The authorization template includes all 306, with approval fields left blank.

The observed exception is P0076 at nT=21 in group 7, despite a dominant group of 5. The source documents the occurrence, not its administrative reason, current availability, or authorization to replace every absent group-7 member. For the 17 corresponding cases, the candidate is added as STANDARD; when H24 is lost, the group's H24 re-optimization supplies it. 17 of these candidate schedules pass all represented constraints using the exact historical eligibility exception. This modeled check still cannot verify legal eligibility, availability, geography or authority approval. They are never counted as automatic recoveries. Within this academic project, leaving these approval fields blank is the completed representation of that boundary; filling them with invented approvals would be incorrect.

All 126 of the 126 attempted H24 recovery models are feasible. Some belong to cases where staffing still fails. H24-only feasibility is therefore not full schedule feasibility, and this result does not establish that H24 will never be a bottleneck in other absence patterns or operational settings.

The denominator is an unweighted set of pattern cases, not an estimated probability distribution of absences. A 58.1% case recovery rate is not a forecast of the fraction of real disruptions that will be manageable. Week-level, multi-absence, correlated-disruption and demand-change experiments remain unimplemented.

## 9. Explainability, oversight and accountability

Implemented explanations comprise parameter provenance, explicit model constraints, lexicographic objective order, scenario comparisons, complete pattern differences and per-event recovery details or constraint failures. They show what changes and why a stated requirement blocks a response. They do not uniquely explain why one pharmacy was selected among all alternative optima.

For example, a scheduled absence in a 17-member group leaves 16 members against the required 17. This explains a staffing failure under the assumed floor. It is not evidence that 17 is a socially sufficient service level. Similarly, a suggested cross-group candidate is historical evidence, not a permission decision.

Counterfactual re-solving (forcing a particular alternative pharmacy) and formal irreducible infeasible subsystem extraction are proposed extensions. They are not implemented or claimed as completed features. A future counterfactual service should state whether an alternative is infeasible, worsens a higher-priority objective, or is equally optimal.

Human oversight is represented by separating computed proposals from authorization. The project intentionally leaves approval fields blank and never turns a historical occurrence into an approval record. This is a complete decision-support design for the supplied evidence, rather than an unfinished effort to obtain unprovided real-world approvals. If the prototype were ever used beyond this coursework scope, responsibility for actual scheduling decisions would remain with the relevant authority.

## 10. Validation and reproducibility

| Component | Evidence | Status |
| --- | --- | --- |
| Data and implementation lineage | Stage manifests and explicit canonical/specification/optimized/robustness links verified | PASS |
| All scenario schedules | All exported schedule constraints and summary metrics checked | PASS |
| Pattern-level recovery | Every reported same-group success and historical candidate materialized and checked | PASS |
| Cross-group boundary | 306 simulated cases need a cross-group decision; no approval records are invented | DOCUMENTED MODEL OUTCOME |
| Group bound | PROVEN: no repartition of 123 pharmacies into 7 groups can raise every group above 17. If all groups must contain at least 17 members, the surplus 4 can give a spare to at most that many groups, so at least 3 groups have zero slack. The observed grouping attains this bound. Group identities are not mathematically fixed; this does not prove minimum numbers of affected weeks or absence scenarios. | PROVEN UNDER STATED ASSUMPTIONS |
| Staffing and workload thresholds | Derived from source minima/maxima and retained by explicit continuity policy | JUSTIFIED MODEL CHOICE |
| Calendar boundary | Final block ends 2027-01-03, six elapsed days after Monday start; source preserved and limitation documented | CAVEAT |
| Dataset-only scope | No geography, actual availability, demand, preferences or external rules added; excluded by project scope | SCOPE SATISFIED |
| Recovery scope | Pattern-level, one absence at a time; H24 moves may affect other patterns, total fairness is not locked | CAVEAT |

Validation has two layers. Shared cross-notebook checks verify the declared constraints, materialized rows, scenario metrics and artifact lineage. A separate audit independently reconstructs every source row, computes direct Jain and pairwise Gini, checks all three saved optimized schedules, reconstructs all 738 recovery plans and tests rejection of corrupted schedules and stale files. The audit also checks an existing-ID mapping extension on a synthetic fixture, without adding those fixture records to the analysis.

The six notebooks execute in separate Python processes using in-process IPython and save fresh text, tables and plot outputs. This runs the actual notebook cells without relying on a retained interactive kernel state. The code can also be opened in Jupyter from the project root. Browser-based Jupyter interaction and a second optimization solver are not claimed as tested. Solver statuses, objective bounds and package versions are included with the evidence.

The report body and LaTeX tables are generated from the verified notebook outputs; no result is typed independently into the final PDF. The appendix below identifies the dependencies and justifications needed to trace each result backward. The two reporting formats use one generated text and result source, avoiding separately maintained numerical claims.

Execution order from the project root:

    python -m pip install -r requirements.txt
    python run_all.py
    python audit_project.py
    python render_report.py

Python 3.12 was used. Direct dependencies are pinned in requirements.txt; the LaTeX report requires a standard TeX Live or equivalent installation, such as Overleaf's full environment. render_report.py generates the editable LaTeX sources and compiles Final_Report.pdf. Student name and email are editable metadata, not computational inputs. No repository URL or commit identifier is invented when none has been supplied.

The raw input SHA-256 is fb9557d29638f0987bf3c8bbf6726da34b3e077177062ef9b10c8ce83380f799. All empirical outputs ultimately depend on this same input. Notebook builder scripts contain synchronized cell sources and do not introduce another model. The complete archive includes the original data, executed notebooks, helper scripts, outputs, audit evidence, PDF and editable LaTeX.

## 11. Interpretation within the agreed scope

The project is a completed analysis of a single calendar under an explicit count-based model. Four boundaries matter for interpreting its results:

1. **Historical rather than externally validated thresholds.** The minimum staffing count and maximum workload are genuine CSV extrema retained by policy. Their values are justified for historical continuity, not claimed to be universal standards.
2. **Equality of counts.** The model optimizes total and H24 workload ranges. It neither estimates absent burden weights nor treats improvement in one index as improvement in all indices.
3. **Hypothetical pattern-level disruptions.** The absence scenarios are generated from observed entities and patterns; they are not records of actual absences or estimates of absence probabilities. Repeated occurrences and cross-pattern H24 moves remain explicit.
4. **Single-source evidence.** Results describe this 53-block calendar. The final six-day boundary is preserved. No claim of another year's behavior, actual authorization or unrecorded information is made.

Geography, actual availability, demand, preferences and external rules are excluded from the project by design. Their absence does not make the dataset-only submission incomplete. Similarly, 306 cases outside automatic within-group recovery are a substantive experimental result, not a requirement to invent substitute approvals. Broader operational extensions are optional future research, not conditions for completing this project.

## 12. Conclusion

The optimization formulation is appropriate for the supplied pharmacy-rotation data and the stated count-based fairness objective. It preserves the modeled historical rotation structure and staffing/H24 constraints while reducing total assignments from 931 to 923, total range from 2 to 1 and H24 range from 3 to 1.

The improvement is precise rather than universal: total Jain improves slightly, total Gini worsens slightly, and full-group is better on those two descriptive total-count indices while using more assignments. There are 11 changed complete patterns, including 2 H24-only changes. The experiment finds 424 within-group recoveries among 730 scheduled pattern cases and 306 cases requiring a cross-group decision; 17 have a historically supported, model-feasible candidate without an invented approval.

Every numerical result is either reconstructed from the supplied CSV, deterministically derived from it, computed by the stated optimization, or produced by the explicitly defined hypothetical experiment. Normative and computational choices are documented and justified. Within this dataset-only scope, the computational work and report constitute a complete, reproducible submission.

## Appendix A. Full derivation and decision trace

The distinction between data and design is not left to implicit code behavior. Notebook 02 exports the justifications below in model_specification.json and policy_justifications.csv. Notebook 03 consumes its scenario priorities; notebook 04 checks its recovery policy; notebook 05 consumes the same recommendation order. Thus a downstream notebook does not silently introduce a different objective or reinterpret a historical candidate as authorization.

| Policy | Justification |
| --- | --- |
| staffing floor | Retain the minimum observed active-pharmacy count to avoid lowering the source calendar's minimum staffing. |
| workload ceiling | Do not exceed the largest observed pharmacy workload in the same 53-block horizon. |
| weekly h24 | Preserve the uniform H24 count measured in every source block. |
| primary group eligibility | Use each pharmacy's dominant observed group to preserve the highly recurrent rotation; the observed exception is retained separately. |
| all group members can receive h24 in model | The supplied file has no capability variable. Treat service type as a reassignable decision within the inferred group; this is a symmetry assumption, not a capability observation. |
| h24 cycle bounds | Allocate each group's cycle H24 slots as evenly as integer counts permit, without introducing unobserved burden weights. |
| same nt | Reuse one decision per nT because equal nT patterns repeat exactly in the source. |
| fairness first | Prioritize total-count disparity, then H24 disparity, then assignment count as the stated ethical objective of this scenario. |
| historical stability | Break higher-objective ties by minimizing changed calendar active/H24 decisions, preserving observed continuity. |
| absence experiment | Enumerate one hypothetical absent pharmacy for each eligible pharmacy/nT pair; no absence log or probability is claimed. |
| recovery policy | Preserve staffing, cycle bounds, ceiling and attained H24 bounds; allow total range to worsen after a disruption so recovery measures feasibility rather than preservation of every optimal objective. |
| cross group boundary | Only exact observed cross-group occurrences suggest candidates; no authorization value is invented. |

| Stage | Direct input | Derivation or decision | Output used downstream |
| --- | --- | --- | --- |
| 00 | Original TURNI CSV | Parse sections/dates, normalize and pseudonymize, infer and test recurring group structure | Canonical schedule and observed profile |
| 01 | Canonical schedule | Count weekly and pharmacy workloads; measure H24, P/C, groups, repeats and exceptions | Baseline evidence and pharmacy profile |
| 02 | Canonical schedule and baseline evidence | Re-derive values; justify policies; state mathematical group bound | Model specification, parameter and policy provenance |
| 03 | Canonical schedule and model specification | Solve declared lexicographic scenarios and materialize every assignment | Three schedules, all scenario metrics, solver evidence |
| 04 | Selected schedule, canonical metadata and model specification | Generate hypothetical pharmacy/nT absences and validate recovery/candidate schedules | Response plans, group results and cross-group decision template |
| 05 | Saved schedules and verified evidence from stages 00-04 | Recompute comparisons, select by the declared rule and explain changes | Final evidence, complete report text and validation checklist |
| Audit | Original source and saved outputs | Separate source parser, independent metric/constraint calculations and regression checks | Audit evidence and correction log |
| Report build | Final verified report text and saved numeric outputs | Typeset the same evidence in the supplied LaTeX style | Editable LaTeX and compiled PDF |

## Appendix B. Optimality bounds and interpretation

### Assignment-minimizing scenario

Every one of 53 blocks requires at least 17 active pharmacies, so every feasible schedule has at least 53*17=901 assignments. Efficiency-first attains 901, proving its assignment total is minimal under the model. The subsequent range objectives are solved after fixing this assignment optimum. Their reported values are supported by the corresponding MILP certificates.

### Fairness-first total range

Groups 1 and 4 each have 17 members and eight calendar occurrences. Every member must therefore work eight times because the staffing floor equals the entire group size. Groups 5 and 6 have only seven occurrences each, so their members cannot exceed seven assignments under primary-group eligibility. Consequently, total range zero is impossible and range at least one is required. The fairness-aware schedule attains range one.

Once range one is fixed, every pharmacy must receive at least seven assignments. Groups 1 and 4 contribute 34*8=272. Groups 2 and 3 each contain 18 pharmacies and occur eight times through six distinct patterns: two occur twice and four once. Removing a pharmacy from a repeated pattern would reduce its total from eight to at most six, violating the seven-assignment minimum implied by range one. Only the four singleton patterns may omit one member each; the staffing floor prevents omitting more than one in a pattern. Each of these groups therefore contributes at least 18*8-4=140 assignments. Groups 5 and 6 together contain 36 pharmacies, and group 7 contains 17; all these 53 pharmacies must work at least seven times. Hence the fairness-first assignment lower bound is 272+2*140+53*7=923. The exported fairness-aware schedule attains it.

### H24 range

Exactly three H24 assignments per block gives 3*53=159 horizon H24 assignments. Since 159 is not divisible by 123, equal integer H24 workloads across all pharmacies are impossible. H24 range is therefore at least one; the optimized scenarios attain one. The independent counting bounds explain the leading objectives, while solver evidence covers the full lexicographic chains and their historical-stability tie-breakers.

### Meaning of the stability objective

For an eligible binary decision with m calendar occurrences and k historical presences, its Hamming-distance contribution is k + (m-2k)*decision. The constant k can be omitted by the solver. Negative signed objective values in solver_evidence.json are therefore valid and must not be read as negative numbers of changes. The report's calendar-change table computes the actual symmetric differences, including constants and the historical cross-group exception.

## Appendix C. Complete changes and robustness details

### Every changed pattern in the selected solution

| nT | Before | After | Active added | Active removed | H24 added | H24 removed |
| --- | --- | --- | --- | --- | --- | --- |
| 9 | 18 | 17 | - | P0021 | - | - |
| 10 | 18 | 17 | - | P0049 | - | - |
| 16 | 18 | 17 | - | P0020 | - | - |
| 17 | 18 | 17 | - | P0045 | - | - |
| 21 | 17 | 17 | P0111 | P0076 | P0111 | P0076 |
| 22 | 17 | 17 | - | - | P0009 | P0003 |
| 23 | 18 | 17 | - | P0029 | - | - |
| 24 | 18 | 17 | - | P0039 | - | - |
| 25 | 17 | 17 | - | - | P0057 | P0067 |
| 30 | 18 | 17 | - | P0034 | - | - |
| 31 | 18 | 17 | - | P0037 | - | - |

The nT=21 change replaces the historical cross-group row by a primary-group member under the stated eligibility policy. Patterns 22 and 25 change H24 assignments without changing active membership. The other eight active-set changes each remove one active assignment from a singleton pattern while preserving the staffing floor and total range. No new pharmacy identity is created by optimization.

### All scheduled-absence response categories

| Response category | Cases |
| --- | --- |
| h24 reoptimization within group | 48 |
| historical candidate requires approval | 17 |
| manual cross group decision required | 289 |
| same group active replacement | 112 |
| same group active replacement and h24 reoptimization | 24 |
| spare capacity absorbs absence | 240 |

### Worked response example

Consider the simulated absence of P0030 at nT=9, group 2. This pharmacy is active and H24 in the selected schedule. The same-group active replacement is P0021. The saved H24 changes are: ADD:P0018@nT=9; REMOVE:P0030@nT=9; REMOVE:P0018@nT=37; ADD:P0030@nT=37. The complete revised schedule passes staffing, H24, horizon workload, cycle-balance, absence, eligibility and repeated-pattern checks. This is an illustrative row selected from the exported response plan, not an invented event or an observation of an actual absence.

### Recovery constraints and invariants

The activity update is local to the absent nT, but H24 may be reassigned across the affected group's six patterns. For each candidate H24 assignment, a binary decision is allowed only if that pharmacy remains active at that pattern. Every group pattern retains three H24 pharmacies; each pharmacy retains its original cycle lower/upper bound and its base optimized horizon H24 interval of 1-2. Unaffected groups remain unchanged. The activity count must stay at least 17 and no pharmacy may exceed eight total assignments. The unavailable pharmacy is absent from every occurrence of the tested nT. Total workload range one is not imposed during recovery.

No same-group spare exists in a size-17 group. In a size-18 group, there is at most one spare when only 17 are active, so candidate enumeration is exhaustive for this dataset. The exported successful schedules and the reported same-group failures are independently rechecked. Cross-group cases remain separate, even when a historically evidenced candidate produces a feasible modeled schedule.

## Appendix D. Delivered artifacts and reproduction evidence

| Artifact | Purpose |
| --- | --- |
| Original CSV in data/ | Sole empirical input, retained unchanged |
| Notebooks 00-05 | Executed analysis in dependency order |
| common_metrics.py | Shared descriptive metric definitions |
| validation.py | Hard-constraint and lineage checks |
| reporting.py | Complete report assembled from verified results |
| run_all.py | Isolated execution of actual notebook code cells |
| audit_project.py | Independent reconstruction and regression checks |
| output/model_specification.json | Derived values and all justified policies |
| output/optimized_schedule_*.csv | All three materialized optimized schedules |
| output/optimization_scenario_summary.csv | Counts, fairness and stability for every scenario |
| output/solver_evidence.json | Status, objective, dual bound and gap of each main solve |
| output/single_absence_response_plan.csv | All 738 eligible pharmacy-pattern experiments |
| output/recovery_pattern_plans.json | Actionable recovery patterns and candidate information |
| output/authorized_substitutions_template.csv | All 306 cross-group cases with blank approval fields |
| output/secondary_eligibility_candidates.csv | The 17 exact-precedent candidate cases |
| output/final_project_evidence.json | Machine-readable final conclusions and lineage |
| output/stage_00_manifest.json through stage_05_manifest.json | Input, output and source hashes |
| output/audit_evidence.json | Independent validation outcomes and package versions |
| report/final_report.tex and supporting sources | Editable report in the supplied LaTeX style |
| Final_Report.pdf | Compiled complete submission report |

The scope is satisfied without another empirical dataset. The remaining editable front-matter fields identify the student; they have no effect on any result. All code and data needed to repeat the analysis are supplied in the archive.


## References

[1] European Commission High-Level Expert Group on AI (2019). Ethics guidelines for trustworthy AI. https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai

[2] Phipson, B. and Smyth, G. K. (2010). Permutation P-values Should Never Be Zero. Statistical Applications in Genetics and Molecular Biology, 9(1), Article 39. https://arxiv.org/pdf/1603.05766

[3] Jain, R., Chiu, D.-M. and Hawe, W. R. (1984). A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems. DEC-TR-301. https://www.cse.wustl.edu/~jain/papers/fairness.htm

[4] SciPy documentation. scipy.optimize.milp. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
