
# Coding task

There are two tasks we would like you to complete. One is a bug fix and the other is adding a feature. We're not expecting you to fully complete the feature. It would be a good idea to spend at most about an hour on the task. If you are not happy with the results or don't have enough time to finish, create a file called COMMENTS.md and let us know what you would do if you had extra time, and what you aren't happy with. We'll discuss the exercise and your comments in a technical interview.


## Bug fix

While working on this microservice, you've received a bug report from one of the other teams. Here's what the report contains:

**Description**: Paying an invoice of $1.47 does not mark the Invoice as Paid.

**Steps to reproduce**

1. Create an invoice with value $1.47.
1. `POST` to `/invoices/<id>/pay`.

**Expected behaviour**: Invoice is paid and status is updated from Pending to Paid

**Actual behaviour**: Amount appears to be deducted correctly but the invoice status is not updated:

        {
          "amount": 1.47,
          "amount_remaining": 0.00,
          "created_at": "Fri, 25 Sep 2020 05:42:39 GMT",
          "description": "Test",
          "id": 1,
          "status": "Pending",
          "updated_at": "Fri, 25 Sep 2020 05:42:39 GMT"
        }

## Feature

In order to enable realtime reporting on revenue we require the invoicing system to notify our reporting systems whenever the current balance of our invoices ledger changes.

Whenever an invoice is paid in full, the invoicing microservice should make a `POST` request to an external endpoint, which should be configurable. The body of the request should include a JSON object containing details of the invoice, including all of the payments. The JSON object should be the same as the existing invoice object, but with a key named `payments`, mapping to an array of payment JSON objects.

        {
            "id": 1,
            "description": "Invoice description",
            "amount": 5.0,
            "amount_remaining": 0.0,
            "created_at": "...",
            "updated_at": "...",
            "status": "Paid",
            "payments": [
                {
                    "id": 12,
                    "amount": 5.0,
                    "payment_date": "...",
                    "invoice_id": 1
                }
            ]
        }

Ideally the external endpoint can be configured by the external reporting team by interacting with the API directly, rather than having to contact us once we have deployed the feature.
