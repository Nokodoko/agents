#!/bin/bash
# terraform-context.sh
# Hook to detect terraform blocks and provide context for tfmaster workflow
#
# This hook is triggered when working with terraform files and provides
# context about the current terraform project structure.

set -e

# Get the current file being edited (passed as argument)
CURRENT_FILE="${1:-}"
CURRENT_DIR="${2:-$(pwd)}"

# Function to find terraform root directory
find_terraform_root() {
    local dir="$1"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/backend.tf" ]] || [[ -f "$dir/main.tf" ]] || [[ -f "$dir/providers.tf" ]]; then
            echo "$dir"
            return 0
        fi
        dir=$(dirname "$dir")
    done
    return 1
}

# Function to detect terraform block type
detect_block_type() {
    local file="$1"
    local content

    if [[ ! -f "$file" ]]; then
        return 1
    fi

    content=$(cat "$file")

    # Detect resource blocks
    if echo "$content" | grep -q 'resource "datadog_monitor"'; then
        echo "monitor"
    elif echo "$content" | grep -q 'resource "datadog_dashboard"'; then
        echo "dashboard"
    elif echo "$content" | grep -q 'resource "datadog_synthetics_test"'; then
        echo "synthetic"
    elif echo "$content" | grep -q 'resource "datadog_role"'; then
        echo "role"
    elif echo "$content" | grep -q 'resource "datadog_team"'; then
        echo "team"
    elif echo "$content" | grep -q 'resource "datadog_api_key"'; then
        echo "api_key"
    elif echo "$content" | grep -q 'resource "datadog_application_key"'; then
        echo "app_key"
    elif echo "$content" | grep -q 'resource "datadog_synthetics_private_location"'; then
        echo "private_location"
    elif echo "$content" | grep -q 'module "'; then
        echo "module"
    elif echo "$content" | grep -q 'variable "'; then
        echo "variable"
    elif echo "$content" | grep -q 'output "'; then
        echo "output"
    else
        echo "unknown"
    fi
}

# Function to get client name from path
get_client_name() {
    local dir="$1"

    # Expected pattern: ~/datadog_terraform/<client-name>/
    if [[ "$dir" =~ datadog_terraform/([^/]+) ]]; then
        echo "${BASH_REMATCH[1]}"
        return 0
    fi

    return 1
}

# Function to check if this is an org-generator managed project
is_org_generator_project() {
    local dir="$1"

    # Check for questionnaire.md (indicator of org-generator managed project)
    if [[ -f "$dir/questionnaire.md" ]]; then
        return 0
    fi

    return 1
}

# Function to output context as JSON
output_context() {
    local terraform_root="$1"
    local block_type="$2"
    local client_name="$3"
    local is_managed="$4"

    cat <<EOF
{
    "terraform_root": "$terraform_root",
    "block_type": "$block_type",
    "client_name": "$client_name",
    "is_org_generator_managed": $is_managed,
    "available_modules": $(list_modules "$terraform_root"),
    "state_backend": $(get_backend_info "$terraform_root")
}
EOF
}

# Function to list available modules
list_modules() {
    local dir="$1"
    local modules_dir="$dir/modules"

    if [[ -d "$modules_dir" ]]; then
        echo -n "["
        local first=true
        for module in "$modules_dir"/*/; do
            if [[ -d "$module" ]]; then
                local name=$(basename "$module")
                if [[ "$first" == true ]]; then
                    first=false
                else
                    echo -n ","
                fi
                echo -n "\"$name\""
            fi
        done
        echo "]"
    else
        echo "[]"
    fi
}

# Function to get backend info
get_backend_info() {
    local dir="$1"
    local backend_file="$dir/backend.tf"

    if [[ -f "$backend_file" ]]; then
        local bucket=$(grep -o 'bucket\s*=\s*"[^"]*"' "$backend_file" | sed 's/.*"\([^"]*\)".*/\1/' || echo "")
        local region=$(grep -o 'region\s*=\s*"[^"]*"' "$backend_file" | sed 's/.*"\([^"]*\)".*/\1/' || echo "us-east-1")
        echo "{\"type\": \"s3\", \"bucket\": \"$bucket\", \"region\": \"$region\"}"
    else
        echo "{\"type\": \"local\"}"
    fi
}

# Main execution
main() {
    local terraform_root=""
    local block_type="unknown"
    local client_name=""
    local is_managed="false"

    # Find terraform root
    if terraform_root=$(find_terraform_root "$CURRENT_DIR"); then
        # Get client name
        if client_name=$(get_client_name "$terraform_root"); then
            : # Success
        else
            client_name=""
        fi

        # Check if org-generator managed
        if is_org_generator_project "$terraform_root"; then
            is_managed="true"
        fi

        # Detect block type if file provided
        if [[ -n "$CURRENT_FILE" ]]; then
            block_type=$(detect_block_type "$CURRENT_FILE")
        fi
    fi

    # Output context
    output_context "$terraform_root" "$block_type" "$client_name" "$is_managed"
}

# Run main if not being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
