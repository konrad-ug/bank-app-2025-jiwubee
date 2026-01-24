Feature: Database persistence
    
    Scenario: User can save accounts to database
        Given Account registry is empty
        And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
        And I create an account using name: "anna", last name: "nowak", pesel: "85050567890"
        When I save accounts to database
        Then Save operation should succeed
    
    Scenario: User can load accounts from database
        Given Account registry is empty
        And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
        And I save accounts to database
        And Account registry is empty
        When I load accounts from database
        Then Number of accounts in registry equals: "1"
        And Account with pesel "90010112345" exists in registry
    
    Scenario: Loading accounts clears current registry
        Given Account registry is empty
        And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
        And I save accounts to database
        And I create an account using name: "anna", last name: "nowak", pesel: "85050567890"
        When I load accounts from database
        Then Number of accounts in registry equals: "1"
        And Account with pesel "90010112345" exists in registry
        And Account with pesel "85050567890" does not exist in registry