Feature: Money transfers
    
    Scenario: User can perform successful transfer between accounts
        Given Account registry is empty
        And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
        And Account with pesel "90010112345" has balance: "1000"
        And I create an account using name: "anna", last name: "nowak", pesel: "85050567890"
        And Account with pesel "85050567890" has balance: "500"
        When I transfer "200" from account "90010112345" to account "85050567890"
        Then Account with pesel "90010112345" has balance: "800"
        And Account with pesel "85050567890" has balance: "700"

    Scenario: Transfer fails when insufficient funds
        Given Account registry is empty
        And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
        And Account with pesel "90010112345" has balance: "100"
        And I create an account using name: "anna", last name: "nowak", pesel: "85050567890"
        And Account with pesel "85050567890" has balance: "500"
        When I attempt to transfer "200" from account "90010112345" to account "85050567890"
        Then Transfer should fail with error "Insufficient funds"
        And Account with pesel "90010112345" has balance: "100"
        And Account with pesel "85050567890" has balance: "500"

    Scenario: Transfer fails when sender account does not exist
        Given Account registry is empty
        And I create an account using name: "anna", last name: "nowak", pesel: "85050567890"
        When I attempt to transfer "100" from account "99999999999" to account "85050567890"
        Then Transfer should fail with error "Account not found"

    Scenario: Express transfer with fee
        Given Account registry is empty
        And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
        And Account with pesel "90010112345" has balance: "1000"
        When I make express transfer of "200" from account "90010112345"
        Then Account with pesel "90010112345" has balance: "799"