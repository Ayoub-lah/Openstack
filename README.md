# Cloud & Edge Computing — OpenStack Infrastructure

> Private cloud infrastructure built from scratch on a personal PC — no AWS, no Azure, just open source.

**Stack:** OpenStack · Terraform · Python · Flask · VirtualBox · Linux · Cron · REST API

---

## Architecture Overview

```mermaid
%%{init: {"theme": "dark", "themeVariables": {"primaryColor": "#1A2332", "primaryTextColor": "#85B7EB", "primaryBorderColor": "#378ADD", "lineColor": "#378ADD", "secondaryColor": "#0D1117", "tertiaryColor": "#161B22", "fontSize": "13px"}}}%%

flowchart TB
  classDef core    fill:#1A2332,stroke:#378ADD,stroke-width:1px,color:#85B7EB
  classDef iaas    fill:#0F2318,stroke:#1D9E75,stroke-width:1px,color:#5DCAA5
  classDef saas    fill:#1F1A0A,stroke:#BA7517,stroke-width:1px,color:#EF9F27
  classDef iac     fill:#1A2C0F,stroke:#3B6D11,stroke-width:1px,color:#97C459
  classDef monitor fill:#2C1A1A,stroke:#A32D2D,stroke-width:1px,color:#F09595
  classDef client  fill:#1A1A2C,stroke:#534AB7,stroke-width:1px,color:#AFA9EC

  subgraph CLIENT["Client"]
    direction LR
    BR["Browser User"]:::client
    HZ["Horizon Dashboard"]:::client
    BR --> HZ
  end

  subgraph OPENSTACK["OpenStack DevStack 2026.1 — Ubuntu 24.04 — 192.168.56.102"]
    direction LR
    KS["Keystone Auth"]:::core
    GL["Glance Images"]:::core
    NV["Nova Calcul"]:::core
    NT["Neutron SDN"]:::core
    KS --> NV
    GL --> NV
    NT --> NV
  end

  subgraph IAAS["IaaS — Infrastructure as a Service"]
    direction LR
    CVM["CirrOS VM 192.168.233.198 m1.tiny"]:::iaas
    SGR["Security Groups SSH ICMP 5000"]:::iaas
    KEY["SSH Key ma-cle-ssh"]:::iaas
    KEY --> CVM
    SGR --> CVM
  end

  subgraph SAAS["SaaS — Software as a Service"]
    direction LR
    UVM["Ubuntu VM 172.24.4.70 m1.small"]:::saas
    FLK["Flask Task Manager CRUD"]:::saas
    API["REST API port 5000"]:::saas
    UVM --> FLK --> API
  end

  subgraph IAC["IaC — Infrastructure as Code"]
    direction LR
    MTF["main.tf HCL config"]:::iac
    CYM["clouds.yaml Keystone v3"]:::iac
    TFA["terraform apply 1 resource added"]:::iac
    CTO["centos-terraform ACTIVE"]:::iac
    MTF --> TFA
    CYM --> TFA
    TFA --> CTO
  end

  subgraph MONITORING["Monitoring — SLA Supervision"]
    direction LR
    SLJ["sla.json 99.5% target"]:::monitor
    MSL["monitor_sla.py Python SDK"]:::monitor
    CRN["Cron 5 min"]:::monitor
    RPT["rapport_sla.json CONFORME"]:::monitor
    SLJ --> MSL
    CRN --> MSL
    MSL --> RPT
  end

  HZ -->|HTTP| OPENSTACK
  NV -->|provisions| IAAS
  NV -->|provisions| SAAS
  NV -->|provisions| IAC
  MSL -->|Nova API| NV
  BR -->|Task Manager 5000| API
```

---

## Project Phases

```mermaid
timeline
  title Cloud and Edge Computing Project

  section Phase 0 - Preparation
    Week 1 : VirtualBox 7.x installation
           : Ubuntu 24.04 LTS VM creation
           : NAT + Host-Only network config
           : SSH access validated

  section Phase 1 - OpenStack
    Week 2 : DevStack clone from OpenDev
           : local.conf configuration
           : stack.sh execution 30-60 min
           : Horizon Dashboard validated

  section Phase 2 - IaaS
    Week 3 : SSH key pair generation
           : Security Groups configuration
           : CirrOS 0.6.3 instance launch
           : Linux tests whoami ip a df -h

  section Phase 3 - SaaS
    Week 3 : Ubuntu 22.04 VM creation
           : Flask transfer via SCP offline
           : Task Manager CRUD deployment
           : App live at 172.24.4.70:5000

  section Phase 4 - Terraform IaC
    Week 4 : Terraform v1.14.8 installation
           : clouds.yaml Keystone v3 config
           : terraform init and apply
           : centos-terraform VM auto-provisioned

  section Phase 5 - SLA Monitoring
    Week 4 : SLA target 99.5% in sla.json
           : monitor_sla.py development
           : Cron automation every 5 min
           : rapport_sla.json CONFORME
```

---

## SLA Monitoring Loop

```mermaid
flowchart TB
  classDef cron    fill:#26215C,stroke:#534AB7,stroke-width:1.5px,color:#CECBF6
  classDef script  fill:#0C447C,stroke:#185FA5,stroke-width:1.5px,color:#B5D4F4
  classDef api     fill:#EEEDFE,stroke:#534AB7,stroke-width:1px,color:#3C3489
  classDef calcul  fill:#E6F1FB,stroke:#185FA5,stroke-width:1px,color:#0C447C
  classDef ok      fill:#EAF3DE,stroke:#3B6D11,stroke-width:2px,color:#27500A
  classDef nok     fill:#FCEBEB,stroke:#A32D2D,stroke-width:2px,color:#791F1F
  classDef rapport fill:#FAEEDA,stroke:#854F0B,stroke-width:1.5px,color:#633806
  classDef dec     fill:#F1EFE8,stroke:#5F5E5A,stroke-width:1.5px,color:#2C2C2A

  CRON["Cron Scheduler every 5 minutes"]:::cron
  CRON -->|triggers| SCRIPT
  SCRIPT["monitor_sla.py Python + OpenStack SDK"]:::script
  SCRIPT -->|HTTP request| NOVA

  subgraph OPENSTACK["OpenStack - Nova API"]
    direction LR
    NOVA["Nova API GET /servers"]:::api
    VM1["centos-terraform ACTIVE"]:::ok
    VM2["ubuntu ACTIVE"]:::ok
    VM3["cirros-test ACTIVE"]:::ok
    NOVA --> VM1
    NOVA --> VM2
    NOVA --> VM3
  end

  NOVA -->|instances + status| CALCUL
  CALCUL["Availability calculation Active / Total x 100"]:::calcul
  CALCUL -->|compare target| DECISION
  DECISION{"Rate >= 99.5% ?"}:::dec
  DECISION -->|YES| CONFORME
  DECISION -->|NO| NONCONF
  CONFORME["CONFORME SLA respected rate = 100%"]:::ok
  NONCONF["NON CONFORME SLA violated alert triggered"]:::nok
  CONFORME -->|writes| RAPPORT
  NONCONF -->|writes| RAPPORT
  RAPPORT["rapport_sla.json date - rate - status - detail"]:::rapport
  RAPPORT -->|wait 5 min| CRON
```

---

## Project Structure

```
cloud-edge-computing-openstack/
├── README.md
├── diagrams/
│   ├── workflow.md
│   ├── architecture.md
│   ├── sla_boucle.md
│   └── timeline.md
├── code/
│   ├── main.tf
│   ├── monitor_sla.py
│   └── sla.json
└── rapport/
    └── Rapport.pdf
```

---

## Key Challenges Solved

- Flask offline installation via SCP without internet access inside OpenStack VM
- Terraform authentication with OpenStack resolved using `clouds.yaml`
- Nova compute stuck in "Powering On" — fixed via `virt_type=qemu` in nova config
- `br-ex` interface losing IP on reboot — fixed with persistent network configuration
- SLA monitoring integrated with Nova API using Python OpenStack SDK

---

## Author

**LAHLAIBI Ayoub** — Master SIT & Big Data, FST Tanger  
Université Abdelmalek Essaâdi
