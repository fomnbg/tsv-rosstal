from validate_adress import validate_address


def run_tests():
    # Test case 1: Valid address
    result1 = validate_address('Mittenwalder Straße 28', '82431 Kochel')
    print(f'Test 1 - Result: {result1}, Expected: True')
    assert result1 == True

    # Test case 2: Invalid address (non-existent street and city)
    result2 = validate_address('Nonexistent Street 123', 'Nonexistent City')
    print(f'Test 2 - Result: {result2}, Expected: False')
    assert result2 == False

    # Test case 3: Invalid address (invalid city name)
    result3 = validate_address('Musterstraße 42', 'InvalidCityName')
    print(f'Test 3 - Result: {result3}, Expected: False')
    assert result3 == False

    # Test case 4: Invalid address (missing street)
    result4 = validate_address('', 'City Name')
    print(f'Test 4 - Result: {result4}, Expected: False')
    assert result4 == False

    # Test case 5: Invalid address (missing city)
    result5 = validate_address('Street Name', '')
    print(f'Test 5 - Result: {result5}, Expected: False')
    assert result5 == False

    # Test case 6: Invalid address (empty street and city)
    result6 = validate_address('', '')
    print(f'Test 6 - Result: {result6}, Expected: False')
    assert result6 == False

if __name__ == '__main__':
    run_tests()