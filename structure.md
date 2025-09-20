We are building a book review app where book covers can be uploaded along side information about books that re going to be reviewed. Reviews can be collected using a form and stored it a database. We will be using SQLite as out database and an ORM to communicate with it.

## Important checks

Set DEBUG to False when running app in production. Set to true to get the static files to be loaded correctly during local development.

## Models we need

**Book Model** - creates table for the book with name, title and publisher

**Contributor model** - creates table for the contributors, e.g authors, co-authors and editor. Fields include first_name, last_name and email

**Publisher model** - creates table for the book publishers. Fields include name, website and email

**BookContributor model** - Creates reference table for the relationship between Book and Contributors Model that includes fields like name of Book, Name of Contributor and their roles.

## Views we need

Book view
review view
