# Conectarea la baza de date MariaDB din Docker

Pentru a accesa baza de date MariaDB care rulează într-un container Docker, urmați pașii de mai jos:

## Comandă utilă pentru conexiune

Folosiți următoarea comandă pentru a intra în containerul MariaDB și a vă conecta la baza de date `myapp` cu utilizatorul `admin`:

```bash
docker exec -it backendanalyzer-maria-db-1 mariadb -uadmin -padmin_password myapp
```

### Explicație:
1. **`docker exec -it backendanalyzer-maria-db-1`**: Accesează containerul cu numele specificat.
2. **`mariadb`**: Rulează clientul MariaDB din container.
3. **`-uadmin`**: Se conectează folosind utilizatorul `admin`.
4. **`-padmin_password`**: Specifică parola pentru utilizatorul `admin`.
5. **`myapp`**: Deschide baza de date `myapp`.

---

## Verificarea conexiunii
După rularea comenzii, ar trebui să vedeți promptul MariaDB:

```sql
MariaDB [myapp]>
```

De aici, puteți rula comenzi SQL precum:

- **Vizualizarea tabelelor:**
  ```sql
  SHOW TABLES;
  ```

- **Interogarea unui tabel:**
  ```sql
  SELECT * FROM investigations;
  ```

---

## Rezolvarea problemelor
### Verificarea containerului
Asigurați-vă că containerul este activ:

```bash
docker ps
```

Confirmați că `backendanalyzer-maria-db-1` este listat și în stare „Up”.

### Utilizator sau parolă incorectă
Verificați dacă variabilele de mediu din fișierul `docker-compose.yml` sunt corecte:

```yaml
MARIADB_USER: admin
MARIADB_PASSWORD: admin_password
```

### Conexiune ca root
Dacă utilizatorul `admin` întâmpină probleme, încercați să vă conectați cu utilizatorul `root`:

```bash
docker exec -it backendanalyzer-maria-db-1 mariadb -uroot -ppass1234
