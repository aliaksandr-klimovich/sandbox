from pprint import pprint
import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()

# shortcuts
es = c.executescript


def fa(s):
    c.execute(s)
    pprint(c.fetchall())


# main
es("""
    create table items(
        item_id integer,
        price real,
        currency text
    );
    
    create table rates(
        currency text,
        date numeric,
        rate real
    );
    
    insert into items values
        (1, 100, 'USD'),
        (2, 10,  'EUR'),
        (3, 20,  'USD'),
        (4, 40,  'USD'),
        (5, 20,  'EUR'),
        (6, 30,  'BYN'),
        (7, 400, 'USD'),
        (8, 50,  'EUR'),
        (9, 60,  'USD');
    
    insert into rates values 
        ('USD', '2015-01-10', 1.9 ),
        ('USD', '2015-01-11', 1.9 ),
        ('USD', '2015-01-12', 2.0 ),
        ('USD', '2015-01-13', 2.0 ),
        ('EUR', '2015-01-12', 2.5 ),
        ('EUR', '2015-01-11', 2.4 ),
        ('RUR', '2015-01-11', 0.03);
""")

fa('select i.item_id, i.price * r.rate as price_in_byn '
   'from items i join '
   '(select currency, rate from rates group by currency having max(date)'
   'union '
   'values ("BYN", 1.0)) as r '
   'on i.currency = r.currency')

fa('select (strftime("%s", "2017-02-21 14:32") - strftime("%s", "2017-02-03 00:00")) / 60 / 60 / 24')
fa('values (case when strftime("%Y", "2017-02-21 14:32") = "2017" then 1 else 0 end)')
