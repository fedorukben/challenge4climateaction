





-- This is the basic structure of a table in SQL
CREATE TABLE basically_a_dictionary_of_zipped_lists(
    num int,
    words char(20),
    price float,
    PRIMARY KEY (num)
);











-- In python we query with SQL through a library
qry = 'SELECT * FROM table'
result = sqlobj.query(qry)

-- ^ in the above example query is some SQL code we put in 
-- a string and pass through SQL












-- How to think about SQL
'Hey can you get all the temperatures from 1968 to 1990 above 30 
degrees celcius in America?'

-- How is the database structured?
SELECT * FROM global_temps_1900_to_2000

'
ping_id*  sensor_id* date        temperature_celsius  country  city         
1         10344      04-02-1936  39                   AMERICA  Florida        
2         90333      04-02-1978  50                   CANADA   Thunder Bay 
...       ...        ...         ...                  ...      ...

'





-- What tools do we have?
SELECT id, fname, mass FROM group_members
WHERE age > 20
AND fname LIKE 'R%'
OR fname LIKE 'B%'
AND mass BETWEEN 220 AND 300

'''
id* fname   mass
04  Russell massive 
'''








-- Back to the question...
'Hey can you get all the temperatures from 1968 to 1990 above 30 
degrees celcius in America?'
SELECT temperature_celsius, date, country FROM global_temps_1900_to_2000
WHERE date BETWEEN 1968 AND 1990
AND temperature_celsius > 30
AND country = America

'
ping_id*  sensor_id* date        temperature_celsius  country  city         
1         10344      1936        39                   AMERICA  Florida        
2         90333      1978        50                   CANADA   Thunder Bay 
...       ...        ...         ...                  ...      ...

'






-- Another question arises
'Yo, great that you got me all this data but could you sort it by date?'

-- What tools do we have?
SELECT fname FROM group_members
ORDER BY fname DESC/ASC

'
fname
Russell
Kai
Harrison
Ben
'








-- Back to the original question...
'Yo, great that you got me all this data but could you sort it by date?'
SELECT temperature_celsius, date, country FROM global_temps_1900_to_2000
WHERE date BETWEEN 1968 AND 1990
AND temperature_celsius > 30
AND country = America
ORDER BY date

'
ping_id*  sensor_id* date        temperature_celsius  country  city         
1         10344      04-02-1936  39                   AMERICA  Florida        
2         90333      04-02-1978  50                   CANADA   Thunder Bay 
...       ...        ...         ...                  ...      ...

'














-- Now for a hard question 
'      (                      )
      |\    _,--------._    / |
      | `.,'            `. /  |
      `  '              ,-'   '
       \/_         _   (     /
      (,-.`.    ,',-.`. `__,'
       |/#\ ),-','#\`= ,'.` |
       `._/)  -'.\_,'   ) ))|
       /  (_.)\     .   -'//
      (  /\____/\    ) )`'\
       \ |V----V||  ' ,    \
        |`- -- -'   ,'   \  \      _____
 ___    |         .'    \ \  `._,-'     `-
    `.__,`---^---'       \ ` -'
       -.______  \ . /  ______,-
               `.     ,'            ap

------------------------------------------------
https://asciiart.website/index.php?art=creatures/devils
'













'Can you find out which country had the most temperatures above 30 degrees celcius
from 1910 to 1940?'

-- THE TOOLS BABY!
SELECT fname, COUNT(id) as id_count FROM telephone_book
WHERE phone_number LIKE '666-*-*666'
-- This is how you get the max value
ORDER BY id_count
LIMIT 1

'
fname  count
Kevin  654
'
-- ^ NOTE: In the above query count is not a primary key field. This would be
-- completely useless because the answer would be 1.









-- Back to the question...
'Can you find out which country had the most temperatures above 30 degrees celcius
from 1910 to 1940?'
SELECT country, COUNT(country) as temp_count FROM global_temps_1900_to_2000
WHERE temperature_celsius > 30
AND date BETWEEN 1910 AND 1940
ORDER BY temp_count DESC
LIMIT 1

'
ping_id*  sensor_id* date        temperature_celsius  country  city         
1         10344      1936        39                   AMERICA  Florida        
2         90333      1978        50                   CANADA   Thunder Bay 
...       ...        ...         ...                  ...      ...
'










































-- CONGRATULATIONS YOU ARE WINNER!!!