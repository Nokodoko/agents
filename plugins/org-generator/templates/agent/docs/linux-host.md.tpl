# Linux Host Installation Guide

## Prerequisites

- Linux distribution (Ubuntu, Debian, RHEL, CentOS, Amazon Linux, etc.)
- Root/sudo access
- Outbound internet access to `*.{{SITE}}`

## Installation

### One-Line Install (Recommended)

```bash
{{SITE_PARAM}}DD_API_KEY="YOUR_API_KEY" DD_AGENT_MAJOR_VERSION=7 bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"
```

### Manual Installation

#### Ubuntu/Debian

```bash
# Add Datadog repository
sudo sh -c "echo 'deb [signed-by=/usr/share/keyrings/datadog-archive-keyring.gpg] https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
sudo touch /usr/share/keyrings/datadog-archive-keyring.gpg
sudo chmod a+r /usr/share/keyrings/datadog-archive-keyring.gpg

curl https://keys.datadoghq.com/DATADOG_APT_KEY_CURRENT.public | sudo gpg --no-default-keyring --keyring /usr/share/keyrings/datadog-archive-keyring.gpg --import --batch

# Install agent
sudo apt-get update
sudo apt-get install datadog-agent datadog-signing-keys
```

#### RHEL/CentOS

```bash
# Add Datadog repository
cat <<EOF | sudo tee /etc/yum.repos.d/datadog.repo
[datadog]
name = Datadog, Inc.
baseurl = https://yum.datadoghq.com/stable/7/x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://keys.datadoghq.com/DATADOG_RPM_KEY_CURRENT.public
       https://keys.datadoghq.com/DATADOG_RPM_KEY_B01082D3.public
       https://keys.datadoghq.com/DATADOG_RPM_KEY_FD4BF915.public
       https://keys.datadoghq.com/DATADOG_RPM_KEY_E09422B3.public
EOF

# Install agent
sudo yum makecache
sudo yum install datadog-agent
```

## Configuration

1. Copy the main configuration:
   ```bash
   sudo cp datadog.yaml /etc/datadog-agent/datadog.yaml
   ```

2. Set your API key:
   ```bash
   sudo sed -i 's/YOUR_API_KEY_HERE/<your-actual-api-key>/' /etc/datadog-agent/datadog.yaml
   ```

3. Copy integration configs:
   ```bash
   # Example for custom logs
   sudo mkdir -p /etc/datadog-agent/conf.d/custom_logs.d
   sudo cp conf.d/custom_logs.yaml /etc/datadog-agent/conf.d/custom_logs.d/conf.yaml
   ```

4. Set permissions:
   ```bash
   sudo chown -R dd-agent:dd-agent /etc/datadog-agent
   sudo chmod 640 /etc/datadog-agent/datadog.yaml
   ```

## Start the Agent

```bash
sudo systemctl enable datadog-agent
sudo systemctl start datadog-agent
sudo systemctl status datadog-agent
```

## Verify Installation

```bash
sudo datadog-agent status
sudo datadog-agent configcheck
```

## Troubleshooting

### Agent won't start

```bash
sudo cat /var/log/datadog/agent.log
sudo datadog-agent configcheck
```

### Permission issues

```bash
sudo chown -R dd-agent:dd-agent /etc/datadog-agent
sudo usermod -a -G adm dd-agent
```

## Useful Commands

```bash
sudo systemctl restart datadog-agent
sudo datadog-agent config
sudo datadog-agent check <integration_name>
sudo datadog-agent flare
```
