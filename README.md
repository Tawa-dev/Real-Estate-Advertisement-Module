# 🏡 Odoo Real Estate Advertisement Module
## 🌟 Project Overview
This Odoo module is a comprehensive Real Estate Advertisement solution designed to streamline property listing, management, and sales processes. This module demonstrates advanced Odoo development skills and innovative approach to real estate management.

## ✨ Key Features
### 🔍 Property Management
- Comprehensive property listing with detailed attributes
- Dynamic property states (New, Offer Received, Offer Accepted, Sold, Cancelled)
- Intelligent offer management system

### 📊 Advanced Functionality
- Automatic deadline calculations for property offers
- Price validation and constraints
- Integrated accounting with commission and administrative fee generation

## 🚀 Technical Highlights
### Architectural Approach
- Modular design following Odoo best practices
- Clean, maintainable code structure
- Extensible models with robust constraints and compute methods

### Models Implemented
- `estate.property`: Core property listing model
- `estate.property.offer`: Offers management
- `estate.property.type`: Property categorization
- `estate.property.tag`: Flexible tagging system

## 📦 Installation
### Prerequisites
- Odoo 18.0
- Python 3.8+

### Comprehensive Installation Guide

#### 1. Download and Install Odoo
1. Visit the official Odoo website (https://www.odoo.com/page/download)
2. Download the Odoo Community Edition (18.0)
3. Run the installer
4. During installation, allow Odoo to install PostgreSQL
   - If prompted, select "Install PostgreSQL"
   - Note the PostgreSQL password you set during installation

#### 2. VS Code Setup for Odoo Development

##### Installation and Configuration
1. Download and install Visual Studio Code
2. Install the Python extension from the VS Code marketplace
3. Open VS Code
4. Press `Ctrl+Shift+P` and type "Python: Select Interpreter"
5. Choose the Python executable from your Odoo installation directory

##### Debugging Configuration
1. Click on the "Run and Debug" icon in the left sidebar (Ctrl+Shift+D)
2. Click "create a launch.json file"
3. Select "Python Debugger"
4. Replace the contents of `launch.json` with:

```json
{
    "version": "0.2.0",
    "configurations": [{
        "name": "Python: Odoo18",
        "type": "python",
        "request": "launch",
        "stopOnEntry": false,
        "python": "C:\\Users\\Tawa-dev\\Documents\\Odoo18\\python\\python.exe",
        "console": "integratedTerminal",
        "program": "${workspaceRoot}\\odoo-bin",
        "args": [
            "--config=${workspaceRoot}\\odoo.conf",
        ],
        "cwd": "${workspaceRoot}",
        "env": {},
        "envFile": "${workspaceRoot}/.env",
        "debugOptions": [
            "RedirectOutput"
        ]
    }]
}
```

##### Important Notes
- Adjust the `python` path to match your specific Odoo installation path
- If Odoo is installed in Program Files and you lack write permissions:
  - Right-click VS Code and select "Run as Administrator"
  - Alternatively, install Odoo in a user-accessible directory

#### 3. Module Installation
1. Copy the `estate` and `estate_account` directories to your Odoo custom addons folder
2. Update the `addons_path` in your `odoo.conf` file to include the custom addons directory
3. Start the Odoo server
4. Activate Developer Mode in Odoo:
   - Go to Settings
   - Click on the "Developer Mode" option (top right)
5. Update the Apps list
6. Search for "estate" in the Apps
7. Install both `estate` and `estate_account` modules

## 🌈 Key Innovations
### Smart Offer Management
- Automatic price comparison
- Deadline tracking
- Status-based workflow management

### Accounting Integration
- Automatic invoice generation upon property sale
- 6% commission calculation
- Standardized administrative fee handling

## 📝 Development Notes
### Design Principles
- Domain-driven design
- Separation of concerns
- Extensible architecture

### Performance Considerations
- Efficient compute methods
- Minimal database queries
- Intelligent constraints

## 🤝 Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Commit with clear, descriptive messages
4. Submit a pull request


## 👨‍💻 Author
**Tawanda Mutasa**
- GitHub: [@Tawa-dev](https://github.com/Tawa-dev)

## 🌍 Acknowledgements
Special thanks to the team at CodeBurnout for the opportunity to showcase Odoo development skills.

---
**Developed with ❤️ and 🧠 by a passionate Odoo developer**
