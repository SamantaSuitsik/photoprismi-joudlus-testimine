Photoprismi jooksutamise käsk:
```docker compose up -d```

Photoprismile pääseb ligi siit:
http://127.0.0.1:2342

Enne testide jooksutamist on soovitatav läbi Photoprismi lisada pilte kausta nimega Review.

Locusti jooksutamise käsud:
1. `cd locust`
2. `locust -f scenarios.py --logfile locust.log`

Et kõik stsenaariumid saaksid joosta on soovituslik teste jooksutada vähemalt 10-ne kasutajaga.

Locusti testid saab käivitada siit:
http://localhost:8089/


