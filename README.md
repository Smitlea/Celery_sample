graph TD
    A[Start] --> B[Prepare API Key]
    B --> C[Set API Endpoint]
    C --> D[Compose Request Payload]
    D --> E[Send POST Request]
    E --> F{Check Response Status}
    F -->|Success| G[Process Response Data]
    F -->|Failure| H[Handle Error]
    G --> I[End]
    H --> I[End]
