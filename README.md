# Edge Hub

## Overview
Edge Hub is a microservice in the Aku platform ecosystem. It acts as a gateway for edge devices, handling data ingestion, device management, and secure communication.

## Features
- REST API for edge device integration
- Scalable Node.js backend

## Getting Started

### Prerequisites
- Node.js 20+
- Docker (optional)

### Development
```bash
git clone <repo-url>
cd EdgeHub
npm install
npm run dev
```

### Docker
```bash
docker build -t edge-hub:latest .
docker run -p 8080:8080 edge-hub:latest
```

### Testing
```bash
npm test
```

## Deployment
See `.github/workflows/ci.yml` for CI/CD pipeline.

## License
MIT
