---
name: validate
description: Validate environment variables and terraform configuration
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
argument-hint: "<client-name>"
---

# org-generator:validate

Validates that all required environment variables are set and terraform configuration is valid.

## Usage

```
/org-generator:validate <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Prerequisites

1. S3 backend must exist (`<client-name>-backend`)
2. Terraform structure must exist at `~/datadog_terraform/<client-name>/`

## Validation Steps

### Step 1: Validate S3 Backend

```bash
aws s3 ls s3://<client-name>-backend --region us-east-1
```

**Expected**: Bucket exists and is accessible
**Error**: Bucket does not exist or access denied

### Step 2: Validate Environment Variables

Check for required Datadog credentials using the TF_VAR pattern:

```bash
# Client name with hyphens converted to underscores
# e.g., acme-corp -> acme_corp

test -n "$TF_VAR_<client_name>_api_key" && echo "API key: SET" || echo "API key: MISSING"
test -n "$TF_VAR_<client_name>_app_key" && echo "App key: SET" || echo "App key: MISSING"
```

**Expected**: Both variables are set
**Error**: One or both variables are missing

### Step 3: Re-source Environment (if needed)

If variables are missing, attempt to re-source shell profile:

```bash
# Detect shell and source appropriate file
if [ -n "$ZSH_VERSION" ]; then
  source ~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
  source ~/.bashrc
fi
```

Then re-check variables.

### Step 4: Terraform Init

```bash
cd ~/datadog_terraform/<client-name>/
terraform init
```

**Expected**: Initialization complete with no errors
**Errors**:
- Backend configuration invalid
- Provider download fails
- Module not found

### Step 5: Terraform Validate

```bash
cd ~/datadog_terraform/<client-name>/
terraform validate
```

**Expected**: "Success! The configuration is valid."
**Errors**:
- Missing required variable
- Syntax error
- Invalid resource configuration

## Environment Variable Convention

Client credentials follow this pattern:

```bash
# Pattern: TF_VAR_{client_name}_api_key
# Hyphens in client name become underscores

# Example for client "acme-corp":
export TF_VAR_acme_corp_api_key="your-api-key-here"
export TF_VAR_acme_corp_app_key="your-app-key-here"
```

## Creating Datadog Keys

If keys are missing, instruct user:

1. **API Key**:
   - Go to Datadog > Organization Settings > API Keys
   - Create new key named `<client-name>-terraform`
   - Copy the key value

2. **App Key**:
   - Go to Datadog > Organization Settings > Application Keys
   - Create new key named `<client-name>-terraform`
   - Copy the key value

3. **Add to environment**:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc:
   export TF_VAR_<client_name>_api_key="your-api-key"
   export TF_VAR_<client_name>_app_key="your-app-key"

   # Then source the file:
   source ~/.bashrc  # or source ~/.zshrc
   ```

## Validation Report

Output a summary:

```
Validation Report for <client-name>
====================================

S3 Backend:
  Bucket: <client-name>-backend
  Status: EXISTS / MISSING

Environment Variables:
  TF_VAR_<client_name>_api_key: SET / MISSING
  TF_VAR_<client_name>_app_key: SET / MISSING

Terraform Init:
  Status: SUCCESS / FAILED
  Error: <error message if failed>

Terraform Validate:
  Status: SUCCESS / FAILED
  Error: <error message if failed>

Overall: READY / NOT READY
```

## Error Resolution

| Issue | Resolution |
|-------|------------|
| S3 bucket missing | Run `/org-generator:backend <client-name>` |
| API key missing | Create in Datadog UI, add to environment |
| App key missing | Create in Datadog UI, add to environment |
| Terraform init fails | Check backend config, AWS credentials |
| Terraform validate fails | Check variable definitions, module syntax |

## Example

```
/org-generator:validate acme-corp
```

This will:
1. Check S3 backend `acme-corp-backend` exists
2. Verify `TF_VAR_acme_corp_api_key` is set
3. Verify `TF_VAR_acme_corp_app_key` is set
4. Run `terraform init`
5. Run `terraform validate`
6. Output validation report
