;; Test cases for timelocked-wallet and smart-claimant contracts

;; Initialize test addresses
(define-constant wallet-owner 'ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM)
(define-constant beneficiary-1 'ST1J4G6RR643BCG8G8SR6M2D9Z9KXT2NJDRK3FBTK)
(define-constant beneficiary-2 'ST20ATRN26N9P05V2F1RHFRV24X8C8M3W54E427B2)
(define-constant beneficiary-3 'ST21HMSJATHZ888PD0S0SSTWP4J61TCRJYEVQ0STB)
(define-constant beneficiary-4 'ST2QXSK64YQX3CQPC530K79XWQ98XFAM9W3XKEH3N)

;; Test locking functionality
(define-public (test-lock)
    (begin
        ;; Test successful lock
        (try! (as-contract (contract-call? .timelocked-wallet lock beneficiary-1 u1000 u100)))
        
        ;; Test lock with invalid unlock height (in past)
        (asserts! (is-err (as-contract (contract-call? .timelocked-wallet lock beneficiary-1 u1 u100))) true)
        
        ;; Test lock with zero amount
        (asserts! (is-err (as-contract (contract-call? .timelocked-wallet lock beneficiary-1 u1000 u0))) true)
        
        ;; Test lock when already locked
        (asserts! (is-err (as-contract (contract-call? .timelocked-wallet lock beneficiary-2 u1000 u100))) true)
        
        (ok true)
    )
)

;; Test bestow functionality
(define-public (test-bestow)
    (begin
        ;; Test successful bestow
        (try! (as-contract (contract-call? .timelocked-wallet bestow beneficiary-2)))
        
        ;; Test bestow from non-beneficiary
        (asserts! (is-err (contract-call? .timelocked-wallet bestow beneficiary-3)) true)
        
        (ok true)
    )
)

;; Test claim functionality
(define-public (test-claim)
    (begin
        ;; Test claim before unlock height
        (asserts! (is-err (as-contract (contract-call? .timelocked-wallet claim))) true)
        
        ;; Advance block height (in real deployment this happens naturally)
        ;; Test successful claim
        (try! (as-contract (contract-call? .timelocked-wallet claim)))
        
        ;; Test claim distribution through smart-claimant
        (try! (as-contract (contract-call? .smart-claimant claim)))
        
        ;; Verify balances of all beneficiaries
        ;; Note: In actual testing, you would check STX balances here
        
        (ok true)
    )
)

;; Test error conditions
(define-public (test-errors)
    (begin
        ;; Test owner-only functions with non-owner
        (asserts! (is-err (contract-call? .timelocked-wallet lock beneficiary-1 u1000 u100)) true)
        
        ;; Test beneficiary-only functions with non-beneficiary
        (asserts! (is-err (contract-call? .timelocked-wallet bestow beneficiary-2)) true)
        
        (ok true)
    )
)

;; Run all tests
(define-public (run-all-tests)
    (begin
        (try! (test-lock))
        (try! (test-bestow))
        (try! (test-claim))
        (try! (test-errors))
        (ok true)
    )
)
