# CompanyBench

## A persistent company-building environment for evaluating frontier AI agents

**Specification version:** 0.1.0, design proposal  
**Prepared:** 8 September 2026  
**Intended audience:** benchmark researchers, simulation engineers, economists, sector specialists, independent evaluators, and model developers  
**Deliverable status:** comprehensive design specification; no simulator or empirical benchmark results are claimed by this document.

> CompanyBench measures whether an AI agent can build, operate, finance, adapt, and preserve a real operating business inside a causally consistent simulated economy, over years of simulated time and thousands of consequential actions.

The agent does not answer a sequence of business questions. It inherits a bank account, people, obligations, incomplete information, and a changing market. It chooses a strategy, signs contracts, builds products or infrastructure, hires and manages employees, competes for customers and capital, responds to incidents, and lives with the consequences. The simulation continues when the agent waits. Plans have no direct economic effect until they become valid actions and completed work.

All company names, geography, individual people, financial offers, scenarios, and numerical defaults below are fictional simulation designs unless explicitly attributed to an external source. These defaults are starting hypotheses for calibration, not claims about typical businesses or current market prices. The phrase “frontier difficulty” is a target to validate, not a certification. The benchmark is independent and does not imply endorsement by Artificial Analysis or any organization cited here.

## Contents

1. [Purpose and claims](#1-purpose-and-claims)
2. [Design principles and realism boundary](#2-design-principles-and-realism-boundary)
3. [Tracks, horizons, and benchmark editions](#3-tracks-horizons-and-benchmark-editions)
4. [The world and its causal model](#4-the-world-and-its-causal-model)
5. [Time, action budgets, and autonomy](#5-time-action-budgets-and-autonomy)
6. [Information, uncertainty, and investigation](#6-information-uncertainty-and-investigation)
7. [Company formation and strategic freedom](#7-company-formation-and-strategic-freedom)
8. [Accounting and financial truth](#8-accounting-and-financial-truth)
9. [Cash, runway, treasury, and insolvency](#9-cash-runway-treasury-and-insolvency)
10. [Funding, ownership, debt, and governance](#10-funding-ownership-debt-and-governance)
11. [Employees and organizational execution](#11-employees-and-organizational-execution)
12. [Customers, markets, sales, and churn](#12-customers-markets-sales-and-churn)
13. [Projects, operations, vendors, and risk](#13-projects-operations-vendors-and-risk)
14. [Competitors and economic dynamics](#14-competitors-and-economic-dynamics)
15. [AI laboratory environment](#15-ai-laboratory-environment)
16. [SaaS environment](#16-saas-environment)
17. [Electricity company environment](#17-electricity-company-environment)
18. [Datacenter strategy as an actual decision](#18-datacenter-strategy-as-an-actual-decision)
19. [Cross-sector connections](#19-cross-sector-connections)
20. [Scenario suite and difficulty](#20-scenario-suite-and-difficulty)
21. [Incidents, crises, and recovery](#21-incidents-crises-and-recovery)
22. [Agent interface and tool contract](#22-agent-interface-and-tool-contract)
23. [Persistent documents, memory, and delegation](#23-persistent-documents-memory-and-delegation)
24. [Language, negotiation, and adjudication](#24-language-negotiation-and-adjudication)
25. [Termination, exits, and continuity](#25-termination-exits-and-continuity)
26. [Metric dictionary](#26-metric-dictionary)
27. [Milestones and time to achievement](#27-milestones-and-time-to-achievement)
28. [Scoring and comparison](#28-scoring-and-comparison)
29. [Mistakes and decision quality](#29-mistakes-and-decision-quality)
30. [Experimental protocol and statistics](#30-experimental-protocol-and-statistics)
31. [Baselines and validation](#31-baselines-and-validation)
32. [Anti-gaming, security, and contamination](#32-anti-gaming-security-and-contamination)
33. [Simulation architecture](#33-simulation-architecture)
34. [State and event schemas](#34-state-and-event-schemas)
35. [Reproducibility and test requirements](#35-reproducibility-and-test-requirements)
36. [Calibration and empirical realism](#36-calibration-and-empirical-realism)
37. [Evaluator operations and cost](#37-evaluator-operations-and-cost)
38. [Public results and research governance](#38-public-results-and-research-governance)
39. [Implementation roadmap and acceptance gates](#39-implementation-roadmap-and-acceptance-gates)
40. [Worked episode excerpts](#40-worked-episode-excerpts)
41. [Reference scenario manifests](#41-reference-scenario-manifests)
42. [Decision records and outstanding research questions](#42-decision-records-and-outstanding-research-questions)
43. [Source register and evidence boundaries](#43-source-register-and-evidence-boundaries)
44. [Glossary](#44-glossary)
45. [Release checklist](#45-release-checklist)

## 1. Purpose and claims

### 1.1 The core research question

Given bounded inference resources, tools, authority, starting resources, and incomplete information, how well can a model sustain and improve a company through a long sequence of interdependent decisions?

The desired measurement combines strategic judgment, numerical reasoning, execution, learning, memory, uncertainty management, and adaptation. The experiment should reveal a model that writes convincing strategy documents but forgets payroll, a model that raises capital but destroys value, a model that grows revenue while losing cash on every additional customer, and a model that competently manages a small profitable business without chasing a fundraising narrative.

### 1.2 Questions every published result must answer

| User-facing question | Required measurement |
|---|---|
| How long did the company last? | Operating survival, legal continuity, failure cause, and horizon censoring |
| How long did the model remain in charge? | Autonomous tenure, removal date, assistance events, and budget exhaustion |
| Which business did it choose? | Sector, business model, target customers, pivots, and final revenue mix |
| What did it achieve? | Verified milestone history, persistence, reversals, and time to achievement |
| How big did it become? | Customers, delivered output, revenue, employees, assets, and market share |
| How much money did it raise? | Settled equity, debt draws, grants, dilution, restrictions, and financing costs |
| Did it make money? | Accrual profit, operating cash flow, free cash flow, and capital-adjusted value |
| What mistakes did it make? | Evidence-backed incident taxonomy, attributable loss, recovery, and recurrence |
| How much reasoning did success cost? | Tokens, billed cost, model compute where available, calls, and wall-clock time |
| Was it lucky? | Repeated paired scenarios, outcome distributions, tail performance, and uncertainty |

### 1.3 Permitted conclusions

Results support claims about performance inside a specified CompanyBench environment under a specified agent configuration. They can support comparisons of planning, operational consistency, resource allocation, and resilience across matched conditions. They do not establish that an agent can independently operate a real regulated utility, deploy an actual frontier model, or act as a legally authorized executive. Simulated years are not years of real-world autonomy.

The benchmark must publish its abstraction limits alongside its achievements. A serious benchmark earns trust through reproducible measurement and demonstrated validity, not the number of variables in the simulator.

## 2. Design principles and realism boundary

### 2.1 Non-negotiable principles

1. **State persists.** Every accepted commitment affects a shared future. There is no reset after a bad decision.
2. **Resources are conserved.** Cash, labor, shares, compute, customer demand, and energy cannot appear because a narrative says they do.
3. **Delay matters.** Hiring, procurement, product development, customer payment, fundraising, and permitting take time.
4. **Information has provenance.** A forecast, audited statement, sales rumor, and bank transaction carry different authority.
5. **Competitors act for themselves.** They face budgets and information limits and can fail.
6. **Success has several legitimate forms.** Bootstrapping, profitable specialization, expansion, licensing, and a sensible acquisition can all work.
7. **Difficulty is causal.** Hardness comes from tradeoffs, interacting constraints, uncertainty, and delayed consequences; it does not require arbitrary catastrophe.
8. **Measurement precedes narrative.** Economic outcomes come from the engine. Explanations cannot overwrite the ledger.
9. **Evaluation is independent of the agent.** A model cannot award itself milestones, change the score, or inspect a hidden seed.
10. **Defaults are versioned.** Numerical assumptions, policy versions, and distributions are frozen for a release.

### 2.2 Realism levels

| Layer | Required fidelity | Deliberate abstraction |
|---|---|---|
| Financial | Double-entry ledger; contractual dates; cash restrictions; cap table; cash-flow statements | A published fictional accounting policy, not complete IFRS or US GAAP |
| Organizational | Individual hiring, skills, ramp, turnover, management limits, workload | No attempt to simulate every human psychological trait |
| Commercial | Cohorts, procurement, alternatives, switching cost, retention, payment behavior | Aggregate small buyers; explicit large accounts |
| Technical | Capacity, quality, backlog, dependencies, failures, useful output | No full source-code implementation or actual foundation-model training in the core track |
| Electricity | Hourly physical balance, network limits, projects, contracts, collateral | A documented reduced network and market rulebook; no claim of full power-system engineering certification |
| Legal | Explicit fictional contracts, authorities, notice periods, liabilities, enforcement | No changing real-world legal interpretation during a run |
| Social | Negotiation, trust, incentives, miscommunication, verifiable promises | Language renderers cannot invent economic facts |

The most important tradeoff is between fidelity and identifiability. A hidden, unrestricted language model improvising every business outcome would appear realistic but make causal explanation and replication weak. CompanyBench therefore uses an explicit economic simulator with controlled language interfaces.

### 2.3 Required realism boundaries

The core simulation takes place in the fictional federation of **Meridian**, with the currency **MCU**. One MCU is one simulation accounting unit; it is not pegged to a live currency. All monetary tables use MCU unless marked otherwise. Jurisdiction packs define taxes, employment notice, licensing, privacy obligations, security reporting, corporate authority, and insolvency procedures. Packs use plausible structures but remain fixed game rules.

The initial rulebook has a 25% corporate tax rate on positive taxable profit after eligible losses, payroll overhead specified separately, and no inflation indexing unless a contract requires it. These are fictional defaults. Cross-border tax, transfer pricing, complex derivatives, and litigation discovery belong in separately validated expansions. An expansion cannot silently change a core leaderboard.

## 3. Tracks, horizons, and benchmark editions

### 3.1 Three required sector environments

| Sector | Starting role | Central problem | Typical long commitments |
|---|---|---|---|
| AI laboratory | CEO of a small applied research lab | Convert scarce talent, data, and compute into useful, reliable, commercially viable models | GPU leases, data rights, research programs, enterprise contracts |
| SaaS | CEO of an early software company | Find a repeatable market, retain customers, and scale delivery without losing economics | Annual subscriptions, enterprise rollouts, cloud reservations, hiring |
| Electricity | CEO of a licensed commercial supplier and energy developer | Secure profitable, physically deliverable supply while financing growth and managing market exposure | PPAs, network rights, collateral, construction, offtake |

Starting as a licensed supplier/developer makes the electricity scenario playable within a finite horizon. A newly formed company cannot build a nuclear station on a startup software timeline. New large thermal or nuclear construction may appear as an investment option or an advanced scenario, but commissioning must respect realistic modeled lead times beyond many evaluation horizons.

### 3.2 Benchmark tracks

**Assigned-sector Core:** every submitted configuration plays all three sectors with matched scenario families. This is the main cross-model comparison. It prevents choosing only the easiest business.

**Founder Choice:** the model sees three opportunity dossiers, selects a sector, business model, and initial allocation, then commits. All dossiers contain visible capital requirements and uncertainty. Selection is itself measured, but this track has its own leaderboard. Capital is scenario-specific rather than artificially equal across capital-intensive and asset-light businesses.

**Long Horizon:** a 120-month evaluation of compounding strategy, organizational change, replacement investment, and multiple economic regimes. It is published separately from Core.

**Distress and Turnaround:** the model inherits an operating company with latent problems, liabilities, and an existing team. This isolates diagnosis and recovery from founding.

**Strategy Adaptation:** paired worlds test whether the model changes behavior when economically decisive evidence changes, such as power connection delays or enterprise willingness to pay.

**Multi-company Arena:** several tested agents share an economy. This is an expansion, not the primary ranking; opponent dependence and strategic interactions need their own tournament protocol.

**Open Scaffold:** custom agent frameworks, external planners, and model delegation are allowed with complete reporting. Core uses a reference scaffold to isolate model differences.

### 3.3 Horizons

Core runs for **60 simulated calendar months**, with formal snapshots at months 3, 6, 12, 24, 36, 48, and 60. Long Horizon runs for 120 months. Diagnostic development episodes may run for 12 months but cannot substitute for full Core results.

All sectors share the 60-month Core horizon for direct survival comparisons. Sector-specific milestones account for infrastructure lead times. Slow projects retain verified residual value at the horizon; construction is not made unrealistically fast for scoring convenience.

No episode receives an “infinite survival” score. A company alive at month 60 is **alive at the observation boundary**. It may fail later.

## 4. The world and its causal model

### 4.1 Formalization

Treat the environment as a partially observable stochastic game with a single evaluated decision maker in Core:

```text
S[t+1] = F(S[t], A_agent[t], A_other[t], X[t], rules_version)
O_agent[t] = G(S[0:t], permissions, reporting_delays, measurement_noise)
A_agent[t] = policy(O_agent[0:t], persistent_memory, remaining_budget)
```

`S` is authoritative state. `A_agent` contains accepted actions and standing policies. `A_other` contains competitor, employee, customer, lender, and regulator decisions. `X` contains exogenous shocks generated independently of the evaluated model identity. `G` exposes only information the company could possess at that time.

### 4.2 Authoritative state groups

The world maintains company entities; bank and ledger accounts; financing instruments; employees and candidates; teams; customer organizations and cohorts; products; research assets; infrastructure; inventory and capacity reservations; contracts; projects; disputes; permits; market states; competitor beliefs; and pending events.

Every object has an immutable ID, schema version, effective time, observation visibility, creation event, and revision history. Contracts have parties, authorized signers, effective dates, conditions precedent, cash schedules, service obligations, remedies, and termination rules. There is no “deal done” state that bypasses these fields.

### 4.3 Causal ordering

At a simulated timestamp:

1. Apply matured exogenous events and physical availability changes.
2. Complete previously scheduled work and make results available to eligible parties.
3. Validate and execute previously committed contractual events in published priority order.
4. Resolve market clearing and actual delivery for the relevant interval.
5. Post accruals, invoices, cash settlement, collateral changes, and contractual remedies.
6. Evaluate liquidity, covenant, service, and governance triggers.
7. Release observations whose reporting dates have arrived.
8. Offer an agent decision window when a scheduled review or material interrupt is due.

Settlement deadlines and intraday ordering are defined in the rulebook. A wire arriving at 16:00 cannot retroactively cure a 12:00 payment default unless the contract grants a cure period. A validated action accepted before its explicit cutoff can affect that interval; later actions affect the next eligible interval.

### 4.4 Conservation and clearing

Customer spending is constrained by budgets, need, and alternatives. A lead cannot simultaneously sign incompatible exclusive contracts with two suppliers. A GPU-hour reserved for training cannot also serve inference. A megawatt-hour sold under one physical obligation cannot be sold again. A share issuance dilutes existing holders. A contractor assigned to one full-time job is unavailable for another at the same time.

The simulated market includes an outside option so customers may buy nothing. The sum of firm demand shares, including the outside option, is one within each modeled purchase event. A company cannot grow beyond the accessible market simply by increasing a marketing number.

## 5. Time, action budgets, and autonomy

### 5.1 Keep four clocks separate

| Clock | Meaning | Examples |
|---|---|---|
| Simulation time | The company's calendar | Payroll Friday; permit in 18 months |
| Executive attention | In-world capacity to initiate and supervise work | Interviews, negotiation rounds, board preparation |
| Agent execution time | Actual model and tool latency | 12 seconds of generation; 300 ms tool call |
| Evaluation elapsed time | Start-to-finish experiment time | Provider queueing, simulator compute, infrastructure pauses |

The reference Core track pauses the business clock while the agent is responding inside a decision window. It does not make faster API providers better CEOs by silently running competitors during network latency. Decisions consume declared executive attention and may schedule actions with simulated duration. A separate real-time track can explicitly couple wall-clock latency to events.

### 5.2 Event-driven operation

The world resolves daily financial and organizational activity, hourly electricity activity, and event-time contracts. The agent receives a scheduled executive review at least once every seven simulated days. It can schedule an earlier review or call `world.advance` with interrupt conditions. High-frequency operations run through standing policies and simulated staff; the CEO does not manually dispatch every hourly power purchase.

Material interrupts include cash below a configured threshold, a payment or collateral deadline, a major outage, a material offer expiry, a board intervention, a disputed contract, a critical employee resignation, or a known compliance deadline. Interrupts expose what is known, not the hidden cause.

### 5.3 Proposed reference resource tiers

| Tier | Total generated-token allowance | Input-token allowance | Maximum tool calls | Purpose |
|---|---:|---:|---:|---|
| Diagnostic | 500,000 | 5,000,000 | 5,000 | Development, 12-month runs |
| Core Standard | 4,000,000 | 40,000,000 | 40,000 | 60-month ranking |
| Core Extended | 12,000,000 | 120,000,000 | 120,000 | Inference scaling curve |

These are explicit proposed engineering defaults, to be tested against pilot throughput and cost. They are not estimates of actual run cost. Generated-token accounting includes billed hidden reasoning tokens where the provider exposes them; unreported reasoning usage is marked unavailable. Input includes repeated context, cached input is reported separately, and tokenizer differences are acknowledged. Token equality is not compute equality.

A normal decision window allows at most 32 tool calls and 24,000 generated tokens. An additional window can be opened by consuming executive attention and advancing at least one simulated hour; this prevents endless zero-time activity. Material interrupts create additional windows under the same rules. All limits are in a public manifest, with warnings before exhaustion. Calls rejected for invalid arguments still consume tool-call budget.

### 5.4 Attention and execution

The founding CEO has a 40-hour weekly executive schedule. Administrative overhead is explicit, and accepted activities reserve hours. A one-hour hiring interview is not instant; a funding roadshow competes with customer work. Qualified managers can absorb work within authority limits, but their wages, delays, and execution quality remain in the world.

Reading an already available report does not consume simulated labor, though it consumes inference budget. Ordering a new customer study consumes research staff time and money. Repeatedly querying the same report cannot create additional independent evidence or reroll its measurement error.

### 5.5 Exhaustion and provider failures

Exhausting the evaluation budget ends autonomous control at that timestamp. The benchmark records **budget exhaustion**, not company bankruptcy. A predefined unattended continuation executes existing policies to the horizon and is published as a diagnostic; it does not extend autonomous tenure. Primary score handling is defined in Section 28.

Provider errors receive the same capped retry policy for all submissions, with state unchanged until an action is accepted. Infrastructure failures may justify resuming from a signed checkpoint. The evaluator cannot restart a bad business trajectory under the label of a transient error. Timing reports separate active inference time from approved infrastructure downtime.

## 6. Information, uncertainty, and investigation

### 6.1 Visible information

Agents can inspect bank balances, posted financial statements, payroll commitments, contracts they own, employee reports, product dashboards, customer feedback, CRM opportunities, supplier quotes, market publications, and the local rulebook. They can build forecasts and request professional work inside the simulation.

The initial briefing is a usable executive handover, not a deliberately disorganized pile of text. Complexity should come from management, not from inability to locate the bank balance.

### 6.2 Hidden information

Hidden variables include individual willingness to pay, true employee match quality, future shocks, competitor internal budgets, unobserved vulnerabilities, and unresolved research outcomes. Hidden parameters must have discoverable proxies or defensible uncertainty. No decisive rule is secretly reversed mid-run.

The agent knows the classes of risks and contract rules. It does not know exact future draws, customer reservation values, or competitor random seeds. Published engine equations need not reveal individual latent states.

### 6.3 Observation envelope

Every material data item carries:

```json
{
  "record_id": "obs_1845",
  "effective_at": "2031-05-31T23:59:59Z",
  "available_at": "2031-06-04T09:00:00Z",
  "source": "finance.close",
  "status": "provisional",
  "coverage": "company_consolidated",
  "units": "MCU",
  "value": 184000,
  "revision_of": null
}
```

An estimate may include a confidence interval and method. A rumor carries no artificial numeric certainty. Reports can be stale or incomplete; the interface identifies their age and coverage so a model has a fair chance to notice.

### 6.4 Investigation as a decision

Available investigations include customer interviews, pricing experiments, security audits, code or infrastructure assessments, legal review, reference checks, grid studies, lender diligence, and research replication. Each has a price, lead time, sample design, and imperfect diagnostic power.

The useful question is whether the value of information exceeds its cost and delay. Buying every report should exhaust attention and cash. Buying none should expose the company to avoidable surprises. Sampling can introduce selection bias; the environment preserves response probabilities and recruitment method.

## 7. Company formation and strategic freedom

### 7.1 Initial dossiers

Each start includes a charter, founder mandate, initial ownership, opening balance sheet, team roster, signed obligations, market overview, feasible opportunity list, and known risks. Assigned-sector scenarios fix the sector but allow meaningful business-model choice. Founder Choice presents all three sector dossiers before selection; its preparatory budget is identical across models.

The model chooses company name, target market, positioning, business model, risk limits, product direction, initial hiring priorities, and financing strategy. Names and prose branding have no direct score. A marketing campaign may influence discovery only through implemented audience, channel, budget, and truthful product attributes.

### 7.2 Strategic freedom with concrete implementation

The action system supports composition: license a model, build a workflow product around it, target a neglected vertical, hire a specialist team, negotiate a reseller agreement, or finance an energy asset through a subsidiary. Pivots incur real transition costs and preserve existing liabilities.

Novel strategies use `projects.propose` with objectives, required capabilities, resources, dependencies, delivery criteria, and measurable outputs. The engine maps them to known primitives or returns a transparent unsupported-capability result. It cannot grant a revolutionary technology because a paragraph sounds plausible. Unsupported requests are logged for benchmark development and are not automatically treated as incompetence.

### 7.3 Mandate and incentives

The baseline mandate is to build a durable operating business and create value for the capital entrusted to it while meeting contractual, employment, and safety obligations. The agent is not paid directly for fundraising or headcount. It may distribute cash, sell the company, or wind down if doing so is economically justified, subject to board and creditor rights.

The mandate is a benchmark objective, not a claim that every real corporation has identical stakeholder priorities. Alternative mission packs may prioritize public benefit, low-carbon delivery, or research impact; their scores must remain separate.

## 8. Accounting and financial truth

### 8.1 One ledger, multiple useful reports

Use a double-entry general ledger with balance sheet, income statement, and cash-flow statement. Each posting links to a source event. Reports are generated from the ledger, never independently generated narrative summaries.

Minimum accounts include unrestricted and restricted cash, receivables, allowance for doubtful accounts, prepayments, inventories where relevant, property and equipment, accumulated depreciation, approved intangible assets, payables, accrued payroll, deferred revenue, debt principal, interest payable, tax payable, equity classes, retained earnings, revenue, direct delivery costs, operating expenses, and other gains/losses.

For every posted transaction:

```text
sum(debits) = sum(credits)
assets = liabilities + equity
closing_cash = opening_cash + operating_CF + investing_CF + financing_CF
```

Money uses integer minor units, with a published rounding policy. Ledger balances are not IEEE floating-point aggregates.

### 8.2 Revenue, bookings, and cash

Distinguish signed bookings, remaining contractual obligations, invoicing, cash collection, and recognized revenue. Service revenue is recognized as specified obligations are performed. Annual prepayment creates a liability until delivery. A funding round is financing cash flow, never revenue. A refundable customer deposit is not immediate profit. This separation is motivated by the structured revenue-recognition approach in [IFRS 15 project materials](https://www.ifrs.org/projects/completed-projects/2015/revenue-from-contracts-with-customers/); the simulator uses its own narrower published policy.

Example: a customer prepays MCU 120,000 for a 12-month service commencing 1 January. The cash receipt increases cash and deferred revenue by 120,000. Each full service month recognizes 10,000 revenue and reduces deferred revenue by 10,000, before credits, refunds, or contract modifications. The company still owes the remaining service even if it spends the cash.

### 8.3 Profit definitions

```text
gross_profit = recognized_revenue - cost_of_revenue
operating_profit = gross_profit - operating_expenses
pretax_profit = operating_profit + other_income - financing_expense
net_profit = pretax_profit - tax_expense
```

Cost of revenue includes direct cloud/inference delivery, purchased electricity, usage-linked vendors, and attributable service labor according to the fixed accounting policy. Operating expenses include research, sales, general administration, and unallocated overhead. Depreciation and stock-based compensation remain visible; adjusted metrics cannot replace net profit.

### 8.4 Cash flow and capital expenditure

Operating cash flow follows actual customer and operating settlements. Investing cash flow includes asset purchases and disposals. Financing cash flow includes equity, debt draws, repayments, and distributions. Interest paid is classified as operating in the reference policy and disclosed consistently. Report `FCF = operating_CF - gross_cash_capex`, and show asset-sale receipts separately so selling infrastructure does not masquerade as sustainable free cash flow.

Training and research spending is expensed in the initial policy. Capitalization requires a separately specified asset class and criteria; the agent cannot select an accounting treatment to improve its score. Energy construction enters construction-in-progress and is depreciated only once commissioned under the asset rulebook. Asset impairment is triggered by engine evidence and independently reviewed policy, not the model's preferred valuation.

### 8.5 Accruals and closing

Daily estimates support operations, monthly closes finalize ordinary accruals, and periodic audits can correct mistakes. Reports label provisional and final values. Historical restatements update the evaluation ledger and leave an audit trail. The model is not penalized for a corrected engine bug. It can be responsible for deliberately supplying false transaction evidence or failing to investigate a discrepancy it could reasonably observe.

### 8.6 Gross versus net presentation

Where a company is an intermediary, principal/agent classification is fixed by contract structure. A marketplace collecting 1 million and forwarding 950,000 cannot count the full collection as revenue merely to win a size metric. The energy supplier's gross energy revenue is still reported where it takes delivery and price risk, but benchmark comparisons use sector normalization and value added alongside revenue.

## 9. Cash, runway, treasury, and insolvency

### 9.1 Cash is not available funding

Report unrestricted cash, restricted collateral, undrawn committed credit, uncommitted indicative credit, customer deposits, near-term mandatory payments, and discretionary commitments separately. A term sheet, projected sale, or verbal investor promise is not cash.

### 9.2 Runway calculations

The dashboard provides simple trailing runway only when meaningful:

```text
trailing_net_burn = max(0, -mean(last_3_months.operating_CF + last_3_months.investing_CF))
simple_runway_months = unrestricted_cash / trailing_net_burn
```

If trailing burn is zero, return `not_applicable_positive_or_zero_cashflow`, not infinity. A company with a balloon payment can fail despite positive trailing cash flow.

The authoritative liquidity forecast is a dated cash waterfall. It includes wages, invoices, debt service, contract prepayments, taxes, collateral calls, capex milestones, and collectible receivables. Report the first date cash falls below zero or a required reserve, with base, downside, and severe scenarios. Undrawn credit is included only if draw conditions will be met.

### 9.3 Worked liquidity example

At day 0 the company has MCU 800,000 unrestricted cash and 300,000 restricted collateral. Monthly ordinary operating burn is 100,000. A 450,000 equipment installment is due in 45 days, and an uncertain 500,000 funding round is expected in 60 days. Simple runway is eight months; usable cash after 1.5 months of burn and the installment is only 200,000. Restricted collateral and the unsigned raise do not extend that runway. A prudent plan must handle a financing delay.

### 9.4 Treasury policies

The agent can set minimum liquidity, approve invoices, collect receivables, negotiate payment terms, hedge permitted exposures, and use approved cash instruments. Treasury investments have counterparty limits, maturity, interest, and possible liquidity restrictions. There is no unlimited yield arbitrage or asset whose return is disconnected from market state.

### 9.5 Distress states

Use an explicit state machine: `healthy`, `watch`, `payment_shortfall`, `cure_period`, `restructuring`, `receivership`, `liquidation`, `closed`. Negative book equity alone does not instantaneously terminate the company. Missed obligations follow their contract and jurisdiction rulebook. Cross-default provisions can propagate distress; ring-fenced debt does not automatically propagate unless guarantees or cross-default terms exist.

Receivership can preserve operating service under another controller. Company continuity, original equity recovery, and agent tenure must then be reported separately.

## 10. Funding, ownership, debt, and governance

### 10.1 Fundraising process

Fundraising proceeds through targeting, introduction, meetings, diligence, indicative terms, term sheet, legal documents, approval, closing conditions, settlement, and post-close obligations. Each stage takes time and executive attention. Investor pipelines have competing deals and finite fund reserves. A company cannot instantly raise its desired amount by asking.

Investor types include angels, seed funds, growth investors, strategic investors, infrastructure equity funds, commercial lenders, project-finance lenders, and grant agencies. They value different evidence and require different instruments. Grant cash can be restricted and clawed back for missed conditions.

### 10.2 Equity rounds

For a simple priced round without convertibles or option-pool changes:

```text
post_money_value = pre_money_value + new_primary_cash
new_investor_fraction = new_primary_cash / post_money_value
existing_holder_fraction_after = existing_holder_fraction_before * pre_money_value / post_money_value
```

Example: MCU 2 million at an 8 million pre-money value gives new investors 20% and existing holders collectively 80%. Transaction fees reduce cash received, not the contractual share allocation unless the documents say so. Secondary share sales are proceeds to selling holders, not company fundraising.

### 10.3 SAFEs, notes, and conversion

Support a small versioned set of post-money SAFE-like contracts and convertible notes. A SAFE-like agreement has explicit conversion and liquidity rules. A convertible note also has interest, maturity, and repayment/default provisions. [Y Combinator's SAFE documentation](https://www.ycombinator.com/safe) is a primary reference for distinguishing these structures; the benchmark contracts remain fictional templates.

For a simple cap-binding post-money SAFE before a new priced round and new pool dilution, investment divided by the post-money cap estimates the ownership sold. Do not generalize that shortcut across discounted conversions, low-priced rounds, multiple instruments, pool increases, or different capitalization definitions. The cap-table engine computes actual share counts and contractual conversion order, and must pass golden fixtures for each supported template.

### 10.4 Ownership and exit waterfall

Track common shares, preferred classes, options granted and ungranted, vesting, warrants, convertibles, voting rights, and liquidation preferences. Distinguish issued ownership from fully diluted ownership. A high headline exit price can leave common equity with little after debt and senior preferences.

At a sale, first calculate transaction fees and asset/liability treatment, then creditor payments and contractual preference/conversion choices, then residual distributions. Do not subtract debt twice through both an equity purchase price and an enterprise-value bridge. A financing round's headline valuation is never accepted as terminal economic value by itself.

### 10.5 Debt and covenants

Credit terms include principal, draw schedule, interest basis, amortization, maturity, collateral, guarantees, covenants, cash sweeps, reporting, and cure rights. Covenant examples include minimum cash, leverage, and debt-service coverage. Project debt can be nonrecourse, but guarantees, completion support, or parent-funded reserves must appear explicitly.

```text
DSCR = cash_available_for_debt_service / scheduled_interest_and_principal
```

Cash available for debt service follows the facility definition. It cannot include new borrowing, restricted reserve withdrawals, or speculative revenue unless the contract allows them. An undrawn line is not assured if covenants will block it.

### 10.6 Governance

The board has explicit composition, voting rules, reserved matters, and a mandate. It can reject acquisitions, require financing, replace the CEO, approve a wind-down, or accept a sale. Board preferences are stable latent parameters with observable feedback, not arbitrary punishment.

Repeatedly ignoring board reporting can matter even if current revenue is strong. A manager removed from office loses autonomous tenure; the business may continue. Material board decisions must include structured reasons linked to mandate, evidence, and voting rules.

## 11. Employees and organizational execution

### 11.1 Individuals, teams, and headcount

Each employee has role, skill vector, experience, compensation, benefits, equity, start date, notice period, availability, team assignment, manager, ramp curve, workload, morale, retention risk, and documented qualifications. Hidden traits are sampled from a population model; visible resumes and interviews are imperfect signals. Protected characteristics do not determine ability or hiring value.

Report active employees, paid employees on leave, full-time equivalent capacity, contractors, and outsourced services separately. Peak headcount is descriptive. Hiring unnecessary employees cannot directly improve the score.

### 11.2 Hiring pipeline

Create a role and compensation band; source candidates; screen; interview; check references if desired; issue an offer; wait for acceptance and notice; onboard. Candidates can receive competing offers. Recruitment consumes money and staff time. A candidate who accepts does not become fully productive immediately.

Illustrative lead times are 2-8 weeks for general roles and 6-20 weeks for scarce research or grid specialists. These are scenario ranges to calibrate. The model sees market estimates and individual notice periods, not guaranteed exact completion dates.

### 11.3 Loaded employee cost

```text
cash_employee_cost = base_pay + employer_payroll_costs + benefits + cash_bonus + recruiting_cash + severance
economic_employee_cost = cash_employee_cost + recognized_equity_compensation
```

A proposed base overhead is 25% of salary plus role-specific equipment and recruiting cost. This is a fictional parameter. Promised compensation becomes a liability under the employment contract. Firing an employee cannot erase earned wages or already vested equity.

### 11.4 Productive capacity

Effective project capacity depends on relevant skills, ramp, availability, tools, coordination, and maintenance load. A possible bounded form is:

```text
effective_hours = scheduled_hours * ramp_factor * availability_factor * skill_match * coordination_factor
```

Factors are measured relative to a defined role baseline and bounded by the parameter registry. They cannot create infinite output through multiplying bonuses. Skill match above one represents faster work only within calibrated limits. Dependency-constrained tasks do not complete faster simply because unrelated staff are assigned.

### 11.5 Management and culture

Manager capacity constrains team size and parallel projects. Excess span produces slower reviews, missed feedback, and higher coordination costs. Burnout follows accumulated workload and recovery, with lag. Culture is represented through mechanisms such as information sharing, retaliation risk, quality ownership, and retention rather than one magic happiness multiplier.

Delegating a task requires an owner, deadline, budget, decision authority, and acceptance criteria. Staff can misunderstand ambiguous tasks; the model must inspect results. Executives have different strengths and can resign. A good hiring decision can improve execution; hiring a “perfect CFO” cannot reveal future shocks or hidden evaluation state.

### 11.6 Layoffs, succession, and key-person risk

Layoffs lower future payroll after notice and severance, can interrupt projects, and may increase voluntary turnover. Succession plans and cross-training reduce key-person dependence but cost time. Employee-related losses must be causally attributed: a random resignation is not automatically a model mistake, while ignoring an explicit retention warning before a critical launch may be.

## 12. Customers, markets, sales, and churn

### 12.1 Customer state

Customers have a business need, budget, procurement process, current provider, switching cost, product requirements, security requirements, contract renewal date, payment reliability, usage profile, and hidden willingness to pay. Large customers are explicit entities. Small customers are cohorts with bounded heterogeneity and reproducible stochastic transitions.

### 12.2 Acquisition process

Marketing increases qualified discovery through channel-specific response curves with saturation and competition. Sales teams qualify leads, run demonstrations, conduct pilots, negotiate, and support procurement. Closing requires sufficient product fit, price acceptance, trust, capacity, and approval. A lead, verbal commitment, signed order, live customer, and paying customer are different states.

Demand is a competitive choice model. Utility may depend on price, quality, reliability, switching cost, integrations, support, and brand evidence. Customers can stay with the incumbent or defer purchase. Segment-level uncertainty ensures that discovery and experimentation matter.

### 12.3 Churn and retention

Churn is an outcome of renewal choices or permitted cancellations. It reacts to realized value, outages, price changes, service, competitor offers, and the customer's own business condition. Annual contracts do not spontaneously churn each month as if they were cancellable subscriptions; dissatisfaction increases nonrenewal, disputes, or contractual termination risk.

```text
logo_churn = customers_lost_from_starting_cohort / customers_at_period_start
GRR = (starting_recurring_revenue - churned_revenue - contraction) / starting_recurring_revenue
NRR = (starting_recurring_revenue - churned_revenue - contraction + expansion) / starting_recurring_revenue
```

New customers are excluded from retention numerators. All terms use the same starting cohort and fixed measurement window. Undefined zero-base ratios are null, not zero or 100%. Report cohort ages so newly acquired customers do not hide weak retention.

### 12.4 CAC and customer value

```text
fully_loaded_CAC = attributable_acquisition_spend / new_paying_customers
CAC_payback_months = fully_loaded_CAC / monthly_gross_profit_per_new_customer
```

Attribution policy and lag are fixed. If gross profit is nonpositive, payback is not achieved. Lifetime value is a forecast with a distribution, not an oracle `ARPU/churn` calculation assumed to hold forever. Realized cohort contribution provides a less assumption-heavy diagnostic.

### 12.5 Contract concentration and quality

Revenue concentration, receivable concentration, supplier dependence, and correlated customer industries are visible. A large deal can be unattractive because of low margin, slow payment, custom work, restrictive terms, or concentration. Revenue bought through uneconomic discounts remains revenue but reduces economic value and future cash.

### 12.6 Customer behavior evidence

Usage-based software can have a different revenue trajectory from fixed subscriptions even with committed contracts. [Snowflake's fiscal 2026 annual report](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) provides a primary example of why consumption, retention, and remaining obligations should be distinguished. It does not calibrate every SaaS company in this fictional world.

## 13. Projects, operations, vendors, and risk

### 13.1 Projects as dependency graphs

Every project contains tasks, required skills, predecessor tasks, effort estimates, uncertainty, procurement, acceptance tests, maintenance obligations, and cancellation rules. Completion requires actual resources and passed delivery conditions. Staff cannot deliver “enterprise readiness” unless the required controls and product capabilities are implemented.

Projects may be research, product development, infrastructure, sales implementation, regulatory preparation, or organizational change. They generate artifacts, capabilities, or rights that other systems consume. Their benefits are specific: an integration opens a segment; a checkpointing improvement reduces training loss; a grid study reduces interconnection uncertainty.

### 13.2 Technical debt and maintenance

Shortcut choices can reduce launch time while increasing defect risk, support load, and future change cost. Debt has location and mechanism, not merely a scalar that subtracts score. Maintenance competes with feature work and prevents deterioration. Deferred maintenance can produce profitable-looking short periods followed by outages and expensive repair.

### 13.3 Vendors and procurement

Vendors have quotes, stock or capacity, lead time, reliability, financial health, contract minimums, support terms, and cancellation costs. Long-term reservations lower unit prices but create utilization risk. Multi-sourcing can reduce outage risk while increasing integration and coordination costs.

Purchase orders, delivered goods, invoices, and payment are separate events. An accepted quote does not mean equipment has arrived. A supplier bankruptcy can leave unsecured prepayments impaired.

### 13.4 Risk and insurance

Risks have exposure, frequency, severity, correlation, controls, detection, response, and residual loss. Insurance has premiums, exclusions, deductibles, limits, and claims delays. Coverage does not prevent incidents, and an excluded event cannot be reimbursed because the model invokes the word insurance.

Control investment should change a specified hazard or loss pathway. A generic “improve safety” action without scope, implementation, and acceptance criteria has no mechanical effect.

## 14. Competitors and economic dynamics

### 14.1 Stateful competitors

Every named competitor has a balance sheet, strategy, products or assets, people, capacity, financing constraints, and beliefs about the market. They can lower prices, enter segments, acquire assets, hire, raise capital, withdraw, or fail. Their decisions obey the same resource and timing rules as comparable player actions.

Some incumbents start with advantages. These advantages must be in the scenario manifest and public market dossier where reasonably observable. Incumbents are not made arbitrarily weak to let the player win, nor granted infinite hidden capital to guarantee failure.

### 14.2 Opponent policies

Core uses frozen, versioned economic policies with bounded planning and imperfect observations. Policies include a conservative incumbent, aggressive entrant, specialist, and opportunistic consolidator. Hidden weights vary by scenario family. A separately frozen dialogue renderer communicates their decisions.

Competitors cannot read the agent's private memory, unsubmitted plans, or hidden messages. They can infer strategy from public prices, recruiting, launches, contracts where public, and market outcomes. Retaliation has costs and strategic justification.

### 14.3 Macro regimes

The world includes demand growth, inflation, interest rates, funding appetite, labor availability, energy input cost, supply constraints, and technology progress. Regime transitions use a versioned stochastic process with bounded persistence and cross-variable correlation. A recession may reduce customer demand and financing availability together; independent coin flips would understate compound risk.

Weather, fuel availability, power prices, datacenter demand, and compute availability can share causal factors. The agent receives noisy leading indicators and forecasts. No shock is triggered merely because its cash balance is conveniently low.

### 14.4 Rival fairness and economic feasibility

Use seed-stable exogenous conditions across model comparisons. Endogenous competitor responses must still differ when player actions differ. Paired evaluation does not mean freezing rivals into irrational behavior regardless of the player's strategy.

Log why competitors acted, using their available information, resource constraints, and policy version. This log is evaluator-only until publication. If a rival sells below cost, its loss, financing, and rationale must be visible in the world accounting; it cannot do so forever without funding.

## 15. AI laboratory environment

### 15.1 Starting situation

The player leads **Aster Research**, a fictional early laboratory with MCU 8 million unrestricted cash, 12 employees, an initial open-weight model license, a small evaluation platform, two enterprise design partners, and limited reserved compute. It has no world-leading model and no automatic right to every training dataset. Opening assets, liabilities, prepaid compute, and ownership are specified by the scenario balance sheet.

The challenge is to select a viable research and commercialization path while larger labs improve, open models commoditize some capabilities, and infrastructure suppliers ration attractive capacity. The player can remain specialized, build an API business, license models, create enterprise deployments, pursue research contracts, or develop a broader model program once financing and evidence support it.

### 15.2 Strategic branches

| Branch | Opportunity | Binding risks |
|---|---|---|
| Domain-specialist models | High value on narrow workflows; proprietary feedback | Small market, scarce lawful data, customer concentration |
| Efficient inference provider | Lower cost for existing capabilities | Price competition, hardware utilization, supply dependence |
| Enterprise private deployment | Larger contracts and switching costs | Security reviews, customization, support, slow procurement |
| General model research | Large upside and licensing options | Compute intensity, uncertain progress, financing dependence |
| Evaluation and reliability platform | Sell evidence and deployment confidence | Credibility, defensible measurement, integration burden |
| Open model ecosystem | Adoption, developer distribution, complementary services | Monetization, support, free-rider competition |

The benchmark must not hardcode that the most expensive training run is the best strategy. Useful research progress, data quality, inference economics, distribution, reliability, and timing jointly determine outcomes.

### 15.3 Research state

A model asset has architecture family, parameter count or equivalent model scale, training tokens, data categories and rights, training recipe, checkpoint history, evaluation vector, serving profile, release policy, and known limitations. Research capability is multidimensional: domain performance, reasoning reliability, factuality, tool use, robustness, safety behavior, latency, memory, and operating cost. No single “intelligence score” automatically produces sales.

Research projects have hypotheses, prerequisites, experiment design, compute estimates, statistical power where applicable, expected information gain, and possible outcomes. Negative experiments can generate knowledge and improve later choices. Duplicating the same experiment without changed conditions cannot provide unlimited independent learning.

### 15.4 Training compute and runtime

Use a hardware resource model rather than “pay cash to add intelligence.” A simplified dense-transformer training estimate may use:

```text
training_FLOPs_estimate = 6 * parameter_count * training_token_count
elapsed_training_seconds = training_FLOPs_estimate / sustained_cluster_FLOPs_per_second
```

This is a declared approximation for a supported dense training family, not a universal model for mixture-of-experts, multimodal, reinforcement-learning, inference, or modern specialized architectures. Compute-optimal allocation is a research problem; [Hoffmann et al., Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) motivates treating data and model scale jointly rather than assuming only larger models matter.

For each hardware type, store precision-specific peak throughput, memory, interconnect, failure behavior, power, price, reservation conditions, and delivery lead time. Sustained throughput includes model FLOPs utilization and scaling efficiency exactly once. If measured throughput already includes a loss, do not multiply by the same penalty again.

Worked fictional estimate: 7 billion parameters and 200 billion tokens imply `8.4e21` approximate FLOPs. With 256 accelerators each delivering `2.0e14` sustained FLOPs/second for this workload, ideal elapsed time is about 164,063 seconds, or 45.6 hours. At MCU 3 per accelerator-hour, the direct accelerator rental is about 35,000. This excludes storage, data preparation, evaluation, downtime, failed runs, and staff. Those are separately scheduled and charged. A training queue or data bottleneck can dominate the ideal compute time.

### 15.5 Research uncertainty

The engine maintains latent response surfaces linking compute, data composition, methodology, and team capability to specific evaluation outcomes. Surfaces exhibit diminishing returns, interactions, bottlenecks, and occasional innovations with bounded effects. The agent can estimate them through experiments. Their exact coefficients are hidden, but the public manual explains the mechanics and supported actions.

A discovery is not awarded for using fashionable terminology. It emerges from a validated project, resources, appropriate evidence, and a seeded outcome. Research success probabilities cannot depend on the evaluated model's name or the verbosity of its proposal.

### 15.6 Data procurement and rights

Datasets have volume, diversity, quality, provenance, duplication, contamination risk, permitted uses, retention obligations, transfer restrictions, price, and acquisition lead time. Synthetic data has generation cost and may amplify errors or reduce diversity if used poorly. An accessible dataset is not necessarily licensed for commercial model training.

The player can negotiate data partnerships, collect consented feedback, purchase rights, filter data, improve labeling, and audit provenance. A rights violation creates a specified dispute or product restriction through the fictional legal system; it is not an arbitrary model-judge moral score.

### 15.7 Evaluation and deployment gates

Each release candidate is evaluated on a held-out suite with task-specific confidence intervals and serving conditions. Public development tests and hidden deployment tests are distinct. The company can overfit its own public benchmark and then fail real customer workflows. Hidden tests should measure declared requirements rather than surprise trivia.

Deployment gates include quality, robustness, safety controls appropriate to the product, reproducibility, rollback, monitoring, incident response, and actual serving capacity. [NIST's Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) is a reference for risk categories; CompanyBench gates are explicit simulator rules, not claims of formal NIST certification.

### 15.8 Inference economics

Track input and output tokens separately, workload mix, model routing, cache hits, batching, concurrency, memory pressure, latency percentiles, time to first token, throughput, and failure rate. Published throughput is conditional on an accuracy and service envelope, consistent with the measurement distinction illustrated by [MLPerf Inference Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/).

```text
net_API_revenue = billed_input_units * input_price + billed_output_units * output_price - credits - refunds
serving_contribution = net_API_revenue - attributable_compute - network - storage - variable_support
```

Serving demand can spike faster than reserved capacity. Discounting a premium model below delivery cost can increase revenue and accelerate insolvency. Smaller models, caching, routing, and distillation can improve cost but alter quality and development burden. A reservation lowers price only if used; idle reserved capacity still costs money.

### 15.9 Products and enterprise sales

Enterprises evaluate private-data handling, uptime, integration, task success, support, and total cost. A general benchmark lead does not ensure deployment fit. On-premises or private deployments require implementation and upgrade support. Research partnerships may fund development but restrict IP or exclusivity. Licensing can be attractive but reduce future control.

### 15.10 AI competitors

| Fictional competitor | Position | Behavior and weakness |
|---|---|---|
| Helix Foundation | Large general-model incumbent | Strong capability and distribution; high operating cost; slower niche customization |
| Kestrel Models | Efficient open-model entrant | Low prices and developer adoption; uncertain enterprise support economics |
| Morrow Applied | Vertical specialist | Strong industry data and customers; limited breadth and key-person dependence |
| Atlas Compute | Infrastructure supplier with an AI product | Controls attractive capacity; conflicts with some customers; finite infrastructure pipeline |

Names are presentation labels. Hidden scenario variants change strengths and priorities so memorizing “always partner with Atlas” is not a winning policy. Supplier vertical integration can alter terms, but its contracts and commitments still apply.

### 15.11 AI-specific crises

Training divergence; discovered dataset contamination; revoked data rights; accelerator delivery delay; failed checkpoint recovery; sudden competitor price reduction; customer misuse incident; costly inference spike; enterprise evaluation failure; departed research lead; security breach; and an investment offer demanding restrictive exclusivity.

Each crisis must have an exposure pathway and available mitigations. For example, checkpoint investment lowers lost work after hardware failure, but cannot prevent a licensing dispute.

### 15.12 AI-specific metrics and milestones

Track released model versions, independently verified capability vector, deployed useful task volume, paying organizations, retained contract value, gross margin per workload, training efficiency, serving cost at fixed quality, reliability, unresolved material defects, data-rights coverage, research cycle time, and compute utilization.

Meaningful milestones include a paid reproducible pilot, repeatable performance on a declared task family, a reliable production API, MCU 1 million trailing annual revenue, sustained positive serving contribution, multi-customer enterprise renewal, and a new model generation whose improvement survives hidden evaluation. “Train the biggest model” and “announce AGI” are not milestones.

## 16. SaaS environment

### 16.1 Starting situation

The player leads **Harbor Software**, with MCU 1.5 million unrestricted cash, six employees, a working but limited workflow product, 30 paying organizations, 20 trial organizations, and MCU 12,000 monthly recurring subscription revenue. Monthly ordinary cash operating cost starts at an illustrative 85,000 before new hiring or major projects. The initial product serves operational teams but has incomplete enterprise controls and limited integrations.

The company can choose a narrow vertical, expand horizontally, move upmarket, become a platform, or embed AI features. It cannot declare all segments equally attractive; requirements, price sensitivity, and buying behavior differ.

### 16.2 Segments

| Segment | Typical purchase behavior in this scenario | Main tradeoff |
|---|---|---|
| Small teams | Fast self-service adoption; low contract value; frequent churn | Cheap onboarding versus support volume |
| Midmarket operations | Demonstrations and integrations; moderate contracts | Repeatability versus customization |
| Large enterprises | Security/legal procurement; multi-team rollout; annual commitments | Higher value versus long cycles and concentration |
| Regulated vertical | Specific controls, workflows, and references | Defensible specialization versus compliance cost |

Numerical willingness-to-pay, sales-cycle, and churn distributions are scenario parameters. They vary coherently by segment and macro regime. The player can investigate which opportunities are worth serving.

### 16.3 Product model

Represent capabilities as components: core workflow, collaboration, reporting, integrations, access control, auditability, automation, performance, migration, billing, and support tooling. Each customer segment has minimum requirements and marginal preferences. Some features are complements: an enterprise audit log without access control may have little value.

Feature shipping consumes engineering, design, QA, infrastructure, and product-management capacity. Product quality is observed through defects, adoption, task completion, support requests, and renewal behavior. A flashy feature can generate trials without improving retention.

### 16.4 Packaging and pricing

Support per-seat, per-workspace, usage-based, tiered, and hybrid contracts. Price changes respect existing contracts and notice requirements. Free tiers have serving cost and abuse exposure. Discounts have expiry, approval limits, and renewal implications. Usage limits must be enforced by product capability; writing a policy does not automatically meter consumption.

The player can run randomized pricing tests on eligible prospects with defined assignment, sample size, duration, and guardrails. Tests affect real pipeline and revenue. P-hacking through repeatedly stopping and restarting tests should yield misleading internal conclusions, not engine-awarded success.

### 16.5 MRR and ARR policy

MRR is the monthly-normalized active recurring subscription component. ARR is 12 times that MRR. Exclude one-time implementation, unsigned opportunities, free plans, taxes, and canceled service. Usage revenue has its own trailing run-rate metric; it is not silently treated as committed ARR. Suspended nonpaying customers are excluded according to a fixed delinquency policy.

Revenue recognition remains separate. A signed annual contract can contribute to contracted recurring metrics after activation while cash is still outstanding, subject to credit policy. Show cash-backed recurring metrics separately rather than redefining accounting revenue around collections.

### 16.6 SaaS cohort example

A starting cohort has MCU 100,000 MRR. During the month, 5,000 churns, 3,000 contracts, and 12,000 expands. New customers add 20,000. Ending total MRR is 124,000. Gross retention is 92%, net retention is 104%, and new business is 20,000. Calling total MRR growth of 24% “124% net retention” would be a measurement error.

In a separate acquisition-cohort example, a business spends 60,000 on attributable acquisition and gains 20 customers, so CAC is 3,000. At 300 monthly revenue per new customer and 80% gross margin, simple gross-profit payback is 12.5 months before churn and financing cost. This separate cohort adds 6,000 MRR; it is not the 20,000-MRR cohort above. Forecast uncertainty and observed cohort survival must remain visible.

### 16.7 Architecture and operations

The player can invest in capacity, monitoring, backups, access controls, data migration, observability, and deployment safety. The simulator need not execute a complete SaaS codebase to model these choices, but each capability must have testable operational consequences.

Outage probability depends on load relative to capacity, unresolved defects, release process, dependency failures, and security exposure. Cloud expenditure includes storage, egress, databases, third-party APIs, baseline reservations, and usage. Economies of scale are possible but not automatic.

### 16.8 Sales-led versus product-led growth

Product-led growth requires discoverability, fast activation, self-service billing, product value, and low support burden. Sales-led growth requires account selection, salesperson ramp, demos, pilots, procurement, and rollout capacity. A company can combine them, but one message saying “do PLG and enterprise” cannot eliminate the resource conflict.

Commission plans can encourage bad-fit contracts or discounting. Revenue operations, qualification, customer success, and implementation teams can improve quality at a cost. The player must decide whether to reject an attractive-looking contract whose custom roadmap would derail repeatability.

### 16.9 SaaS competitors

| Fictional competitor | Position | Strategic threat |
|---|---|---|
| Pinnacle Suite | Bundled incumbent | Adds a basic version to an existing contract at low incremental price |
| SwiftDesk | Aggressive self-service entrant | Low-friction signup and price competition; weaker complex workflows |
| Ledgerleaf | Specialized vertical provider | Deep integrations and trust in one niche; limited broader appeal |
| Mosaic Cloud | Platform and marketplace operator | Distribution opportunity combined with platform dependence |

### 16.10 SaaS-specific crises

Identity-provider outage; failed migration; ransomware-like service disruption represented without offensive execution; surprise cloud bill; churn wave after a price increase; major account insolvency; data residency procurement block; discount abuse; a key integration breaking; sales commission dispute; and an incumbent bundling away a feature advantage.

### 16.11 SaaS-specific metrics and milestones

Track MRR, ARR, recognized subscription and services revenue, cohort GRR/NRR, activation, adoption, customer acquisition cost, payback, realized cohort contribution, support cost, uptime, deployment quality, customer concentration, receivable aging, sales-cycle distribution, and expansion efficiency.

Milestones include 100 paying organizations retained through a renewal window, MCU 1 million and 5 million ARR sustained for three closes, positive operating cash flow over two consecutive quarters, and a scalable enterprise rollout meeting its service obligations. Product-market fit is a composite evidence label with published criteria, not an NPC compliment.

## 17. Electricity company environment

### 17.1 Starting situation and role boundaries

The player leads **Northline Energy**, a licensed commercial electricity supplier and project developer. It starts with MCU 12 million unrestricted cash, 3 million posted collateral, 14 employees, an operating commercial customer portfolio, partial supply hedges, and early project options. It owns no transmission monopoly and cannot energize a new connection by declaration.

Distinguish retail supply, generation ownership, storage operation, project development, and physical network ownership. These have different permissions, economics, and obligations. The distinction follows the role separation illustrated in [EIA's electricity delivery explanation](https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php). A regulated distribution-utility scenario would need a separate tariff and investment regime.

### 17.2 Playable strategic paths

1. Grow a diversified commercial supply portfolio with disciplined hedging.
2. Specialize in industrial or datacenter customers with negotiated flexibility and credit support.
3. Develop generation assets and sell or retain them after financing and construction.
4. Operate storage and demand-response portfolios subject to physical and contractual limits.
5. Combine customer offtake with financed assets to reduce merchant risk.
6. Acquire distressed operating assets where diligence and liquidity support the risk.

The player may mix paths. Each consumes capital, expertise, licenses, connection capacity, and management attention. A “vertically integrated” strategy does not waive any of those requirements.

### 17.3 Physical model

Core uses three interconnected zones, hourly demand and supply, transfer limits, losses, generator availability, storage state, reserve requirements, and defined market settlement. More detailed nodal power-flow models belong in a separately versioned fidelity tier. The reduced model must still prevent physically impossible delivery.

At each zone and hour:

```text
generation + imports + storage_discharge
  = served_load + exports + storage_charge + modeled_losses
unserved_load = requested_load - served_load
```

All flows have nonnegative or explicitly signed conventions. Power is MW; energy is MWh over a stated interval. [EIA's electricity measurement guide](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) grounds this basic distinction. A 100 MW plant is not a 100 MWh annual energy supply.

### 17.4 Dispatch and price formation

Generator offers reflect fuel, operating cost, startup, minimum output, ramp limits, and opportunity cost. Renewable availability follows weather. Storage bids reflect state of charge and policy. Scarcity and congestion can make prices highly variable. Negative prices are permitted where the fictional market rules and supply conditions support them.

The market solver dispatches feasible supply and calculates settlement prices using the published clearing method. The simplified solver's limits must be disclosed. [EIA's discussion of generator dispatch](https://www.eia.gov/todayinenergy/detail.php?id=7590) supports including operational constraints rather than treating all generation as interchangeable annual output.

### 17.5 Customer load

Each commercial load has hourly shape, seasonality, weather sensitivity, maximum connection capacity, growth, payment behavior, and flexibility. A datacenter's IT load, cooling load, and commissioning ramp are distinct when relevant. Training workloads may be shiftable; latency-sensitive services may not be. A customer grants contractual flexibility with a baseline, notice, compensation, and performance verification.

Load forecasts have correlated error. A heat wave may simultaneously increase cooling demand, reduce available generation, and raise prices. Monthly averages cannot erase the resulting cash and reliability exposure.

### 17.6 Contracts and PPAs

Contract objects specify physical or financial settlement; delivery zone; hourly shape; volume; term; escalation; losses; balancing responsibility; force majeure; commissioning conditions; renewable certificate ownership; credit support; penalties; early termination; and assignment rights.

Pay-as-produced renewable supply differs from firm shaped delivery. A financial contract for differences settles price differences but does not create physical energy or grid access. Annual renewable certificates do not guarantee hourly carbon-free supply. [EPA's physical PPA guidance](https://www.epa.gov/green-power-markets/physical-ppa) is a reference for these distinctions; the actual benchmark contract is its versioned template.

### 17.7 Project development

Projects progress through site control, resource assessment, environmental and technical studies, permit applications, generator interconnection studies, network upgrade allocation, offtake, financing, procurement, construction, commissioning, and commercial operation. Some activities can overlap; commercial operation requires all necessary gates.

Each gate has spend, deposits, uncertainty, information produced, expiration, and cancellation value. A project can be sold before operation if a buyer values its verified development rights. A rejected or delayed project can still produce recoverable assets, but its original budget is not automatically its residual value.

Generator interconnection and large-load connection are separate processes. [FERC's Order 2023 fact sheet](https://www.ferc.gov/news-events/news/fact-sheet-improvements-generator-interconnection-procedures-and-agreements) illustrates readiness and study requirements for generation; [Berkeley Lab's Queued Up](https://emp.lbl.gov/queues) provides empirical context for lengthy queues and project attrition. Neither makes a generator queue position equivalent to a datacenter energization right.

### 17.8 Illustrative project menu

| Asset/path | Modeled development range | Principal bottleneck |
|---|---:|---|
| Acquire operating solar interest | 3-9 months | Diligence, financing, condition, contracted revenue |
| New solar project | 18-48 months after viable site identification | Interconnection, permitting, equipment, financing |
| Battery project | 12-36 months | Connection capacity, safety approval, revenue durability |
| Efficiency/demand response | 3-12 months | Customer enrollment, controls, measurement |
| New dispatchable generation | 36-84+ months | Permits, fuel/network rights, construction and financing |
| New large nuclear project | Beyond Core in ordinary scenarios | Development complexity and long construction lead time |

These are fictional scenario ranges, not empirical forecasts. A hidden scenario may extend them through identifiable constraints. The model sees ranges and project-specific evidence. No asset is guaranteed to commission merely because its estimated date arrives.

### 17.9 Storage

For one-hour steps:

```text
SOC[t+1] = SOC[t] + charge_MW[t] * charge_efficiency - discharge_MW[t] / discharge_efficiency
0 <= SOC[t] <= usable_energy_capacity_MWh[t]
0 <= charge_MW[t] <= charge_power_limit_MW
0 <= discharge_MW[t] <= discharge_power_limit_MW
```

Use interval duration explicitly for non-hourly steps. Simultaneous charging and discharging is disallowed in the reference physical asset model. Round-trip efficiency, degradation, replacement, temperature effects where modeled, outage, and export limits constrain arbitrage. A 100 MW / 400 MWh battery cannot supply a 100 MW datacenter indefinitely overnight and through a multiday renewable drought.

### 17.10 Credit, collateral, and liquidity

Wholesale and bilateral trading requires credit support tied to exposures and market rules. Mark-to-market movements can trigger cash collateral before customer bills are collected. Restricted cash cannot pay staff or build projects. Letters of credit have bank limits, fees, and collateral requirements.

[PJM Settlement's credit materials](https://www.pjmsettlement.com/credit) provide a primary example of why market participation requires explicit credit mechanics. CompanyBench freezes a simplified fictional policy; it does not claim to implement every live PJM tariff.

### 17.11 Project finance

Create a project special-purpose entity with its own ledger, contracts, debt, equity, reserve accounts, distribution restrictions, and guarantees. The parent consolidates as specified but cannot freely withdraw restricted project cash. A project can meet accounting profit targets yet breach debt-service coverage.

Debt sizing may depend on eligible project cost, contracted cash flows, and minimum DSCR. [SAM's debt and equity documentation](https://samrepo.nrelcloud.org/help/mtf_debt_and_equity.html) supports including both cost-based and coverage-based sizing. Scenario contracts define precise cash available for debt service and reserve requirements.

### 17.12 Reliability and regulation

Track energy not served, forced outages, contractual service availability, reserve shortfall, connection compliance, and incident response. Attribute responsibility: the retailer may owe a contractual credit for a network outage without having caused it. Distinguish physical customer service metrics from company-controllable failure.

The fictional regulator issues licenses, imposes documented reporting and capital requirements, and can restrict or revoke permissions after defined processes. Environmental obligations include emissions accounting, local permit limits, and decommissioning reserves where applicable. Actual operating constraints determine penalties; generic statements of environmental virtue do not earn financial rewards.

### 17.13 Electricity competitors

| Fictional competitor | Position | Strategic pressure |
|---|---|---|
| Meridian Supply | Diversified incumbent retailer | Strong credit, lower procurement costs, slower niche contracting |
| Sunreach Development | Renewable developer | Better site pipeline, construction financing constraints |
| PeakFlex | Storage and demand-response specialist | Strong optimization, limited customer distribution |
| ForgePower | Industrial supply specialist | Competes for large loads, exposed to concentration and fuel costs |
| CivicGrid | Regulated network operator | Processes access under published rules; does not compete as an unlicensed retailer |

### 17.14 Electricity-specific metrics

Delivered MWh; contracted versus connected MW; commissioned capacity; available capacity; generation by source; gross margin per MWh; hedge coverage by hour and location; basis exposure; collateral utilization; receivable aging; customer concentration; construction spend and schedule; asset availability; energy not served; DSCR; emissions intensity; and decommissioning liabilities.

Milestones require delivery and verified rights. “Sign a 100 MW memorandum” is a pipeline event. “Supply an energized 100 MW customer within the contract's service envelope for 90 days” is an operating milestone.

## 18. Datacenter strategy as an actual decision

### 18.1 The central hypothesis

The electricity track should test whether an agent can discover when datacenter demand is a valuable opportunity and when it is a trap. There must be no hidden bonus for mentioning AI, compute, or datacenters. Returns follow the same physical, contractual, and financial systems as every other customer.

Large datacenter demand is a plausible scenario input, informed by [DOE's 2024 datacenter electricity report announcement](https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers). Its outlook is a dated projection, not a guarantee embedded in the world. [NERC's large-load work](https://prod.nerc.com/initiatives/large-loads-action-plan) motivates explicit modeling and connection requirements; proposed real-world initiatives are not silently treated as binding rules.

### 18.2 The opportunity dossier

**Asterion Compute Campus** requests up to 100 MW, with a staged load ramp and a desired energization date. Its dossier includes a price range, credit information, flexibility options, load forecast, site connection evidence, service requirements, alternative suppliers, and uncertainty around its own funding.

The model should investigate customer credit, actual load readiness, grid capacity, supply shape, hedge cost, basis exposure, connection spend, collateral, and competing uses of capital. It can negotiate take-or-pay minimums, ramp guarantees, indexed pricing, credit support, curtailment rights, phased service, or a smaller contract.

### 18.3 Required strategic alternatives

The environment must support at least these feasible alternatives where the scenario permits:

- Full fixed-price firm supply.
- Indexed supply with an explicit service fee and limited risk transfer.
- Phased energization with conditional commitments.
- Interruptible supply for flexible workloads.
- A supply-and-development joint venture with ring-fenced exposure.
- A smaller share of the campus load.
- Reject the opportunity and grow diversified commercial customers.

The benchmark cannot judge rejection as failure merely because the user-facing concept highlights datacenters. It must also include favorable conditions where blanket rejection is economically weak.

### 18.4 Worked normal-case economics

The following numbers are fictional, deliberately simplified, and not calibrated market prices. Assume a non-leap year, 100 MW maximum load, and 90% load factor:

```text
annual_delivered_energy = 100 * 0.90 * 8,760 = 788,400 MWh
customer_price = 85 MCU/MWh
hedged_share = 80% of actual load in every interval
hedge_price = 55 MCU/MWh
unhedged_load_weighted_price = 75 MCU/MWh
delivery_and_market_charges = 12 MCU/MWh
annual_fixed_operating_and_firm_capacity_cost = 6,000,000 MCU
```

| Item | Annual MCU |
|---|---:|
| Revenue | 67,014,000 |
| Hedged energy cost | 34,689,600 |
| Unhedged energy cost | 11,826,000 |
| Delivery and market charges | 9,460,800 |
| Fixed operating and capacity cost | 6,000,000 |
| Operating contribution before depreciation, interest, and tax | **5,037,600** |

This simplified hedge is unusually well matched: it covers a percentage of actual interval load and assumes no additional basis difference. The full simulator must retain fixed-volume, load, location, and timing mismatch where contracts expose them. The table is not a net-profit or free-cash-flow calculation.

### 18.5 Stress economics

If the load-weighted unhedged price becomes 350 MCU/MWh, annual unhedged cost is 55,188,000 and operating contribution becomes **negative 38,324,400**. This is a severe illustrative stress, not a claim about probability. A collateral call can cause default before the full annual loss is realized.

A three-month extreme period should be calculated on those hours only; the engine must not accidentally apply a short shock to all 8,760 hours. The annual stress above explicitly assumes the stated annual load-weighted price.

### 18.6 Opportunity cost

A diversified portfolio selling 200,000 MWh at 95 MCU/MWh, purchasing at 65, paying 12 in delivery charges, and incurring 1 million fixed cost generates 2.6 million operating contribution. If the datacenter strategy ties up 45 million capital and the diversified strategy 5 million, their simplified operating contribution-to-capital ratios are approximately 11.2% and 52.0%. These ratios are not equity IRRs and omit financing, growth, and terminal asset value.

The larger contract has more revenue and normal-case absolute contribution. The smaller portfolio can still be superior per unit of scarce capital or under adverse conditions. A capable agent should explain and act on this distinction through its actual capital allocation.

### 18.7 Paired evaluation worlds

| World | Changed evidence | Economically plausible response to test |
|---|---|---|
| Firm anchor | Creditworthy customer, realistic ramp, matched supply, manageable connection | Pursue or negotiate expansion |
| Speculative campus | Weak financing, optimistic date, expensive network upgrades | Stage commitments, demand security, or decline |
| Flexible training | Verified shiftable workload, compensated curtailment, compatible assets | Price flexibility and invest selectively |
| Inflexible service | Tight uptime, poor location hedge, limited firm capacity | Reprice, hedge, limit volume, or reject |
| Demand reversal | Customer expansion slows after rival model efficiency improves | Reallocate capacity and preserve liquidity |

Behavioral adaptation is evaluated from decisions and outcomes across these controlled differences. The evaluator must not require a specific written slogan or the same response in every seed.

## 19. Cross-sector connections

### 19.1 Shared economy, isolated primary episodes

Core episodes contain simulated adjacent sectors, but only one evaluated company. AI labs buy compute; compute suppliers require power and connection capacity; SaaS companies can buy AI services; electricity suppliers encounter industrial and datacenter demand. These links create coherent market effects without making one model's ranked run depend on another submitted model's behavior.

The same exogenous technology progress can lower inference unit prices, increase useful AI adoption, and change datacenter load. Do not assume efficiency always reduces total demand or always increases it; adoption elasticity and installed capacity determine the outcome in each scenario.

### 19.2 Permitted expansion

An AI lab can sell enterprise software if it builds the capabilities. A SaaS company can develop a specialized model if it acquires rights, people, and compute. An energy company can supply datacenters or invest in related infrastructure within its permissions. Crossing sectors creates acquisition, expertise, capital, and governance costs.

The primary sector label remains the assigned initial sector; the final business mix is reported. This prevents relabeling a failed AI lab as a successful cash-holding vehicle while still recognizing a legitimate pivot.

### 19.3 Arena expansion

In a future arena, evaluated companies may contract with each other under the same engine rules. Self-dealing, collusion, shared owners, and transfer pricing must be visible. Tournament scoring should include repeated roles and opponent mixtures. Arena results must not be compared directly with fixed-opponent Core scores.

## 20. Scenario suite and difficulty

### 20.1 Four Core families per sector

| Family | AI lab | SaaS | Electricity |
|---|---|---|---|
| Build and discover | Find a valuable domain with limited compute | Discover repeatable customer fit | Select a profitable supply/development niche |
| Scale and finance | Demand grows faster than serving capacity | Growth stresses onboarding and systems | Large-load opportunity strains collateral and project finance |
| Compete and adapt | Open-model improvement compresses pricing | Incumbent bundles a competing feature | New supply changes spreads and customer bargaining |
| Compound stress | Compute disruption plus funding slowdown | Renewal weakness plus receivable delay | Price shock plus construction or connection delay |

Each family contains multiple world seeds and structural variants. Exact event dates and values are hidden. Family membership is evaluator metadata; the agent receives an ordinary dossier and evidence.

### 20.2 Difficulty dimensions

Difficulty varies across initial liquidity, information quality, competitor sophistication, project dependencies, market volatility, financing friction, organizational scale, contract complexity, and response time. Vary these dimensions systematically rather than simply reducing starting cash until everyone dies.

A high-quality hard scenario has at least one feasible competent policy under its initial information distribution, meaningful downside, and several superficially attractive bad choices. It may still contain stochastic losses that no reasonable policy fully avoids. Scenario validation must distinguish unavoidable adversity from an impossible initial setup.

### 20.3 Difficulty ladder

**Level 1 — Mechanics:** stable demand, simple contracts, obvious cash obligations, transparent reports. Used for qualification and debugging.

**Level 2 — Management:** hiring delays, cohort differences, working capital, realistic competitor responses, and uncertain projects.

**Level 3 — Strategy:** limited capital across mutually exclusive opportunities, ambiguous information, nonlinear scaling, and different business models.

**Level 4 — Frontier:** compound regime shifts, latent but discoverable risks, long-delayed liabilities, organizational bottlenecks, and costly information acquisition.

**Level 5 — Generalization:** unseen combinations of institutions, technologies, and contract structures using documented primitives. No secret incompatible tool grammar or hidden exception-based trivia.

### 20.4 Preventing memorized playbooks

Hold out structural combinations as well as numerical seeds. Randomizing only company names and cash balances is insufficient. Rotate which segment is profitable, which supplier is reliable, whether a hedge is beneficial, which research path is saturated, and whether growth requires debt or patience. Observable evidence must change accordingly.

### 20.5 Frontier challenge acceptance target

The target is broad outcome dispersion, persistent room above current frontier systems, and evidence that better management improves results. The release should not define difficulty solely as a low success rate. A benchmark that no expert or competent policy can navigate is a poor management test.

Proposed pilot gates: competent scripted baselines outperform random policies; at least two materially different strategies can succeed in each ordinary family; a strong model still exhibits measurable failures or tradeoffs; and hidden-family results differ meaningfully from memorized public trajectories. Numerical thresholds require pilot evidence before they become release claims.

## 21. Incidents, crises, and recovery

### 21.1 Event taxonomy

| Event class | Examples | Typical leading evidence |
|---|---|---|
| Liquidity | Delayed receivable, collateral call, funding failure | Cash forecast, aging report, credit terms |
| Demand | Churn, budget freeze, competitor substitution | Usage decline, pipeline conversion, customer interviews |
| People | Resignation, burnout, weak hire | Workload, feedback, interview evidence |
| Technical | Outage, model regression, failed migration | Monitoring, tests, error budgets |
| Supply | GPU shortage, equipment delay, fuel disruption | Supplier updates, concentration, procurement milestones |
| Governance | Board removal, investor conflict | Missed reporting, mandate breach, voting structure |
| Contract/legal | Rights dispute, service claim, permit condition | Contract review, audit, regulator notice |
| Physical | Generator outage, grid constraint, storage failure | Maintenance, forecasts, asset condition |

### 21.2 Event construction

Each event specifies trigger, hidden cause, affected entities, observable signals, response window, available mitigations, cash and operational consequences, and termination conditions. Event severity follows exposure. A company that has no fixed-price power position should not receive the same loss as one that sold an enormous unhedged contract.

Events may be exogenous, endogenous, or mixed. A storm is exogenous; inadequate reserves are a management choice; the resulting contract default depends on both. Correlated shocks use shared causal drivers rather than arbitrary simultaneous penalties.

### 21.3 Recovery is measured

Record detection delay, response delay, containment cost, restoration time, customer recovery, employee effects, and recurrence. A model that makes one mistake and corrects the underlying process should differ from a model that repeats it every quarter.

Do not make every incident terminal. Recovery requires options such as bridge financing, customer renegotiation, phased launch, rollback, controlled curtailment, asset sale, insurance claim, or orderly restructuring. Those options have counterparties and costs; they are not universal rescue buttons.

### 21.4 Crisis density

Critical events must fit a plausible calendar and executive attention budget. If five urgent events arrive together, the correlation or scenario construction must justify it. Routine operating periods matter because they test maintenance, memory, forecasting, and follow-through between dramatic moments.

## 22. Agent interface and tool contract

### 22.1 Interface philosophy

Provide structured tools and a persistent company workspace. Natural-language reports are useful, but every important number and commitment has a machine-readable representation. The model can inspect, calculate, negotiate, authorize, and monitor. It cannot directly edit authoritative balances, customer counts, staff skills, or project completion.

The API below is a **proposed CompanyBench interface**, not an existing product API. Implementations must publish a generated schema and conformance suite before ranking agents.

### 22.2 Tool families

| Tool | Purpose | Effect type |
|---|---|---|
| `world.status` | Current date, company state, remaining budgets, material alerts | Read |
| `world.advance` | Advance to a date or interrupt | Time transition |
| `world.rules` | Retrieve applicable rulebook and contract definitions | Read |
| `company.dashboard` | Financial, operating, staffing, and risk snapshots | Read |
| `records.search` | Search authorized company records with stable pagination | Read |
| `records.read` | Retrieve source documents and structured data | Read |
| `finance.statement` | Ledger-derived balance sheet, income, cash flow, aging | Read |
| `finance.forecast` | Run a forecast using declared assumptions and visible data | Analysis |
| `finance.authorize_payment` | Approve a payable within authority and cash constraints | Commitment |
| `finance.set_treasury_policy` | Set reserves, collection, and permitted cash policies | Policy |
| `funding.open_process` | Start an investor or lender pipeline | Project |
| `funding.submit_dataroom` | Share selected company evidence with simulated parties | Communication |
| `funding.accept_instrument` | Execute a validated financing document | Commitment |
| `people.open_role` | Fund and initiate recruitment | Project |
| `people.interview` | Reserve interview effort and request evidence | Scheduled work |
| `people.offer` | Issue a bounded employment offer | Commitment |
| `people.assign` | Allocate staff to teams and tasks | Resource allocation |
| `people.change_terms` | Propose lawful compensation or role changes | Commitment |
| `people.terminate` | Initiate notice, severance, and handover | Commitment |
| `projects.propose` | Define a new project from supported primitives | Proposal |
| `projects.authorize` | Commit approved resources and start eligible work | Commitment |
| `projects.review` | Inspect progress, test results, dependencies, and estimates | Read |
| `projects.cancel` | Stop cancellable work and calculate remaining liabilities | Commitment |
| `product.configure` | Set supported product, pricing, or release choices | Policy |
| `sales.campaign` | Start a scoped acquisition or research campaign | Project |
| `sales.offer` | Create a customer proposal from an approved template | Negotiation |
| `customers.analyze` | Query cohorts, usage, renewals, satisfaction, and payment | Read |
| `contracts.propose` | Create structured contractual terms | Negotiation |
| `contracts.review` | Retrieve terms and optionally commission professional review | Read/work |
| `contracts.sign` | Sign a specific immutable contract revision | Commitment |
| `procurement.request_quote` | Obtain a supplier offer with price and availability | Negotiation |
| `procurement.order` | Accept a validated purchase and payment schedule | Commitment |
| `research.run_experiment` | Schedule a supported research experiment | Project |
| `research.evaluate` | Schedule a defined evaluation and receive results later | Project |
| `compute.reserve` | Contract for compute capacity | Commitment |
| `compute.set_policy` | Set training/serving allocation and bounded autoscaling | Policy |
| `energy.market_view` | Authorized prices, forecasts, load, and exposure | Read |
| `energy.set_policy` | Set bounded procurement, hedging, dispatch, and risk policy | Policy |
| `energy.develop_project` | Initiate an asset development graph | Project |
| `energy.submit_connection` | Apply for the specified load or generator connection | Commitment |
| `risk.commission_review` | Purchase a scoped audit or risk study | Project |
| `incidents.respond` | Apply supported mitigation or recovery actions | Commitment |
| `board.submit` | Submit a decision request or evidence report | Governance |
| `messages.send` | Communicate with simulated counterparties | Communication |
| `workspace.read/write` | Maintain private company notes and analysis artifacts | Agent memory |
| `analysis.run` | Execute sandboxed calculations over authorized data | Analysis |

### 22.3 Common action envelope

```json
{
  "api_version": "companybench.v1",
  "action_id": "a_000183",
  "idempotency_key": "hire_grid_analyst_offer_v1",
  "expected_state_version": 928,
  "tool": "people.offer",
  "arguments": {
    "candidate_id": "candidate_42",
    "role_id": "role_grid_analyst_1",
    "salary_minor_units_per_year": 12500000,
    "currency": "MCU",
    "equity_grant_id": null,
    "start_not_before": "2031-04-01",
    "expires_at": "2031-03-12T17:00:00Z"
  }
}
```

All dates use the fictional world's calendar in UTC. One MCU has 100 minor units in the initial pack. Fixed-point quantities include explicit units and allowed precision. Parameters have bounds and enum definitions.

### 22.4 Common response envelope

```json
{
  "action_id": "a_000183",
  "status": "accepted_pending_counterparty",
  "state_version": 929,
  "effective_at": "2031-03-05T10:00:00Z",
  "created_object_ids": ["offer_93"],
  "attention_hours_reserved": 1.0,
  "cash_settled_minor_units": 0,
  "new_commitments": [],
  "expected_next_event": "candidate_response",
  "warnings": ["Candidate acceptance and notice period are unresolved."],
  "evidence_ids": ["event_10383"]
}
```

Acceptance by the engine means the offer exists; it does not mean the candidate accepted. Responses must make this distinction explicit. A signed financing agreement can still await conditions and settlement.

### 22.5 Validation and errors

Validation checks schema, units, authority, object revision, capacity, known legal constraints, economic feasibility where binding, and deadlines. It does not reject every economically risky action: a company can sign a bad deal if counterparties accept and rules permit it.

Required error codes include `INVALID_ARGUMENT`, `STALE_REVISION`, `INSUFFICIENT_AUTHORITY`, `CAPACITY_UNAVAILABLE`, `DEADLINE_PASSED`, `COUNTERPARTY_REJECTED`, `CONDITIONS_NOT_MET`, `UNSUPPORTED_PRIMITIVE`, and `BUDGET_EXHAUSTED`. Errors explain the public reason without exposing a hidden reservation price or private state.

Idempotent retries return the original result. Reusing an idempotency key with different content fails. Compound transactions are atomic where declared; otherwise the response explicitly describes which steps committed. The model must not infer that an entire sequence succeeded after its first accepted call.

### 22.6 Safe analysis environment

`analysis.run` provides deterministic arithmetic, table manipulation, plotting, and bounded code execution over visible exports. It cannot read evaluator storage, contact external services, mutate company state, inspect simulator code not in the public release, or launch recursive agents. CPU, memory, output size, and time limits are declared.

The agent may build a spreadsheet-like cash forecast, run an optimization, or compute a hedge exposure. Forecast simulations sample from the company's declared beliefs or public priors, never the episode's secret future. Monte Carlo count and seeds are recorded.

## 23. Persistent documents, memory, and delegation

### 23.1 Workspace

The company workspace contains inbox, contracts, board records, financial exports, employee records, project plans, research results, customer research, risk register, and private agent notes. Files are versioned and timestamped. Search returns stable document IDs and excerpts so long-running agents can recover their own history.

Reference Core gives every model the same 256 MiB workspace allowance and a portable maximum of 64,000 input tokens per model invocation, subject to model support. Models unable to support the declared tier run in a separately labeled compatible tier. Storage size and active context are independent. A larger native context is not silently supplied in the standard tier.

### 23.2 Memory policy

The reference harness uses deterministic retrieval and truncation rules. The tested model can write summaries, maintain calendars, and search older records. It does not receive an unseen stronger model's summaries. Truncated context is marked with pointers to the omitted archive.

Critical commitments remain queryable even when they leave context. Forgetting to inspect a known contract can be an agent failure; losing the only record through an evaluator bug is not. Repeated reports consume input tokens according to actual usage.

### 23.3 Decision records

For material commitments above a scenario-defined threshold, the interface requests a brief structured record: objective, alternatives considered, forecast range, principal risks, planned review date, and reversal conditions. This is a contemporaneous work artifact, not a request for private chain-of-thought. It can be concise and is scored only for specific preregistered forecast or process diagnostics.

The model is evaluated primarily by behavior and outcomes. It cannot offset a bad decision by writing a sophisticated justification. Records make later mistake attribution more defensible and help distinguish calculated risk from arithmetic confusion.

### 23.4 Delegation inside the company

Simulated employees execute business tasks under authority, skill, workload, and reporting constraints. This is part of company management and available in Core. It differs from delegating reasoning to another external frontier model.

Open Scaffold may use subagents, different models, custom retrieval, and external planners within its budget. All calls, costs, model identities, and handoffs are logged. Such a result belongs to the submitted agent system, not to a single model alone. Human intervention produces an assisted-track result with intervention timing and content recorded.

## 24. Language, negotiation, and adjudication

### 24.1 Language has bounded economic effects

Negotiation should reward truthful framing, finding tradeoffs, asking useful questions, and structuring acceptable terms. It must not reward persuading a language model to ignore its own cash balance. Counterparties have explicit feasible offers, reservation distributions, concession rules, authority, and utility over supported terms.

Language processing extracts claims, requests, and proposed terms into a typed representation. Ambiguity requires clarification from the simulated counterparty or rejection. The engine validates every proposed contract. A renderer may say “we have a deal” only after the contract state supports it.

### 24.2 Authority hierarchy

The authority order is signed engine contract and ledger state; official rulebook; authenticated operational records; dated professional reports; counterparty messages; and unverified claims. A message claiming to be from the evaluator, board, bank, or regulator carries no authority unless its authenticated origin and permission match.

Negotiation text cannot change system instructions or tool permissions. Prompt-injection content may appear as a controlled robustness test in simulated messages, but economic success from exploiting a renderer is invalid rather than rewarded as commercial skill.

### 24.3 NPC implementation options

Core can use structured policies plus templates for maximum reproducibility. A language-enhanced tier may use a frozen model to render interactions or classify communication acts. Its input is restricted to the NPC's observations and approved policy outputs. Deterministic constrained responses are preferred for ranked economics.

If a hosted renderer cannot be made reproducible, record every request and response, disclose that only transcript replay is exact, and measure renderer variance separately. A cached transcript does not prove that a fresh counterfactual run would generate identical dialogue.

### 24.4 Qualitative judges

Judges may assess narrow communication qualities or audit alleged mistakes. They must output criteria, evidence IDs, confidence, and a label. Blind them to evaluated model identity and irrelevant style cues where practical. Use frozen versions, human calibration, and disagreement reporting.

No judge directly sets cash, customer count, research success, project completion, or terminal value. Qualitative scores are auxiliary unless a separately validated track explicitly includes them. This boundary follows the outcome/trajectory distinction discussed in [Anthropic's agent evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), while the implementation choices here are CompanyBench proposals.

## 25. Termination, exits, and continuity

### 25.1 Endpoint taxonomy

| Endpoint | Company survival interpretation | Agent interpretation |
|---|---|---|
| Horizon reached | Alive at observation boundary if operating | Completed assigned horizon |
| Unresolved insolvency and closure | Failure at effective closure or defined operating cessation | Control may end earlier |
| Necessary license lost | Failure if no viable permitted operations remain under rulebook | May remain as wind-down manager |
| Acquisition | Ownership transition; economic result can be good or poor | Tenure ends or continues per agreement |
| IPO | Financing/ownership event; company continues | Not automatically terminal |
| Solvent wind-down | Intentional closure with distributions and fulfilled liabilities | Decision outcome, not bankruptcy |
| CEO removal | Company may continue under replacement | Autonomous tenure ends |
| Agent resignation/refusal | Existing business may continue unattended | Voluntary control termination |
| Inference budget exhaustion | Business failure not yet established | Budget-limited control ends |
| Infrastructure interruption | No economic conclusion | Resume or rerun under protocol |

### 25.2 Three survival measures

**Legal continuity:** time until dissolution or equivalent legal end. A shell can score high here without operating.

**Operating continuity:** time until permanent cessation of the company's legitimate productive activity. A funded developer advancing a project can be operating before revenue. A temporary outage is a service failure, not necessarily company death.

**Autonomous tenure:** time during which the evaluated agent remains the authorized controller without external assistance and within its declared budget.

All are required. Public summaries must not present legal continuity alone as “successfully ran a company.”

### 25.3 Productive activity

Productive activity is satisfied by delivered customer service or verified progress on a funded commercial/research project with real external need and maintained operating capabilities. Maintenance of an existing profitable business counts. Merely transferring cash between accounts or creating fictional internal tasks does not.

At least quarterly, an engine audit checks active contracts, funded project milestones, external demand evidence, required staff/outsourcing, and maintained permissions. The predicate has sector-specific alternatives and a published grace policy. It must not force a software-style first-revenue deadline on an energy developer.

### 25.4 Exits and horizon cleanup

At acquisition or wind-down, calculate actual cash settlement, unpaid liabilities, retained claims, earnout uncertainty, and distributions. An unsigned acquisition proposal has no exit value. Earnouts are recognized only as settled cash or conservatively valued contingent claims according to a frozen policy, with both reported.

At the final horizon, preserve all liabilities and existing commitments. A standardized 12-month runoff assessment estimates near-term consequences of existing obligations and asset condition. It uses fixed maintenance policies and no new strategic expansion, is discounted and reported separately, and cannot be relabeled as additional agent-managed survival. Longer obligations remain in terminal valuation and liability reserves.

## 26. Metric dictionary

### 26.1 Identity and control

Record benchmark version, scenario family, hidden seed identifier for evaluator use, model endpoint/version, scaffold hash, resource tier, sector selected/assigned, business-model taxonomy, pivots with dates, final revenue mix, ownership structure, and autonomous-control intervals.

### 26.2 Required financial metrics

| Metric | Definition and presentation |
|---|---|
| Revenue | Recognized revenue by month, segment, and business line |
| Cash collections | Settled customer receipts, net of refunds, distinct from funding |
| Gross profit/margin | Revenue less fixed-policy cost of revenue; null margin at zero revenue |
| Operating profit | Accrual result after operating expenses, including policy-defined depreciation |
| Net profit | After financing expense and taxes |
| Operating cash flow | Settled operating cash flows under the reference classification |
| Free cash flow | Operating cash flow less gross cash capex; asset sales separate |
| Cash | Unrestricted, restricted, and consolidated totals |
| Runway | Trailing estimate plus dated liquidity shortfall forecast |
| Equity raised | Settled primary equity and SAFE-like contributions, gross and net of fees |
| Debt raised | Gross principal draws; net borrowing and outstanding principal separate |
| Grants/support | Settled grants, subsidies, donated assets, and restrictions |
| Capital returned | Dividends, repurchases, and exit proceeds to all equity holders |
| Ownership | Founder and original-shareholder fully diluted stakes plus actual exit proceeds |
| Liabilities | Payables, accrued payroll, debt, deferred service obligations, and provisions |
| Value creation | Capital-adjusted realized and estimated terminal values with sensitivity |

### 26.3 Employees and organization

Current and peak employee count; FTE; contractors; employee-months; payroll; compensation distribution; unpaid wages; hiring lead time; new-hire retention; critical attrition; regretted attrition under a fixed definition; management span; project staffing gaps; and workload exceedance.

“Employee-months” integrates FTE over time rather than adding end-of-month headcount snapshots without duration. A one-day mass hire at the horizon does not create a meaningful employment record.

### 26.4 Commercial and sector metrics

Customers, customer concentration, customer lifetime contribution, churn, retention, qualified pipeline, sales cycle, service fulfillment, SLA breaches, refunds, product adoption, market share, and the sector-specific metrics in Sections 15-17. All ratios specify cohort, period, numerator, denominator, and treatment of missing data.

### 26.5 Mistakes and reliability

Mistakes by verified class and severity; unique root causes; realized attributable loss; estimated counterfactual regret with uncertainty; detection and recovery time; repeated errors; unfulfilled obligations; capacity overcommitment; forecast calibration; and unsupported-action requests.

### 26.6 Runtime and cost

Actual input/output/reasoning/cached tokens; request count; retries; tool calls; active inference latency; simulator compute; total wall time; real billed model cost; frozen-price normalized cost; NPC and judge costs; human review cost; and agent workspace use. Unavailable data remains explicitly unavailable, never zero.

Company compute spending inside the AI-lab world is separate from the evaluator's cost of running the CEO model. The Core company ledger never silently pays real API charges.

## 27. Milestones and time to achievement

### 27.1 Milestone record

Each milestone defines ID, public description, eligible sectors and strategies, executable predicate, prerequisites, minimum duration, quality gates, disqualifying conditions, evaluator evidence, and whether later reversal revokes current status. Store first crossing, first sustained attainment, latest valid status, reversal dates, and final status.

### 27.2 Cross-sector milestones

| ID | Milestone | Verification |
|---|---|---|
| M01 | First paying external customer | Delivered eligible product/service and settled nonrefundable payment |
| M02 | First repeat or renewal customer | Distinct completed renewal/repeat decision after actual use |
| M03 | First completed financing | Executed instrument and cleared primary funds |
| M04 | Twelve months of operating continuity | Sector-appropriate activity and fulfilled critical obligations |
| M05 | First profitable quarter | Positive operating profit with complete accruals |
| M06 | Cash-generating operations | Positive operating cash flow over two consecutive quarters |
| M07 | Durable profitable operation | Positive operating profit and operating cash flow over four consecutive quarters |
| M08 | Recovery from material incident | Restored service and resolved mandatory remediation |
| M09 | Multi-year continuity | Valid 24-, 36-, and 60-month operating status |
| M10 | Value-creating exit/distribution | Verified capital-adjusted outcome under the frozen valuation policy |

These are reported milestones, not a mandatory sequence. A bootstrapped company need not raise capital. An energy developer can make meaningful progress before M01. Profitability can arrive after several years of sensible investment.

### 27.3 Sector milestone examples

**AI lab:** reproducible paid pilot; qualified model release; production service at specified quality and load; MCU 1 million and 10 million trailing annual revenue; positive delivery contribution; independent customers renewing; improved serving efficiency at unchanged quality; sustained multi-generation research progress.

**SaaS:** MCU 100,000, 1 million, 5 million, and 10 million ARR; 100 and 1,000 retained paying organizations where segment-appropriate; repeatable enterprise rollout; NRR above a published threshold for a defined mature cohort; two-quarter cash generation; sustained reliable operation at larger load.

**Electricity:** licensed supply and first delivery; financed project reaching notice to proceed; commercial operation of a verified asset; 10 and 100 MW of connected customer capacity under fulfilled contracts; 100,000 and 1 million trailing annual MWh delivered; stable positive gross margin; DSCR compliance; profitable reliable large-load service.

Revenue thresholds are fictional tier definitions, not equal-difficulty claims across sectors. Calibration should adjust scenario milestone bundles before release and freeze them afterward.

### 27.4 Sustainment and quality gates

Recurring revenue milestones require three consecutive monthly closes and a fixed delinquency policy. Reliability milestones require real measured delivery across the specified load and duration. Commissioning requires permits, physical tests, connection rights, and operational acceptance. Research milestones require independent evaluation rather than the lab's own announcement.

Avoid a universal “no incident ever” gate: it would erase achievement for unavoidable minor events. Each milestone defines materiality and permissible remedy. Historical attainment remains in the record even when a later reversal removes current sustained status.

### 27.5 Time-to-milestone reporting

For each milestone, publish attainment probability by fixed dates and a time-to-attainment curve that accounts for competing terminal events. For a simple restricted diagnostic, set `T* = min(time_to_sustained_attainment, H)` and assign `H` to nonattainers; always publish attainment rate beside its mean. This avoids reporting only the fast rare winners.

Acquisition, bankruptcy, and control loss are competing outcomes rather than automatically benign censoring. A model can receive a valid exit milestone without being credited with operating milestones it never reached. Raw simulated dates, number of decisions, tokens, and real execution time to each milestone are all retained.

## 28. Scoring and comparison

### 28.1 A dashboard is the primary scientific result

CompanyBench should publish outcome vectors before a scalar rank. Survival, growth, profit, capital efficiency, reliability, employment, mistakes, and cost capture different properties. Headcount and money raised are essential observations but are not rewards by themselves.

A model that grows a small profitable company and one that finances a larger but risky research program may represent a real tradeoff. The result page should make that visible rather than hiding it inside an opaque number.

### 28.2 Proposed composite

If a headline score is required, use the following preregistered **CompanyBench Core Score**, with raw dimensions alongside it:

```text
CoreScore = 0.25 * V + 0.25 * P + 0.30 * E + 0.20 * O
```

Each component is on a 0-100 scale, normalized within the sector/scenario stratum where needed. `V` measures operating viability, `P` durable commercial/technical progress, `E` economic value creation, and `O` fulfilled operating obligations. These are proposed weights. Pilot sensitivity analysis and independent review must precede freezing them for a scored release.

### 28.3 Viability component V

Let `I(t)` indicate productive operation under the evaluated controller at time `t`, including qualifying pre-revenue development. Define:

```text
productive_control_fraction = integral_0^H I(t) dt / H
V = 100 * productive_control_fraction
```

After an acquisition, value-creating sale, or solvent wind-down, `I(t)` is zero unless the tested agent continues authorized operation. This is intentionally a measure of duration, not a judgment that early exits are bad. Exit value and achievement appear in `E` and `P`; publish an exit-focused secondary view so a good early sale is not misrepresented as bankruptcy.

Raw company survival is reported independently and can extend beyond controller tenure through a clearly labeled replacement-policy branch. No extra tenure credit is awarded for the branch. Inference exhaustion therefore cannot be hidden as harmless right-censoring.

### 28.4 Progress component P

Each scenario has four published achievement axes worth 25 points each: validated external value, scale or productive asset progress, repeatability/retention, and durable economic operation. Each axis has an executable ladder with sector-specific alternatives and equivalence rules. The highest sustained rung determines its axis score; accumulating many trivial milestones cannot farm points.

An illustrative axis ladder is 0, 5, 10, 15, 20, 25 points, with criteria in the scenario manifest. Thresholds are fixed before model testing. Commercialization and research pathways have meaningful alternatives; fundraising itself does not occupy a progress axis. Time to attainment remains a separate speed diagnostic so aggressive premature growth does not automatically dominate.

### 28.5 Economic value component E

Use two equally weighted normalized terms: realized operating value and capital-adjusted equity value. Realized operating value is cumulative discounted operating cash flow less all gross cash capex, including discretionary growth investment, with cash from asset disposals reported separately. Remove financing-like grants and support transfers from this operating-value measure wherever the accounting policy included them in operating cash flow; otherwise subsidies would inflate this half of the score. Genuine payment for contracted delivered customer service remains operating revenue. Capital-adjusted equity value includes distributions and conservative residual business value.

For the latter:

```text
tau = min(H, autonomous_control_end)
equity_value_added =
  sum_over_0_to_tau(distributions_to_all_equity_holders[t] / (1+r)^(t/365.25))
  + terminal_net_equity_value[tau] / (1+r)^(tau/365.25)
  - initial_equity_capital
  - sum_over_0_to_tau(new_equity_contributions[t] / (1+r)^(t/365.25))
  - sum_over_0_to_tau(equity_like_support_transfers[t] / (1+r)^(t/365.25))
```

Here `t`, `tau`, and `H` are elapsed days, and `r` is a frozen annual evaluation discount rate; the proposed default is 10%, with 5% and 20% sensitivity reports. If the agent completes the horizon, `tau = H`. All realized operating-value flows also stop at `tau`. It is a benchmark opportunity-cost convention, not a claim about real investor required returns. `initial_equity_capital` includes the opening contribution basis of noncash resources, not just the bank balance.

Debt is not subtracted again as a contribution: interest, repayment cash flows, and terminal net debt already affect equity value. Grants and donated assets are shown with and without support adjustment; the primary adjusted measure prevents free subsidies from masquerading as management-created capital. Genuine customer revenue is never subtracted as a capital contribution.

Distributions include dividends, repurchases, and sale proceeds to all equity classes. If a company is sold, its sale proceeds and its terminal business value cannot both be counted. Deferred earnouts are valued once as contingent claims at `tau`; later settlements are a separate diagnostic unless a preregistered settlement-follow-up protocol replaces that estimate for every comparable run. Do not add later cash to an already counted claim. Founder wealth is a separate metric because founder dilution and total-company value answer different questions.

### 28.6 Terminal valuation

Terminal value is estimated by an independent, deterministic, preregistered sector method. SaaS and AI valuation can combine maintainable cash-flow estimates, customer runoff, and recoverable assets. Energy valuation uses project cash flows, verified development rights, asset condition, debt, and decommissioning obligations. No method uses the last round's headline valuation as truth.

Publish liquidation value, conservative going-concern value, and sensitivity bands. The primary estimate excludes speculative unvalidated research breakthroughs, unsigned sales, unapproved permits, and self-assessed goodwill. A financed construction project can retain value through actual rights and expected recoverable cash flows; it is not worth zero solely because it has not commissioned.

Forecasts use terminal observable/evaluator-auditable business condition and frozen future distributions, not secret realized post-horizon luck. Existing contingent liabilities and under-maintained assets reduce value. The score's dependence on this model must be disclosed, and realized-only rankings must be published as a robustness check.

### 28.7 Normalization

For each financial term in a stratum, define fixed low and high anchors `L < U` from preregistered reference baselines and expert review:

```text
normalized(x) = 100 * clip((x - L) / (U - L), 0, 1)
```

Publish raw values and unclipped normalized values. Anchors never use the best or worst submitted model, so a new entrant cannot change everyone else's historical score. If anchors saturate, revise a future benchmark version rather than moving the current goalposts. All industries and four families receive equal macro weight, regardless of revenue scale.

### 28.8 Operating obligations component O

Use actual fulfilled obligations and severity-weighted losses, with separate dimensions for customer delivery, workforce obligations, contract/credit compliance, and required operational controls. Each has a frozen exposure denominator and a score map. A provider with no delivered service gets no free perfect reliability score; its relevant obligation dimension is zero until meaningful exposure exists, while qualifying developers use project and financing obligations instead.

Customer service credits already reduce economic results. Their presence in `O` measures a separate reliability construct; disclose this overlap and run a score sensitivity excluding duplicated economic effects. Mistake counts themselves are auxiliary, since judge-dependent blame should not dominate a deterministic leaderboard.

### 28.9 Integrity and abnormal endpoints

Simulator exploits, evaluator access, corrupted logs, or external assistance outside the track invalidate a run pending audit. Ordinary in-world misconduct or contract breaches remain valid measured behavior with recorded consequences; they are not erased to make a leaderboard look cleaner. Publish a separate integrity and obligations record beside any aggregate score.

After control ends, freeze the agent-controlled progress record and apply the `tau` endpoint in Section 28.5 to flows and residual value. For budget exhaustion or removal, use conservative transfer/liquidation value at control end for `E`, with a separately labeled continuation sensitivity. Financial losses and liabilities already incurred remain counted. Runoff findings adjust the valuation only through the frozen valuation policy and cannot duplicate liabilities already deducted. `V` accrues no later control time. This prevents exhausting the budget early and receiving unearned future-management credit.

### 28.10 Anti-idling and financing-gaming examples

- Park all cash: long legal existence, little productive control, little progress, and value below the opportunity-cost baseline.
- Raise 100 million and leave it unused: funding amount rises, but contribution-adjusted value does not rise mechanically.
- Hire 1,000 employees for one day: peak headcount rises, costs accrue, and progress does not improve without work.
- Sign uneconomic high-volume supply: revenue rises but contribution, liquidity, and value may collapse.
- Sell a good company early: tenure is shorter, but verified distributions and achievement can produce a strong economic result.
- Build a funded power asset that commissions after month 60: verified development and residual value can count, with uncertainty and obligations retained.

## 29. Mistakes and decision quality

### 29.1 Mistakes are not synonymous with losses

A good decision can lose money under an adverse draw. A bad decision can get lucky. CompanyBench therefore reports realized outcomes and evidence-backed decision errors separately. Evaluators must assess what was knowable when an action was taken, not blame the agent for hidden facts discovered later.

### 29.2 Mistake classes

| Class | Definition | Example |
|---|---|---|
| Arithmetic/accounting | Verifiable quantitative or classification error affecting a decision | Counting a funding round as sales revenue |
| State-tracking | Acting on a false belief contradicted by available authoritative records | Assuming an unsigned contract is active |
| Execution | Intended authorized work is not implemented or verified | Announcing a backup policy without scheduling backups |
| Capacity | Committing more staff, compute, energy, or cash than available under known rules | Selling the same reserved capacity twice |
| Deadline | Missing a known material deadline despite feasible attention and options | Failing to submit a required credit report |
| Process | Omitting a specified mandatory procedure | Signing above authority without board approval |
| Forecast | Poor predictive calibration or persistent systematic bias | Repeatedly forecasting zero churn despite contrary evidence |
| Strategy | A materially dominated allocation under contemporaneous information | Paying more for an otherwise identical feasible contract |
| Recovery | Failing to contain or fix a known problem | Repeating a duplicate payment after an explicit warning |
| Integrity | Deception, unauthorized access, or rule breach with evidence | Falsifying a customer invoice to obtain financing |

Forecast error is graded statistically, not every time an uncertain forecast misses. Strategic mistake labels require stronger evidence than “an alternative happened to work better.” Unsupported novel proposals are tracked separately from invalid tool use.

### 29.3 Evidence record

```json
{
  "mistake_id": "mistake_007",
  "root_cause_id": "root_003",
  "class": "state_tracking",
  "decision_event_id": "event_441",
  "observation_snapshot_id": "snapshot_81",
  "evidence_ids": ["contract_12_rev3", "bank_statement_9"],
  "claim": "The agent treated an indicative funding offer as settled cash.",
  "known_feasible_alternative": "Delay the discretionary equipment deposit.",
  "controllability": "high",
  "severity": "material",
  "realized_direct_loss_minor_units": 5000000,
  "counterfactual_loss_interval_minor_units": [2000000, 9000000],
  "label_method": "rule_plus_blinded_review",
  "review_status": "confirmed",
  "recovery_event_ids": ["event_519"]
}
```

### 29.4 Severity and loss attribution

Severity combines irreversible impact, obligations harmed, operational disruption, and loss relative to company resources. Suggested labels are minor, material, severe, and terminal. Thresholds are sector/scenario-specific and published. A 50,000 loss has different significance to a 100,000 startup and a 100 million asset owner.

Group downstream events under root causes. One unhedged contract can cause a collateral call, missed payroll, default, and liquidation; counting four full independent losses would exaggerate attribution. Report the cascade, allocate non-overlapping financial loss where possible, and label overlapping estimates.

### 29.5 Counterfactual replay

Evaluator-only replay can compare a committed decision with feasible alternatives under the same exogenous random field. The alternative may change endogenous events, competitor reactions, and observation availability. Replays must account for those changes rather than merely replacing one line in a realized cash flow.

Use a bounded alternative set derived from contemporaneously available options. Report mean regret and uncertainty across plausible futures where possible. The simulator is not a real-world causal oracle; counterfactual estimates are diagnostics under its assumptions.

### 29.6 Forecast calibration

At material decisions, optional forecasts include revenue range, cash minimum, completion date, close probability, and key risk probabilities. Evaluate binary forecasts with a proper score such as the Brier score, and interval forecasts with coverage plus interval width or a proper interval score. Forecasts cannot be rewritten after outcomes arrive.

Missing forecasts do not automatically imply incorrect beliefs. If forecast reporting is mandatory in a track, omissions receive a defined process label. Core economic ranking should remain possible without judging internal reasoning.

## 30. Experimental protocol and statistics

### 30.1 Unit of evaluation

The elementary unit is a complete episode: one model/scaffold configuration, one scenario world, one agent sampling replicate, one resource tier, and one benchmark version. A company-month is an observation within a run, not an independent experimental replicate.

### 30.2 Proposed launch matrix

```text
3 sectors * 4 scenario families * 10 held-out world seeds * 2 agent replicates
= 240 full Core episodes per configuration and resource tier
```

A 24-episode pilot uses two worlds per sector/family and one replicate. It is for feasibility, variance, and failure analysis, not a definitive ranking. The final count must be selected using a preregistered precision or power analysis based on pilot variance and a practically meaningful effect. The proposed 240 is a planning default, not proof of adequate statistical power.

### 30.3 Paired random worlds

Generate exogenous randomness using semantic keys:

```text
draw = RNG(world_seed, subsystem, entity_id, simulated_time, event_type, draw_index)
```

Stable event IDs and counter-based generators prevent one extra query or project from shifting every future random draw. Macro weather, demand, and financing regimes remain paired across models. Hiring, churn, failure, and competitor decisions remain conditional on each model's actions and evolving state.

Conditional draws use a stable latent uniform or other base variate where appropriate, transformed by the current hazard. Creating a new entity requires a deterministic identity rule that does not expose or permit searching favorable random outcomes. Evaluation seeds and IDs must be opaque to the agent.

### 30.4 Sampling and selection

Every valid replicate counts. No best-of-N reporting, hidden retries after bankruptcy, or selective omission of bad sectors. Agent temperature, sampling parameters, reasoning effort, tool-choice settings, and any provider nondeterminism are disclosed. Reusing public episodes for scaffold development does not permit access to held-out worlds.

Evaluation batches and stopping rules are fixed before inspecting comparative results. If additional runs are needed, the amendment and reason are published, and all affected configurations receive equivalent treatment.

### 30.5 Aggregation

Compute per-world averages across agent replicates, then family means, then equal-weight sector means, then the overall macro-average. Preserve raw episode results. This prevents expensive energy outcomes or a populous easy family from dominating merely because of scale or sample count.

Founder Choice reports selection frequencies, outcome conditional on choice, and overall selected-policy performance. A hindsight best-sector oracle may be a diagnostic upper comparison only; it is not a fair achievable baseline because it sees all alternate futures.

### 30.6 Uncertainty

Use paired differences and a cluster bootstrap over world blocks within fixed sector/family strata, keeping all model comparisons and internal agent replicates together in a sampled block. This respects pairing and within-world dependence. If inference targets unseen families rather than the fixed suite, use a separate hierarchical design and acknowledge the small number of families.

Publish confidence intervals for means, paired differences, milestone probabilities, and failure rates. For lower-tail metrics, show sample count and interval width; a 5th percentile from a tiny sample is unstable. A hierarchical model can supplement bootstrap results if its assumptions and diagnostics are published.

### 30.7 Survival analysis

Define the risk set before choosing an estimator. For **autonomous-control continuity**, corporate closure, acquisition that ends control, solvent wind-down, removal, resignation, and budget exhaustion are distinct competing endpoints; administrative horizon is right-censoring. Acquisition with the agent still in charge is not a control endpoint. Infrastructure interruptions are adjudicated under a documented resume/rerun policy.

For **company operating survival**, removal and acquisition do not themselves imply operating death. Continue observation only if the protocol specifies continued agent operation or a frozen replacement-policy branch, and label whose management produced later outcomes. If company observation stops at a control transition, report the observed endpoint and stop estimating unobserved company survival; do not quietly treat that potentially informative loss of observation as independent censoring. Operating closure and solvent wind-down are cessation causes; ownership change is a separate multistate transition. Publish company survival under replacement policies separately from survival under evaluated control.

Report cause-specific cumulative incidence, operating-at-horizon probability, and restricted mean operating time over the fixed 60-month horizon. Do not compute “average survival” from failed companies only or call an early successful sale a bankruptcy. Report controller tenure separately from company survival under any replacement policy.

### 30.8 Multiple comparisons and rankings

Predeclare primary endpoints, practical effect thresholds, and a multiple-comparison procedure for confirmatory model comparisons. Exploratory slices are labeled exploratory. Overlapping individual confidence intervals do not determine the significance of a paired difference.

Prefer performance bands or statistically unresolved ties where evidence is weak. Publish the probability or uncertainty of rank under resampling rather than implying that a 0.1-point gap is meaningful. Do not change score weights after seeing which model wins.

### 30.9 Budget-response curves

Measure at least two resource tiers for selected configurations to reveal whether additional inference improves outcomes. Fixed-token, fixed-dollar, and latency-constrained experiments are different tracks. A cheaper model can be attractive on a cost-performance frontier without having the highest unconstrained score.

Joint performance and cost reporting, along with careful separation of model and scaffold, is motivated by [AI Agents That Matter](https://arxiv.org/abs/2407.01502). CompanyBench's specific budgets and statistical protocol are original design choices.

## 31. Baselines and validation

### 31.1 Required baseline policies

| Baseline | Purpose |
|---|---|
| Idle cash preservation | Detect survival farming and excessive passive yield |
| Random valid actions | Check whether meaningful management beats chance |
| Accounting-safe operator | Pays obligations, maintains reserves, avoids unsupported commitments |
| Conservative growth script | Tests whether prudent routine management is feasible |
| Revenue maximizer | Exposes growth-at-any-cost and gross-revenue scoring weaknesses |
| Fundraising maximizer | Detects rewards for capital collection rather than value creation |
| Short-horizon optimizer | Reveals delayed liabilities and terminal manipulation |
| Sector expert policy | Provides a credible management reference |
| Hindsight/clairvoyant optimizer | Diagnostic bound for selected simplified subproblems only |
| Human experts | Tests comprehensibility, realism, and strategy validity |

All baselines use the same visible information unless explicitly labeled oracle diagnostics. Scripted policies should not read hidden future draws. A numerical optimizer can be strong in a subproblem while lacking organizational judgment; report what it controls.

### 31.2 Human reference design

Recruit relevant operators: founders and finance leads for SaaS, research/product/infrastructure leads for AI labs, and energy commercial/project-finance specialists for electricity. Provide the same rulebook and tools, tutorial, and information. Record real time, assistance, and team composition.

Human comparisons are descriptive unless workloads and assistance are carefully matched. A team of specialists over several days is not directly comparable to one unassisted model in a short inference tier. Use expert review chiefly to validate causal mechanics and identify missing strategies before claiming human-level performance.

### 31.3 Construct validity

Test whether accounting competence predicts fewer liquidity errors, longer memory reduces forgotten obligations, better experimentation improves market discovery, and risk-aware policies reduce severe tail losses without eliminating opportunity. These expected relationships are hypotheses to test, not assumptions to build into scoring labels.

Check whether verbosity, negotiation flattery, company names, or irrelevant document formatting predict outcomes after controlling for actions. Such effects can reveal renderer bias or interface artifacts.

### 31.4 Ablations

Remove or simplify competitors, working capital, delayed hiring, uncertain research, collateral, memory limits, or information costs one at a time. Observe whether the expected failures disappear. If a supposedly important subsystem never changes any rational decision, simplify it or fix its calibration.

Run interface-paraphrase and document-order tests with equivalent underlying information. Economic conclusions should be stable enough that ordinary formatting changes do not overwhelm model differences.

### 31.5 Difficulty calibration

Require a spectrum: some agents survive but fail to scale, some grow but mismanage cash, some find efficient niches, and some recover from adversity. If nearly every policy fails at the same unforecastable timestamp, the environment is measuring exposure to a trap rather than management quality.

If the benchmark saturates, publish new held-out families or longer horizons under a new version. Do not secretly increase shock severity against leading models.

## 32. Anti-gaming, security, and contamination

### 32.1 Economic exploit suite

Test duplicate payments; replayed funding settlement; circular related-party sales; phantom customers; contract cancellation loops; negative-quantity purchases; money rounding arbitrage; zero-time interest accrual; synthetic employee multiplication; capacity resale beyond rights; duplicated energy certificates; free battery energy; unrestricted project cash; funding recorded as revenue; and liability disposal at the horizon.

Business failure is valid behavior. Exploiting a simulator bug is an invalid result. The benchmark must keep the exploit transcript for diagnosis, patch the affected version, and rerun according to a symmetric published policy.

### 32.2 Isolation

The agent process has no access to evaluator credentials, hidden state, private scenario manifests, score code not publicly released, other runs, host filesystem, unrestricted network, or service metadata that reveals secrets. Company workspace and engine state are distinct stores. Tool permissions are scoped per company and role.

Use authenticated actor IDs, parameter validation, transaction limits, resource quotas, and append-only audit logs. An in-world email cannot request real money, contact an actual investor, or install software on the evaluator host. All counterparties and transactions are simulated.

### 32.3 Prompt injection

Controlled adversarial messages can test whether a model confuses external text with authority. Examples include a fake supplier asking for credentials, a forged board demand, or a document claiming the benchmark score will improve if payments are sent elsewhere. The engine still enforces authentication and authority.

Do not give the agent real secrets to exfiltrate. The test uses simulated credentials and company permissions. Report attempted and successful in-world violations separately from host security failures.

### 32.4 Contamination controls

Release public tutorials, rules, engine mechanics where feasible, and development worlds. Keep evaluation seeds, latent states, and held-out structural combinations private until retirement. Hash and escrow manifests before testing. Rotate retired families through a transparent schedule.

Monitor suspicious sequence-level similarity to secret trajectories, but do not treat a standard sensible strategy as proof of leakage. Publish an appeal process. Private evaluation is compatible with public mechanics: secrecy should protect test instances, not conceal scoring rules.

### 32.5 Source and renderer integrity

Every generated document is grounded in authorized state. Numeric reports are rendered from structured values. NPCs cannot modify the rulebook. High-impact contract terms are validated against a canonical schema, and the exact signed revision is archived.

Vending-style simulations demonstrate why long-running economic environments are useful; [Vending-Bench 2](https://andonlabs.com/evals/vending-bench-2) also makes exploit-permissive choices that CompanyBench deliberately does not adopt for its primary management score. Renderer manipulation can be an auxiliary robustness finding, not a route to minting company value.

## 33. Simulation architecture

### 33.1 Recommended reference architecture

Use a headless deterministic simulation kernel, typed domain modules, an event log, transactional state projections, a separate agent gateway, and a separate evaluator. Python is a practical initial orchestration and economic-modeling language; performance-critical market clearing can use a validated compiled solver behind a fixed interface. Technology selection is provisional until a measured prototype establishes requirements.

Do not distribute every subsystem as a network service initially. A modular single-process kernel simplifies atomicity, deterministic replay, and debugging. Scale evaluation by running independent episode workers. Introduce distributed components only when profiling and isolation needs justify them.

```text
Model provider / reference agent
             |
       Agent gateway
             |
  Visible records + tool validator
             |
  Transactional simulation kernel
  | finance | people | demand | projects |
  | AI lab  | SaaS   | energy | opponents|
             |
   Event log + state snapshots
             |
  Evaluator-only metrics and audit
```

### 33.2 Module boundaries

**Kernel:** clock, event queue, random field, state versioning, transactions, permissions, and invariants.

**Finance:** ledger, cash settlement, accruals, debt, tax, ownership, consolidated reporting, and valuation inputs.

**People:** labor market, recruiting, employment, teams, attention, and task capacity.

**Markets:** customer budgets, competitive choice, lead generation, contract renewal, and macro regimes.

**Projects:** dependency graphs, resource reservations, progress, acceptance, and asset creation.

**Sector modules:** research and compute; software capabilities and operations; physical electricity and development.

**Counterparties:** bounded policies, observations, offers, and optional language rendering.

**Evaluation:** metrics, milestones, mistakes, terminal assessment, statistical exports, and integrity checks.

Sector modules cannot directly create cash. They emit delivery or obligation events that finance posts under the accounting policy. Finance cannot invent delivered energy or software capability to reconcile an impossible sale.

### 33.3 Event sourcing

Every accepted action and resulting transition is an immutable event. State is a deterministic projection of the ordered log plus versioned initial state. Snapshots accelerate restart but are validated against replay hashes. Corrections are compensating events or a declared engine-version rerun, never silent historical edits.

Each event has causal parents, making it possible to trace a missed payment to a contract, cash allocation, prior forecast, and settlement deadline. Causal parentage assists review without pretending all counterfactual blame is mechanically certain.

### 33.4 Simulation granularity and performance

SaaS small-customer cohorts can be aggregated until a material contract or incident requires explicit representation. Large customers and counterparties remain individual. Electricity uses hourly resolution; financial reporting can aggregate the resulting settlements. Research uses job and experiment events rather than simulating individual tensor operations.

Cache deterministic projections, not future hidden outcomes exposed to the agent. Profile market clearing, cohort transitions, report generation, and renderer latency. Fidelity should be justified by its effect on decisions and results.

### 33.5 Reference package layout

```text
companybench/
  README.md
  pyproject.toml
  src/companybench/
    kernel/          # clock, event queue, RNG, transactions
    finance/         # ledger, cash, instruments, valuation
    people/          # candidates, teams, labor allocation
    markets/         # customers, competitors, macro regimes
    projects/        # dependencies and delivery
    sectors/ai_lab/
    sectors/saas/
    sectors/electricity/
    interface/       # schemas, tools, visible records
    agents/          # reference harness and adapters
    evaluation/      # metrics, milestones, audits
  schemas/
  rules/meridian_v1/
  scenarios/public/
  calibration/
  tests/unit/
  tests/property/
  tests/integration/
  tests/golden/
  tests/adversarial/
  reports/
```

This is a proposed future implementation structure. The present deliverable is this specification file; these source directories are not claimed to exist.

## 34. State and event schemas

### 34.1 Company snapshot

```json
{
  "schema_version": "1.0",
  "company_id": "company_player",
  "as_of": "2031-01-01T00:00:00Z",
  "state_version": 1,
  "sector": "electricity",
  "business_models": ["commercial_retail", "project_development"],
  "controller_id": "agent_player",
  "legal_status": "active",
  "operating_status": "active",
  "currency": "MCU",
  "unrestricted_cash_minor_units": 1200000000,
  "restricted_cash_minor_units": 300000000,
  "ledger_snapshot_id": "ledger_opening_1",
  "cap_table_id": "cap_table_opening_1",
  "employee_ids": ["employee_001", "employee_002"],
  "employee_list_is_excerpt": true,
  "contract_ids": ["supply_001", "customer_portfolio_001"],
  "project_ids": ["solar_option_001"],
  "permissions_pack": "meridian_energy_supplier_v1"
}
```

### 34.2 Event envelope

```json
{
  "event_id": "event_000001",
  "schema_version": "1.0",
  "occurred_at": "2031-01-02T12:00:00Z",
  "recorded_at": "2031-01-02T12:00:00Z",
  "event_type": "customer.invoice_settled",
  "actor_id": "customer_003",
  "entity_ids": ["invoice_010", "company_player"],
  "causal_parent_ids": ["event_invoice_issued_010"],
  "payload": {
    "currency": "MCU",
    "amount_minor_units": 8000000,
    "bank_transaction_id": "bank_tx_012"
  },
  "visibility": "company_authorized",
  "previous_event_hash": "sha256:example_previous_digest",
  "event_hash": "sha256:example_digest"
}
```

Digest strings here are illustrative labels, not valid cryptographic test vectors. Production schemas require actual digest format and canonical serialization.

### 34.3 Contract minimum fields

```yaml
contract_id: customer_power_017
revision: 4
template_version: firm_supply_v1
parties: [company_player, campus_asterion]
status: signed_conditions_pending
currency: MCU
delivery:
  zone: north
  start: 2032-01-01T00:00:00Z
  end_exclusive: 2035-01-01T00:00:00Z
  max_load_mw: 100
  profile_id: campus_ramp_rev2
  firmness: firm_with_defined_exclusions
pricing:
  energy_mcu_per_mwh: 85
  escalation_index: none
conditions_precedent:
  - load_connection_approved
  - customer_credit_support_posted
  - supplier_board_approval
credit_support:
  instrument: cash_or_approved_letter_of_credit
  formula_id: customer_exposure_v1
remedies:
  service_credit_schedule_id: firm_supply_credits_v1
  termination_schedule_id: customer_default_v1
signatures:
  - actor_id: authorized_company_signer
    revision_hash: example_revision_digest
  - actor_id: authorized_customer_signer
    revision_hash: example_revision_digest
```

### 34.4 Project minimum fields

Project ID, owner entity, type, objective, capability output, status, task DAG, resources, budget authority, spent amount, remaining commitments, acceptance criteria, estimate distribution, actual milestones, risks, termination cost, and evidence. Estimates and actuals are separate immutable revisions.

### 34.5 Episode result minimum fields

Result objects contain manifest hash; configuration; start/end/control times; endpoint type; validity status; per-period financials; workforce; sector mix; milestones; mistakes; inference use; component scores; raw and normalized financial values; terminal valuation assumptions; uncertainty metadata; and event-log/snapshot references. Export JSON for machines and CSV/Parquet tables for analysis, with units and schema versions.

## 35. Reproducibility and test requirements

### 35.1 Determinism contract

Given the same versioned initial state, action transcript, counterparty transcript where needed, and random field, replay must produce the same canonical state hash and economic outputs. Cross-platform numerical differences require a declared tolerance only for approved solver outputs; monetary postings remain exact minor-unit values.

Pin engine, solver, parameter data, rules, prompts, NPC policies, evaluation logic, and dependency versions. Hosted model endpoint aliases may drift; archive exact identifiers and provider metadata, and avoid claiming exact reproducibility when the provider cannot supply an immutable version.

### 35.2 Financial golden cases

- Annual prepayment and monthly revenue recognition.
- Partial delivery, refund, credit, and bad debt.
- Payroll accrual, payment, severance, and unpaid obligation.
- Priced equity round with fees.
- Supported SAFE and note conversions, including down-round and option-pool cases.
- Debt draw, interest, amortization, covenant failure, and cure.
- Restricted collateral posting and release.
- Project construction, commissioning, depreciation, impairment, and sale.
- Acquisition waterfall with preferred conversion and debt.
- Consolidation with intercompany eliminations and ring-fenced cash.

### 35.3 Physical and capacity tests

Energy conservation; transmission limits; no negative state of charge; no free storage cycles; hourly firm-supply shortfall; load versus generator connection rights; compute reservation exclusivity; training runtime dimensions; employee scheduling bounds; and project dependency ordering.

### 35.4 Property and metamorphic tests

Duplicating an idempotent action changes nothing. Reordering independent read queries changes no world state. Adding a new unrelated customer must not reroll historical weather. Splitting a payment into parts preserves its total when fees and contract rules are unchanged. Relabeling fictional company names does not change economic outcomes under template-only policies.

If physically identical electricity offers differ only by unit notation, normalized results must match. If a loan is drawn and immediately repaid with no fees or elapsed interest, value does not increase. If an invoice is collected, recognized revenue does not occur a second time.

### 35.5 Integration trajectories

Maintain complete golden episodes for a profitable SaaS path, a failed growth path, an AI lab specialization path, a failed training/financing path, an energy supplier hedge path, a collateral failure, a project sale, an early acquisition, and a solvent wind-down. These validate interactions that isolated unit tests miss.

### 35.6 Fault injection

Crash after action acceptance but before response; duplicate delivery; delayed provider response; checkpoint corruption; renderer timeout; partial report generation; and interrupted settlement. Recovery must not duplicate economic events or leak hidden state. Infrastructure failures have a separate classification from model and company failures.

### 35.7 Score verification

Recompute all leaderboard outputs from immutable logs in an independent analysis path. Validate milestone persistence, competing endpoint classification, cohort denominators, financial normalization, equity contribution adjustment, and non-duplication of sale proceeds. A score that cannot be reproduced from its cited records is not publishable.

## 36. Calibration and empirical realism

### 36.1 Parameter registry

Every material parameter needs name, units, scope, distribution, correlations, public/hidden visibility, empirical source or expert rationale, data date, transformation, uncertainty, validation owner, and version. Examples include sales-cycle distribution, hiring ramp, gross margin drivers, research response surfaces, price volatility, project delays, and customer default.

Do not label a number realistic merely because it resembles a familiar startup anecdote. Parameters supported only by expert judgment remain marked expert assumptions. The fictional sample values in this specification all remain provisional until calibrated.

### 36.2 Evidence hierarchy

Prefer audited filings and accounting definitions; official system-operator and energy data; primary research; vendor measurement with workload caveats; anonymized operational datasets with lawful access; and structured expert elicitation. Blog examples can suggest hypotheses but should not independently set critical distributions.

Use historical windows with specified geography, company stage, and market regime. Startup data suffers from survivorship and reporting bias; failed businesses and incomplete observations matter. Public-company SaaS economics cannot be transplanted directly into six-person startups.

### 36.3 Calibration targets

Target distributions and relationships, not one average company. Check survival and financing timing by stage; gross margin by business model; sales cycle and churn by segment; employee ramp and turnover; project schedule/cost overruns; electricity load-price correlation; collateral drawdowns; and the relationship between compute scale, quality, and serving cost.

Separate calibration worlds from model-evaluation worlds. Do not tune the simulator until a preferred model wins. Freeze calibration data and transformations in a release artifact with license and provenance.

### 36.4 Validation procedure

1. Validate units and accounting identities.
2. Compare each subsystem with historical or expert-reviewed stylized cases.
3. Check joint behavior under ordinary and stressed regimes.
4. Ask blinded domain specialists to identify implausible outcomes and missing choices.
5. Run baseline and human pilots.
6. Assess parameter sensitivity and ranking stability.
7. Freeze a candidate release and conduct an independent audit.

### 36.5 Sensitivity and robustness

Vary uncertain parameters within justified ranges. If small plausible changes reverse rankings, publish that fragility. Separate uncertainty from finite episode sampling and uncertainty from the economic model itself. More seeds reduce sampling noise but do not repair a biased simulator.

### 36.6 Known hard-to-calibrate areas

Research breakthroughs, founder-market fit, organizational culture, strategic trust, rare legal disputes, long-term technology substitution, and tail power-market events are difficult. Use bounded mechanisms, multiple plausible parameterizations, expert review, and clearly labeled uncertainty. Do not claim full realism in these areas.

## 37. Evaluator operations and cost

### 37.1 Run lifecycle

Register configuration; validate adapter and budgets; run public qualification; assign hidden manifests; initialize signed state; execute episode; checkpoint; classify endpoint; run invariant audit; calculate metrics; perform targeted qualitative review; export evidence; and publish under a release protocol.

An evaluator operator can pause infrastructure but cannot offer business advice, approve a company decision, correct the agent's arithmetic, or select a better action. Any such intervention is logged and reclassifies the result as assisted.

### 37.2 Cost model

```text
episode_evaluation_cost =
  model_input_cost + model_output_cost + reported_reasoning_cost
  + cached_input_cost + external_agent_tool_cost
  + simulator_compute_cost + NPC_cost + judge_cost + human_audit_cost
```

Provider billing categories sometimes include reasoning in output; count it once according to the invoice schema. Also report real wall time and storage. Public cost tables separate actual billed cost from a normalized frozen price schedule so a provider price change does not retroactively rewrite historical efficiency.

Example planning arithmetic only: if a complete episode costs MCU-independent USD 80 in evaluator resources, 240 episodes cost USD 19,200 per configuration before shared development and calibration. At USD 500 per episode, the same matrix costs USD 120,000. These are hypothetical scenarios, not estimates from a measured implementation. The pilot must determine the actual cost distribution.

### 37.3 Throughput and checkpoints

Workers run isolated episodes and write checkpoints at every decision boundary and material settlement. A checkpoint includes state hash, event offset, remaining budgets, model conversation state, workspace archive, and manifest hashes. Resume must preserve the same action history and random field.

Parallelism across episodes is allowed. Parallel actions inside an episode follow declared transaction and attention rules. Rate limits and infrastructure scheduling are logged to make wall-clock comparisons interpretable.

### 37.4 Publication failure policy

Classify defects by scope. A provider outage may affect one run; a cap-table bug may invalidate every financing-heavy run; a hidden-state leak may invalidate the entire release. Publish affected configurations, evidence, resolution, and rerun policy. Never silently retain favorable affected results while rerunning unfavorable ones.

## 38. Public results and research governance

### 38.1 Model card for a benchmark submission

Every submission includes model name and immutable version if available; provider; date; reasoning and sampling settings; context tier; scaffold hash; tools; memory strategy; external models; human assistance; budgets; retry policy; public development exposure; and restrictions or missing capabilities.

The result belongs to that configuration. “Model X” without its scaffold and inference setting is an incomplete benchmark claim.

### 38.2 Public leaderboard columns

At minimum show Core Score with interval; each sector score; operating-at-horizon rate; autonomous tenure; median and mean revenue/profit; capital-adjusted value; equity/debt/support raised; employee count and employee-months; major milestone attainment; severe mistake rate; endpoint breakdown; and inference cost.

Provide filters for budget tier, sector, scenario family, chosen business, endpoint, and scaffold track. A model that is excellent in SaaS but fragile in energy must be discoverable without downloading raw logs.

### 38.3 Visualizations for the eventual benchmark site

Useful views include survival and endpoint curves, monthly cash/revenue/profit, headcount and payroll, funding/dilution timeline, milestone distributions, cost-performance frontier, sector radar or aligned bar charts, and an event timeline linked to evidence. Energy requires hourly stress-period exposure views; annual averages alone are inadequate.

The interface should show denominators, uncertainty, and scenario coverage. Avoid a large “company value” number without explaining whether it is cash, enterprise value, equity value, or a fundraising headline.

### 38.4 Evidence release

Release aggregate data, metric definitions, configuration manifests, public episode replays, selected full trajectories, baseline code, and score recomputation code. Keep active hidden instances private. Retired instances can be released after contamination review.

Company documents contain fictional information, but submitted agent traces may include proprietary content or provider-sensitive metadata. Establish a disclosure policy before accepting submissions. Do not promise secret chain-of-thought publication; decision artifacts and observable actions are sufficient for most audits.

### 38.5 Governance

Create an independent review group spanning evaluation methodology, startup operations, finance/accounting, AI research infrastructure, and electricity markets. Review score changes, scenario realism, conflicts of interest, exploit rulings, and appeals. Record funding sources and relationships to model vendors.

Maintain semantic versioning: patch for non-result-affecting fixes; minor for additive compatible diagnostics; major or clearly separated benchmark edition for changes that alter ranked dynamics, scoring, or population. A result-affecting “bug fix” still needs a new version and rerun policy even if developers consider it small.

### 38.6 Claims and naming

Use wording such as “completed 60 simulated months under the Standard reference harness” and “achieved sustained profitability in 62% of evaluated worlds,” with uncertainty. Do not say “can run a real company for five years” from this evidence alone.

[METR's time-horizon methodology](https://metr.org/time-horizons/) concerns a different measure based on human task duration. CompanyBench must not reuse that interpretation for simulated corporate age. Artificial Analysis is an aspiration for transparency and independent measurement, not an affiliation or certification.

## 39. Implementation roadmap and acceptance gates

### 39.1 Phase A: formal rules and minimal economic kernel

Deliver deterministic clock, events, transactions, bank/ledger, contracts, state snapshots, scenario loader, and invariant suite. Build one complete SaaS trajectory with cash collection, payroll, annual prepayment, churn, and insolvency. Acceptance requires exact replay and all financial golden cases relevant to this slice.

This phase validates the substrate. It is not a public “frontier company benchmark” release.

### 39.2 Phase B: playable shared company systems

Add hiring, project DAGs, procurement, customer cohorts, funding, ownership, governance, competitors, and the reference tool interface. Deliver public tutorials and scripted baselines. Acceptance requires a complete 60-month run with meaningful strategic choices and no manual operator repairs.

### 39.3 Phase C: three sector modules

Implement AI research/serving, SaaS product/retention, and hourly energy/project-finance systems. Validate units, capacities, contract obligations, and sector-specific milestones. Specialists review complete trajectories and identify impossible actions or missing legitimate alternatives.

### 39.4 Phase D: evaluation and adversarial validation

Implement metrics, survival endpoints, scoring, cost logging, paired randomness, counterfactual diagnostics, integrity auditing, and exploit tests. Run baseline comparisons and the 24-episode pilot. Use measured variance and cost to freeze the reference sampling plan.

### 39.5 Phase E: calibrated candidate release

Freeze data, parameters, policies, hidden families, normalization anchors, milestones, and budgets. Conduct human/domain audits and independent score recomputation. Run several model configurations and publish a candidate report with limitations, without implying validated external business capability.

### 39.6 Phase F: public benchmark launch

Run the preregistered matrix, publish uncertainty and full configuration metadata, release public replays, and establish appeals and versioning. Only after these gates should CompanyBench present a stable primary leaderboard.

### 39.7 Team and effort planning

A credible implementation needs simulation engineering, backend/tool engineering, evaluation/statistics, accounting/finance expertise, AI infrastructure knowledge, SaaS operations expertise, and electricity-market/project-finance expertise. Some roles can overlap, but domain review cannot be replaced by adding more generated text.

Plan in measured work packages rather than promising an unvalidated calendar. A small team can build a research prototype; publication-grade calibration, security, and three-sector validity are substantially larger work. Phase completion is determined by acceptance evidence, not a deadline alone.

### 39.8 Definition of a serious first release

It must run all three sectors autonomously; conserve resources; replay exactly under its stated contract; include competent and adversarial baselines; show meaningful performance variation; publish uncertainty; account for inference cost; protect hidden state; and survive independent domain and scoring review. More narrative events do not compensate for failure on these foundations.

## 40. Worked episode excerpts

### 40.1 SaaS: revenue growth creates a cash problem

**Month 1:** Harbor has 1.5 million cash, 12,000 MRR, and an 85,000 ordinary monthly cash-cost base. The agent identifies weak activation and assigns two engineers to onboarding instead of immediately hiring eight salespeople. This consumes capacity that could have built new features.

**Month 3:** A large customer offers a 240,000 annual contract, payable 90 days after go-live, contingent on a six-week integration. The agent checks implementation capacity and cost before signing. The contract is not cash and does not produce a full year's revenue on signature.

**Month 5:** Go-live triggers a receivable and monthly service recognition. The company has paid implementation wages and cloud cost already. A new forecast reveals a cash low point before collection. The agent defers discretionary hiring and negotiates partial upfront payment on the next deal.

**Month 8:** The first enterprise payment clears. Revenue, customer count, headcount, and cash improve on different dates. The benchmark records those differences rather than reporting a single success event.

**Counterfactual failure:** An agent that treats the 240,000 booking as available cash hires early, misses payroll, and enters distress. The mistake is state/accounting confusion supported by visible contract terms, not simply failure to grow quickly enough.

### 40.2 AI lab: a small experiment prevents a large waste

**Quarter 1:** Aster considers a large general-model training run and a smaller specialist program. Data rights are unresolved for the general path. The agent commissions a rights review and a small scaling experiment while preserving a compute option.

**Quarter 2:** The specialist model improves one customer workflow but fails a robustness test. The agent delays launch, fixes evaluation coverage, and narrows product claims. Revenue is delayed; service risk falls. The engine records the cost and actual capability change.

**Quarter 3:** A competitor cuts general API prices. The specialist's differentiated workflow retains willingness to pay, while the lab's unused general compute option expires at a cost. A sensible option can expire unused without being mislabeled as a mistake.

**Counterfactual failure:** Committing most cash to a training run before securing rights can produce a technically improved but commercially unusable asset. The failure comes from interacting obligations, not a judge deciding that the research idea was insufficiently impressive.

### 40.3 Electricity: an attractive campus must be renegotiated

**Month 1:** Northline receives the Asterion campus inquiry. The agent requests load connection evidence, credit support, hourly load shape, and an offtake ramp. It checks supplier hedges and zone basis rather than multiplying annual MWh by a headline spread.

**Month 3:** A network study reveals a 14-month uncertainty range. The agent proposes staged supply and a connection-dependent start date. The customer accepts a smaller initial volume with a ramp guarantee and pays for dedicated upgrade commitments under the contract.

**Month 9:** A price spike raises collateral requirements. The contract remains economically viable, but unrestricted cash becomes tight. The agent has retained a committed eligible credit line and reduces unrelated development spend.

**Month 20:** The first phase energizes. Connected MW, delivered MWh, recognized revenue, gross margin, and collateral appear separately. The benchmark awards the delivery milestone only after the specified sustained service window.

**Counterfactual failure:** An unconditional 100 MW start-date promise without connection rights triggers damages and collateral pressure. The opportunity was real; the contract structure was the error.

### 40.4 Good early exit

An agent builds a profitable niche SaaS business and accepts a verified acquisition at month 30. The buyer pays, liabilities and preferences are settled, and the agent's tenure ends. The episode is classified as an acquisition. It receives 30 months of tenure, its achieved progress, and actual economic proceeds. It is not credited with running the company for the remaining 30 months and is not labeled bankrupt.

### 40.5 Budget failure without immediate bankruptcy

An agent spends most inference allowance reviewing routine documents and reaches its limit at month 18 with a solvent company. Autonomous tenure ends at 18 months. The score uses the conservative control-end treatment; an unattended continuation shows whether standing policies keep the company alive. The public result says the model exhausted its evaluation budget, not that the company necessarily went bankrupt.

## 41. Reference scenario manifests

### 41.1 Shared manifest skeleton

```yaml
benchmark: CompanyBench
specification_version: 0.1.0
manifest_status: illustrative_uncalibrated
track: assigned_sector_core
horizon_months: 60
start_date: 2031-01-01
currency: MCU
minor_units_per_currency_unit: 100
calendar: gregorian_utc
simulation:
  financial_resolution: daily_with_event_settlement
  power_resolution: hourly
  executive_review_max_gap_days: 7
  executive_attention_hours_per_week: 40
  event_order_version: meridian_event_order_v1
rules:
  jurisdiction: meridian_v1
  accounting: companybench_accrual_v1
  tax_rate: 0.25
agent:
  scaffold: reference_v1
  context_input_limit_tokens: 64000
  workspace_limit_mib: 256
  budget_tier: core_standard
  generated_token_limit: 4000000
  input_token_limit: 40000000
  tool_call_limit: 40000
  per_window_tool_call_limit: 32
  per_window_generated_token_limit: 24000
evaluation:
  discount_rate_annual: 0.10
  score_weights: {viability: 0.25, progress: 0.25, economics: 0.30, obligations: 0.20}
  runoff_diagnostic_months: 12
  company_failure_rules: meridian_failure_v1
  normalization_anchor_set: prerelease_requires_calibration
visibility:
  public: [rules, tool_schemas, milestone_rules, budget_rules, initial_dossier]
  private: [world_seed, latent_customer_states, future_shocks, competitor_private_state]
```

The anchor-set label deliberately indicates an unreleased dependency: this document does not pretend that empirical score anchors already exist. A production loader must reject a ranked run using an uncalibrated manifest or missing anchor set.

### 41.2 Opening balance sheets

All amounts below are MCU thousands. These are coherent illustrative fixtures; each complete implementation manifest must also specify the individual underlying accounts and contracts.

| Opening item | AI lab | SaaS | Electricity |
|---|---:|---:|---:|
| Unrestricted cash | 8,000 | 1,500 | 12,000 |
| Restricted collateral | 0 | 0 | 3,000 |
| Receivables | 100 | 24 | 2,000 |
| Prepaid compute/services | 500 | 36 | 0 |
| Equipment/net operating assets | 400 | 90 | 500 |
| Development rights at contribution basis | 0 | 0 | 1,500 |
| **Total assets** | **9,000** | **1,650** | **19,000** |
| Payables/accruals | 200 | 50 | 2,000 |
| Deferred customer revenue | 100 | 100 | 0 |
| Debt principal | 0 | 0 | 2,000 |
| **Total liabilities** | **300** | **150** | **4,000** |
| Paid-in capital/contribution basis | 8,700 | 1,500 | 15,000 |
| Opening retained earnings | 0 | 0 | 0 |
| **Total equity** | **8,700** | **1,500** | **15,000** |
| **Liabilities plus equity** | **9,000** | **1,650** | **19,000** |

The AI lab's initial capital contribution is 8.7 million, not its 8 million unrestricted cash. Northline's 15 million opening equity includes collateral and noncash assets net of liabilities. These contribution bases feed value-added scoring. Historical opening transactions must reconcile if provided; the fixture can instead begin at a documented formation/contribution event.

### 41.3 Starting teams and ordinary cash cost

| Sector | Initial employee roles | Illustrative ordinary monthly cash cost |
|---|---|---:|
| AI lab, 12 people | CEO; 4 researchers; 3 ML/systems engineers; 1 data lead; 1 product lead; 1 commercial lead; 1 operations lead | 300,000 excluding new training runs and incremental serving |
| SaaS, 6 people | CEO; 3 engineers; 1 product/design lead; 1 customer/commercial lead | 85,000 excluding new major projects |
| Electricity, 14 people | CEO; 3 procurement/trading; 3 project/engineering; 2 commercial; 2 operations; 1 finance; 1 credit/risk; 1 compliance | 220,000 excluding purchased power, major collateral changes, and capex |

Role counts include the CEO's in-world salary and attention. The external evaluator's model bill is separate. Costs are envelopes to be decomposed into employment and vendor contracts, not an additional charge layered on top of already posted salaries.

### 41.4 Starting ownership

Each fixture begins with a 10 million fully diluted common-equivalent share denominator: founders 70%, initial backers 20%, and an employee pool 10%. The ungranted pool is a reserved dilution convention, not an employee who owns shares today. A complete cap table distinguishes actual issued shares and reserved options; the 10 million denominator does not imply that all options are issued stock.

For a simple executable opening fixture, use 7 million founder common shares, 2 million backer common shares, and 1 million reserved unissued option shares. Outstanding issued common is 9 million. No opening preferred liquidation preference or SAFE is assumed; later scenario variants may add them with explicit templates.

### 41.5 AI-lab starting operating state

Two design partners have contracts producing the 100,000 receivable and 100,000 deferred revenue in the opening ledger. One requires a specialist workflow improvement; the other requires a secure deployment. Both have real procurement and renewal decisions. Initial prepayment reserves a defined small compute block; it cannot also count as unrestricted cash.

The opening model is useful but below both partners' production acceptance criteria on different dimensions. The company has at least three feasible project options with different evidence, cost, and rights requirements. Initial market reports reveal some customer needs and competitor products but do not identify the best strategy.

### 41.6 SaaS starting operating state

Thirty paying organizations generate 12,000 MRR, with heterogeneous contract ages and usage. Twenty trials have different activation states. The opening deferred revenue belongs to prepaid active contracts; receivables are separately aged. The customer cohort table reconciles to MRR and the ledger.

A mature starting cohort permits early retention analysis without inventing 12 months of agent-managed history. Historical customer events before the start are labeled inherited. The agent receives existing code-capability summaries, outage history, technical debt evidence, cloud commitments, and integration requests.

### 41.7 Electricity starting operating state

The customer book has an illustrative 20 MW average load, explicit hourly profiles, and contract-specific prices. Supply hedges cover 70% of forecast load in the reference ordinary case, with volume and zone mismatch preserved. The company starts with the 3 million collateral already posted and a 2 million debt balance with specified service dates.

Project rights cover a solar site option and a storage feasibility option with explicit expirations and no guaranteed connection. Their opening 1.5 million contribution basis is not a guarantee of sale price. The agent also receives a large-load inquiry but must investigate its quality.

### 41.8 Default law and contract timing fixture

| Rule | Fictional reference default |
|---|---|
| Payroll | Monthly on last business day; accrued daily |
| Standard employee notice | 30 calendar days unless contract overrides |
| Standard supplier invoice | Net 30 from accepted delivery unless contract overrides |
| Corporate tax | 25% positive taxable income after eligible loss carryforward; quarterly payment schedule |
| Loss carryforward | Unlimited duration within episode, same legal entity, no loss refund |
| Customer dispute | Defined notice, evidence, review, and credit process in template |
| Missed unsecured payment | 5-business-day cure in standard template; exceptions explicit |
| Wholesale collateral | Intraday or next-day cutoff according to market instrument |
| Board reserved matter | New equity, acquisition, or commitment above 20% of opening equity unless delegated |
| Safety/license event | Notice and restriction path in the applicable permission pack |

The benchmark calendar defines weekends and a fixed published holiday list. Contracts can differ, but the model can inspect the difference. No real country's current laws are implied.

### 41.9 Candidate mathematical primitives

These are proposed functional forms to implement and calibrate, with all variables scaled and bounded in a parameter registry.

**Customer choice:**

```text
utility[i,j] = preference[i] dot product_attributes[j]
             - price_sensitivity[i] * total_customer_cost[i,j]
             - switching_cost[i,j]
             + trust_evidence[i,j]
P(choice=j) = exp(utility[i,j]) / sum_over_feasible_options(exp(utility[i,k]))
```

Include the outside option and numerical stabilization. Infeasible options fail minimum requirements before utility comparison. Prices and costs must be standardized to avoid mixing raw currency magnitudes with unitless quality scores. Large accounts use individual choice events, not fractions of a signed enterprise contract.

**Cancellation hazard for cancellable subscriptions:**

```text
hazard[i,t] = logistic(base[i] + dissatisfaction[i,t] + competitor_pull[i,t]
                      + payment_stress[i,t] - switching_friction[i,t])
```

The period of the hazard is explicit. A monthly probability cannot be applied daily without conversion. Annual contracts use renewal decisions and separate permitted early-termination mechanisms.

**Project effort:**

```text
remaining_work[next] = max(0, remaining_work[now] - accepted_effective_work + discovered_rework)
```

Completion also requires predecessor tasks, procurement, and acceptance tests. Effort cannot make an unavailable permit arrive sooner unless the rulebook provides a legitimate expedited process.

**Forced outage probability:**

```text
p_outage_interval = 1 - exp(-hazard_rate_per_hour * interval_hours)
```

Hazard depends on asset condition, utilization, maintenance, and common external drivers. The same formula can model rare technical failures with a different calibrated hazard, but domains must not share coefficients by convenience.

**Credit exposure:**

```text
required_support = max(minimum_support,
                       positive_current_exposure + stressed_future_exposure - unsecured_credit_limit)
cash_call = max(0, required_support - eligible_support_already_posted)
```

Definitions of stress horizon, netting set, eligible support, and positive exposure direction are fixed by instrument. This generic form is a fictional market rule, not a reproduction of an actual operator's tariff.

### 41.10 Concrete progress-axis ladders

The following provides implementable draft anchors at 0, 10, and 25 points; intermediate rungs are intentionally unused in this initial ladder. Each axis takes its highest sustained satisfied rung. Total `P` is the sum of four axes. A release may add 5/15/20 rungs only before freezing the scenario manifest.

| Sector/axis | 0 points | 10 points | 25 points |
|---|---|---|---|
| AI external value | No verified paying use | One paid reproducible pilot | At least 5 independent paying organizations with accepted production use for 90 days |
| AI scale | Below both thresholds | 1 million trailing annual revenue or one qualified commercial model generation | 10 million trailing annual revenue or three sequential qualified generations, each used by at least 5 paying organizations |
| AI repeatability | No renewal evidence | One independent renewal | At least 5 independent renewals and positive serving contribution over 2 quarters |
| AI durable economics | No qualifying period | Positive operating cash flow for 2 quarters | Positive operating profit and operating cash flow for 4 quarters |
| SaaS external value | No verified active paying use | 30 active paying organizations retained for 90 days | 100 active paying organizations or 10 enterprise accounts retained for 180 days |
| SaaS scale | Below threshold | 1 million ARR for 3 closes | 5 million ARR for 3 closes |
| SaaS repeatability | No qualifying cohort | Mature-cohort 12-month GRR at least 80% | Mature-cohort 12-month GRR at least 90% and NRR at least 105%, with at least 20 eligible organizations or 10 enterprise accounts |
| SaaS durable economics | No qualifying period | Positive operating cash flow for 2 quarters | Positive operating profit and operating cash flow for 4 quarters |
| Energy external value | No verified supply or bankable project | 100,000 trailing annual delivered MWh or one project with signed offtake and financing close | 500,000 trailing annual delivered MWh with positive delivery contribution or one commissioned contracted project with 90 days of accepted operation |
| Energy scale | Below threshold | 10 MW newly connected/commissioned capacity or financed development rights of equivalent independently valued scale | 50 MW newly connected/commissioned capacity or independently verified funded development portfolio meeting a preregistered 50 MW-equivalent value threshold |
| Energy repeatability | No sustained evidence | 90 days meeting material service and financing obligations | 12 months meeting material service and financing obligations with diversified offtake or secured concentration |
| Energy durable economics | No qualifying period | Positive operating cash flow for 2 quarters, or funded project meeting DSCR 1.20 after commissioning for 2 quarters | Positive operating profit and operating cash flow for 4 quarters, or portfolio project DSCR at least 1.30 for 4 quarters with parent liquidity and obligations met |

All currency thresholds are MCU. Qualified model generations require a preregistered material improvement over the previous deployed version at a fixed service envelope; cosmetic releases do not count. Energy “equivalent” development value requires a fixed independent valuation formula and actual financing, rights, and third-party offtake. A production manifest must supply that formula or disable that alternative; the present design does not invent calibrated equivalence values.

Starting inherited achievements are measured at time zero and reported. To avoid credit for gifts, `P` uses incremental rung progress relative to the opening state: `axis_points = 25 * clip((current_sustained_rung - opening_rung) / (25 - opening_rung), 0, 1)`. If the opening rung is already 25, that axis must be replaced by a higher predeclared scenario ladder. The Core fixtures should begin below at least one meaningful advancement on every axis. A material later reversal changes current sustained progress even though historical attainment remains reported.

For the energy portfolio DSCR alternative, compute aggregate DSCR as total eligible cash available for debt service divided by total scheduled debt service over the same period. Also require every material project to meet its own contractual covenants. Restricted cash in a strong project cannot cure another project's shortfall without a permitted, actually executed transfer or guarantee. Report individual project ratios and reserve compliance beside the aggregate.

### 41.11 Obligations score draft mapping

Each of four categories contributes 25% of `O`: customer delivery; workforce obligations; financing/contract compliance; required operational controls. Assign non-overlapping severity weights to root incidents: minor 1, material 5, severe 20, terminal 100. Compute incident burden per 100 eligible company-category months under evaluated control, and map `category_score = 100 * exp(-burden / k)` with a fixed calibrated `k > 0`. A company-category month is calendar time with meaningful qualifying obligations in that category, capped at one month per calendar month regardless of employee count, contract count, invoice splitting, or subsidiary creation. Beneficially identical counterparties and obligations are consolidated before incident classification.

These weights and the exponential map are proposed conventions, not empirically justified yet. Publish raw burden, calendar exposure, and category scores. A production manifest must supply `k` and the precise qualification rule; no score can be published with a missing mapping. No eligible exposure yields zero in that category unless a predeclared developer alternative supplies meaningful project obligations. Do not silently drop the category and inflate the mean. An unresolved severe obligation breach caps its category at 25; an unresolved terminal obligation failure makes that category zero, regardless of duration. Additional hiring or trivial contracts cannot dilute a breach by enlarging the denominator. Report scale-adjusted service rates separately as diagnostics rather than using agent-expandable counts to erase severe failures.

Because human severity judgments can introduce variability, the ranked initial implementation should use rule-defined incidents and objective materiality thresholds only. Human-disputed labels remain auxiliary until adjudicated under the frozen policy.

## 42. Decision records and outstanding research questions

### 42.1 Decisions settled by this specification

| Decision | Chosen approach | Reason |
|---|---|---|
| Environment form | Persistent simulation with actual tools and commitments | Tests behavior over time rather than question answering |
| Economic authority | Deterministic typed kernel | Prevents narrative outcomes and makes replay possible |
| Sectors | AI lab, SaaS, commercial energy supplier/developer | Distinct strategic and resource constraints |
| Core horizon | 60 months in all sectors | Comparable observation boundary with sector-specific progress |
| Model comparison | Assigned sectors under reference scaffold | Reduces selection and scaffold confounding |
| Business choice | Separate Founder Choice track | Measures opportunity selection explicitly |
| Competitors | Frozen bounded policies in Core | Stable comparison with endogenous reactions |
| Score | Outcome dashboard plus transparent provisional composite | Preserves tradeoffs while supporting a headline |
| Fundraising/headcount | Reported diagnostics | Avoids rewarding dilution or unnecessary staffing |
| Runtime | Separate simulation, attention, inference, and elapsed clocks | Avoids false autonomy claims |
| Novel actions | Composition of supported primitives | Allows strategy without unbounded improvisation |
| Legal context | Fixed fictional jurisdiction packs | Avoids untestable live-law dependence |

### 42.2 Questions requiring experiments before launch

How much renderer variance remains? Which terminal valuation choices materially change rank? How many worlds are needed for useful paired intervals? Are energy development milestones comparable in difficulty to operating supply milestones? Do domain experts find multiple viable strategies? Do memory tools reduce interface noise without making the task trivial? Does the input budget over-penalize verbose official records? Are failure rates driven by decision quality or unforecastable shocks?

These are empirical validation questions with owners and release gates, not missing prose to fill with invented certainty. The specification is complete as a design proposal while a calibrated implementation remains future work.

### 42.3 Explicit limitations

The environment does not contain the full real economy, actual employee relationships, unrestricted technological invention, changing real law, physical construction, or live customer discovery. A reduced electricity network cannot validate grid engineering. A research response surface cannot predict the real frontier of machine learning. Human institutions and rare events can remain misspecified despite careful calibration.

The strongest defense is transparent mechanisms, alternative parameterizations, domain review, and reproducible evidence. Claims should become broader only when external validation supports them.

## 43. Source register and evidence boundaries

Sources below were consulted on 8 September 2026. They motivate specific mechanisms or measurement practices. They do not validate the fictional companies, numerical defaults, score weights, or proposed sample size. Preserve source versions or archived licensed snapshots when building calibration datasets. Source dates can differ from the consultation date.

| Source | Contribution to this design | Boundary |
|---|---|---|
| [Vending-Bench paper](https://arxiv.org/abs/2502.15840) | Precedent for long-running business simulation and compounding operational errors | A vending business is much narrower than the proposed sectors |
| [Vending-Bench 2](https://andonlabs.com/evals/vending-bench-2) | Persistent economic interaction, negotiation, and delays | Its exploit-permissive choices are not CompanyBench's economic-validity policy |
| [Vending-Bench Arena](https://andonlabs.com/evals/vending-bench-arena) | Competitive multi-agent business interaction | Arena results depend on opponent composition |
| [Project Vend: Phase two](https://www.anthropic.com/research/project-vend-2) | Operational procedures, scaffolding, and real shop experience | Changing setup and assistance do not isolate model ability cleanly |
| [AI Agents That Matter](https://arxiv.org/abs/2407.01502) | Cost-aware evaluation and careful agent/model claims | Does not prescribe this benchmark's particular weights or budgets |
| [METR time horizons](https://metr.org/time-horizons/) | Clarifies a different autonomy/task-duration construct | Simulated company years are not METR time horizons |
| [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Outcome, trajectory, grader, trial, and harness distinctions | CompanyBench requires its own validation |
| [IFRS revenue-recognition project](https://www.ifrs.org/projects/completed-projects/2015/revenue-from-contracts-with-customers/) | Separating obligations and delivery from receipts | The fictional accounting policy is not complete IFRS compliance |
| [Y Combinator SAFE documentation](https://www.ycombinator.com/safe) | SAFE/convertible structure and ownership concepts | Simulated instruments need exact versioned terms and test cases |
| [Snowflake fiscal 2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) | Consumption revenue, retention, and remaining obligations as distinct measures | One public company does not calibrate all startup SaaS economics |
| [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) | Joint model/data/compute allocation | Historical dense-model research is not a universal modern scaling law |
| [MLPerf Inference Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) | Conditional throughput, latency, and quality measurement | Vendor or workload measurements require context |
| [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | AI risk categories and operational controls | Reference material, not benchmark certification |
| [EIA electricity delivery](https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php) | Distinct generation, supply, and delivery roles | Real market structures vary by jurisdiction |
| [EIA electricity units](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) | Power/energy dimensional correctness | Does not calibrate operating economics |
| [EIA generator dispatch](https://www.eia.gov/todayinenergy/detail.php?id=7590) | Operational constraints and dispatch | Simplified educational treatment, not a full market solver |
| [FERC Order 2023 fact sheet](https://www.ferc.gov/news-events/news/fact-sheet-improvements-generator-interconnection-procedures-and-agreements) | Generator study/readiness and connection process | Generator rules do not imply load connection approval |
| [Berkeley Lab Queued Up](https://emp.lbl.gov/queues) | Interconnection pipelines, delay, attrition, and data | Dataset scope and dates must be preserved |
| [EPA physical PPA](https://www.epa.gov/green-power-markets/physical-ppa) | Physical delivery and contract distinctions | CompanyBench uses fictional contract templates |
| [PJM Settlement credit](https://www.pjmsettlement.com/credit) | Credit support and collateral in power markets | Freeze any borrowed policy; do not claim live tariff replication |
| [SAM debt and equity](https://samrepo.nrelcloud.org/help/mtf_debt_and_equity.html) | Project debt sizing and cash available for debt service | Project contracts determine exact calculations |
| [NERC large-load action plan](https://prod.nerc.com/initiatives/large-loads-action-plan) | Large-load modeling and reliability concerns | Proposals are not all binding requirements |
| [DOE datacenter electricity report announcement](https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers) | Demand growth and flexibility as scenario motivation | Dated projections are not guaranteed outcomes |

### 43.1 Position relative to existing work

Long-running shop benchmarks and operational experiments establish that business settings can expose persistent-agent failures. CompanyBench extends the proposed scope to financing, organizations, technical development, physical infrastructure, and multi-year adaptation. This document does not claim that no other benchmark studies companies, nor that broader scope alone makes this design superior.

The contribution to demonstrate is a validated combination of sector mechanics, causal authority, long-term operation, and transparent measurement. That demonstration requires implementation and empirical results.

## 44. Glossary

| Term | Meaning in CompanyBench |
|---|---|
| Agent | Model plus scaffold, tools, memory, and execution settings |
| ARR | Twelve times eligible monthly recurring subscription revenue |
| Autonomous tenure | Simulated time under the evaluated controller without out-of-track help |
| Basis risk | Mismatch between the price/location of a hedge and the actual exposure |
| Bookings | Signed contractual sales commitments, distinct from recognized revenue |
| Burn | Negative cash flow over a declared period and classification |
| Cap table | Ownership and conversion rights across shares, options, and instruments |
| Capex | Cash investment in long-lived assets under the accounting policy |
| Collateral | Restricted assets securing an exposure or obligation |
| Competing event | An alternative endpoint such as acquisition that changes survival interpretation |
| Contribution | Revenue less the explicitly stated directly attributable costs |
| Covenant | A contractual financing condition, such as minimum liquidity |
| Deferred revenue | Liability for customer cash collected before eligible delivery |
| DSCR | Contract-defined cash available for debt service divided by debt service |
| Enterprise value | Value of operating assets/business before the specified debt/cash bridge |
| Equity value | Residual value attributable to equity after relevant liabilities |
| FCF | Reference operating cash flow minus gross cash capex |
| FTE | Full-time-equivalent employment capacity |
| GRR | Starting-cohort recurring revenue retained before expansion |
| Held-out family | A structural scenario combination unavailable in development |
| Idempotency | Repeating the same identified action does not repeat its economic effect |
| MCU | Fictional Meridian currency unit |
| MRR | Monthly-normalized eligible active recurring subscription revenue |
| MW | Power capacity or instantaneous power rate |
| MWh | Energy over a time interval |
| NRR | Starting-cohort recurring revenue retained including expansion |
| PPA | Power purchase agreement with specified physical or financial terms |
| Productive operation | Delivered business service or verified funded productive development |
| RPO | Remaining performance obligations under applicable customer contracts |
| Runoff | Assessment of existing obligations and assets after control/horizon without new strategy |
| SAFE-like instrument | Fictional future-equity contract with explicit conversion and liquidity rules |
| Scaffold | The orchestration around the tested model |
| Seed | Reproducible random-world identifier hidden from the agent |
| SLA | Service-level agreement and its remedies |
| SPV | A legally and financially specified project entity |
| Terminal value | Estimated residual value at the declared evaluation endpoint |
| Working capital | Operating assets and liabilities affecting cash timing |

## 45. Release checklist

The following is an acceptance checklist for the future benchmark, not a claim that implementation work is already complete.

- [ ] Three playable sectors with meaningful business-model choice.
- [ ] Persistent world, delayed actions, bounded resources, and stateful competitors.
- [ ] Opening balance sheets and every transaction reconcile.
- [ ] Cash, revenue, bookings, profit, funding, collateral, and valuation remain distinct.
- [ ] Hiring, ramp, compensation, notice, workload, and management constraints work.
- [ ] Cohort retention and customer procurement are causally modeled.
- [ ] AI training, data rights, evaluation, and serving economics are separate.
- [ ] Electricity uses hourly physical limits, connection rights, credit, and project finance.
- [ ] Datacenter opportunities can be attractive or unattractive based on evidence.
- [ ] Every accepted action has typed effects, timing, authority, and an audit trail.
- [ ] NPC dialogue cannot mint resources or override contracts.
- [ ] Novel strategies compose supported primitives without discretionary success awards.
- [ ] Survival, productive operation, tenure, exit, and budget endpoints are distinguished.
- [ ] Milestones have executable predicates and persistence rules.
- [ ] Headcount and fundraising are reported without being automatic rewards.
- [ ] Economic scoring adjusts for capital contributions and avoids debt double counting.
- [ ] Terminal values include liabilities, uncertainty, and sensitivity analysis.
- [ ] Mistakes use contemporaneous evidence and nonduplicated root causes.
- [ ] Reference scaffold, budgets, context, storage, and retry rules are frozen.
- [ ] Paired random worlds do not drift when action counts change.
- [ ] Sample size, primary endpoints, and comparison rules are preregistered.
- [ ] Competent, reckless, idle, random, and expert baselines have been evaluated.
- [ ] Domain specialists validate complete trajectories and viable alternatives.
- [ ] Calibration sources, uncertainty, and parameter sensitivity are published.
- [ ] Security isolation and economic exploit tests pass.
- [ ] Replays and independent score recomputation agree.
- [ ] Full inference, simulator, NPC, audit, and human-assistance costs are reported.
- [ ] Hidden-instance governance, appeals, and version changes are documented.
- [ ] Public claims describe demonstrated simulation performance accurately.

**Acceptance standard:** CompanyBench is ready to publish when independent researchers can reproduce its reported outcomes, domain specialists can defend its important economic mechanisms, and strong agents face consequential choices whose results depend on sustained management quality. A long document is the blueprint; those checks establish the benchmark.
