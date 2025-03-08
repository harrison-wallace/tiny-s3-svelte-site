# Static Site Deployment Template

This repository provides a template for deploying a static website to AWS S3 using Terraform and a Jenkins pipeline. It’s designed to be modular and customizable for dev and prod environments.

## Prerequisites
- **AWS Account** with credentials configured (AWS CLI or Jenkins credentials).
- **Jenkins Server** with AWS CLI and Terraform installed.
- **Git** for version control.

## Repository Structure
- `Jenkinsfile`: CI/CD pipeline configuration.
- `manifest.json`: Controls deployment for dev/prod.
- `terraform/`: Terraform configurations for S3 hosting.
- `src/`: Static site files (e.g., `index.html`).
- `LICENSE`: MIT License for public use.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone <your-repo-url>
   cd tiny-s3-svelte-site