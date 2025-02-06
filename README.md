# defi-timelock-wallet

A secure, time-based asset distribution system built for Web3 applications.

## Overview
This smart contract system enables time-locked asset distribution with the following features:
- Secure fund locking mechanism
- Time-based release conditions
- Multiple beneficiary support
- Automatic asset distribution

## Key Features
- **Time-Lock Mechanism**: Assets are locked until a specified block height
- **Beneficiary Management**: Support for multiple beneficiaries with equal share distribution
- **Ownership Controls**: Clear separation between contract owner and beneficiary rights
- **Automated Distribution**: Smart distribution system dividing assets among beneficiaries

## Contract Architecture
The system consists of two main contracts:
1. `timelocked-wallet`: Manages the locking and release conditions
2. `smart-claimant`: Handles the distribution logic for multiple beneficiaries

## Functions
### Timelocked Wallet
- `lock`: Secures assets with time-based conditions
- `bestow`: Transfers beneficiary rights
- `claim`: Releases assets when conditions are met

### Smart Claimant
- `claim`: Executes the distribution logic among beneficiaries

## Security Features
- Owner-only access controls
- Time-lock validation
- Balance checks
- Error handling for invalid operations

## Use Cases
- Treasury management
- Vesting schedules
- Trust fund distribution
- Decentralized inheritance
- Payment scheduling

## Getting Started

### Prerequisites
- Node.js installed
- Git installed
- Clarinet installed for contract deployment
- Basic knowledge of smart contracts


1. Deploy `timelocked-wallet` contract
2. Deploy `smart-claimant` contract
3. Lock assets using owner account
4. Wait for unlock height
5. Execute claim function

## Security Considerations
- All functions include proper access controls
- Time conditions are strictly enforced
- Balance validation before transfers
- Protected against common attack vectors
