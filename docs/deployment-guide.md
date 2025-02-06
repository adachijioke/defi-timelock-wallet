# Deployment Guide

## Prerequisites
- Clarinet installed
- Stacks wallet configured
- Test STX tokens for testnet

## Deployment Steps
1. Deploy timelocked-wallet contract
```bash
clarinet contract deploy timelocked-wallet
```

2. Deploy smart-claimant contract
```bash
clarinet contract deploy smart-claimant
```

3. Initialize wallet
```bash
contract-call? .timelocked-wallet lock [beneficiary] [unlock-height] [amount]
```

## Testing
1. Check deployment status
2. Verify lock function
3. Test claim mechanism
4. Validate distribution

## Common Issues
- Insufficient balance
- Incorrect unlock height
- Invalid beneficiary address
