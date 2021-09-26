# web-scraping-challenge

This project generates a mars data page by scraping from several different websites and saving that to a Mongo database for display. A flask server which hosts a webpage from which the scrape can be launched and then the data can be seen.

## Prerequisites

To run this project the following tools are needed:

* Web browser
* Python (tested with v3.85, earlier versions may work as well, but have not been tested)
* Flask
* MongoDB
* Jupyter Notebooks and/or Jupyter Labs (to explore the scraping functions)
* Anaconda is recommended though library dependencies can be installed individually as well.

## Usage

* Clone the respository
* Install any dependencies
* Run `flask run`
* Open the root webpage in a web browser
* Click the scrape button
* View the latest mars data

## Known Issues

* The scraping would run faster in headless mode and should be added later

## References

* [Getting the base URL](https://stackoverflow.com/questions/35616434/how-can-i-get-the-base-of-a-url-in-python)
* [Python sleep](https://realpython.com/python-sleep/)