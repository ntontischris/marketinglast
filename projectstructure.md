graph TD
    A[📁 marketing-agents-system/] --> B[📁 src/]
    A --> C[📁 config/]
    A --> D[📁 data/]
    A --> E[📁 tests/]
    A --> F[📁 docs/]
    A --> G[📁 scripts/]
    A --> H[📁 deployments/]
    A --> I[📄 requirements.txt]
    A --> J[📄 .env.example]
    A --> K[📄 docker-compose.yml]
    A --> L[📄 README.md]
    A --> M[📄 pyproject.toml]

    %% Source Code Structure
    B --> B1[📁 agents/]
    B --> B2[📁 workflows/]
    B --> B3[📁 tools/]
    B --> B4[📁 models/]
    B --> B5[📁 utils/]
    B --> B6[📁 api/]
    B --> B7[📁 monitoring/]
    B --> B8[📄 main.py]

    %% Agents Structure
    B1 --> B1A[📁 core/]
    B1 --> B1B[📁 social_media/]
    B1 --> B1C[📁 content/]
    B1 --> B1D[📁 analytics/]
    B1 --> B1E[📁 quality/]
    B1 --> B1F[📁 crisis/]

    %% Core Agents
    B1A --> B1A1[📄 base_agent.py]
    B1A --> B1A2[📄 campaign_manager.py]
    B1A --> B1A3[📄 content_strategy.py]
    B1A --> B1A4[📄 market_research.py]
    B1A --> B1A5[📄 social_coordinator.py]
    B1A --> B1A6[📄 publishing_scheduler.py]

    %% Social Media Agents
    B1B --> B1B1[📄 instagram_agent.py]
    B1B --> B1B2[📄 linkedin_agent.py]
    B1B --> B1B3[📄 twitter_agent.py]
    B1B --> B1B4[📄 tiktok_agent.py]
    B1B --> B1B5[📄 facebook_agent.py]
    B1B --> B1B6[📄 youtube_agent.py]
    B1B --> B1B7[📄 platform_base.py]

    %% Content Agents
    B1C --> B1C1[📄 content_creator.py]
    B1C --> B1C2[📄 copywriter.py]
    B1C --> B1C3[📄 visual_content.py]
    B1C --> B1C4[📄 video_content.py]

    %% Analytics Agents
    B1D --> B1D1[📄 performance_analyzer.py]
    B1D --> B1D2[📄 sentiment_analyzer.py]
    B1D --> B1D3[📄 trend_analyzer.py]
    B1D --> B1D4[📄 roi_calculator.py]

    %% Quality Agents
    B1E --> B1E1[📄 content_reviewer.py]
    B1E --> B1E2[📄 brand_compliance.py]
    B1E --> B1E3[📄 legal_checker.py]

    %% Crisis Management
    B1F --> B1F1[📄 crisis_detector.py]
    B1F --> B1F2[📄 crisis_responder.py]
    B1F --> B1F3[📄 escalation_manager.py]

    %% Workflows Structure
    B2 --> B2A[📄 content_workflow.py]
    B2 --> B2B[📄 campaign_workflow.py]
    B2 --> B2C[📄 social_media_workflow.py]
    B2 --> B2D[📄 crisis_workflow.py]
    B2 --> B2E[📄 analytics_workflow.py]
    B2 --> B2F[📁 graph_definitions/]

    B2F --> B2F1[📄 content_graph.py]
    B2F --> B2F2[📄 campaign_graph.py]
    B2F --> B2F3[📄 monitoring_graph.py]
    B2F --> B2F4[📄 optimization_graph.py]

    %% Tools Structure
    B3 --> B3A[📁 social_media/]
    B3 --> B3B[📁 content_generation/]
    B3 --> B3C[📁 analytics/]
    B3 --> B3D[📁 scheduling/]
    B3 --> B3E[📁 research/]

    B3A --> B3A1[📄 instagram_api.py]
    B3A --> B3A2[📄 linkedin_api.py]
    B3A --> B3A3[📄 twitter_api.py]
    B3A --> B3A4[📄 tiktok_api.py]
    B3A --> B3A5[📄 facebook_api.py]
    B3A --> B3A6[📄 youtube_api.py]

    B3B --> B3B1[📄 text_generator.py]
    B3B --> B3B2[📄 image_generator.py]
    B3B --> B3B3[📄 video_editor.py]
    B3B --> B3B4[📄 hashtag_generator.py]

    B3C --> B3C1[📄 google_analytics.py]
    B3C --> B3C2[📄 social_metrics.py]
    B3C --> B3C3[📄 sentiment_tools.py]
    B3C --> B3C4[📄 competitor_analysis.py]

    B3D --> B3D1[📄 scheduler.py]
    B3D --> B3D2[📄 calendar_manager.py]
    B3D --> B3D3[📄 optimal_timing.py]

    B3E --> B3E1[📄 web_scraper.py]
    B3E --> B3E2[📄 trend_finder.py]
    B3E --> B3E3[📄 audience_research.py]

    %% Models Structure
    B4 --> B4A[📄 content_models.py]
    B4 --> B4B[📄 campaign_models.py]
    B4 --> B4C[📄 user_models.py]
    B4 --> B4D[📄 analytics_models.py]
    B4 --> B4E[📄 platform_models.py]

    %% Utils Structure
    B5 --> B5A[📄 logger.py]
    B5 --> B5B[📄 config_loader.py]
    B5 --> B5C[📄 database.py]
    B5 --> B5D[📄 cache_manager.py]
    B5 --> B5E[📄 security.py]
    B5 --> B5F[📄 validators.py]

    %% API Structure
    B6 --> B6A[📁 routes/]
    B6 --> B6B[📁 middleware/]
    B6 --> B6C[📄 app.py]
    B6 --> B6D[📄 auth.py]

    B6A --> B6A1[📄 agents.py]
    B6A --> B6A2[📄 campaigns.py]
    B6A --> B6A3[📄 content.py]
    B6A --> B6A4[📄 analytics.py]
    B6A --> B6A5[📄 webhooks.py]

    B6B --> B6B1[📄 rate_limiter.py]
    B6B --> B6B2[📄 cors.py]
    B6B --> B6B3[📄 error_handler.py]

    %% Monitoring Structure
    B7 --> B7A[📄 metrics.py]
    B7 --> B7B[📄 alerts.py]
    B7 --> B7C[📄 health_check.py]
    B7 --> B7D[📄 performance_tracker.py]

    %% Config Structure
    C --> C1[📄 agents_config.yaml]
    C --> C2[📄 platforms_config.yaml]
    C --> C3[📄 workflows_config.yaml]
    C --> C4[📄 database_config.yaml]
    C --> C5[📄 api_keys.yaml.example]
    C --> C6[📄 logging_config.yaml]

    %% Data Structure
    D --> D1[📁 templates/]
    D --> D2[📁 prompts/]
    D --> D3[📁 training/]
    D --> D4[📁 cache/]

    D1 --> D1A[📄 content_templates.json]
    D1 --> D1B[📄 campaign_templates.json]

    D2 --> D2A[📄 agent_prompts.yaml]
    D2 --> D2B[📄 platform_prompts.yaml]

    D3 --> D3A[📄 sample_campaigns.json]
    D3 --> D3B[📄 brand_guidelines.json]

    %% Tests Structure
    E --> E1[📁 unit/]
    E --> E2[📁 integration/]
    E --> E3[📁 e2e/]
    E --> E4[📄 conftest.py]

    E1 --> E1A[📄 test_agents.py]
    E1 --> E1B[📄 test_workflows.py]
    E1 --> E1C[📄 test_tools.py]

    E2 --> E2A[📄 test_api_integration.py]
    E2 --> E2B[📄 test_platform_integration.py]

    E3 --> E3A[📄 test_full_workflow.py]
    E3 --> E3B[📄 test_user_scenarios.py]

    %% Documentation
    F --> F1[📄 architecture.md]
    F --> F2[📄 api_reference.md]
    F --> F3[📄 deployment_guide.md]
    F --> F4[📄 agent_configuration.md]
    F --> F5[📁 examples/]

    F5 --> F5A[📄 basic_campaign.py]
    F5 --> F5B[📄 custom_agent.py]
    F5 --> F5C[📄 workflow_example.py]

    %% Scripts
    G --> G1[📄 setup.py]
    G --> G2[📄 migrate.py]
    G --> G3[📄 seed_data.py]
    G --> G4[📄 deploy.sh]
    G --> G5[📄 backup.py]

    %% Deployments
    H --> H1[📁 docker/]
    H --> H2[📁 kubernetes/]
    H --> H3[📁 terraform/]
    H --> H4[📁 monitoring/]

    H1 --> H1A[📄 Dockerfile]
    H1 --> H1B[📄 docker-compose.prod.yml]

    H2 --> H2A[📄 deployment.yaml]
    H2 --> H2B[📄 service.yaml]
    H2 --> H2C[📄 configmap.yaml]

    H3 --> H3A[📄 main.tf]
    H3 --> H3B[📄 variables.tf]

    H4 --> H4A[📄 prometheus.yml]
    H4 --> H4B[📄 grafana-dashboard.json]

    %% Styling
    classDef folderClass fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef pythonClass fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef configClass fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef docClass fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef deployClass fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class A,B,B1,B1A,B1B,B1C,B1D,B1E,B1F,B2,B2F,B3,B3A,B3B,B3C,B3D,B3E,B4,B5,B6,B6A,B6B,B7,C,D,D1,D2,D3,E,E1,E2,E3,F,F5,G,H,H1,H2,H3,H4 folderClass
    
    class B1A1,B1A2,B1A3,B1A4,B1A5,B1A6,B1B1,B1B2,B1B3,B1B4,B1B5,B1B6,B1B7,B1C1,B1C2,B1C3,B1C4,B1D1,B1D2,B1D3,B1D4,B1E1,B1E2,B1E3,B1F1,B1F2,B1F3,B2A,B2B,B2C,B2D,B2E,B2F1,B2F2,B2F3,B2F4,B3A1,B3A2,B3A3,B3A4,B3A5,B3A6,B3B1,B3B2,B3B3,B3B4,B3C1,B3C2,B3C3,B3C4,B3D1,B3D2,B3D3,B3E1,B3E2,B3E3,B4A,B4B,B4C,B4D,B4E,B5A,B5B,B5C,B5D,B5E,B5F,B6A1,B6A2,B6A3,B6A4,B6A5,B6B1,B6B2,B6B3,B6C,B6D,B7A,B7B,B7C,B7D,B8,E1A,E1B,E1C,E2A,E2B,E3A,E3B,E4,F5A,F5B,F5C,G1,G2,G3,G5 pythonClass
    
    class C1,C2,C3,C4,C5,C6,D1A,D1B,D2A,D2B,D3A,D3B,I,J pythonClass
    
    class F1,F2,F3,F4,L docClass
    
    class H1A,H1B,H2A,H2B,H2C,H3A,H3B,H4A,H4B,K,M,G4 deployClass