# Formal Consensus Algorithm & Mathematical Evidence Specification
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D3-CA-v1.0`  
**Classification:** Tier-2 Global Banking System Architecture  
**Author:** AI Systems Architect, Zetheta Algorithms  

---

## 1. Consensus Objective & Problem Formulation

In a multi-agent compliance surveillance architecture, autonomous agents frequently evaluate the same underlying entity through distinct observational modalities:
* `TM-01` evaluates numerical market anomalies and transaction timings.
* `CS-01` evaluates unstructured communication transcripts and semantic intent.
* `RU-01` evaluates statutory definitions and cross-border regulatory mandates.

When these agents observe an event, their subjective assessments may align, diverge, or directly contradict. The consensus engine must synthesize these heterogeneous probability signals into a unified, mathematically defensible belief state while quantifying inter-agent conflict.

---

## 2. Mathematical Formalization: Dempster-Shafer Theory of Evidence

Meridian deploys **Dempster-Shafer Theory (DST)** augmented with **Bayesian Posterior Calibration**. Unlike standard Bayesian inference which requires complete prior probability distributions that are difficult to justify during novel market manipulation schemes, DST explicitly models ignorance and epistemic uncertainty.

### 2.1 Frame of Discernment ($\Theta$)
For any investigated entity or transaction cluster, the frame of discernment $\Theta$ consists of mutually exclusive propositions:

$$\Theta = \{V, \; \neg V\}$$

Where:
* $V$: A regulatory violation has occurred.
* $\neg V$: No regulatory violation has occurred (legitimate transaction / false positive).

The power set $2^\Theta$ contains all possible hypothesis subsets:

$$2^\Theta = \{\emptyset, \; \{V\}, \; \{\neg V\}, \; \{V, \neg V\}\}$$

Where $\{V, \neg V\}$ represents **total uncertainty / uncommitted belief** (ignorance).

### 2.2 Basic Belief Assignment (Mass Function $m$)
Each agent $i \in \{\text{TM}, \text{CS}, \text{RU}\}$ assigns a basic belief mass $m_i: 2^\Theta \to [0, 1]$ satisfying:

$$m_i(\emptyset) = 0 \quad \text{and} \quad \sum_{A \subseteq \Theta} m_i(A) = 1$$

* $m_i(\{V\})$: Direct belief that a violation occurred.
* $m_i(\{\neg V\})$: Direct belief that the activity is benign (e.g., pre-cleared block trade).
* $m_i(\{V, \neg V\})$: Uncommitted epistemic uncertainty (the degree of lack of evidence).

### 2.3 Dempster's Rule of Combination
To combine independent evidence masses from two agents $m_1$ and $m_2$, Dempster's orthogonal sum $m_{1,2} = m_1 \oplus m_2$ is computed:

$$m_{1,2}(A) = \frac{\sum_{B \cap C = A} m_1(B) \cdot m_2(C)}{1 - K} \quad \forall A \neq \emptyset$$

Where $K$ represents the **measure of inter-agent conflict**:

$$K = \sum_{B \cap C = \emptyset} m_1(B) \cdot m_2(C)$$

* **Conflict Interpretation:**
  * When $K \to 0$: Agents are in complete consensus.
  * When $K > 0.65$: Critical inter-agent conflict is detected (e.g., `TM-01` reports 0.90 probability of wash trading, while `CS-01` finds documented pre-negotiated institutional block rebalancing matching CS-18).
  * If $K \ge 0.85$ (Zadeh's Paradox boundary): Normal combination is halted, and the conflict arbiter triggers immediate human Tier 3 review rather than computing a misleading artifact.

```mermaid
flowchart TD
    subgraph AgentBeliefs["Independent Agent Evidence"]
        TM_Mass["TM-01 Mass Function<br/>m_TM({V}), m_TM(¬V), m_TM(Θ)"]
        CS_Mass["CS-01 Mass Function<br/>m_CS({V}), m_CS(¬V), m_CS(Θ)"]
        RU_Mass["RU-01 Mass Function<br/>m_RU({V}), m_RU(¬V), m_RU(Θ)"]
    end

    subgraph ConflictCheck["Conflict Measurement (K)"]
        K_Calc["Compute Conflict Metric K<br/>K = Σ m_1(B) * m_2(C) for B ∩ C = ∅"]
    end

    subgraph ResolutionPath["Consensus Decision Logic"]
        NormalDST["Dempster's Rule Orthogonal Sum<br/>m_combined(V) >= 0.80"]
        YagerFallback["Yager Modified Combination Rule<br/>Allocate Conflict to Uncertainty Θ"]
        HumanArbiter["Trigger Conflict Arbiter<br/>Tier 3 Compliance Review"]
    end

    TM_Mass & CS_Mass & RU_Mass --> K_Calc
    K_Calc -->|K < 0.65| NormalDST
    K_Calc -->|0.65 <= K < 0.85| YagerFallback
    K_Calc -->|K >= 0.85 (High Conflict)| HumanArbiter
```

---

## 3. Bayesian Belief Updating for Continuous Monitoring

When surveillance spans multi-day rolling windows (such as insider trading accumulation over 3 weeks in CS-01), the posterior belief $P(V \mid E_t)$ is updated recursively via Bayes' rule:

$$P(V \mid E_{1:t}) = \frac{P(E_t \mid V) \cdot P(V \mid E_{1:t-1})}{P(E_t \mid V) \cdot P(V \mid E_{1:t-1}) + P(E_t \mid \neg V) \cdot P(\neg V \mid E_{1:t-1})}$$

Where:
* $P(V \mid E_{1:t-1})$ is the prior probability from previous days.
* $P(E_t \mid V)$ is the likelihood of observed trade/chat patterns given an active insider trading scheme.
* Prior probabilities are calibrated using historical enforcement rates (e.g., baseline market abuse prior $P(V) \approx 0.001$).

---

## 4. Concrete Consensus Trace: Scenario CS-18 (False Positive Block Trade)

In **CS-18**, an institutional client executes a $450 million block trade (8% of Average Daily Volume):
1. **`TM-01` Evaluation:**
   * Raw trade volume surge triggers threshold breach.
   * However, `TM-01` queries the block trade desk registry and finds valid pre-trade documentation.
   * $m_{\text{TM}}(\{V\}) = 0.15, \quad m_{\text{TM}}(\{\neg V\}) = 0.75, \quad m_{\text{TM}}(\Theta) = 0.10$.
2. **`CS-01` Evaluation:**
   * Scans institutional order desk communication channels.
   * Verifies standard client mandate confirmation, no off-channel chatter.
   * $m_{\text{CS}}(\{V\}) = 0.05, \quad m_{\text{CS}}(\{\neg V\}) = 0.85, \quad m_{\text{CS}}(\Theta) = 0.10$.
3. **Combination & Outcome:**
   * Conflict metric $K = (0.15 \times 0.85) + (0.75 \times 0.05) = 0.1275 + 0.0375 = 0.165$ (Low conflict).
   * Combined belief: $m_{\text{combined}}(\{\neg V\}) = 0.942$.
   * **Result:** Alert is definitively **suppressed** with documented audit reasoning. Zero false positive escalation.
