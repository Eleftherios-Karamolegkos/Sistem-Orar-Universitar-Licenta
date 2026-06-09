# Sistem Orar Universitar

Aplicatie desktop pentru gestionarea unui orar universitar, construita cu PyQt6 si SQLite.

## Rulare

```powershell
pip install -r requirements.txt
python main.py
```

Baza de date se creeaza automat la prima pornire in `backend/database/orar.db`.

## Conturi demo

| Rol | Utilizator | Parola |
| --- | --- | --- |
| Admin | `admin` | `admin123` |
| Profesor | `popescu` | `prof123` |
| Profesor | `ionescu` | `prof123` |
| Student anul 1 | `student1` | `student123` |
| Student anul 2 | `student2` | `student123` |
| Student anul 3 | `student3` | `student123` |

## Functionalitati

- autentificare pe roluri: admin, profesor, student;
- dashboard admin cu statistici;
- CRUD pentru profesori, studenti, materii si sali;
- creare, stergere si generare automata de orar;
- detectare conflicte pentru profesor, sala si anul de studiu;
- vizualizare orar filtrat pentru profesor sau student.
