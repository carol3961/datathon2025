from yumminess_def import cafe_quality_positive, cafe_quality_negative
import re

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()

def calculate_yumminess_score(review):
    """
    Takes in the review and returns a "yumminess" score from -1 to 1.

    Input: 
    ---------------------
    review: string
    ---------------------

    Output: 
    ---------------------
    score: float
    ---------------------
    """

    text = preprocess_text(review)

    if len(text) == 0:
        return 0
    
    good_count = 0
    bad_count = 0
    for word in text:
        if word in cafe_quality_positive: good_count += 1
        if word in cafe_quality_negative: bad_count += 1
    return (good_count-bad_count)/(good_count+bad_count)

tests = {
    "Food was good, but overpriced.  Sandwiches came with stale chips.  Although we didn't try any, the beers may be good, but a glass of the house chardonnay which was sweet and simple was $8.  Likewise, mixed drinks were $9 for a small drink.  Our tab for 2 was $85 with tip and included 2 sandwiches and 2 drinks apiece.  Nice atmosphere, but won't be a place we visit often, if we do indeed return.",
    "Delicious coffee and espresso drinks and a cute little cafe. If you come during the morning rush hour, be prepared to wait a while for your drink. There are a decent number of seats here, but again, if you come in the morning, you might feel a little uncomfortable with the people in line crowding your space. I am a big coffee drinker, so I like that their refills are 75 cents, if I remember correctly. The baristas are also very friendly. My major problem with La Columbe is their lack of wifi. It's the 21st century, guys! It's a good place to hang out for a few hours with a friend or do some non-computer-requiring work, but the lack of wifi is seriously limiting.",
    "Great place for studying and yummy drinks! It definitely can get packed though so you just have to hope you get lucky if you're trying to sit there. Service is pretty fast and prices are about average for a boba shop. I got the sunset tea and it was so refreshing and I couldn't put it down. I also ended up getting the crispy tofu as I got the study munchies and that was such a good decision. I'm writing this review a day later, and I miss the tofu! I will definitely be going back if I get the chance :)"
}
scores = set()
for test in tests:
    print(calculate_yumminess_score(test))
