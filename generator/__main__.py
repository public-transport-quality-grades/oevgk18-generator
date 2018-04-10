import records

def main():
    db = records.Database('postgresql://test:test@db:5432/oevgk18')
    rows = db.query('select * from person;')
    for r in rows:
        print(r.id, r.name)

main()