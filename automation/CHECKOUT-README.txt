# Checkout automation (NV4)

CheckoutTest covers these cases:

- TC-CHK-01: full information moves to checkout overview.
- TC-CHK-02.1 to TC-CHK-02.5: required checkout information validation.
- TC-CHK-03: cancelling the information step returns to cart and keeps the item.
- TC-CHK-01 [BUG-03] (@Tag("known-bug")): problem_user cannot enter Last Name; expected to fail.
- TC-CHK-04: one-item overview totals ($29.99 + $2.40 tax = $32.39).
- TC-CHK-05: completing an order and clearing the cart badge.
- TC-CHK-06: cancelling from Overview returns to inventory and preserves one cart item.
- TC-CHK-07: two-item totals ($39.98 + $3.20 tax = $43.18) and order completion.

Run from this directory:

```powershell
mvn test "-Dtest=CheckoutTest" "-Dheadless=false"
```

Test case details are in `checkout-test-cases.csv`. Screenshots are in `../evidence/NV4/`.
