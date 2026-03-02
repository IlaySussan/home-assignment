import pytest
from formatter import PercentageListFormatter
from dimensions import CountryDimension

def test_formatter_empty_data():
    formatter = PercentageListFormatter()
    dim = CountryDimension()
    result = formatter.format({}, dim)
    assert result == "Country:\nNo data\n"

def test_formatter_zero_total_count():
    formatter = PercentageListFormatter()
    dim = CountryDimension()
    # E.g., keys exist but counts are 0 somehow
    result = formatter.format({"United States": 0}, dim)
    assert result == "Country:\nNo data\n"

def test_formatter_basic_percentages():
    formatter = PercentageListFormatter()
    dim = CountryDimension()
    data = {"United States": 50, "Canada": 30, "Mexico": 20}
    
    result = formatter.format(data, dim)
    expected = (
        "Country:\n"
        "United States 50.00%\n"
        "Canada 30.00%\n"
        "Mexico 20.00%\n"
    )
    assert result == expected

def test_formatter_sorting_and_top_5():
    formatter = PercentageListFormatter()
    dim = CountryDimension()
    data = {
        "A": 10,
        "D": 40,
        "C": 30,
        "B": 20,
        "E": 5,
        "F": 3,
        "G": 2
    }
    # Total = 110
    # D: 40/110 = 36.36%
    # C: 30/110 = 27.27%
    # B: 20/110 = 18.18%
    # A: 10/110 = 9.09%
    # E: 5/110 = 4.55%
    # Rest (F+G) -> 5/110 = 4.55%... wait, no "Other" unless requested?
    # Ah, let's check the formatter logic for top 5 and "Other"
    
    result = formatter.format(data, dim)
    expected = (
        "Country:\n"
        "D 36.36%\n"
        "C 27.27%\n"
        "B 18.18%\n"
        "A 9.09%\n"
        "E 4.55%\n"
        "Other 4.55%\n"
    )
    assert result == expected

def test_formatter_existing_other():
    formatter = PercentageListFormatter()
    dim = CountryDimension()
    # Total = 100
    # Top 5: A(40), B(30), C(10), D(5), E(5) = 90
    # F(2) goes to "Other". Existing "Other"(8) aggregates with F(2) to make Other(10)
    data = {
        "A": 40,
        "B": 30,
        "C": 10,
        "Other": 8,
        "D": 5,
        "E": 5,
        "F": 2
    }
    
    result = formatter.format(data, dim)
    expected = (
        "Country:\n"
        "A 40.00%\n"
        "B 30.00%\n"
        "C 10.00%\n"
        "D 5.00%\n"
        "E 5.00%\n"
        "Other 10.00%\n"
    )
    assert result == expected
