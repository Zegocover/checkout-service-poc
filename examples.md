```
response = requests.post("http://127.0.0.1:8000/checkout-session", json={"invoices": [str(uuid4())], "success_url":"www.google.com", "cancel_url":"www.ebay.co.uk"})
```

```python
import requests
from uuid import uuid4

response= requests.post("http://127.0.0.1:8000/checkout-session", json={"quote_id": str(uuid4()[:-1]+ "5"), "success_url":"www.google.com", "cancel_url":"www.ebay.co.uk"})
```
