# Find a football match
![termial output](media/fafm.png)


# Application will prompt user in CLI for input for the following things:
- Their postcode
- Date on which they wish to see a game
- How far they are willing to travel

# upon receipt of the above, application will display the following in the terminal:
- All football teams from the premier league that are playing at home within the users chosen distance, on the given day
- Print Google maps link to see how to get to each match from their postcode
- Print official website for team in order to check ticket availability.

# This repository also utilizes github actions to:
- perform code QL analysis on push or PR to main
- on success of above, package (test and lint in 3 python versions)
- on success of qbove, build and push docker image to dockerHub


![tests passing](media/tests_passed.png)
