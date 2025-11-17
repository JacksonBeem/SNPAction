# SNP Serverless Deployment (AWS + Terraform + Ansible + GitHub Actions)

This repository deploys the **SNP** application — a Python-based AWS Lambda backend and a static HTML/CSS/JS frontend — as a fully automated **serverless infrastructure** using:

- **Terraform** – Infrastructure-as-Code for Lambda, API Gateway, S3 + CloudFront  
- **Ansible** – Automates S3 upload and CloudFront invalidation  
- **GitHub Actions** – Continuous Integration / Continuous Deployment (CI/CD) pipeline  

---

## Architecture Overview


### AWS Components
| Component | Purpose |
|------------|----------|
| **Lambda** | Python 3.12 function (`lambda_handler.py`) |
| **API Gateway (HTTP API)** | Public endpoint forwarding requests to Lambda |
| **S3 Bucket** | Hosts static frontend assets (private bucket) |
| **CloudFront** | CDN + HTTPS edge delivery for S3 content |
| **IAM Roles** | Scoped roles for Lambda execution and CI/CD access |
| **S3 + DynamoDB Backend** | Stores Terraform state and lock |

---

## How the Automation Works

| Stage | Tool | Description |
|--------|------|-------------|
| **1. Build** | **GitHub Actions** | Packages `backend/` into a ZIP for Lambda |
| **2. Infrastructure** | **Terraform** | Provisions Lambda, API Gateway, S3, CloudFront, IAM roles |
| **3. State Storage** | **S3 + DynamoDB** | Remote Terraform backend for consistency |
| **4. Deploy Frontend** | **Ansible** | Uploads all files from `frontend/` to S3 and invalidates CloudFront cache |
| **5. Continuous Deployment** | **GitHub Actions** | Runs automatically on every push to `main` |

---

  
---

## Deployment Steps (New Workflow)

### 1️⃣ **Prepare AWS credentials**
In your GitHub repo →  
**Settings → Secrets and variables → Actions**

Add:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

(Use the IAM user `terraform` that has Admin or sufficient rights.)

---

### 2️⃣ **Push to main branch**
GitHub Actions triggers automatically:
1. Builds the Lambda ZIP  
2. Creates/updates Terraform remote state (S3 + DynamoDB)  
3. Applies Terraform (`infra/`)  
4. Runs Ansible to upload frontend and invalidate CloudFront  

You can also run manually:  
**Actions → Deploy SNP Serverless → Run workflow**

---

### 3️⃣ **Outputs**
When the workflow finishes successfully, the console shows:

| Output | Example |
|--------|----------|
| **S3 Bucket** | `snp-9a12b3cd` |
| **CloudFront Domain** | `d1234abcd.cloudfront.net` |
| **API URL** | `https://abc123.execute-api.us-east-2.amazonaws.com` |

Open the CloudFront domain in a browser to view your deployed frontend.

---

## Steps We Took to Build This

1. **Created core app structure**
   - `backend/lambda_handler.py` for the Python Lambda.  
   - `frontend/index.html` for the static site.

2. **Wrote Terraform definitions**
   - IAM Role, Lambda, API Gateway, S3 bucket, CloudFront (OAC).  
   - Added remote state (S3 + DynamoDB).  
   - Added unique suffixes and lowercase normalization.

3. **Built GitHub Actions pipeline**
   - Automatic packaging of backend.  
   - Remote-state initialization.  
   - `terraform init/validate/plan/apply`.  
   - Captured Terraform outputs for Ansible.

4. **Wrote Ansible playbook**
   - Generates `config.json` (with API URL).  
   - Syncs `frontend/` to S3 (`community.aws.s3_sync`).  
   - Invalidates CloudFront cache (`community.aws.cloudfront_invalidation`).

5. **Iterated and debugged**
   - Fixed capitalization rules for S3.  
   - Added remote state to prevent 409 conflicts.  
   - Adjusted Terraform formatting.  
   - Corrected CloudFront invalidation module arguments.  
   - Verified end-to-end deployment from GitHub Actions.

    ---
    


