def test_data_loading():
    import pandas as pd
    df = pd.read_csv('data/processed/filtered_complaints.csv', nrows=100)
    assert len(df) > 0
    assert 'Consumer complaint narrative' in df.columns

def test_visualization_imports():
    import matplotlib.pyplot as plt
    import seaborn as sns
    assert True