# 🏦 CryptoStock Control System

## 📘 Abstract
The **CryptoStock Control System** is an innovative solution designed to automate inventory management and purchasing processes using **blockchain technology** and **cryptocurrency transactions**.  
This system ensures transparency, security, and automation in the supply management process. It integrates **Flask**, **MetaMask**, and **the Hedera network** to enable automatic supplier notifications, quotation responses, and crypto-based purchases.

---

## 🎯 Objectives
The main goal of this project is to **automate the management and replenishment of stock** in a company using decentralized technologies.  
The specific objectives are:
- To monitor stock levels automatically.
- To alert suppliers when stock is low.
- To receive and process supplier quotations.
- To enable secure and verifiable crypto transactions for restocking.
- To record all stock events transparently on the **Hedera Hashgraph blockchain**.

---

## 🧠 Introduction
Traditional stock management systems rely heavily on manual operations and centralized databases. These systems often face challenges such as delays in supplier communication, human error, and lack of transparency in transactions.  
The **CryptoStock Control System** addresses these issues by leveraging blockchain technology and decentralized communication protocols to ensure reliability, traceability, and automation.

---

## ⚙️ System Architecture
The system is composed of three main layers:

1. **Application Layer (Flask Backend + Frontend)**  
   - Manages user interactions and simulates stock levels.  
   - Sends automatic email alerts when stock falls below a predefined threshold.  
   - Receives supplier responses with updated prices.

2. **Blockchain Layer (Hedera Smart Contracts)**  
   - Records each purchasing transaction in a transparent and immutable manner.  
   - Ensures that all parties have access to the same verified data.  
   - Handles crypto payments through the MetaMask wallet and Ethers.js integration.

3. **Data Layer (Local JSON Storage)**  
   - Stores event logs (alerts, purchases, responses) for traceability.  
   - Allows local analysis of transaction history and stock evolution.

---

## 🧩 System Workflow
1. The Flask application continuously monitors stock levels.  
2. When stock drops below a threshold, an **automatic email** is sent to the supplier.  
3. The supplier responds with a **price quotation** and available quantity.  
4. The company can confirm the purchase through **MetaMask**, completing a transaction recorded on the **Hedera network**.  
5. The local database updates the stock level and stores all transaction details.

---

## 🔐 Technologies Used
| Layer | Technology | Description |
|-------|-------------|-------------|
| **Backend** | Flask (Python) | Controls logic, email alerts, and blockchain interaction |
| **Blockchain** | Hedera Hashgraph | Records and secures smart contract operations |
| **Smart Contracts** | Solidity | Defines transaction logic and purchase flow |
| **Frontend** | HTML, JavaScript, Ethers.js | Manages user interface and crypto wallet interaction |
| **Wallet** | MetaMask | Enables decentralized crypto payments |
| **Email Automation** | Flask-Mail (SMTP) | Sends supplier alerts automatically |
| **Data Storage** | JSON Files | Stores logs and transaction details locally |

---

## 🧮 Features
- Automatic detection of low stock levels.  
- Instant supplier notifications via email.  
- Supplier quotation handling and verification.  
- Crypto-based purchase execution using MetaMask.  
- Immutable blockchain records for every transaction.  
- Event logging and historical traceability.

---

## 📊 Advantages
- **Transparency:** All stock and payment activities are stored on a public ledger.  
- **Automation:** Minimal human intervention in routine purchasing tasks.  
- **Security:** Transactions verified by the Hedera blockchain.  
- **Reliability:** Reduces errors and delays in supply chain communication.

---

## 🧠 Future Enhancements
- Integration with **IoT devices** for real-time stock measurement.  
- Development of an **analytics dashboard** for decision-making.  
- Implementation of **multi-supplier smart contracts** to handle competitive offers.  
- Integration with **IPFS** for decentralized storage of invoices and purchase records.

---

## 📚 Conclusion
The **CryptoStock Control System** demonstrates the potential of blockchain technology to revolutionize industrial processes such as stock management and procurement.  
By combining **automation**, **decentralization**, and **cryptocurrency payments**, this system achieves a high level of transparency, security, and efficiency — representing a significant step toward the **Industry 4.0** vision.

---

## 👤 Author
**Abdou [@abduu771-hub](https://github.com/abduu771-hub)**  
Fifth-Year Computer Science Engineering Student — Morocco  

---

