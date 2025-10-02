# Architecture Diagrams - Agentic Research System

## 1. Research Loop Flow Diagram

```mermaid
graph TD
    A[Start: User Query] --> B[Initialize Research Loop]
    B --> C[Iteration = 0]

    C --> D{Check Termination}
    D -->|Cost Limit Reached| Z1[End: Cost Exceeded]
    D -->|Max Iterations| Z2[End: Max Reached]
    D -->|Continue| E[Sequential Thinking: Create Plan]

    E --> F[Generate Research Angles]
    F --> G[Spawn N Agents in Parallel]

    G --> H1[Agent 1: Angle A<br/>5 Searches]
    G --> H2[Agent 2: Angle B<br/>5 Searches]
    G --> H3[Agent 3: Angle C<br/>5 Searches]
    G --> H4[Agent 4: Angle D<br/>5 Searches]
    G --> H5[Agent 5: Angle E<br/>5 Searches]

    H1 --> I[anyio.gather<br/>Wait All Agents]
    H2 --> I
    H3 --> I
    H4 --> I
    H5 --> I

    I --> J[Collect All Findings]
    J --> K[Sequential Thinking: Verify]

    K --> L{Confidence >= 0.85?}
    L -->|Yes| M[Context Editing]
    L -->|No| N[Identify Gaps]

    N --> O[Generate New Angles]
    O --> P[Iteration++]
    P --> D

    M --> Q[Synthesis Agent]
    Q --> R[Final Report]
    R --> S[End: Success]

    style B fill:#e1f5ff
    style E fill:#fff3cd
    style G fill:#d4edda
    style K fill:#cfe2ff
    style M fill:#e7d5f7
    style R fill:#d4edda
```

## 2. Verification Criteria Flow

```mermaid
graph TD
    A[Findings Collection] --> B[Sequential Thinking<br/>Verification]

    B --> C1[Coverage Analysis]
    B --> C2[Depth Analysis]
    B --> C3[Source Quality Analysis]
    B --> C4[Consistency Analysis]

    C1 --> D1[Coverage Score<br/>0.0-1.0]
    C2 --> D2[Depth Score<br/>0.0-1.0]
    C3 --> D3[Quality Score<br/>0.0-1.0]
    C4 --> D4[Consistency Score<br/>0.0-1.0]

    D1 --> E[Weighted Combination]
    D2 --> E
    D3 --> E
    D4 --> E

    E --> F[Overall Confidence<br/>Score]

    F --> G{Score >= Threshold?}
    G -->|Yes| H[decision: complete]
    G -->|No| I[decision: continue]

    I --> J[Gap Analysis]
    J --> K[Recommended Angles]
    K --> L[Next Iteration]

    style B fill:#fff3cd
    style E fill:#cfe2ff
    style F fill:#e1f5ff
    style J fill:#f8d7da
```

## 3. MCP Integration Architecture

```mermaid
graph TD
    A[Research Loop] --> B{MCP Integration}

    B --> C[Sequential Thinking MCP]
    B --> D[Omnisearch MCP]

    C --> C1[create_research_plan]
    C --> C2[verify_research]
    C --> C3[analyze_gaps]
    C --> C4[plan_synthesis]

    D --> D1[search - Auto Select]
    D --> D2[multi_provider_search]
    D --> D3[search_with_fallback]
    D --> D4[generate_query_variations]

    C1 --> E1[5-Step Reasoning<br/>Research Plan]
    C2 --> E2[6-Step Reasoning<br/>Verification]
    C3 --> E3[Gap Analysis<br/>Recommendations]
    C4 --> E4[Synthesis Plan<br/>Structure]

    D1 --> F1[Provider Selection<br/>Query Type Based]
    D2 --> F2[Parallel Searches<br/>Multiple Providers]
    D3 --> F3[Automatic Fallback<br/>On Failure]
    D4 --> F4[Query Diversification<br/>5 Variations]

    style C fill:#fff3cd
    style D fill:#d4edda
    style E1 fill:#e1f5ff
    style E2 fill:#e1f5ff
    style F1 fill:#cfe2ff
    style F2 fill:#cfe2ff
```

## 4. Provider Selection Logic

```mermaid
graph TD
    A[Query Input] --> B{Analyze Query Type}

    B -->|Factual| C1[Tavily or<br/>Perplexity]
    B -->|Technical| C2[Brave or<br/>Kagi]
    B -->|Academic| C3[Exa or<br/>Kagi]
    B -->|Extraction| C4[Jina or<br/>Firecrawl]
    B -->|General| C5[Tavily, Brave,<br/>or Exa]

    C1 --> D{Check Quality<br/>Requirement}
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D -->|High Quality| E1[Filter by<br/>Quality >= 5]
    D -->|Medium Quality| E2[Filter by<br/>Quality >= 4]

    E1 --> F{Check Latency<br/>Requirement}
    E2 --> F

    F -->|Fast| G1[Filter<br/>Latency = fast]
    F -->|Medium| G2[Filter<br/>Latency <= medium]
    F -->|Slow OK| G3[All Latencies]

    G1 --> H[Check Budget]
    G2 --> H
    G3 --> H

    H -->|$| I1[Filter Cost = $]
    H -->|$$| I2[Filter Cost <= $$]
    H -->|$$$| I3[All Costs]

    I1 --> J[Select Provider]
    I2 --> J
    I3 --> J

    J --> K[Execute Search]

    style B fill:#fff3cd
    style D fill:#e1f5ff
    style F fill:#cfe2ff
    style H fill:#f8d7da
    style J fill:#d4edda
```

## 5. Metrics Tracking System

```mermaid
graph TD
    A[Research Operation] --> B{Track Event Type}

    B --> C1[Compression Event]
    B --> C2[Search Event]
    B --> C3[Token Usage Event]
    B --> C4[Iteration Event]

    C1 --> D1[CompressionMetric<br/>- Original size<br/>- Compressed size<br/>- Ratio<br/>- Time]

    C2 --> D2[SearchMetric<br/>- Provider<br/>- Query<br/>- Time<br/>- Success/Fail]

    C3 --> D3[TokenUsageMetric<br/>- Model type<br/>- Input/Output tokens<br/>- Cost<br/>- Operation]

    C4 --> D4[IterationMetric<br/>- Searches count<br/>- Confidence<br/>- Duration<br/>- Gaps]

    D1 --> E[MetricsTracker<br/>Storage]
    D2 --> E
    D3 --> E
    D4 --> E

    E --> F1[get_compression_stats]
    E --> F2[get_search_stats]
    E --> F3[get_token_stats]
    E --> F4[get_iteration_stats]

    F1 --> G[Generate Report]
    F2 --> G
    F3 --> G
    F4 --> G

    G --> H1[Markdown Report]
    G --> H2[JSON Export]
    G --> H3[Recommendations]

    style E fill:#e1f5ff
    style G fill:#fff3cd
    style H1 fill:#d4edda
    style H2 fill:#d4edda
    style H3 fill:#f8d7da
```

## 6. Parallel Agent Execution

```mermaid
sequenceDiagram
    participant RL as Research Loop
    participant ST as Sequential Thinking
    participant A1 as Agent 1
    participant A2 as Agent 2
    participant A3 as Agent 3
    participant A4 as Agent 4
    participant A5 as Agent 5
    participant OS as Omnisearch

    RL->>ST: Create research plan
    ST-->>RL: 5 research angles

    par Parallel Agent Spawning
        RL->>A1: Spawn (Angle 1)
        RL->>A2: Spawn (Angle 2)
        RL->>A3: Spawn (Angle 3)
        RL->>A4: Spawn (Angle 4)
        RL->>A5: Spawn (Angle 5)
    end

    par Parallel Search Execution
        A1->>OS: 5 searches (Angle 1)
        A2->>OS: 5 searches (Angle 2)
        A3->>OS: 5 searches (Angle 3)
        A4->>OS: 5 searches (Angle 4)
        A5->>OS: 5 searches (Angle 5)
    end

    par Parallel Results
        OS-->>A1: Results 1
        OS-->>A2: Results 2
        OS-->>A3: Results 3
        OS-->>A4: Results 4
        OS-->>A5: Results 5
    end

    par Parallel Summarization
        A1->>A1: Summarize findings
        A2->>A2: Summarize findings
        A3->>A3: Summarize findings
        A4->>A4: Summarize findings
        A5->>A5: Summarize findings
    end

    A1-->>RL: Findings 1
    A2-->>RL: Findings 2
    A3-->>RL: Findings 3
    A4-->>RL: Findings 4
    A5-->>RL: Findings 5

    RL->>ST: Verify all findings
    ST-->>RL: Verification result

    alt Confidence >= Threshold
        RL->>RL: Proceed to synthesis
    else Confidence < Threshold
        RL->>ST: Analyze gaps
        ST-->>RL: New angles
        RL->>RL: Next iteration
    end
```

## 7. Verification Scoring Details

```mermaid
graph LR
    A[All Findings] --> B[Coverage Analysis]
    A --> C[Depth Analysis]
    A --> D[Source Quality]
    A --> E[Consistency Check]

    B --> B1{All aspects<br/>covered?}
    B1 -->|Yes 100%| B2[Score: 1.0]
    B1 -->|Partial| B3[Score: 0.0-0.9]

    C --> C1{Sufficient<br/>detail?}
    C1 -->|Deep| C2[Score: 1.0]
    C1 -->|Moderate| C3[Score: 0.5-0.9]
    C1 -->|Shallow| C4[Score: 0.0-0.4]

    D --> D1{Source<br/>authority?}
    D1 -->|High| D2[Score: 0.9-1.0]
    D1 -->|Medium| D3[Score: 0.6-0.8]
    D1 -->|Low| D4[Score: 0.0-0.5]

    E --> E1{Findings<br/>agree?}
    E1 -->|Strong consensus| E2[Score: 1.0]
    E1 -->|Some conflict| E3[Score: 0.6-0.9]
    E1 -->|Major conflict| E4[Score: 0.0-0.5]

    B2 --> F[Weighted Sum]
    B3 --> F
    C2 --> F
    C3 --> F
    C4 --> F
    D2 --> F
    D3 --> F
    D4 --> F
    E2 --> F
    E3 --> F
    E4 --> F

    F --> G[Overall Confidence<br/>= Coverage×0.30 +<br/>Depth×0.25 +<br/>Quality×0.25 +<br/>Consistency×0.20]

    style F fill:#fff3cd
    style G fill:#d4edda
```

## 8. Cost Optimization Flow

```mermaid
graph TD
    A[Research Task] --> B{Task Type}

    B -->|Search| C1[Small Model<br/>Haiku/GPT-5-mini]
    B -->|Compression| C2[Small Model<br/>Haiku]
    B -->|Planning| C3[Big Model<br/>Sonnet/GPT-5]
    B -->|Verification| C4[Big Model<br/>Sonnet]
    B -->|Synthesis| C5[Big Model<br/>Sonnet]

    C1 --> D1[Cost: ~$0.004]
    C2 --> D2[Cost: ~$0.002]
    C3 --> D3[Cost: ~$0.024]
    C4 --> D4[Cost: ~$0.018]
    C5 --> D5[Cost: ~$0.024]

    D1 --> E[Track Usage]
    D2 --> E
    D3 --> E
    D4 --> E
    D5 --> E

    E --> F{Total Cost}
    F -->|< 50%| G1[Continue]
    F -->|50-80%| G2[Warning]
    F -->|> 80%| G3[Alert]
    F -->|>= 100%| G4[Terminate]

    G1 --> H[Next Task]
    G2 --> H
    G3 --> I{Continue?}
    G4 --> J[End Session]

    I -->|Yes| H
    I -->|No| J

    style C1 fill:#d4edda
    style C2 fill:#d4edda
    style C3 fill:#fff3cd
    style C4 fill:#fff3cd
    style C5 fill:#fff3cd
    style G4 fill:#f8d7da
```

## 9. Data Flow Summary

```mermaid
graph LR
    A[User Query] --> B[Research Loop]
    B --> C[Sequential Thinking<br/>Planning]
    C --> D[Research Angles]

    D --> E1[Agent 1]
    D --> E2[Agent 2]
    D --> E3[Agent 3]
    D --> E4[Agent 4]
    D --> E5[Agent 5]

    E1 --> F[Omnisearch MCP]
    E2 --> F
    E3 --> F
    E4 --> F
    E5 --> F

    F --> G1[Tavily]
    F --> G2[Brave]
    F --> G3[Exa]
    F --> G4[Kagi]
    F --> G5[Others]

    G1 --> H[Compression Hooks]
    G2 --> H
    G3 --> H
    G4 --> H
    G5 --> H

    H --> I[Compressed Findings]

    I --> J[Sequential Thinking<br/>Verification]

    J --> K{Sufficient?}
    K -->|No| L[Gap Analysis]
    L --> D

    K -->|Yes| M[Context Editor]
    M --> N[Synthesis Agent]
    N --> O[Final Report]

    B -.-> P[Metrics Tracker]
    C -.-> P
    E1 -.-> P
    E2 -.-> P
    F -.-> P
    H -.-> P
    J -.-> P

    P --> Q[Performance Report]

    style B fill:#e1f5ff
    style C fill:#fff3cd
    style F fill:#d4edda
    style H fill:#f8d7da
    style J fill:#cfe2ff
    style P fill:#e7d5f7
```

## 10. System Components Overview

```mermaid
graph TD
    A[Agentic Research System] --> B[Core]
    A --> C[MCP]
    A --> D[Providers]
    A --> E[Agents]
    A --> F[Hooks]
    A --> G[Utils]

    B --> B1[research_loop.py<br/>Iterative loop logic]
    B --> B2[metrics.py<br/>Performance tracking]
    B --> B3[cost_tracker.py<br/>Cost monitoring]
    B --> B4[rate_limiter.py<br/>Rate limiting]

    C --> C1[omnisearch.py<br/>Search provider wrapper]
    C --> C2[sequential_thinking.py<br/>Reasoning wrapper]

    D --> D1[base.py<br/>Provider interface]
    D --> D2[claude_provider.py]
    D --> D3[openai_provider.py]
    D --> D4[gemini_provider.py]

    E --> E1[orchestrator.py<br/>Main coordinator]
    E --> E2[search_agent.py<br/>Search specialist]
    E --> E3[verification_agent.py<br/>Quality control]
    E --> E4[compression_agent.py<br/>Content compression]
    E --> E5[synthesis_agent.py<br/>Report generation]

    F --> F1[compression_hooks.py<br/>Auto compression]
    F --> F2[validation_hooks.py<br/>Pre-tool validation]
    F --> F3[context_hooks.py<br/>Context optimization]

    G --> G1[config_loader.py<br/>Configuration]
    G --> G2[provider_factory.py<br/>Provider creation]

    style B fill:#e1f5ff
    style C fill:#fff3cd
    style D fill:#d4edda
    style E fill:#cfe2ff
    style F fill:#f8d7da
    style G fill:#e7d5f7
```

---

## Key Architectural Principles

1. **Separation of Concerns**
   - Each module has a single, well-defined responsibility
   - Clear interfaces between components

2. **Parallel Execution**
   - Uses `anyio.gather()` for concurrent agent execution
   - Non-blocking I/O throughout

3. **Provider Agnostic**
   - BaseProvider abstraction allows any LLM
   - Easy switching between providers

4. **Cost Optimization**
   - Strategic model selection (big/small)
   - Automatic compression
   - Budget tracking and limits

5. **Quality Assurance**
   - Multi-criteria verification
   - Iterative improvement
   - Gap-based refinement

6. **Performance Monitoring**
   - Comprehensive metrics tracking
   - Optimization recommendations
   - JSON export for analysis
