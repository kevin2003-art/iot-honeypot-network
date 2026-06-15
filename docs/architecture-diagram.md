# Architecture Diagram

\`\`\`mermaid
graph TD
    A[Attacker] -->|SSH/Telnet on 2222/2223| B[Docker Network 172.20.0.0/24]
    B --> C[Cowrie Honeypot Container]
    C --> D[Fake Filesystem: MedDevice-IoT-001]
    C --> E[cowrie.log / cowrie.json]
    E --> F[Python Analysis Scripts]
    F --> G[Dashboard JSON Data]
    G --> H[HTML Dashboard - 7 Tabs]
    F --> I[Geolocation Enrichment]
    I --> H
    F --> J[Final Reports - Markdown]

    style A fill:#330000,stroke:#ff4444,color:#ff4444
    style C fill:#003300,stroke:#00ff41,color:#00ff41
    style H fill:#001a33,stroke:#38bdf8,color:#38bdf8
\`\`\`

## Component Description

| Component | Description |
|---|---|
| Attacker | External entity probing the exposed honeypot ports |
| Docker Network | Isolated subnet preventing lateral movement |
| Cowrie Honeypot | Simulated medical IoT device (PVM-2000X) |
| Fake Filesystem | honeyfs with device info, passwd, hostname |
| Logs | JSON and text event logs of all activity |
| Analysis Scripts | 15+ Python/Bash scripts for IoC extraction |
| Dashboard | Real time military-style threat visualization |
