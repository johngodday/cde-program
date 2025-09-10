
-- #############################################################################
-- ########## Question 4.
-- #############################################################################

/* 
Show the region for each sales rep with their accounts. 
Columns: region name, sales rep name, account name.
Sort alphabetically by account name.
*/
-- #############################################################################


SELECT r.name AS region,
       s.name AS sales_rep,
       a.name AS account
FROM region r
JOIN sales_reps s ON r.id = s.region_id
JOIN accounts a   ON s.id = a.sales_rep_id
ORDER BY account ASC;
