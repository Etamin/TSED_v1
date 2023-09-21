## Tree Similarity of Editing Distance 
A modified branch from [@Daniel4SE/SQLAST](https://github.com/Daniel4SE/SQLAST)

### Installation

1. Clone the repository to your local machine:
2. Install the required dependencies:

### Usage

```
>>> from TSED import TSED
>>> TSED('SELECT DISTINCT country_name FROM Beneficiary JOIN Transactions ON Transactions.beneficiary_id = Beneficiary.beneficiary_id WHERE client_id=996720','SELECT COUNT(*) FROM singer')
0.038461538461538436
```
