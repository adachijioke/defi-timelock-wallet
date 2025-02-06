# Technical Specification

## Contract Architecture
### Timelocked Wallet Contract
- Owner: Singular contract owner
- State Variables:
  - beneficiary: Optional principal
  - unlock-height: uint
- Key Functions:
  - lock(): Secures assets with time conditions
  - bestow(): Transfers beneficiary rights
  - claim(): Releases assets on conditions met

### Smart Claimant Contract
- Purpose: Distribute claimed assets
- Distribution Logic: Equal shares among 4 beneficiaries
- Error Handling: Comprehensive checks for failed transfers

## Technical Flow
1. Owner locks assets with beneficiary and time conditions
2. System validates unlock height
3. Beneficiary claims post time-lock
4. Smart-claimant executes distribution

## Security Measures
- Time-based validation
- Owner-only operations
- Balance verification
- Failed transfer handling
