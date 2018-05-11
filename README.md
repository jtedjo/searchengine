# searchengine

STEP 1: Create a user on MySql: user1//password
(line to run on MysSql)
GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';
Run the mysql script associated with the files


STEP 2: Tokenize the File using BeautifulSoup
	Determine where the tokens are inside the HTML file. Do we look at paragraphs,header, etc.?
	Or maybe easier, are we just ignoring things that are inside the <> such as <a?>

STEP 3: Write the content of the dictionary inside to the database (MYSQL)
	This is done by writing tuples in fashion such as: 
		<token><term freq><doc id>

	Delete the old dictionary to clear up RAM

STEP 4: Calculate the IDF of a token after you have all the files tokenized. This is easy with MYSQL
	because you can probably use COUNT function to calculate how many times the terms occur since
	each document should only produce a SINGLE tuple entry for a particular term.

STEP 5: Calculate the TF-IDF within the Token tuples.
