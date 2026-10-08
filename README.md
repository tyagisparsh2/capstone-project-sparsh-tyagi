SQL Setup and Reports

From the MySQL client, load the SQL files in this order:

SOURCE sql/schema.sql;
SOURCE sql/seed_data.sql;
SOURCE sql/reports.sql;

schema.sql creates the database tables. seed_data.sql loads the customer, product, and order data. reports.sql runs the required business reports and calculations.
