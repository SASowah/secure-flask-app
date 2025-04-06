# secure-flask-app
# Secure Flask App with HTTPS, MongoDB, and Artifact Hash Verification

## 📌 Project Overview
This project demonstrates a secure DevOps pipeline to deploy a **Flask** web application with **MongoDB**, **Let's Encrypt SSL**, and **artifact hash verification** for integrity checks. The deployment is automated using **Jenkins**, **Ansible**, and **GitHub**.

## 🏗️ Architecture
The project consists of three AWS EC2 instances:
- **Jenkins Master** (Amazon Linux) - Manages CI/CD pipeline
- **Jenkins Agent** (CentOS 8) - Builds and verifies artifacts
- **Application Server** (Ubuntu 20.04) - Hosts Flask app with MongoDB

## 🛠️ Technologies Used
- **Flask** (Python Web Framework)
- **MongoDB** (Database for storing app messages)
- **Jenkins** (CI/CD Automation)
- **Ansible** (Configuration Management)
- **Nginx** (Reverse Proxy & SSL Termination)
- **Certbot** (Let's Encrypt SSL Certificate)
- **GitHub** (Version Control)

## 🔧 Infrastructure Setup
| Server Name | OS | Role |
|-------------|--------------|---------------------------------|
| `jenkins-master` | Amazon Linux | Jenkins Master |
| `jenkins-agent` | CentOS 8 | Jenkins Agent (build & verify) |
| `app-server` | Ubuntu 20.04 | Flask App + MongoDB + Nginx |

## 🚀 Project Workflow
1. **Code Commit** - Developer pushes Flask app to GitHub.
2. **Jenkins Build** - Jenkins pulls the latest code, packages the app, and generates `hash.txt` (SHA-256 checksum).
3. **Artifact Verification** - Ansible checks artifact integrity before deployment.
4. **Ansible Deployment** - Deploys Flask app, MongoDB, Nginx (reverse proxy), and SSL certificate.
5. **Application Access** - The app is accessible via HTTPS on port `443`.

## 📂 Project Structure
```bash
secure-flask-app/
│
│-- roles/
│   │-- app_server/
│   │-- jenkins_agent/
│   │
│-- src/│   │
│   │-- app.py
│   │-- requirements.txt
│   │-- init.db.js
│   │-- templates/
│   │   ├── index.html
│   │
│-- templates/
│   │-- flask_app.service.j2
│   │-- index.html
│   │
│-- jenkins/
│   │-- Jenkinsfile
│-- README.md
```

## 🛠️ Installation & Deployment
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SASowah/secure-flask-app.git
cd secure-flask-app
```

### 2️⃣ Install Dependencies on Application Server
```bash
sudo apt update && sudo apt install -y python3-pip nginx certbot
pip3 install -r src/requirements.txt
```

### 3️⃣ Setup Jenkins Pipeline
- Configure Jenkins on `jenkins-master`.
- Create a pipeline job pointing to GitHub.
- Add **Jenkinsfile** to automate builds.

### 4️⃣ Run Ansible Playbook
```bash
ansible-playbook -i inventory ansible/deploy.yml
```

## ✅ Expected Output
- The application should display:
  ```
  Secure DevOps app deployed with verified artifact!
  ```
- Accessible via `https://yourdomain.com`

## 🔮 Future Enhancements
- Implement CI/CD for automatic rollback on failure
- Add Prometheus & Grafana for monitoring
- Implement Kubernetes for scalability

---
