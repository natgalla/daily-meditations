# daily-meditations
A Flask app that provides a daily quote from two of my favorite sources of wisdom: Buddhist monk Thich Nhat Hanh, and the Gospel of Thomas  

scrape.py scrapes the quotes and stores them in a MongoDB  
app.py provides a new quote each day, and includes logic so that the same quote will not repeat within a 30 day period
