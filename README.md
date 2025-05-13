# Solana Staking Application

![Solana](https://img.shields.io/badge/Solana-4.0-purple)
![React](https://img.shields.io/badge/React-18.0-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-4.9-blue)

A modern, user-friendly web application for staking SOL tokens on the Solana blockchain. Built with React, TypeScript, and Solana Web3.js.

## ✨ Features

- **Wallet Integration**: Connect with Phantom, Solflare, and other Solana wallets
- **Real-time Balance**: See your SOL balance update in real-time
- **Staking Management**: Stake SOL tokens with validators on Solana devnet
- **Transaction History**: View your complete staking transaction history
- **Transaction Verification**: Direct links to Solana Explorer for each transaction
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark Mode Support**: Toggle between light and dark themes

## 🛠️ Technologies

- **Frontend**: React, TypeScript, CSS3
- **Blockchain**: Solana Web3.js
- **Wallet Adapters**: Solana Wallet Adapter
- **State Management**: React Hooks
- **Styling**: Custom CSS with responsive design

## 📋 Prerequisites

- Node.js (v14 or later)
- npm or yarn
- A Solana wallet (Phantom recommended)
- SOL tokens on Devnet for testing

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/daffhaidar/solana-staking-app.git
   cd solana-staking-app
   ```

2. Install the dependencies:
   ```bash
   # For frontend
   cd frontend
   npm install
   # or with yarn
   yarn install
   ```

3. Start the development server:
   ```bash
   npm start
   # or with yarn
   yarn start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## 📝 Usage Guide

### Connecting Your Wallet

1. Click the "Connect Wallet" button in the top section of the app
2. Select your preferred wallet (Phantom, Solflare, etc.)
3. Approve the connection request in your wallet

### Staking SOL

1. Enter the amount of SOL you want to stake in the input field
2. Click "Stake Now" to initiate the transaction
3. Approve the transaction in your wallet
4. Once confirmed, you'll see a success message with a link to view the transaction on Solana Explorer

### Viewing Transaction History

- Your staking history is displayed in the table below the staking form
- Each entry shows the date, amount, status, and a link to view the transaction details

### Switching Themes

- Click the sun/moon icon in the top-right corner to toggle between light and dark modes

## 🔧 Development

### Project Structure

```
solana-staking-app/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StakingForm.tsx    # Main staking functionality
│   │   │   └── ...
│   │   ├── App.tsx                # Main application component
│   │   ├── App.css                # Global styles
│   │   └── ...
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

### Building for Production

```bash
cd frontend
npm run build
# or with yarn
yarn build
```

The optimized production build will be created in the `build` folder.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

If you have any questions, feel free to reach out:

- Email: [daffahaidar1501@gmail.com](mailto:daffahaidar1501@gmail.com)
- LinkedIn: [Daffa Haidar](https://www.linkedin.com/in/daffhaidar/)
- GitHub: [daffhaidar](https://github.com/daffhaidar/)

---

Made with ❤️ by Daffa Haidar 
