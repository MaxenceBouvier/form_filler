# Architecture Diagrams

## Current Architecture (Legacy)

```mermaid
graph TD
    subgraph "Monolithic Scripts"
        GS[generate_stub.py]
        FF[fill_form.py]
    end

    PDF[PDF File] --> GS
    GS --> JSON1[stub.json]

    JSON2[user_data.json] --> FF
    PDF --> FF
    FF --> FPDF[Filled PDF]

    style GS fill:#ffcccc
    style FF fill:#ffcccc
```

## Proposed Architecture (From DEV_PLAN.md)

```mermaid
graph TD
    subgraph "CLI Layer"
        CLI[cli.py]
        CMD1[extract-required-info]
        CMD2[update-user-info]
        CMD3[fill-in-pdf]
    end

    subgraph "Core Modules"
        FI[form_inspector.py]
        UDM[user_data_manager.py]
        FM[field_matcher.py]
        FF2[form_filler.py]
    end

    subgraph "LLM Modules"
        LA[assistant.py]
        LM[models.py]
    end

    subgraph "Utils"
        FIO[file_io.py]
        VAL[validators.py]
    end

    CLI --> CMD1
    CLI --> CMD2
    CLI --> CMD3

    CMD1 --> FI
    CMD2 --> UDM
    CMD3 --> FF2

    FF2 --> FM
    UDM --> FIO
    FI --> VAL

    LA --> LM
    UDM -.-> LA

    style CLI fill:#ffeb99
    style FI fill:#99ccff
    style UDM fill:#99ccff
    style FM fill:#99ccff
    style FF2 fill:#99ccff
```

## Recommended Hexagonal Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        CLI[CLI Commands]
        WEB[Web Interface<br/>Future]
        API[REST API<br/>Future]
    end

    subgraph "Application Layer (Use Cases)"
        UC1[Extract Fields<br/>Use Case]
        UC2[Update User Data<br/>Use Case]
        UC3[Fill Form<br/>Use Case]
        FM2[Field Matching<br/>Service]
    end

    subgraph "Domain Layer (Core)"
        subgraph "Models"
            FF3[FormField]
            UD[UserData]
            PDF2[PDFForm]
        end
        subgraph "Interfaces"
            PDFI[PDFProcessor<br/>Interface]
            REPO[Repository<br/>Interface]
            LLMI[LLM<br/>Interface]
        end
    end

    subgraph "Infrastructure Layer (Adapters)"
        subgraph "PDF Adapters"
            PYPDF[PyPDFForm<br/>Adapter]
            PYPDF2[PyPDF2<br/>Adapter]
        end
        subgraph "Persistence Adapters"
            JSONR[JSON<br/>Repository]
            YAMLR[YAML<br/>Repository]
            ENCR[Encrypted<br/>Repository]
        end
        subgraph "LLM Adapters"
            HF[HuggingFace<br/>Adapter]
            OAI[OpenAI<br/>Adapter]
        end
    end

    CLI --> UC1
    CLI --> UC2
    CLI --> UC3
    WEB -.-> UC1
    WEB -.-> UC2
    WEB -.-> UC3

    UC1 --> PDFI
    UC2 --> REPO
    UC3 --> PDFI
    UC3 --> FM2
    FM2 -.-> LLMI

    PDFI --> PYPDF
    PDFI --> PYPDF2
    REPO --> JSONR
    REPO --> YAMLR
    REPO --> ENCR
    LLMI -.-> HF
    LLMI -.-> OAI

    style CLI fill:#ffeb99
    style WEB fill:#ffe6e6
    style API fill:#ffe6e6
    style UC1 fill:#99ff99
    style UC2 fill:#99ff99
    style UC3 fill:#99ff99
    style FM2 fill:#99ff99
    style FF3 fill:#ff99cc
    style UD fill:#ff99cc
    style PDF2 fill:#ff99cc
    style PDFI fill:#ffccff
    style REPO fill:#ffccff
    style LLMI fill:#ffccff
    style PYPDF fill:#99ccff
    style JSONR fill:#99ccff
    style HF fill:#ffcc99
```

## Dependency Flow (Clean Architecture)

```mermaid
graph LR
    subgraph "Dependencies Point Inward"
        EXT[External<br/>Libraries]
        INF[Infrastructure<br/>Layer]
        APP[Application<br/>Layer]
        DOM[Domain<br/>Layer]
    end

    EXT --> INF
    INF --> APP
    APP --> DOM

    style DOM fill:#90EE90
    style APP fill:#87CEEB
    style INF fill:#DDA0DD
    style EXT fill:#FFB6C1
```

## Module Dependency Graph (Recommended)

```mermaid
graph TD
    subgraph "Entry Points"
        CLI[presentation/cli]
    end

    subgraph "Application Services"
        EF[application/extract_fields]
        UUD[application/update_user_data]
        FF4[application/fill_form]
        FMS[application/field_matching]
    end

    subgraph "Domain"
        MOD[domain/models]
        INT[domain/interfaces]
        EXC[domain/exceptions]
    end

    subgraph "Infrastructure"
        PDF3[infrastructure/pdf]
        PER[infrastructure/persistence]
        LLM2[infrastructure/llm]
    end

    subgraph "Shared"
        VAL2[shared/validators]
    end

    CLI --> EF
    CLI --> UUD
    CLI --> FF4

    EF --> INT
    UUD --> INT
    FF4 --> INT
    FF4 --> FMS
    FMS --> INT

    PDF3 -.-> INT
    PER -.-> INT
    LLM2 -.-> INT

    EF --> MOD
    UUD --> MOD
    FF4 --> MOD
    FMS --> MOD

    CLI --> VAL2
    EF --> VAL2
    UUD --> VAL2

    style CLI fill:#ffeb99
    style EF fill:#99ff99
    style UUD fill:#99ff99
    style FF4 fill:#99ff99
    style FMS fill:#99ff99
    style MOD fill:#ff99cc
    style INT fill:#ffccff
    style PDF3 fill:#99ccff
    style PER fill:#99ccff
    style LLM2 fill:#ffcc99
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant UseCase
    participant Domain
    participant Repository
    participant PDFProcessor
    participant LLM

    User->>CLI: fill-in-pdf command
    CLI->>UseCase: Execute FillFormUseCase
    UseCase->>Repository: Load user data
    Repository-->>UseCase: UserData object
    UseCase->>PDFProcessor: Extract form fields
    PDFProcessor-->>UseCase: FormField list
    UseCase->>Domain: Create mapping

    alt LLM Assistance Needed
        UseCase->>LLM: Request field matching
        LLM-->>UseCase: Suggested mappings
    end

    UseCase->>PDFProcessor: Fill form with data
    PDFProcessor-->>UseCase: Success
    UseCase-->>CLI: Form filled
    CLI-->>User: Success message
```

## Security Boundaries

```mermaid
graph TB
    subgraph "Untrusted Zone"
        USER[User Input]
        LLM3[LLM Output]
    end

    subgraph "Validation Layer"
        IV[Input Validator]
        OS[Output Sanitizer]
    end

    subgraph "Trusted Zone"
        subgraph "Encrypted Storage"
            UDATA[User Data]
        end
        subgraph "Application Core"
            BL[Business Logic]
        end
    end

    subgraph "Output Zone"
        PDFO[PDF Output]
    end

    USER --> IV
    LLM3 --> OS
    IV --> BL
    OS --> BL
    BL <--> UDATA
    BL --> PDFO

    style USER fill:#ffcccc
    style LLM3 fill:#ffcccc
    style IV fill:#ffff99
    style OS fill:#ffff99
    style UDATA fill:#99ff99
    style BL fill:#99ccff
```

## Parallel Development Workflow

```mermaid
gantt
    title Multi-Developer Timeline
    dateFormat  YYYY-MM-DD
    section Foundation
    Define Interfaces        :done, 2024-01-01, 3d
    Setup Structure          :done, 2024-01-03, 2d

    section Track A (PDF)
    PDF Infrastructure       :active, 2024-01-05, 5d
    Extract Fields UseCase   :active, 2024-01-05, 5d

    section Track B (Data)
    Persistence Layer        :active, 2024-01-05, 5d
    Update Data UseCase      :active, 2024-01-05, 5d

    section Track C (Filling)
    Fill Form UseCase        :active, 2024-01-05, 5d
    Field Matching           :active, 2024-01-05, 5d

    section Integration
    CLI Integration          :2024-01-10, 3d
    End-to-End Testing       :2024-01-12, 3d
```

## Plugin Architecture

```mermaid
graph TD
    subgraph "Core System"
        PR[Plugin Registry]
        PI[Plugin Interface]
        CORE[Core Functionality]
    end

    subgraph "Optional Plugins"
        subgraph "LLM Plugin"
            LLMP[LLM Plugin<br/>requires: transformers]
        end
        subgraph "Cloud Plugin"
            CP[Cloud Storage<br/>requires: boto3]
        end
        subgraph "Web Plugin"
            WP[Web Interface<br/>requires: flask]
        end
    end

    CORE --> PI
    PR --> PI

    LLMP -.-> PR
    CP -.-> PR
    WP -.-> PR

    style CORE fill:#99ff99
    style PI fill:#ffccff
    style PR fill:#ffeb99
    style LLMP fill:#ffcc99
    style CP fill:#99ccff
    style WP fill:#ff99cc
```

## Testing Strategy

```mermaid
graph TD
    subgraph "Test Pyramid"
        UT[Unit Tests<br/>80% coverage]
        IT[Integration Tests<br/>Key workflows]
        E2E[End-to-End Tests<br/>Critical paths]
        CT[Contract Tests<br/>Module interfaces]
    end

    subgraph "Test Types"
        SEC[Security Tests<br/>Data protection]
        PERF[Performance Tests<br/>Large PDFs]
        ACC[Acceptance Tests<br/>User scenarios]
    end

    UT --> IT
    IT --> E2E
    IT --> CT

    E2E --> SEC
    E2E --> PERF
    E2E --> ACC

    style UT fill:#99ff99
    style IT fill:#ffeb99
    style E2E fill:#ff99cc
    style CT fill:#99ccff
```

## Legend

### Colors
- 🟨 Yellow: Presentation/Interface Layer
- 🟩 Green: Application/Business Logic Layer
- 🟦 Blue: Infrastructure/External Layer
- 🌸 Pink: Domain/Core Layer
- 🟪 Purple: Abstract/Interface Layer
- 🟥 Red: Security Concern/Legacy Code

### Line Types
- Solid Line (→): Direct dependency
- Dotted Line (-.->): Optional/plugin dependency
- Double Arrow (↔): Bidirectional communication
