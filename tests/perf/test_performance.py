"""
Performance tests for Bank API
Adapted to API structure with /api prefix and PESEL-based identification

API endpoints:
- POST /api/accounts (create)
- DELETE /api/accounts/{id} (delete by ID)
- POST /api/accounts/{pesel}/transfer (transfer by PESEL)
- GET /api/accounts/{id} (get account)
"""

import pytest
import requests
import time


# API Configuration
BASE_URL = "http://localhost:5000/api"  # Note: /api prefix!
API_TIMEOUT = 0.5  # Maximum response time in seconds (500ms)


class TestAccountPerformance:
    """Performance tests for account operations"""
    
    def test_create_and_delete_account_100_times(self):
        """
        Test tworzenia i usuwania konta 100 razy.
        Każda operacja (create i delete) musi być szybsza niż 0.5s.
        Sprawdza poprawność response code.
        """
        print("\n" + "="*70)
        print("TEST 1: Create and Delete Account 100 times")
        print("="*70)
        
        create_times = []
        delete_times = []
        failed_requests = []
        created_ids = []  # Track created account IDs
        
        for i in range(1, 101):
            pesel = f"{87110745612 + i}"  # Unique PESEL
            
            # === CREATE ACCOUNT ===
            account_data = {
                "name": f"TestUser{i}",
                "balance": 0,
                "pesel": pesel
            }
            
            try:
                start_time = time.time()
                create_response = requests.post(
                    f"{BASE_URL}/accounts",
                    json=account_data,
                    timeout=API_TIMEOUT
                )
                create_duration = time.time() - start_time
                create_times.append(create_duration)
                
                # Sprawdź response code
                assert create_response.status_code == 201, \
                    f"Iteration {i}: CREATE returned {create_response.status_code}"
                
                # Sprawdź czas odpowiedzi
                assert create_duration < API_TIMEOUT, \
                    f"Iteration {i}: CREATE took {create_duration:.3f}s (max {API_TIMEOUT}s)"
                
                # Get account ID from response
                account_id = create_response.json().get('id')
                created_ids.append(account_id)
                
            except requests.Timeout:
                failed_requests.append(f"Iteration {i}: CREATE timeout")
                pytest.fail(f"CREATE request timeout at iteration {i}")
            except AssertionError as e:
                failed_requests.append(str(e))
                raise
            except Exception as e:
                failed_requests.append(f"Iteration {i}: CREATE error - {str(e)}")
                raise
            
            # === DELETE ACCOUNT ===
            try:
                start_time = time.time()
                delete_response = requests.delete(
                    f"{BASE_URL}/accounts/{account_id}",
                    timeout=API_TIMEOUT
                )
                delete_duration = time.time() - start_time
                delete_times.append(delete_duration)
                
                # Sprawdź response code
                assert delete_response.status_code == 204, \
                    f"Iteration {i}: DELETE returned {delete_response.status_code}"
                
                # Sprawdź czas odpowiedzi
                assert delete_duration < API_TIMEOUT, \
                    f"Iteration {i}: DELETE took {delete_duration:.3f}s (max {API_TIMEOUT}s)"
                
            except requests.Timeout:
                failed_requests.append(f"Iteration {i}: DELETE timeout")
                pytest.fail(f"DELETE request timeout at iteration {i}")
            except AssertionError as e:
                failed_requests.append(str(e))
                raise
            except Exception as e:
                failed_requests.append(f"Iteration {i}: DELETE error - {str(e)}")
                raise
            
            # Progress indicator co 10 iteracji
            if i % 10 == 0:
                avg_create = sum(create_times) / len(create_times)
                avg_delete = sum(delete_times) / len(delete_times)
                print(f"Progress: {i}/100 | "
                      f"CREATE avg: {avg_create:.3f}s | "
                      f"DELETE avg: {avg_delete:.3f}s")
        
        # === PODSUMOWANIE ===
        print("\n" + "-"*70)
        print("STATISTICS")
        print("-"*70)
        print(f"Total iterations: 100")
        print(f"Failed requests: {len(failed_requests)}")
        
        print("\nCREATE operations:")
        print(f"  Average: {sum(create_times)/len(create_times):.3f}s")
        print(f"  Min: {min(create_times):.3f}s")
        print(f"  Max: {max(create_times):.3f}s")
        
        print("\nDELETE operations:")
        print(f"  Average: {sum(delete_times)/len(delete_times):.3f}s")
        print(f"  Min: {min(delete_times):.3f}s")
        print(f"  Max: {max(delete_times):.3f}s")
        print("="*70)
        
        # Sprawdź czy wszystkie requesty się powiodły
        assert len(failed_requests) == 0, \
            f"Some requests failed:\n" + "\n".join(failed_requests)
    
    def test_100_incoming_transfers_performance(self):
        """
        Test 100 przelewów przychodzących.
        Każdy transfer musi być szybszy niż 0.5s.
        Sprawdza końcowe saldo konta i poprawność response codes.
        """
        print("\n" + "="*70)
        print("TEST 2: 100 Incoming Transfers Performance")
        print("="*70)
        
        pesel = "87110745612"
        transfer_amount = 100
        expected_balance = transfer_amount * 100  # 10000
        
        account_data = {
            "name": "PerfTestUser",
            "balance": 0,
            "pesel": pesel
        }
        
        transfer_times = []
        failed_requests = []
        account_id = None
        
        # === CREATE ACCOUNT ===
        try:
            create_response = requests.post(
                f"{BASE_URL}/accounts",
                json=account_data,
                timeout=API_TIMEOUT
            )
            assert create_response.status_code == 201, \
                f"Account creation failed: {create_response.status_code}"
            
            account_id = create_response.json().get('id')
            print(f"✓ Account created: ID={account_id}, PESEL={pesel}")
            
        except Exception as e:
            pytest.fail(f"Failed to create account: {str(e)}")
        
        # === 100 INCOMING TRANSFERS ===
        try:
            for i in range(1, 101):
                transfer_data = {
                    "amount": transfer_amount,
                    "type": "incoming"
                }
                
                try:
                    start_time = time.time()
                    transfer_response = requests.post(
                        f"{BASE_URL}/accounts/{pesel}/transfer",
                        json=transfer_data,
                        timeout=API_TIMEOUT
                    )
                    transfer_duration = time.time() - start_time
                    transfer_times.append(transfer_duration)
                    
                    # Sprawdź response code
                    assert transfer_response.status_code == 200, \
                        f"Transfer {i}: returned {transfer_response.status_code}"
                    
                    # Sprawdź czas odpowiedzi
                    assert transfer_duration < API_TIMEOUT, \
                        f"Transfer {i}: took {transfer_duration:.3f}s (max {API_TIMEOUT}s)"
                    
                except requests.Timeout:
                    failed_requests.append(f"Transfer {i}: timeout")
                    pytest.fail(f"Transfer {i} timeout")
                except AssertionError as e:
                    failed_requests.append(str(e))
                    raise
                except Exception as e:
                    failed_requests.append(f"Transfer {i}: {str(e)}")
                    raise
                
                # Progress co 10 transferów
                if i % 10 == 0:
                    avg_time = sum(transfer_times) / len(transfer_times)
                    print(f"Progress: {i}/100 | Avg time: {avg_time:.3f}s")
            
            # === SPRAWDŹ KOŃCOWE SALDO ===
            balance_response = requests.get(
                f"{BASE_URL}/accounts/{account_id}",
                timeout=API_TIMEOUT
            )
            assert balance_response.status_code == 200, \
                "Failed to get account balance"
            
            account_data_result = balance_response.json()
            actual_balance = account_data_result.get("balance")
            
            print("\n" + "-"*70)
            print("RESULTS")
            print("-"*70)
            print(f"Expected balance: {expected_balance}")
            print(f"Actual balance: {actual_balance}")
            print(f"Balance correct: {actual_balance == expected_balance}")
            
            print("\nTRANSFER STATISTICS:")
            print(f"  Total transfers: 100")
            print(f"  Failed requests: {len(failed_requests)}")
            print(f"  Average time: {sum(transfer_times)/len(transfer_times):.3f}s")
            print(f"  Min time: {min(transfer_times):.3f}s")
            print(f"  Max time: {max(transfer_times):.3f}s")
            print("="*70)
            
            # === CLEANUP ===
            try:
                requests.delete(f"{BASE_URL}/accounts/{account_id}", timeout=API_TIMEOUT)
                print("✓ Cleanup complete")
            except:
                pass
            
            # === ASSERTIONS ===
            assert len(failed_requests) == 0, \
                f"Some transfers failed:\n" + "\n".join(failed_requests)
            assert actual_balance == expected_balance, \
                f"Balance mismatch: expected {expected_balance}, got {actual_balance}"
            
        except Exception as e:
            # Cleanup on error
            if account_id:
                try:
                    requests.delete(f"{BASE_URL}/accounts/{account_id}", timeout=API_TIMEOUT)
                except:
                    pass
            raise

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])