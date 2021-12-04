import random
# function to pick a random quote from a list, as long as its not in stale_quotes
# returns today's quote and the updated list of stale_quotes
def fresh_quote(list, stale_quotes, interval=29):
    todays_quote = ''
    new_quote = False
    while not new_quote:
        quote = random.choice(list)
        if quote not in stale_quotes:
            todays_quote = quote
            # if there are 30 stale quotes, reset stale_quotes with only the new quote
            # otherwise add the quote to the stale quotes list
            if len(stale_quotes) > interval:
                stale_quotes = [quote]
            else:
                stale_quotes.append(quote)
            # breaks the loop when a new quote is found
            new_quote = True
    return todays_quote, stale_quotes
