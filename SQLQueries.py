#Drop
dropHM = "DROP TABLE IF EXISTS hm"
dropHMDetail = "DROP TABLE IF EXISTS hmdetail"

#Create
createHM = """
CREATE TABLE IF NOT EXISTS hm
(
    id TEXT,
    link TEXT,
    title TEXT,
    description TEXT,
    crawl BOOL,
    source TEXT,
    PRIMARY KEY (id)
)
"""
createHMDetail = """
CREATE TABLE IF NOT EXISTS hmdetail
(
    id TEXT,
    img TEXT,
    PRIMARY KEY (id, img),
    FOREIGN KEY (id) REFERENCES hm (id)
)
"""
#Insert
insertHM = """
INSERT INTO hm (id, link, title, description, crawl, source)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

insertHMDetail = """
INSERT INTO hmdetail (id, img)
VALUES (%s, %s)
ON CONFLICT (id, img) DO NOTHING;
"""

#Update
updateHM = """
UPDATE hm
SET description = %s, crawl = %s
WHERE id = %s
"""

#Select
selectHM = """
SELECT id, link
FROM hm
WHERE crawl = FALSE
LIMIT %s
"""

#List
nameTables = ["hm", "hmdetail"]
dropTables = [dropHM, dropHMDetail]
createTables = [createHM, createHMDetail]