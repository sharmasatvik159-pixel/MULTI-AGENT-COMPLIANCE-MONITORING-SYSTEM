# Formal Consensus Algorithm & Mathematical Evidence Specification
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D3-CA-v2.0`  
**Classification:** Tier-2 Global Banking Architecture Specification  
**Author:** AI Systems Architect, Zetheta Algorithms  

---

## 1. Mathematical Consensus Problem Formulation

In the Meridian compliance monitoring ecosystem, autonomous agents evaluate potential regulatory infractions across heterogeneous surveillance modalities:
* $\text{Agent } \text{TM-01}$: Operates over high-frequency structured market feeds, tick data, and payment ledgers.
* $\text{Agent } \text{CS-01}$: Operates over unstructured multilingual communication transcripts, audio streams, and sentiment lexicons.
* $\text{Agent } \text{RU-01}$: Operates over statutory definitions, legal precedents, and cross-border regulatory circulars.

When an entity is investigated, each agent produces an independent belief function. The **Consensus Engine** must synthesize these disparate signals into a unified, mathematically defensible decision state while quantifying inter-agent conflict and preventing false-positive escalations.

---

## 2. Confidence Calibration Formulation

Raw machine learning model probabilities $S_a \in [0, 1]$ (e.g., neural network softmax outputs or isolation forest anomaly scores) are notorious for being poorly calibrated in low-base-rate domains such as financial fraud. The Consensus Engine first maps each agent's raw detection score $S_a$ to a **Calibrated Confidence Metric** $C_a \in [0, 1]$ using historical empirical validation statistics:

$$C_a = P(V \mid S_a) = \frac{\alpha_a \cdot S_a}{\alpha_a \cdot S_a + \beta_a \cdot (1 - S_a)}$$

Where:
* $V$: The proposition that a genuine statutory violation has occurred.
* $\alpha_a = P(S_a \ge \tau \mid V)$: The **Historical True Positive Rate (Sensitivity)** of Agent $a$ on benchmark scenarios.
* $\beta_a = P(S_a \ge \tau \mid \neg V)$: The **Historical False Positive Rate (1 - Specificity)** of Agent $a$.
* $S_a$: The normalized raw anomaly score output by Agent $a$ ($0.0 \le S_a \le 1.0$).

### 2.1 Empirical Agent Calibration Parameters

```
+---------------------------------------------------------------------------------------------------+
| AGENT IDENTIFIER | SURVEILLANCE DOMAIN            | HISTORICAL TPR (α) | HISTORICAL FPR (β) | NOISE (ε) |
+---------------------------------------------------------------------------------------------------+
| TM-01            | High-Speed Trade Surveillance  | 0.94               | 0.04               | 0.08      |
| CS-01            | Multimodal NLP Communication   | 0.88               | 0.07               | 0.12      |
| RU-01            | Regulatory Ingestion & Diffing | 0.98               | 0.01               | 0.04      |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Dempster-Shafer Theory (DST) Evidence Fusion

To fuse calibrated confidence scores while accounting for uncommitted ignorance, Meridian employs **Dempster-Shafer Theory of Evidence**.

### 3.1 Frame of Discernment ($\Theta$)
The discrete frame of discernment contains mutually exclusive exhaustive outcomes:

$$\Theta = \{V, \; \neg V\}$$

Where:
* $V$: Regulatory Violation Present.
* $\neg V$: Benign Activity / Legitimate Business Action.

The power set $2^\Theta$ comprises:

$$2^\Theta = \{\emptyset, \; \{V\}, \; \{\neg V\}, \; \{V, \neg V\}\}$$

Where $\{V, \neg V\} \equiv \Theta$ represents **epistemic uncertainty** (uncommitted belief).

### 3.2 Basic Belief Assignment (BBA) Mapping
Each agent $a$ maps its calibrated confidence $C_a$ and observational noise parameter $\epsilon_a \in (0, 0.20)$ into a valid mass function $m_a: 2^\Theta \to [0, 1]$ satisfying $\sum_{A \subseteq \Theta} m_a(A) = 1$:

$$m_a(\{V\}) = C_a \cdot (1 - \epsilon_a)$$

$$m_a(\{\neg V\}) = (1 - C_a) \cdot (1 - \epsilon_a)$$

$$m_a(\Theta) = \epsilon_a$$

$$m_a(\emptyset) = 0$$

### 3.3 Dempster's Rule of Combination
To combine evidence from two independent agents $m_1$ and $m_2$, the orthogonal sum $m_{1,2} = m_1 \oplus m_2$ is computed:

$$m_{1,2}(A) = \frac{\sum_{B \cap C = A} m_1(B) \cdot m_2(C)}{1 - K} \quad \forall A \neq \emptyset$$

Where the **Inter-Agent Conflict Metric ($K$)** measures the degree of direct contradiction:

$$K = \sum_{B \cap C = \emptyset} m_1(B) \cdot m_2(C) = m_1(\{V\}) \cdot m_2(\{\neg V\}) + m_1(\{\neg V\}) \cdot m_2(\{V\})$$

* **Conflict Threshold Handling:**
  * If $K < 0.65$: Normal Dempster combination proceeds.
  * If $0.65 \le K < 0.85$: **Yager's Modified Combination Rule** is applied, reallocating conflicting belief masses to uncommitted uncertainty $m(\Theta)$ rather than artificially inflating certainty.
  * If $K \ge 0.85$: Severe conflict deadlock (**Zadeh's Paradox** boundary); combination is suspended, and the event is routed directly to the Conflict Arbiter (Tier 3 Manager).

---

## 4. Worked Step-by-Step Mathematical Example

### Scenario Context: Spoofing Surveillance with Ambiguous Communications
* **Observation:** `TM-01` flags algorithmic crude oil futures trading exhibiting high order cancellation rates ($OTR = 35:1$ within 250ms).
* **Communication Context:** `CS-01` scans the desk's Bloomberg chat transcripts and finds general market commentary without overt conspiratorial phrases.

### Step 1: Compute Calibrated Confidence
* **`TM-01` Calculation:**
  * Raw anomaly score: $S_{\text{TM}} = 0.90$.
  * Historical rates: $\alpha_{\text{TM}} = 0.94, \; \beta_{\text{TM}} = 0.04$.
  $$C_{\text{TM}} = \frac{0.94 \times 0.90}{(0.94 \times 0.90) + (0.04 \times 0.10)} = \frac{0.846}{0.846 + 0.004} = \frac{0.846}{0.850} \approx \mathbf{0.995}$$
  * For conservatism, system caps individual single-agent confidence at **0.850**: $C_{\text{TM}} = 0.850$.
* **`CS-01` Calculation:**
  * Raw NLP intent score: $S_{\text{CS}} = 0.20$ (benign chatter dominates).
  * Historical rates: $\alpha_{\text{CS}} = 0.88, \; \beta_{\text{CS}} = 0.07$.
  $$C_{\text{CS}} = \frac{0.88 \times 0.20}{(0.88 \times 0.20) + (0.07 \times 0.80)} = \frac{0.176}{0.176 + 0.056} = \frac{0.176}{0.232} \approx \mathbf{0.758}$$
  * Let us test a case where `CS-01` actively evaluates the communication as benign: $C_{\text{CS}} = 0.200$.

### Step 2: Formulate Basic Belief Mass Functions
* **Agent `TM-01` Mass Function ($\epsilon_{\text{TM}} = 0.10$):**
  $$m_{\text{TM}}(\{V\}) = 0.850 \times (1 - 0.10) = \mathbf{0.765}$$
  $$m_{\text{TM}}(\{\neg V\}) = (1 - 0.850) \times (1 - 0.10) = 0.150 \times 0.90 = \mathbf{0.135}$$
  $$m_{\text{TM}}(\Theta) = \mathbf{0.100}$$
  *Verification:* $0.765 + 0.135 + 0.100 = 1.000$.

* **Agent `CS-01` Mass Function ($\epsilon_{\text{CS}} = 0.15$):**
  $$m_{\text{CS}}(\{V\}) = 0.200 \times (1 - 0.15) = \mathbf{0.170}$$
  $$m_{\text{CS}}(\{\neg V\}) = (1 - 0.200) \times (1 - 0.15) = 0.800 \times 0.85 = \mathbf{0.680}$$
  $$m_{\text{CS}}(\Theta) = \mathbf{0.150}$$
  *Verification:* $0.170 + 0.680 + 0.150 = 1.000$.

### Step 3: Compute Orthogonal Intersections & Conflict Metric ($K$)

```
+---------------------------------------------------------------------------------------------------+
| INTERSECTION (B ∩ C)         | TM-01 FOCAL MASS         | CS-01 FOCAL MASS         | PRODUCT      |
+---------------------------------------------------------------------------------------------------+
| {V} ∩ {V} = {V}              | m_TM({V}) = 0.765        | m_CS({V}) = 0.170        | 0.13005      |
| {V} ∩ {¬V} = ∅ (CONFLICT)    | m_TM({V}) = 0.765        | m_CS({¬V}) = 0.680       | 0.52020      |
| {V} ∩ Θ = {V}                | m_TM({V}) = 0.765        | m_CS(Θ) = 0.150          | 0.11475      |
| {¬V} ∩ {V} = ∅ (CONFLICT)    | m_TM({¬V}) = 0.135       | m_CS({V}) = 0.170        | 0.02295      |
| {¬V} ∩ {¬V} = {¬V}           | m_TM({¬V}) = 0.135       | m_CS({¬V}) = 0.680       | 0.09180      |
| {¬V} ∩ Θ = {¬V}              | m_TM({¬V}) = 0.135       | m_CS(Θ) = 0.150          | 0.02025      |
| Θ ∩ {V} = {V}                | m_TM(Θ) = 0.100          | m_CS({V}) = 0.170        | 0.01700      |
| Θ ∩ {¬V} = {¬V}              | m_TM(Θ) = 0.100          | m_CS({¬V}) = 0.680       | 0.06800      |
| Θ ∩ Θ = Θ                    | m_TM(Θ) = 0.100          | m_CS(Θ) = 0.150          | 0.01500      |
+---------------------------------------------------------------------------------------------------+
```

* **Compute Total Conflict $K$:**
  $$K = 0.52020 + 0.02295 = \mathbf{0.54315}$$
* **Normalization Denominator:**
  $$1 - K = 1 - 0.54315 = \mathbf{0.45685}$$

### Step 4: Aggregate Focal Elements & Normalize
* **Numerator for $\{V\}$:**
  $$\text{Numerator}(\{V\}) = 0.13005 + 0.11475 + 0.01700 = \mathbf{0.26180}$$
  $$m_{\text{TM,CS}}(\{V\}) = \frac{0.26180}{0.45685} \approx \mathbf{0.5730}$$

* **Numerator for $\{\neg V\}$:**
  $$\text{Numerator}(\{\neg V\}) = 0.09180 + 0.02025 + 0.06800 = \mathbf{0.18005}$$
  $$m_{\text{TM,CS}}(\{\neg V\}) = \frac{0.18005}{0.45685} \approx \mathbf{0.3941}$$

* **Numerator for $\Theta$ (Uncertainty):**
  $$\text{Numerator}(\Theta) = 0.01500$$
  $$m_{\text{TM,CS}}(\Theta) = \frac{0.01500}{0.45685} \approx \mathbf{0.0328}$$

* **Verification of Unity:**
  $$0.5730 + 0.3941 + 0.0328 = 0.9999 \approx \mathbf{1.000}$$

### Step 5: Decision Resolution & Action Trigger
1. **Conflict Evaluation:** $K = 0.543$ indicates moderate conflict (below the $0.65$ deadlock threshold).
2. **Belief vs Plausibility:**
   * $\text{Bel}(V) = m(\{V\}) = \mathbf{0.573}$.
   * $\text{Pl}(V) = m(\{V\}) + m(\Theta) = 0.573 + 0.033 = \mathbf{0.606}$.
3. **Escalation Decision:**
   * Because $\text{Bel}(V) < 0.80$, the system does **not** trigger an automatic SAR compilation.
   * However, because $K > 0.40$ and $\text{Bel}(V) > 0.50$, the event is classified as **MEDIUM ALERT (Priority 3)** and routed to **Tier 2 (Senior Analyst)** for contextual review with an automated request to inspect execution venue logs.
