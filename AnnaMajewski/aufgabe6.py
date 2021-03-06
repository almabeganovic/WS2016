## Date: 04.09.2016
## Author: Anna Majewski
## Description: Parser für FASTA-files

#db = [{"id": "", "desc": "", "sequence": "", "raw": ""}]
# leere Datenbank mit den erforderlichen Feldern.

from pprint import pprint

def fasta_parser(filename):
    file_handle = open(filename, "r")
# Öffnet eine Datei in read mode
    position = 0
    for index, line in enumerate(file_handle):
# Index, weil für den ersten Eintrag eine Datenbank erstellt werden muss.
        if line.startswith(">"):
            line = line.strip()
            position = line.index(" ")
            header = line[0:position-1]
            desc = line[position+1:]
# Da erstes " " als Trennung zwischen Header und Beschreibung gilt,
# zuerst bis position von " " = header, alles danach = description.
            if index == 0:
                db = [{"id": header, "desc": desc, "sequence": "", "raw": line}]
# Eine Datenbank wird erstellt.
            else:
                db.append({"id":header, "desc":desc, "raw":line, "sequence":""})
# In die vorhandene Datenbank wird ein neuer Eintrag eingefügt.
        else:
            line = line.strip()
            db[-1]['sequence'] += line
            db[-1]['raw'] += line
    return(db)
# Ich habe die gesamte Datenbank als Rückgabewert gespeichert.

my_db = fasta_parser("sequence.fasta")

## Der Parser ist erstellt, jetzt die zusätzlichen Funktionen.
# F1: get_raw(db,	index))	-	gibt	den	raw	String	des	indizierten	Sequenz-Objekt	zurück

def get_raw(db, index):
# Die Datenbank wird durch die 1. Funktion beschrieben.
# Index ist ein bestimmter Datensatz.
    return db[index]['raw']

print(get_raw(my_db, 9))

# F2: get_id(db,	index))	-	gibt	die	id	des	indizierten	Sequenz-Objekt	zurück

def get_id(db, index):
    return db[index]['id']
# Wie die Funktion von vorhin, nur auf ein anderes Feld wird zugegriffen.

print(get_id(my_db, 9))

# F3: get_description(db,	index))	-	gibt	die	description	des	indizierten	Sequenz-Objekt	zurück

def get_description(db, index):
    return db[index]['desc']
# Wie die Funktionen vorher, nur auf ein anderes Feld wird zugegriffen.

print(get_description(my_db, 9))

# F4: get_sequence(db,	index)	-	gibt	die	sequence	des	indizierten	Sequenz-Objekt	zurück

def get_sequence(db, index):
    return db[index]['sequence']
# Wie die anderen Fkt, Sequenz als Feld.

# F5: get_fasta(db,	index) - Kreiert aus id, desc + seq eine Fasta Seq mit max 80 Zeichen pro Zeile.

def get_fasta(db, index):
    fasta_seq = db[index]['id']+db[index]['desc']+db[index]['sequence']
# fasta_seq ist die gesamte Sequenz, die sich aus den Teilen zusammensetzt.
    new_seq = ""
# Initiation der Variable new_seq, in die die "neue" Sequenz gespeichert wird.
    for index, char in enumerate(fasta_seq):
        if (index+1) % 80 == 0:
# Wenn der Index (+1) durch 80 dividiert 0 ergibt, so haben wir 80 Zeichen in der Zeile.
# Deshalb wird eine neue Zeile eröffnet und dort weitergemacht.
            new_seq += "\n"
            new_seq += char
        else:
            new_seq += char
    return new_seq
# Diese neue Sequenz, die alle 80 Zeichen in einer neuen Zeile beginnt, ist der Rückgabewert.

print(get_fasta(my_db, 9))

# F6: get_feature(db,	index,	feature)	-	Gibt	das	gesuchte	Feature	zurück

def get_feature(db, index, feature):
    return(db[index][feature])

print(get_feature(my_db, 9, "id"))

# F7: add_feature(db,	index,	feature,	value)	-	Fügt	ein	neues	Feature	zu	einem	bestehenden	Daten-Objekt	hinzu.

def add_feature(db, index, feature, value):
    db[index][feature] = value
    return db[index]

print(add_feature(my_db, 9, "organism", "bacteria"))

# F8: add_sequence_object(db,id,description,sequence,**features)-Fügt ein komplett neues Daten-Objekt, ohne	zuvor ein File zu parsen, hinzu.

def add_sequence_object(db, id, description, sequence, **features):
    db.append({"id":id, "desc":description, "sequence":sequence, **features})
    return(db)
# Hier wird an eine bereits bestehende db ein Objekt angefügt.
# Mir ist aber nicht klar, WO ich diese DB definieren soll. Soll das der User selbst machen?

my_other_db = []
# Habe hier eine leere DB definiert.
# Würde ich meine andere db nutzen, dann würde ich ja eine Datei parsen und das sollen wir ja nicht.
print(add_sequence_object(my_other_db, ">gi|123456789|ref|XM_000000.2", "PREDICTED: non existing protein", "AAACGCGCGTAGCCATGCTACGATGCTACGTAGCTACTGATC"))
print(add_sequence_object(my_other_db, ">gi|123456789|ref|XM_000000.2", "PREDICTED: non existing protein", "AAACGCGCGTAGCCATGCTACGATGCTACGTAGCTACTGATC"))

# F9: get_gc_content(db,	index)	-	Berechnet	den	GC-Gehalt	von	Nucleotid	Sequenzen.

def get_gc_content(db, index):
    seq = db[index]["sequence"]
    count = 0
    for ind, char in enumerate(seq):
        if (char == "A") or (char == "T"):
            continue
        else:
            count +=1
    content = count / (ind+1)
    content *= 100
    return content

print(get_gc_content(my_db, 9))

#F10: get_output(db,	index,	type='markdown')	-	Formatiert	den	Output	zum	Beispiel	als	markdown,	html	oder	csv	output	(Advanced)

def get_output(db, index, type):
    if type == "markdown":
# Wenn markdown ausgesucht wurde, dann wird der Text in Markdown dargestellt.
        output = "# H1" + db[index]["id"] + "*" + db[index]["desc"] + "*" + "\n" + "```" + db[index]["sequence"] + "```"
    elif type == "html":
# Wenn html ausgesucht wurde, dann mit HTML.
# Da ich csv nicht kenne, hab ich es mal nicht formatiert, aber das ist auch möglich.
        output = "<h1>" + db[index]["id"] + "</h1><i>" + db[index]["desc"] + "</i>" + "<br><br>" + "<code>" + db[index]["sequence"] + "</code>"
    else:
# Sollte nichts ausgewählt worden sein, so nutze ich die standard Ausgabe.
        output = db[index]["id"] + db[index]["desc"] + db[index]["sequence"]
    return output

print(get_output(my_db, 9, type="html"))
