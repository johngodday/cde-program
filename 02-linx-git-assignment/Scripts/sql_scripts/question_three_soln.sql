
-- #############################################################################
-- ########## Question 3. 
-- #############################################################################
/* 
Find all company names that:
- start with 'C' or 'W'
- AND their primary contact contains 'ana' or 'Ana'
- BUT does not contain 'eana'
*/
-- #############################################################################

SELECT name AS company_name, primary_poc
FROM accounts
WHERE (name LIKE 'C%' OR name LIKE 'W%')
  AND (primary_poc ILIKE '%ana%')
  AND (primary_poc NOT ILIKE '%eana%');

