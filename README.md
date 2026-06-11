# Sistem Orar Universitar

Aplicatie desktop pentru gestionarea unui orar universitar, construita cu PyQt6 si SQLite.

## Rulare

```powershell
pip install -r requirements.txt
python main.py
```

Baza de date se creeaza automat la prima pornire in `backend/database/orar.db`.

## Notificari email

Aplicatia trimite notificari la schimbarea orarului catre `eleftherioskaram@gmail.com`.
Pentru trimitere reala prin email, seteaza datele SMTP inainte de pornire:

```powershell
$env:ORAR_SMTP_HOST="smtp.gmail.com"
$env:ORAR_SMTP_PORT="587"
$env:ORAR_SMTP_USER="adresa_ta@gmail.com"
$env:ORAR_SMTP_PASSWORD="parola_de_aplicatie_gmail"
$env:ORAR_SMTP_FROM="adresa_ta@gmail.com"
python main.py
```

Daca SMTP nu este configurat, aplicatia salveaza notificarea in `backend/notifications.log`.

## Conturi demo

| Rol | Utilizator | Parola |
| --- | --- | --- |
| Admin | `admin` | `admin123` |
| Profesor | `popescu` | `prof123` |
| Profesor | `ionescu` | `prof123` |
| Student anul 1 | `student1` | `student123` |
| Student anul 2 | `student2` | `student123` |
| Student anul 3 | `student3` | `student123` |

Cand adminul adauga un profesor sau un student, aplicatia creeaza automat un cont de login si il afiseaza in Dashboard.

## Functionalitati

- autentificare pe roluri: admin, profesor, student;
- dashboard admin cu statistici;
- creare automata de conturi la adaugare profesor/student;
- CRUD pentru profesori, studenti, materii si sali;
- creare, stergere si generare automata de orar;
- notificare la schimbarea orarului;
- detectare conflicte pentru profesor, sala si anul de studiu;
- vizualizare orar filtrat pentru profesor sau student.
