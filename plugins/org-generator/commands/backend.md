---
name: backend
description: Create S3 backend bucket for Terraform state
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "<client-name>"
---

# org-generator:backend

Creates an S3 backend bucket for storing Terraform state following the `{client-name}-backend` naming convention.

## Usage

```
/org-generator:backend <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Workflow

### Step 1: Check Existing Backends

1. Read `~/Portfolio/aws/variables.tf`
2. Check if `<client-name>-backend` already exists in the `s3` variable map
3. If exists, skip creation and validate bucket exists

### Step 2: Add Backend Entry

Add entry to `~/Portfolio/aws/variables.tf`:

```hcl
variable "s3" {
  description = "s3 buckets"
  type        = map(any)
  default = {
    # ... existing entries ...
    <client-name>-backend = {
      env        = "projects"
      encryption = "AES256"
    }
  }
}
```

### Step 3: Apply Terraform

```bash
cd ~/Portfolio/aws/
terraform init
terraform plan -target=module.s3["<client-name>-backend"]
terraform apply -target=module.s3["<client-name>-backend"] -auto-approve
```

### Step 4: Validate Creation

```bash
aws s3 ls s3://<client-name>-backend --region us-east-1
```

## S3 Backend Configuration

The backend bucket is created with:
- **Encryption**: AES256 server-side encryption
- **Versioning**: Enabled (via module configuration)
- **Region**: us-east-1
- **Environment tag**: projects

## Module Reference

Uses the S3 module at `~/Portfolio/aws/modules/s3/`:

```hcl
module "s3" {
  source     = "./modules/s3/"
  for_each   = var.s3
  name       = each.key
  env        = each.value.env
  encryption = each.value.encryption
}
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Bucket already exists | Skip creation, verify access |
| AWS credentials missing | Run `aws configure` or set environment variables |
| Terraform init fails | Check AWS provider configuration |
| Apply fails | Check IAM permissions for S3 bucket creation |

## Example

```
/org-generator:backend acme-corp
```

This will:
1. Add `acme-corp-backend` to `~/Portfolio/aws/variables.tf`
2. Run terraform apply to create the bucket
3. Verify bucket exists and is accessible
