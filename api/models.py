from django.db import models

class Encryption(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    public_key = models.CharField(max_length=3220)
    private_key_part = models.CharField(max_length=3220)
    recovery = models.CharField(max_length=3220)
    password = models.CharField(max_length=3220)

    def __str__(self):
        return self.id

## NEKE KORISNE FUNKCIJE, UKRATKO:

# data1 = Encryption(id="first9Iu8NXRMTfWoSDWqz7mnUqkLLLy5mNM9MYcXA7fnuchMxDmUy0qnAI7Cn5h",
#                    public_key="firstObtUVgJgwNDcrMSnWz3721yR9C1W4YTgOTcE8uK4qurW0q34WF6xwofV8kjDqaPPylBXV123serBMRXUeLFrhgJs69y5424m1N2JKAMej5LLwHvhqzs2HgQy3AhwzACAWQN20hbmEIPWPGgPbTumsObhS6teHv3yVTi92lB1W6qt9A3hf7qZYlyiYm4POcyB8KqQEg47QkU1kN00w1fCL310q57jKhrvKT0uhLYZJaE9Sw6GJE4N1N6AUeF",
#                    private_key_part="firstObtUVgJgwNDcrMSnWz3721yR9C1W4YTgOTcE8uK4qurW0q34WF6xwofV8kjDqaPPylBXV123serBMRXUeLFrhgJs69y5424m1N2JKAMej5LLwHvhqzs2HgQy3AhwzACAWQN20hbmEIPWPGgPbTumsObhS6teHv3yVTi92lB1W6qt9A3hf7qZYlyiYm4POcyB8KqQEg47QkU1kN00w1fCL310q57jKhrvKT0uhLYZJaE9Sw6GJE4N1N6AUeF",
#                    recovery="firstObtUVgJgwNDcrMSnWz3721yR9C1W4YTgOTcE8uK4qurW0q34WF6xwofV8kjDqaPPylBXV123serBMRXUeLFrhgJs69y5424m1N2JKAMej5LLwHvhqzs2HgQy3AhwzACAWQN20hbmEIPWPGgPbTumsObhS6teHv3yVTi92lB1W6qt9A3hf7qZYlyiYm4POcyB8KqQEg47QkU1kN00w1fCL310q57jKhrvKT0uhLYZJaE9Sw6GJE4N1N6AUeF",
#                    password="firstObtUVgJgwNDcrMSnWz3721yR9C1W4YTgOTcE8uK4qurW0q34WF6xwofV8kjDqaPPylBXV123serBMRXUeLFrhgJs69y5424m1N2JKAMej5LLwHvhqzs2HgQy3AhwzACAWQN20hbmEIPWPGgPbTumsObhS6teHv3yVTi92lB1W6qt9A3hf7qZYlyiYm4POcyB8KqQEg47QkU1kN00w1fCL310q57jKhrvKT0uhLYZJaE9Sw6GJE4N1N6AUeF")
# Encryption.objects.all()      # vraca celokupan sadrzaj tabele
# Encryption.objects.filter(public_key="kasdpo43DSF9jxczv5$WGdsewrqwqs6secxv")      # vraca sve objekte kod kojih je ispnjen uslov