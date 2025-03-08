// Знайти Items які входять в конкретний Order
MATCH (item:Item)-[r:IS_IN]->(order:Order{id: 6})
RETURN item.title, item.price, r.count

// Підрахувати вартість конкретного Order
MATCH (item:Item)-[r:IS_IN]->(o:Order{id: 1})
RETURN o.id, SUM(r.count * item.price)

// Знайти всі Orders конкретного Customer
MATCH (o:Order)-[r:ORDERED_BY]->(c:Customer{name:'Ivan Karpenko'})
RETURN o.id, r.created_at

// Знайти всі Items куплені конкретним Customer (через Order)
MATCH (i:Item)-[r1:IS_IN]->(o:Order)-[r2:ORDERED_BY]->(c:Customer {name: 'Ivan Karpenko'})
RETURN DISTINCT i.title

// Знайти кількість Items куплені конкретним Customer (через Order)
MATCH (i:Item)-[r1:IS_IN]->(o:Order)-[r2:ORDERED_BY]->(c:Customer {name: 'Ivan Karpenko'})
RETURN  i.title,COUNT(i.title) AS no_times_was_ordered, SUM(r1.count) AS no_items

// Знайти для Customer на яку суму він придбав товарів (через Order)
MATCH (i:Item)-[r1:IS_IN]->(o:Order)-[r2:ORDERED_BY]->(c:Customer {name: 'Ivan Karpenko'})
RETURN  SUM(r1.count * i.price)

// Знайті скільки разів кожен товар був придбаний, відсортувати за цим значенням
MATCH (i:Item)-[r1:IS_IN]->(o:Order)
RETURN i.title, COUNT(i) AS no_was_ordered
ORDER BY COUNT(i)

// Знайти всі Items переглянуті (view) конкретним Customer
MATCH (c:Customer{name: 'Maryna Velychko'})-[r:VIEWED]->(i:Item)
RETURN i.title, r.viewed_at

// Знайти інші Items що купувались разом з конкретним Item (тобто всі Items що входять до Order-s разом з даними Item)
MATCH (o1:Order)<-[:IS_IN]-(: Item {title: 'Drawing album 12 pages'})
MATCH (i: Item)-[:IS_IN]->(o2:Order)
WHERE o2 = o1
RETURN i.title, o2.id

// Знайти Customers які купили даний конкретний Item
MATCH (i:Item WHERE i.title CONTAINS 'Gel Pen')-[r1:IS_IN]->(o:Order)-[r2:ORDERED_BY]->(c:Customer)
RETURN c.name, SUM(r1.count)

// Знайти для певного Customer(а) товари, які він переглядав, але не купив
MATCH (c:Customer {name: 'Ivan Karpenko'})-[r:VIEWED]->(i:Item)
WHERE NOT (i)-[:IS_IN]->(:Order)-[:ORDERED_BY]->(c)
RETURN i.title