This project revolved around gathering information about all the content providers in the US. It was completed in 2 parts

 - First, all the information was extracted from json data available on the home page itself
 - Next, each individual title was opened using the url to get more detailed information (more work pending)
 

**Caveat**: Had to pull data in smaller chunks as the limit for json data per provider-genre pair is 1,500 

**Issue**: There is one known issue so far that it does not pull in all the titles for each provider 
*(as of Sep2018, it was pulling in data for ~64k titles as opposed to ~69k mentioned on the website)*
