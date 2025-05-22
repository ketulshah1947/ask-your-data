CREATE TABLE orders (
  InvoiceNo VARCHAR,
  StockCode VARCHAR,
  Description TEXT,
  Quantity INT,
  InvoiceDate TIMESTAMP,
  UnitPrice NUMERIC,
  CustomerID VARCHAR,
  Country TEXT
);

COPY orders(InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country)
FROM '/docker-entrypoint-initdb.d/ecommerce_data.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'LATIN1');