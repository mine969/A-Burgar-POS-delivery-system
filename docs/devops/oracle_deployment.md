# Deploying to Oracle Cloud

This guide explains how to deploy the Fullstack Container application to an Oracle Cloud Infrastructure (OCI) Compute Instance.

## Prerequisites

1.  An Oracle Cloud account (Free Tier is sufficient).
2.  SSH Key pair (public and private keys).

## Step 1: Create a Compute Instance

1.  Log in to the **Oracle Cloud Console**.
2.  Go to **Compute** -> **Instances**.
3.  Click **Create Instance**.
4.  **Name**: Give your instance a name (e.g., `food-delivery-app`).
5.  **Image and Shape**:
    - **Image**: Canonical Ubuntu 22.04 or 24.04 (recommended).
    - **Shape**:
      - **VM.Standard.A1.Flex** (Ampere ARM) is a great choice for the Free Tier (up to 4 OCPUs, 24GB RAM).
      - **VM.Standard.E2.1.Micro** (AMD) is also free but less powerful.
6.  **Networking**:
    - Create a new virtual cloud network (VCN) or select an existing one.
    - Ensure "Assign a public IPv4 address" is selected.
7.  **Add SSH Keys**:
    - Upload your public key file (`.pub`) or paste the key content.
8.  Click **Create**.

## Step 2: Configure Security List (Firewall)

By default, Oracle Cloud only allows SSH (port 22). You need to open ports for the application.

1.  In the Instance details page, click on the **Subnet** link (under Primary VNIC).
2.  Click on the **Security List** for your subnet (e.g., `Default Security List for...`).
3.  Click **Add Ingress Rules**.
4.  Add the following rules:
    - **Source CIDR**: `0.0.0.0/0` (Allows access from anywhere)
    - **IP Protocol**: TCP
    - **Destination Port Range**: `3000, 3001, 8888` (Comma separated or add separate rules)
      - `3000`: Frontend
      - `3001`: Backend API
      - `8888`: PHPMyAdmin (Optional, for database management)
5.  Click **Add Ingress Rules**.

## Step 3: Connect to the Instance

Use your terminal (or PuTTY on Windows) to SSH into the VM.

```bash
ssh -i /path/to/your/private_key ubuntu@<YOUR_VM_PUBLIC_IP>
```

## Step 4: Deploy the Application

Once connected to the VM, follow these steps:

1.  **Clone the Repository**:

    ```bash
    git clone <YOUR_GITHUB_REPO_URL>
    cd fullstack_container
    ```

    _(Note: You might need to generate an SSH key on the VM and add it to GitHub, or use HTTPS with a Personal Access Token)_

2.  **Run the Setup Script**:
    We have provided a script to automate the installation of Docker and the application setup.

    ```bash
    chmod +x oracle_setup.sh
    ./oracle_setup.sh
    ```

    This script will:

    - Update the system.
    - Install Docker and Docker Compose.
    - Create a `.env` file with secure random passwords.
    - Build and start the containers.

## Step 5: Configure Instance Firewall (iptables)

Oracle Ubuntu images often have `iptables` rules that block traffic even if the Security List allows it. You need to open the ports on the VM itself.

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 3000 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 3001 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8888 -j ACCEPT
sudo netfilter-persistent save
```

_(If `netfilter-persistent` is not installed, the script might have installed Docker which handles some iptables rules, but it's good to be sure. You can also use `ufw` if you prefer, but be careful not to lock yourself out)._

## Step 6: Access the Application

Open your browser and visit:

- **Frontend**: `http://<YOUR_VM_PUBLIC_IP>:3000`
- **Backend API**: `http://<YOUR_VM_PUBLIC_IP>:3001`
- **PHPMyAdmin**: `http://<YOUR_VM_PUBLIC_IP>:8888`

## Troubleshooting

- **Cannot access the site?**
  - Check the Oracle Cloud Security List (Ingress Rules).
  - Check the VM's internal firewall (`sudo iptables -L` or `sudo ufw status`).
  - Check if containers are running: `sudo docker compose ps`.
  - Check logs: `sudo docker compose logs -f`.
