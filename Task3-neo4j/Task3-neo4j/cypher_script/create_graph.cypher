// Customers
CREATE (ivan:Customer {name: 'Ivan Karpenko', email: 'ivan_karpenko@email.com', age: 25})
CREATE (maryna:Customer {name: 'Maryna Velychko', email: 'maryna_velychko@email.com', age: 31})
CREATE (oleksandr:Customer {name: 'Oleksandr Guk', email: 'oleksandr_guk@email.com', age: 22})
CREATE (viktorija:Customer {name: 'Viktorija Byk', email: 'viktorija_byk@email.com', age: 24})

// Items
CREATE (pencils12:Item {id: 4, title: 'Color Pencils Kiten, 12 Colors', price: 7.0, no_like:0})
CREATE (pencils18:Item {title: 'Color Pencils Kiten, 18 Colors', price: 9.0})
CREATE (marker:Item {title: 'Crayola Broad Line Markers, Assorted Classic Colors, Box Of 10, 18 Colors', price: 7.0})
CREATE (album12:Item {title: 'Drawing album 12 pages', price: 10.0})
CREATE (album24:Item {title: 'Drawing album 24 pages', price: 13.50})
CREATE (stiker1:Item {title: 'Suatelier Deco Stickers Unicorns', price: 1.40})
CREATE (stiker2:Item {title: 'Suatelier Deco Stickers Paw Patrol', price: 1.60})
CREATE (stiker3:Item {title: 'Suatelier Deco Stickers Spiderman', price: 1.40})
CREATE (gelpen:Item {title: 'PILOT Juice Limited Edition Gel Pen ', price: 2.0})
CREATE (notebook:Item {title: 'Matte Cover Spiral Notebook - A5 - Dot Line', price: 1.50})
CREATE INDEX FOR (n:Item) ON (n.id);

// Orders
// ORDER 1
CREATE (order1:Order {id: 1})
MERGE (pencils12)-[:IS_IN {count: 1}]->(order1)
MERGE (album24)-[:IS_IN {count: 1}]->(order1)
MERGE (stiker3)-[:IS_IN {count: 1}]->(order1)
MERGE (gelpen)-[:IS_IN {count: 1}]->(order1)
// Customer who ordered the 'order1'
MERGE (order1)-[:ORDERED_BY {created_at:date("2025-01-31")}]->(ivan)
// Customer viewed items
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-01-31")}]->(pencils12)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-01-31")}]->(pencils18)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-01-31")}]->(album24)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-01-31")}]->(stiker3)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-01-31")}]->(notebook)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-01-31")}]->(gelpen)

// ORDER 2
CREATE (order2:Order {id: 2})
MERGE (notebook)-[:IS_IN {count: 2}]->(order2)
MERGE (gelpen)-[:IS_IN {count: 4}]->(order2)

MERGE (order2)-[:ORDERED_BY {created_at:date("2025-02-24")}]->(ivan)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-02-24")}]->(gelpen)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-02-24")}]->(notebook)
MERGE (ivan)-[:VIEWED {viewed_at:date("2025-02-24")}]->(marker)

// ORDER 3
CREATE (order3:Order {id: 3})
MERGE (marker)-[:IS_IN {count: 1}]->(order3)
MERGE (album12)-[:IS_IN {count: 1}]->(order3)

MERGE (order3)-[:ORDERED_BY {created_at:date("2025-02-25")}]->(oleksandr)
MERGE (oleksandr)-[:VIEWED {viewed_at:date("2025-02-25")}]->(album12)
MERGE (oleksandr)-[:VIEWED {viewed_at:date("2025-02-25")}]->(album24)
MERGE (oleksandr)-[:VIEWED {viewed_at:date("2025-02-25")}]->(marker)

// ORDER 4
CREATE (order4:Order {id: 4})
MERGE (stiker1)-[:IS_IN {count: 10}]->(order4)
MERGE (stiker2)-[:IS_IN {count: 10}]->(order4)

MERGE (order4)-[:ORDERED_BY {created_at:date("2025-03-01")}]->(maryna)
MERGE (maryna)-[:VIEWED {viewed_at:date("2025-03-01")}]->(stiker3)
MERGE (maryna)-[:VIEWED {viewed_at:date("2025-03-01")}]->(stiker2)
MERGE (maryna)-[:VIEWED {viewed_at:date("2025-03-01")}]->(stiker1)
MERGE (maryna)-[:VIEWED {viewed_at:date("2025-03-01")}]->(pencils18)

// ORDER 5
CREATE (order5:Order {id: 5})
MERGE (pencils18)-[:IS_IN {count: 1}]->(order5)

MERGE (order5)-[:ORDERED_BY {created_at:date("2025-03-03")}]->(maryna)
MERGE (maryna)-[:VIEWED {viewed_at:date("2025-03-03")}]->(pencils18)

// ORDER 6
CREATE (order6:Order {id: 6})
MERGE (pencils18)-[:IS_IN {count: 10}]->(order6)
MERGE (album12)-[:IS_IN {count: 20}]->(order6)
MERGE (album24)-[:IS_IN {count: 10}]->(order6)
MERGE (notebook)-[:IS_IN {count: 30}]->(order6)
MERGE (pencils12)-[:IS_IN {count: 20}]->(order6)
MERGE (gelpen)-[:IS_IN {count: 100}]->(order6)

MERGE (order6)-[:ORDERED_BY {created_at:date("2025-03-03")}]->(viktorija)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(pencils18)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(album12)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(album24)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(notebook)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(pencils12)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(gelpen)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(stiker1)
MERGE (viktorija)-[:VIEWED {viewed_at:date("2025-03-04")}]->(stiker3)