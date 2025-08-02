graph TD
    A[Marketing Request Input] --> B{Request Classification}
    
    B -->|Content Creation| C[Content Strategy Agent]
    B -->|Campaign Planning| D[Campaign Manager Agent]
    B -->|Analytics/Research| E[Market Research Agent]
    B -->|Social Media| F[Social Media Coordinator]
    
    %% Content Strategy Branch
    C --> C1[Analyze Brand Guidelines]
    C1 --> C2[Generate Content Ideas]
    C2 --> C3[Create Content Calendar]
    C3 --> G[Content Review Gate]
    
    %% Campaign Manager Branch
    D --> D1[Define Campaign Objectives]
    D1 --> D2[Budget Allocation Planning]
    D2 --> D3[Channel Strategy Selection]
    D3 --> H[Campaign Approval Gate]
    
    %% Market Research Branch
    E --> E1[Competitor Analysis]
    E1 --> E2[Audience Research]
    E2 --> E3[Trend Analysis]
    E3 --> I[Research Synthesis]
    
    %% Social Media Coordinator Branch
    F --> F1{Platform Selection}
    
    F1 -->|Instagram| J[Instagram Specialist Agent]
    F1 -->|LinkedIn| K[LinkedIn Specialist Agent]
    F1 -->|Twitter/X| L[Twitter Specialist Agent]
    F1 -->|TikTok| M[TikTok Specialist Agent]
    F1 -->|Facebook| N[Facebook Specialist Agent]
    F1 -->|YouTube| O[YouTube Specialist Agent]
    
    %% Platform Specialists Workflows
    J --> J1[Visual Content Creation]
    J1 --> J2[Story/Reel Planning]
    J2 --> J3[Hashtag Strategy]
    J3 --> P[Instagram Content Queue]
    
    K --> K1[Professional Content Creation]
    K1 --> K2[Industry Insights]
    K2 --> K3[Network Engagement Strategy]
    K3 --> Q[LinkedIn Content Queue]
    
    L --> L1[Real-time Content Creation]
    L1 --> L2[Thread Planning]
    L2 --> L3[Trending Topics Integration]
    L3 --> R[Twitter Content Queue]
    
    M --> M1[Short-form Video Concepts]
    M1 --> M2[Trending Audio/Effects]
    M2 --> M3[Viral Content Strategy]
    M3 --> S[TikTok Content Queue]
    
    N --> N1[Community-focused Content]
    N1 --> N2[Event/Group Integration]
    N2 --> N3[Ad Campaign Alignment]
    N3 --> T[Facebook Content Queue]
    
    O --> O1[Long-form Video Planning]
    O1 --> O2[SEO Optimization]
    O2 --> O3[Thumbnail/Title Strategy]
    O3 --> U[YouTube Content Queue]
    
    %% Quality Control and Approval Gates
    G --> V[Content Quality Agent]
    H --> V
    I --> W[Data Validation Agent]
    
    V --> V1[Brand Consistency Check]
    V1 --> V2[Legal/Compliance Review]
    V2 --> V3[A/B Testing Preparation]
    
    W --> W1[Data Accuracy Verification]
    W1 --> W2[Insight Validation]
    W2 --> W3[Recommendation Scoring]
    
    %% Content Queues merge into Publishing
    P --> X[Publishing Scheduler Agent]
    Q --> X
    R --> X
    S --> X
    T --> X
    U --> X
    
    %% Publishing and Monitoring
    X --> X1[Cross-platform Scheduling]
    X1 --> X2[Optimal Timing Analysis]
    X2 --> X3[Content Publishing]
    X3 --> Y[Social Media Monitor Agent]
    
    Y --> Y1[Engagement Tracking]
    Y1 --> Y2[Sentiment Analysis]
    Y2 --> Y3[Performance Metrics]
    Y3 --> Z[Analytics Dashboard]
    
    %% Feedback Loop
    Z --> Z1[Performance Analysis]
    Z1 --> Z2[Optimization Recommendations]
    Z2 --> AA{Trigger New Workflow?}
    
    AA -->|Yes| BB[Strategy Adjustment Agent]
    AA -->|No| CC[Report Generation]
    
    BB --> BB1[Analyze Performance Data]
    BB1 --> BB2[Identify Improvement Areas]
    BB2 --> BB3[Update Agent Parameters]
    BB3 --> A
    
    %% Crisis Management Branch
    Y --> DD{Crisis Detection?}
    DD -->|Yes| EE[Crisis Management Agent]
    DD -->|No| Y1
    
    EE --> EE1[Assess Crisis Severity]
    EE1 --> EE2[Generate Response Strategy]
    EE2 --> EE3[Coordinate Team Response]
    EE3 --> FF[Emergency Publishing]
    FF --> Y
    
    %% Final Reporting
    CC --> GG[Executive Summary Agent]
    GG --> HH[Stakeholder Reports]
    
    %% Styling
    classDef agentClass fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef platformClass fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef processClass fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef decisionClass fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef outputClass fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class C,D,E,F,J,K,L,M,N,O,V,W,X,Y,BB,EE,GG agentClass
    class J1,J2,J3,K1,K2,K3,L1,L2,L3,M1,M2,M3,N1,N2,N3,O1,O2,O3 platformClass
    class C1,C2,C3,D1,D2,D3,E1,E2,E3,V1,V2,V3,W1,W2,W3,X1,X2,X3,Y1,Y2,Y3 processClass
    class B,F1,AA,DD decisionClass
    class P,Q,R,S,T,U,Z,HH outputClass