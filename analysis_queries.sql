-- Join tables
Select *
from LeetcodeTop150Solutions natural join LeetcodeTop150Problems
;

-- Count # problems for each difficulty
-- Easy: 117
-- Medium: 279
-- Hard: 53
Select difficulty, Count(*) as count_per_difficulty
from LeetcodeTop150Solutions natural join LeetcodeTop150Problems
group by difficulty
;

-- Sanity Check: Count # of unique problems (should be 150)
Select count(distinct ProblemNumber)
from LeetcodeTop150Solutions natural join LeetcodeTop150Problems
;

-- Sanity Ceck: Count # of problems without 3 records in the table (should be 0)
SELECT *
FROM LeetcodeTop150Solutions
NATURAL JOIN LeetcodeTop150Problems
GROUP BY ProblemName
HAVING COUNT(ProblemNumber) <> 3
;

-- Count unique authors: 222
Select count(distinct Author)
from LeetcodeTop150Solutions natural join LeetcodeTop150Problems
;

-- Order authors by frequency of writing top ranked solutions
SELECT Author, COUNT(*) AS AuthorFrequency
from LeetcodeTop150Solutions natural join LeetcodeTop150Problems
GROUP BY Author
ORDER BY AuthorFrequency DESC
;


-- Save adversarial data as a temporary table to export to CSV
CREATE TABLE ModelTable (
    model TEXT
);

INSERT INTO ModelTable (model) VALUES
('BLOOM'),
('CodeLlama'),
('Gemma');


CREATE TABLE TempTable AS
SELECT Solution, Size, Language, ProblemName, model
FROM LeetcodeTop150Solutions
NATURAL JOIN LeetcodeTop150Problems
NATURAL JOIN ModelTable;

SELECT * FROM TempTable;

-- Drop temporary table
DROP TABLE TempTable;

-- Get size of all text (important for tokenization in LLMs): 306207
SELECT SUM(size)
FROM LeetcodeTop150Solutions NATURAL JOIN LeetcodeTop150Problems;