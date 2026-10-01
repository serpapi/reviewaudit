"""Review text for the demo: what customers of each kind of place write, in lines the generator deals out (demo.py).

Short lines stay under eight words so they never count as echoes; the long ones are dealt at most once per place."""

CORPUS = {'cruise': {'short_good': ['Gorgeous sunset, great food, would go again.',
                           'Best night of our trip!',
                           'loved every minute of it',
                           'Beautiful views of the lighthouse.',
                           'Crew was so friendly.',
                           'Perfect anniversary dinner on the water.',
                           'Food was way better than expected.',
                           'Worth every penny honestly.',
                           'great date night idea',
                           'Sunset over the islands was unreal.',
                           'Smooth ride, good lobster.',
                           'Highly recommend the evening sailing.',
                           'Kids loved it, so did we.',
                           'Amazing evening on Casco Bay.',
                           '10/10 would cruise again',
                           'Great music and a fun crew.',
                           'Chowder was excellent!',
                           'So relaxing. Booking again next summer.',
                           'Fantastic way to see Portland.',
                           'Lovely staff and a calm bay.',
                           'Took my parents, they loved it.',
                           'Beautiful boat, very clean.',
                           'Unforgettable night out.',
                           'Fun for a birthday group!',
                           'Saw seals! Dinner was good too.',
                           'Easy boarding, great views',
                           'Really nice evening, good wine list.',
                           'A Portland highlight for us.',
                           'Well run and very scenic.',
                           "Dessert and sunset, can't beat it."],
            'short_bad': ['Overpriced and the food was cold.',
                          "Way too crowded, couldn't see anything.",
                          'Rude crew, never again.',
                          'Rained and no refund offered.',
                          'Food was cafeteria quality.',
                          'Not worth the price at all.',
                          'Left forty minutes late.',
                          'seasick and the bar ran out',
                          'Boring. Mostly just sat there.',
                          'Tables crammed together, very loud.',
                          'Lobster was rubbery, sad.',
                          'Disappointing for an anniversary.'],
            'good': ['We boarded right at 6 from the wharf on Commercial Street and the whole process took maybe ten minutes.',
                     'The lobster bisque was rich and creamy, easily the best thing I ate all week in Maine.',
                     'Watching the sun drop behind the city skyline from the upper deck was worth the ticket alone.',
                     'Our server kept checking on us without hovering, and refilled the water glasses before we even noticed.',
                     'We passed Portland Head Light right as the light turned golden, and everyone ran to the rail for photos.',
                     'The boat itself is spotless, with real tablecloths and comfortable chairs instead of plastic benches.',
                     'My husband had the steak and said it was cooked a perfect medium rare, which surprised him on a boat.',
                     "There's a small dance floor downstairs and the DJ played a nice mix that got even the older couples moving.",
                     'Parking was easy in the garage across the street, and the crew told us exactly where to go.',
                     "We booked for my mom's 70th and they brought out a little cake with a candle without us asking.",
                     'Ride was smooth the whole time, and I get queasy easily, so that meant a lot.',
                     'The captain came on the speaker a few times to point out the forts and islands, which was a nice touch.',
                     'Prices are fair for what you get, a three course dinner plus two hours around the bay.',
                     'Bring a jacket because it gets chilly after dark, but they also had blankets available at the bar.',
                     'The haddock was flaky and well seasoned, and the roasted potatoes on the side were crispy.',
                     'We got a window table and could see Fort Gorges go by while we ate our salads.',
                     'Bartender made a really good blueberry mojito, not too sweet, and the pours were generous.',
                     'Staff handled my gluten allergy carefully and the kitchen made a separate plate for me.',
                     'Our whole office came for a team outing and they managed forty of us without any chaos.',
                     'Saw a couple of harbor seals on the rocks near Cushing Island, my daughter talked about it for days.',
                     'Boarding was organized by table number so nobody had to push or rush for seats.',
                     'The blueberry crisp for dessert was warm with a scoop of vanilla on top, perfect ending.',
                     'It never felt crowded even though the boat was fully booked on a Saturday in July.',
                     'Honestly coming back into the harbor with all the city lights on was my favorite part.',
                     'They give you a good amount of time on the open deck between courses to walk around.',
                     'Crew members were young but very professional and clearly liked their jobs.',
                     'We got engaged up top and the staff helped set it up quietly, she said yes!',
                     'Wine list had a few local options and the server knew which one would go with the scallops.',
                     'Check in was quick, they just scanned the code on my phone and pointed us to the gangway.',
                     'The clam chowder was thick and loaded with clams, not that watery stuff you get at tourist spots.',
                     'Restrooms on board were clean, which sounds minor but on a boat it matters.',
                     'Live acoustic guitar outside for the first hour set a really relaxed mood.',
                     'We went in late September and the light over the water was just gorgeous, fewer crowds too.',
                     'The kids menu had chicken fingers and mac and cheese so our picky eaters were happy.',
                     'My dad uses a cane and the crew helped him on and off without making a fuss.',
                     'Heated indoor dining room was cozy when the wind picked up on the way back.',
                     'We were a little worried about weather but they kept us posted by text the afternoon before.',
                     'Crab cakes came out hot with a tangy remoulade, we almost ordered a second round.',
                     'Got lovely photos of Bug Light and the old forts, bring a real camera if you have one.',
                     'If you only have one evening in town this is a great way to see Casco Bay.',
                     'The pace of dinner was relaxed, nobody rushed us and plates came out at a good rhythm.',
                     'We sat outside for dessert and watched the sky go pink and purple over the islands.',
                     'Celebrated our 25th aboard and they gave us a complimentary glass of bubbly.',
                     'The ticket booth on the wharf sells same day seats too, which made it easy to book last minute.',
                     'Even the vegetarian risotto was creamy and full of flavor, my sister cleaned her plate.'],
            'bad': ['We paid nearly two hundred dollars for two and the food tasted like it came from a banquet hall.',
                    'The boat left almost forty minutes late and nobody explained why we were standing on the dock.',
                    'Our table was in the back corner with no window, so we barely saw the sunset at all.',
                    'The lobster was overcooked and chewy, and the drawn butter was cold by the time it arrived.',
                    'Staff seemed overwhelmed and we waited half an hour between the salad and the main course.',
                    "Music downstairs was so loud we couldn't hear each other across a small table.",
                    'They oversold this trip, there was nowhere to stand up top when we passed the lighthouse.',
                    'It started raining and we got no rain check, no partial refund, nothing.',
                    'Drinks are wildly overpriced, fourteen bucks for a plain vodka soda in a plastic cup.',
                    'Our server forgot our dessert entirely and then acted annoyed when we asked about it.',
                    'Bathrooms were out of paper towels and smelled pretty bad by the second hour.',
                    'The steak was gray and tough, I left most of it on the plate.',
                    'Boarding was a total mess with one line for everyone and no one checking table numbers.',
                    'The captain barely said anything about the islands, so it felt like dinner in a floating room.',
                    'Got really choppy past the lighthouse and nobody warned us, half our group felt sick.',
                    'Online booking charged me twice and it took three phone calls to get the duplicate refunded.',
                    'They seated us beside a loud bachelorette party that was drunk before we left the wharf.',
                    'Portions were tiny for the price, I was hungry again an hour after getting off.',
                    'Chowder was lukewarm and tasted like it came out of a can.',
                    'The vegetarian option was just plain pasta with a bit of oil, really lazy.',
                    'Windows were so smudged that the photos from inside came out blurry and gray.',
                    'It was sold as a sunset trip but the sun had already gone down before we pulled away.',
                    "Parking near the wharf cost us thirty dollars and they don't validate.",
                    'My mom has trouble with stairs and there was no help getting up to the deck.',
                    "Two hours felt like four, there's really not much to do once dinner is over.",
                    'Bar ran out of the house white before dessert, on a Saturday night.',
                    'Crew spent more time chatting with each other than paying attention to guests.',
                    'Our anniversary note in the reservation was totally ignored, not even a card.',
                    'Tables are packed so close that the server kept bumping my chair all night.',
                    'The dessert was a dry slice of cheesecake that tasted like it had been frozen.'],
            'mixed': ["The views were great but the food was just okay, about what you'd expect for a big group dinner.",
                      "Nice enough evening, though I'd skip dinner next time and just do a drinks cruise.",
                      'Service was friendly but slow, and the boat felt a bit dated inside.',
                      'Good for tourists I guess, but locals can get a better meal and a ferry ride for less.',
                      'Sunset was pretty, chowder was fine, steak was forgettable.',
                      "We had fun, but it's pricey for what amounts to a buffet-level meal with a view.",
                      'Weather was cold and windy so we stayed inside most of the time, not their fault really.',
                      'Crew was nice, music was a bit cheesy, overall a decent night out.',
                      "I'd give the scenery five stars and the kitchen maybe two and a half.",
                      'It was fine. Not magical, not bad, just a pleasant boat ride with dinner.'],
            'long_good': ["Booked this for my wife's birthday after seeing it on a list of things to do in Portland, and I'm glad we did. We checked "
                          'in at the wharf around 5:45, got a window table on the lower level, and the server brought out a little card signed by '
                          'the crew. She had the scallops, I had the haddock, both really good. The best part was heading out past the forts and '
                          'seeing Portland Head Light as the sun went down. Only complaint is the cocktails are expensive, like sixteen dollars for '
                          'a margarita. Still a five star night for us.',
                          "my parents were visiting from Ohio and I wanted to do something special that wasn't just another restaurant. this was "
                          'perfect. dad has bad knees and the crew helped him down the ramp without making him feel awkward about it. we split the '
                          "crab cakes, then mom got the lobster and said it was the best she'd had on the trip. the captain pointed out the islands "
                          'and told a story about one of the old forts that had my dad asking questions all the way home. it got cold up top after 8 '
                          'so bring layers. would absolutely do it again',
                          "We came as a group of twelve for my sister's bachelorette and I was nervous it'd be stuffy, but it ended up being the "
                          'perfect mix. Dinner first, then the DJ downstairs started up and we danced most of the way back into the harbor. The '
                          'staff were great sports, one of the bartenders even made us a pink drink special for the bride. Food was solid, the '
                          'chicken was juicy and the blueberry crisp was gone in about a minute. The bathroom line got long later on, but five stars '
                          'overall.',
                          'Honestly went in with low expectations because dinner cruises usually mean mediocre food, but this one was legitimately '
                          'good. The chowder was thick and peppery, my steak was cooked right, and the vegetables actually tasted like vegetables. '
                          'We sat on the starboard side and had the sunset directly in front of us for most of the meal. Service was a little slow '
                          'between the entree and dessert, but we were too busy staring out the window to mind. Parking in the garage on Fore Street '
                          'was easy. Good value for a once a summer kind of splurge.',
                          'This was our 30th anniversary and we wanted something on the water. The note about our anniversary actually got read, '
                          'which almost never happens, and they gave us a table near the bow with a little candle. We had a glass of Prosecco, the '
                          'lobster bisque, and shared the seafood pasta. As we came around near Bug Light the sky went orange and pink and my '
                          'husband got a little teary. The ride was calm, the crew was warm, and nobody hurried us at all. Wish the dessert menu had '
                          "more than two options but that's nitpicking.",
                          'Took my two kids (8 and 11) on the earlier sailing and it was a hit. They had a kids menu with chicken tenders and fries, '
                          'and the server brought them crayons and a little map of Casco Bay to color. My son spotted seals near one of the islands '
                          'and that was basically the highlight of his summer. I had the haddock which was good, simple and fresh. The only downside '
                          'was that the indoor room got a bit warm and stuffy, so we ate dessert outside instead. Recommend for families.',
                          "I proposed on this cruise last Friday!! Called ahead and the guy on the phone helped me plan the timing so we'd be on the "
                          'top deck right as we passed the lighthouse. A crew member hung back and took photos for us, which came out amazing. After '
                          "that it's kind of a blur but I remember the scallops being excellent and the champagne they brought over being a sweet "
                          'surprise. The boat was full but they somehow made the moment feel private. My only gripe is the wait to get off at the '
                          'end, it took a while. She said yes though so who cares',
                          "Came here with coworkers for an end of summer outing and it beat any office party I've been to. Check in was fast, drinks "
                          'were flowing, and the passed appetizers outside were a nice change from sitting at a table all night. Then dinner was '
                          'served downstairs: I went with the risotto and it was creamy and filling. The captain did a little narration about the '
                          "lighthouses which I liked more than I expected. Drinks are pricey, I'll say that, but our company was paying so I didn't "
                          'feel it too much.'],
            'long_bad': ['Booked this for our anniversary and it was a letdown from start to finish. We stood on the wharf for 35 minutes past '
                         'departure with no explanation. Once on board we were put at a table in the middle of the room with no window. The lobster '
                         "was rubbery and the butter was cold. By the time dessert came the sun was gone and we'd missed the lighthouse entirely "
                         'because we were waiting on our check. For almost $200 I expected a lot more.',
                         'Do not do this if the weather looks iffy. It poured the whole time, they kept everyone inside, and the windows fogged up '
                         "so you couldn't see a thing. Fine, weather happens. But when I asked about a credit for another date they said no, tickets "
                         'are final. The food was banquet quality, chicken was dry and the salad was wilted. Staff were polite but clearly just '
                         'trying to get through the night.',
                         "So disappointed. They clearly sell more tickets than the boat can comfortably hold. We couldn't get near the rail "
                         'upstairs, the bar line was 20 minutes long, and the dining room was so loud with a party next to us that we gave up on '
                         "talking. The chowder was lukewarm. My husband's steak came out well done when he asked for medium rare and nobody came "
                         'back to check on us. Felt like a cattle boat with tablecloths.',
                         'We got charged twice for our tickets and spent a week fighting to get the money back. Then the actual cruise was meh at '
                         'best. The captain said almost nothing about the bay, the music was some generic playlist, and the dessert was a frozen '
                         "cheesecake slice. Server was nice enough but obviously had way too many tables. You'd be better off grabbing dinner in the "
                         'Old Port and taking a ferry to one of the islands.',
                         "my mom uses a walker and I called ahead to ask about accessibility, was told it's no problem. it was a problem. the ramp "
                         'was steep, nobody offered to help and the only accessible restroom was out of order. we ended up sitting in one spot all '
                         "night. food was fine nothing special. i'm leaving this so other families know to ask very specific questions before "
                         'booking.']},
 'pizza': {'dishes': ['Margherita',
                      'Marinara',
                      'Diavola',
                      'Garlic knots',
                      'Sausage and broccoli rabe',
                      'Hot honey soppressata',
                      'Quattro formaggi',
                      'Arugula and prosciutto',
                      'Caesar salad',
                      'Cannoli'],
           'short_good': ['Best pizza in Portland, period.',
                          'great pizza, friendly staff',
                          'That crust! Perfect char.',
                          'Margherita was perfect.',
                          'So good we came back twice.',
                          'Real Neapolitan, finally.',
                          'Loved the spicy honey pie.',
                          'quick, hot, delicious',
                          'Fresh mozz makes all the difference.',
                          'Great spot for a casual dinner.',
                          'Wood oven pizza done right.',
                          'My kids devoured everything.',
                          'Garlic knots are addictive.',
                          'Cozy place, awesome pies.',
                          'Seriously good dough.',
                          'Our new Friday night spot.',
                          'Cannoli was a nice surprise!',
                          'Fast takeout, still crispy at home.',
                          'Worth the wait for a table.',
                          'Great beer list too.',
                          'perfect slice of heaven',
                          'Simple ingredients, amazing flavor.',
                          'The sausage pie is unreal.',
                          'Friendly service, fair prices.',
                          'Better than Boston honestly.',
                          "Can't stop thinking about that crust.",
                          'Lovely little neighborhood pizza place.',
                          'Pizza came out in minutes.',
                          'Excellent. Will be back soon.',
                          'Gluten free crust was legit good!'],
           'short_bad': ['Soggy center, burnt edges.',
                         'Waited an hour for takeout.',
                         'Way too salty for me.',
                         'Overpriced for such small pizzas.',
                         'Rude host, cold pizza.',
                         'Crust was raw in the middle.',
                         'Not real Neapolitan, sorry.',
                         'Delivery showed up cold.',
                         'Tiny portions, big prices.',
                         'Toppings were super skimpy.',
                         'Loud, cramped and slow.',
                         'Wrong order twice. Done.'],
           'good': ['The Margherita had that leopard-spotted crust you only get from a really hot wood oven.',
                    'Dough was light and chewy with a little tang, you can tell they let it ferment properly.',
                    'Our server Danielle recommended the hot honey soppressata and she was absolutely right about it.',
                    'The garlic knots come out piping hot and drenched in butter and parsley, get two orders.',
                    'We got a table by the oven and loved watching the guys stretch and launch the pies.',
                    'Pizza came out about eight minutes after we ordered, which is crazy for how good it was.',
                    'The San Marzano sauce is bright and simple, not that sugary stuff from chain places.',
                    'Fresh mozzarella was creamy and melted in pools rather than a solid rubbery sheet.',
                    'Prices are reasonable, two of us ate well with a salad and a pie for under fifty.',
                    'Kids loved watching the oven and the staff gave them little balls of dough to play with.',
                    'The arugula and prosciutto pie had a great peppery bite with shaved parm on top.',
                    'Tommy behind the bar poured us a couple of local IPAs and gave good suggestions.',
                    'They do takeout in vented boxes so the crust was still crisp when we got it home.',
                    "Parking can be tough on the street but there's a lot about a block down.",
                    'The Diavola has a real kick from the chili oil, my husband was sweating and happy.',
                    'Caesar salad was crunchy with real anchovy in the dressing, a great starter to share.',
                    'Small dining room but it feels warm and lively, perfect for a weeknight dinner.',
                    "Cannoli shells were crisp and filled to order so they didn't get soggy.",
                    'Gluten free crust is actually good here, my celiac friend nearly cried.',
                    'Even on a busy Saturday they got us seated within twenty minutes.',
                    'Our waitress Priya was super patient with our big group and split the check five ways no problem.',
                    'The marinara with just garlic and oregano shows how good their tomatoes really are.',
                    'Sausage and broccoli rabe was a perfect balance of bitter greens and fennel-y pork.',
                    'Crust has just the right amount of char without tasting burnt at all.',
                    'They let us go half and half on a pie so we could try two flavors.',
                    'Bathrooms were clean and the whole place smells like woodsmoke and basil.',
                    'Wine by the glass is affordable and the house red goes great with everything.',
                    'We came in right at opening on a Sunday and had the place almost to ourselves.',
                    'Online ordering was easy and the pickup was ready exactly when they said.',
                    'Leftovers reheated in a cast iron pan the next morning were almost as good as fresh.',
                    'The quattro formaggi is rich, a bit funky from the gorgonzola, and totally worth it.',
                    'Staff was welcoming to our dog on the little patio and brought out a water bowl.',
                    'Pies are personal sized, so one each is perfect or share two with an app.',
                    'Sean, the guy at the counter, remembered our order from the last visit which was a nice touch.',
                    'Olive oil drizzle and fresh basil added right out of the oven make it smell incredible.',
                    "It's a great stop before a show at Merrill, quick and not too heavy.",
                    'Vegan cheese option was surprisingly melty and my daughter loved it.',
                    'Music is at a decent volume so you can actually have a conversation.',
                    'Their housemade chili oil on the table is so good I asked to buy a jar.',
                    'The pepperoni cups up and gets crispy around the edges, just how I like it.',
                    'Affogato for dessert was a simple scoop of gelato with a shot of espresso, really nice.',
                    "We celebrated my son's tenth birthday here and they stuck a candle in a Nutella pizza.",
                    'Everything tastes fresh, nothing tastes like it came out of a freezer bag.',
                    "They had a seasonal pie with corn and bacon in August that I'm still thinking about.",
                    'Counter service is fast and friendly even with a line out the door.'],
           'bad': ['The middle of my pizza was a soupy mess and the slices fell apart when I picked them up.',
                   'We waited over an hour for a takeout order they said would be ready in twenty minutes.',
                   'Edges were burnt black, not charred, actually burnt and bitter.',
                   'Way too much salt on everything, I was chugging water all night.',
                   'Seventeen dollars for a pizza the size of a dinner plate feels like a lot.',
                   'The host was dismissive when we asked how long the wait would be.',
                   'Our delivery arrived lukewarm and the box was soggy on the bottom.',
                   'They put three slices of pepperoni on a whole pie, that was it.',
                   'Dough tasted undercooked and gummy, like it was pulled too soon.',
                   'Server never came back after dropping off our food, we had to flag someone down for the check.',
                   "The garlic knots were dry and hard, like they'd been sitting out for a while.",
                   "Tables are jammed so tight I had someone's elbow in my back the whole meal.",
                   'They got our order wrong and then charged us for the extra pie they made.',
                   'Sauce was bland and watery, no basil, no real flavor.',
                   "It's so loud in there you have to shout to be heard.",
                   'Bathroom was filthy and out of soap on a Friday night.',
                   'Got food poisoning after eating here, never coming back.',
                   'Gluten free crust was crumbly and tasted like cardboard.',
                   'The salad was mostly wilted iceberg with a sad drizzle of dressing.',
                   'They refused to do a simple substitution even though I offered to pay for it.',
                   'Cannoli filling was runny and the shell was soft.',
                   "Took forty minutes just to get our drinks, and the place wasn't even full.",
                   'Prices went up a lot since last year but the pizza got smaller.',
                   "Online order said ready at 7 and they hadn't even started it when I walked in.",
                   'The cheese was rubbery and greasy, nothing like real fresh mozzarella.',
                   'Staff were clearly more interested in their phones than the customers.',
                   'Arugula was piled on dry with no oil or lemon, just a heap of leaves on bread.',
                   "My kid's plain cheese pizza came out with a long hair on it.",
                   'Hot honey pie was so sweet it tasted like dessert, not in a good way.',
                   'No reservations and no waitlist, so you just stand by the door awkwardly.'],
           'mixed': ['Pizza was good, not life changing, and the wait was longer than it should have been.',
                     'Crust was great but the toppings were a little sparse for the price.',
                     'Nice atmosphere, decent pies, service a bit scattered.',
                     'Fine for a quick bite, I just think there are better options in town.',
                     'I liked the Margherita but the specialty pie was too salty.',
                     'Takeout was okay, it loses a lot of the magic once it sits in the box.',
                     'Solid three stars from me, good dough but so-so sauce.',
                     'The pizza was tasty but they forgot our garlic knots and the drinks took forever.',
                     "Good food, but cramped and noisy enough that we didn't linger.",
                     'Pretty decent overall, though a little pricey for personal sized pizzas.'],
           'long_good': ['We were in Portland for a long weekend and ended up eating here twice. First night we sat at the counter facing the oven '
                         'and our server Priya talked us through the menu. Got the Margherita and the sausage with broccoli rabe and both had that '
                         'soft, puffy crust with blistered spots. Second night we did takeout to eat by the water and it held up pretty well in the '
                         "box. Only thing I'd change is the counter stools are kind of hard. Still the best pizza we had in Maine.",
                         'Took my parents here after my graduation and it was such a good call. There were six of us and they pushed two tables '
                         'together without any fuss. We ordered four pies to share plus garlic knots and the Caesar. My dad, who claims nothing '
                         "beats New York pizza, admitted the Diavola was 'pretty close.' The cannoli at the end were filled fresh and crunchy. It "
                         'got loud around 7:30 when the place filled up, so if you want a quiet dinner go earlier. Otherwise perfect.',
                         "i've tried just about every pizza place in town and this is the one i keep going back to. the dough has real flavor, like "
                         'a slightly sour bread, and the bottom stays crisp under the sauce. my usual is the hot honey soppressata with a side of '
                         "the chili oil. last time Tommy at the bar gave me a taste of a new local pilsner that went perfectly with it. it's not "
                         'cheap, about $19 a pie, but you get what you pay for. only gripe: parking on a weekend is rough',
                         'My daughter has celiac so we usually avoid pizza places, but a friend told us they take it seriously here and she was '
                         'right. They make the gluten free pies on a separate tray and the server walked us through how they avoid cross contact. '
                         'The crust was crispy and actually tasty. Meanwhile my son and I split the quattro formaggi and a marinara. The only reason '
                         'I hesitated on five stars is the wait, we stood outside for 25 minutes on a cold night. Worth it though.',
                         'Date night win. We got a little two-top by the window, ordered a bottle of the house red and the arugula and prosciutto '
                         'pie plus a Margherita. Both came out within ten minutes, steaming, with fresh basil on top. Our server Danielle was funny '
                         "and attentive without hanging around too much. We finished with the affogato which was a small but perfect ending. It's a "
                         'cozy room with low lighting and you can smell the woodsmoke from down the block. Wish they took reservations, but we got '
                         'lucky on a Tuesday.',
                         'Ordered for pickup on a Friday night expecting chaos, but it was ready right on time and still hot when I got it home ten '
                         "minutes away. The boxes have little vents so the crust didn't go limp. We got the pepperoni, which curls into crispy "
                         'little cups, and a plain cheese for the kids. Everyone was happy, which basically never happens in my house. I knocked my '
                         "mental score down a hair because they forgot the extra side of ranch I paid for, but honestly the pizza doesn't need it.",
                         'Came in alone after a long day at a conference and sat at the bar. Sean behind the counter chatted with me about the oven '
                         '(it runs around 900 degrees apparently) and recommended the seasonal pie, which had corn, bacon and a little jalapeño. '
                         'Sweet, smoky and spicy all at once. I had a glass of white and a side salad and the whole thing came to about thirty five '
                         "bucks. Felt like a local spot, not a tourist trap. Seating at the bar is a bit tight but I'd sit there again.",
                         "We hosted my son's 10th birthday dinner here with eight kids and four adults and lived to tell the tale. The staff were "
                         'incredibly patient, brought out dough balls for the kids to play with while the pies baked, and put a candle in a Nutella '
                         'dessert pizza for the birthday boy. Pizzas came in waves so everyone was eating at the same time. The kids went through '
                         'three Margheritas and a pepperoni in about ten minutes. Bill was reasonable for that many people. Room got loud but that '
                         'was mostly us, sorry to the couple next to us!'],
           'long_bad': ['Was really excited to try this after all the hype but left pretty disappointed. We waited 45 minutes for a table even '
                        "though there were empty seats, the host said they were 'short in the kitchen.' The Margherita came out with a wet, soupy "
                        "center and the cheese slid right off when I picked up a slice. The edges were fine but you can't call it great pizza if the "
                        'middle is raw. Server was nice but clearly slammed. Not worth the wait or the $18.',
                        'Ordered delivery on a Saturday night. Took an hour and twenty minutes and showed up lukewarm with the box soaked through on '
                        'the bottom. The pepperoni pie had maybe five slices of pepperoni on the whole thing. Called to let them know and the person '
                        "on the phone just said 'it's busy tonight' and basically hung up. I get that it's busy, but a simple sorry would have gone "
                        "a long way. Won't be ordering again.",
                        "The pizza itself was okay but the experience was rough. Tables are crammed together, it's deafening inside, and our server "
                        "disappeared for twenty minutes at a time. We asked for chili flakes three times. When the check came they'd charged us for "
                        "a pie we didn't order and it took another fifteen minutes to fix. For a place charging these prices I expect better "
                        'service. There are plenty of other pizza spots in Portland.',
                        'I have a dairy allergy and asked if they could do a pie without cheese. They said no substitutions, period, even though the '
                        'marinara on the menu is literally the same thing. Ended up ordering a salad which was mostly limp lettuce and a few sad '
                        'tomatoes. My friends said their pizzas were too salty and the crust was burnt underneath. Felt unwelcoming overall and we '
                        "didn't stay for dessert.",
                        'Third time here and quality has really slipped. The crust used to be light and airy, this time it was dense and gummy and '
                        'the bottom was burnt in spots. Sauce tasted flat. Prices have gone up at least three dollars per pie since spring, and the '
                        "garlic knots were hard like they'd been reheated. Kind of sad, this used to be my favorite place in the neighborhood."]},
 'deli': {'dishes': ['Pastrami on rye',
                     'Corned beef special',
                     'Matzo ball soup',
                     'Reuben',
                     'Potato knish',
                     'Chopped liver',
                     'Lox and bagel',
                     'Black and white cookie',
                     'Half-sour pickles',
                     'Egg cream'],
          'short_good': ['Best pastrami in town.',
                         'Matzo ball soup cured my cold.',
                         'Worth the line, every time.',
                         'Huge sandwiches, great rye.',
                         'Pickles alone are worth the trip!',
                         'Real deli, finally in Maine.',
                         'Reuben was perfect.',
                         'Feels like New York, love it.',
                         'Line moves faster than it looks.',
                         'so much meat omg',
                         'Great knish, crispy outside.',
                         'My weekly lunch spot.',
                         'Rye bread is fantastic.',
                         'Friendly counter guys, awesome food.',
                         'Half a sandwich fed me twice.',
                         'Corned beef was melt in mouth.',
                         "Egg cream like my grandpa's!",
                         'Bagels and lox on point.',
                         'Never had a bad meal here.',
                         'Quick lunch, huge flavor.',
                         'Classic deli, no nonsense.',
                         'Hands down the best Reuben.',
                         'Pastrami so tender, unbelievable.',
                         'Love the black and white cookies.',
                         'Busy but totally worth it.',
                         'Chopped liver like bubbe made.',
                         'Soup is the real deal.',
                         'Great value for the size.',
                         'Always fresh, always good.',
                         'Pickle bowl is amazing.'],
          'short_bad': ['Cash only? In 2026?',
                        'Forty minute line for lunch.',
                        'Dry pastrami, stale bread.',
                        'Rude at the counter.',
                        'Way overpriced for a sandwich.',
                        'Soup was salty and cold.',
                        'Nowhere to sit, ever.',
                        'Messed up my order again.',
                        'Tiny sandwich for eighteen bucks.',
                        'Card minimum is ridiculous.',
                        'Pickles were soft and old.',
                        'Not worth the hype.'],
          'good': ['The pastrami is hand cut, peppery, and so tender it falls apart when you pick up the sandwich.',
                   'Rye bread has a nice crackly crust and caraway seeds, sturdy enough to hold all that meat.',
                   'Matzo ball soup came with a fluffy ball the size of a fist in a really golden broth.',
                   'The line was out the door at noon but it moved quickly and we had our food in fifteen minutes.',
                   'Every table gets a bowl of half sours and full sours, and they refill without asking.',
                   'One sandwich could easily feed two people, I took half home for dinner.',
                   "The guys behind the counter joke around with regulars and made us feel like we'd been coming for years.",
                   'Reuben was griddled perfectly with melty swiss and just enough Russian dressing.',
                   'Potato knish was crispy on the outside and soft and peppery inside, get it with mustard.',
                   'Got a black and white cookie for the road and it was soft and cakey, not dried out.',
                   'The corned beef was lean but still juicy, which is hard to pull off.',
                   "Chopped liver on rye with raw onion took me straight back to my grandmother's kitchen.",
                   "Prices are high-ish but you're getting nearly a pound of meat, so it evens out.",
                   'Bagel with lox and cream cheese was a great breakfast, the lox was silky and not too salty.',
                   "Egg cream was fizzy and chocolatey, exactly how it's supposed to taste.",
                   'If you go before 11:30 you can usually walk right up and order.',
                   "They take cards now, though there's a small minimum, so the cash only thing is old news.",
                   'Booths are a little worn but it all adds to the old school charm.',
                   'Mustard on every table is the spicy brown kind, which is the only correct choice.',
                   'Ordered a platter for an office meeting and it showed up on time and beautifully arranged.',
                   'My kid got a grilled cheese and they cut it into little triangles without being asked.',
                   'Soup came out scalding hot, which I appreciate on a freezing January day in Portland.',
                   "They let you sample the pastrami if you can't decide what to get.",
                   'Coleslaw is vinegary and crunchy rather than drowning in mayo, I loved it.',
                   'Even with the place packed the room still felt fun and lively rather than chaotic.',
                   "The brisket sandwich with gravy on the side was a sleeper hit, don't skip it.",
                   'Walked down from Munjoy Hill for lunch and it was worth every step back up.',
                   "Staff remembered I'd been in the week before and asked how the soup held up reheated.",
                   'Turkey is roasted in house and tastes like Thanksgiving, not the slimy packaged stuff.',
                   "There's a small ledge by the window where you can eat if all the tables are full.",
                   'Takeout was packed well with the pickles in a separate container so nothing got soggy.',
                   'Latkes were thin and crispy with applesauce and sour cream on the side.',
                   'Cheesecake is dense and creamy, the New York style kind with a graham crust.',
                   'We got the combo with half a sandwich and a cup of soup and it was plenty for lunch.',
                   'Seeing them slice the pastrami right in front of you is half the fun.',
                   'Rugelach by the register are dangerous, I bought a dozen and they were gone by night.',
                   "Owner came by our table to make sure everything was good, which you don't see much anymore.",
                   "It's my go-to after a doctor's appointment, chicken soup and a pickle fixes everything.",
                   'Their hot dogs have a real snap to them and come with kraut and onions.',
                   'Rainy Sunday brunch here with the paper and a pot of coffee is pretty much perfect.',
                   'Bread is delivered fresh every morning and you can taste it.',
                   'I brought my visiting brother from New Jersey and even he approved of the pastrami.',
                   'The tuna melt is underrated, crisp bread and a generous scoop with sharp cheddar.',
                   'The queue stays orderly and someone comes by to take your order while you wait.',
                   'The smell of cured meat and fresh rye hits you the second you open the door.'],
          'bad': ['We stood in line for forty minutes and then they ran out of pastrami right before we got up.',
                  'The pastrami was dry and stringy, like it had been sitting under a heat lamp all day.',
                  'Eighteen dollars for a sandwich is steep when the bread is soggy by the time you sit down.',
                  "Card minimum is twenty dollars, so if you just want soup you're stuck finding an ATM.",
                  'Guy at the register rolled his eyes when I asked what came on the Reuben.',
                  'There were zero open tables and nobody was clearing the dirty ones.',
                  'Matzo ball was dense and heavy like a hockey puck, broth was way too salty.',
                  'They forgot the coleslaw on my order and the extra pickles I paid for.',
                  'Pickles tasted old and were soft instead of crunchy.',
                  'Floor was sticky and the trash by the door was overflowing at lunch.',
                  'Waited twenty five minutes for a to-go order I called in ahead of time.',
                  'Rye bread was stale and crumbled apart before I finished half of it.',
                  'The corned beef was fatty and gristly, I ended up pulling most of it out.',
                  'Prices keep going up but the sandwiches seem to keep getting smaller.',
                  'Staff was yelling at each other in the back the entire time we were eating.',
                  'My soup came lukewarm and when I sent it back it returned barely warmer.',
                  "There's no real system for the line, people just cut in from the side door.",
                  'The knish was microwaved, soggy and gray in the middle.',
                  'Bathroom was out of order and they said to use the coffee shop down the street.',
                  'Lox was overly salty and the bagel was clearly from yesterday.',
                  'Not a single vegetarian option worth mentioning besides an egg salad.',
                  "They wouldn't split a sandwich between two plates without charging an extra five dollars.",
                  "Seating is cramped and you end up practically eating in a stranger's lap.",
                  'Delivery took over an hour and the soup had spilled all over the bag.',
                  'Asked for lean pastrami and got a pile of fat.',
                  'Black and white cookie was hard as a rock, must have been days old.',
                  'Felt rushed to leave the minute we finished, they kept hovering to take our table.',
                  'Reuben was swimming in dressing and the bread was completely soaked.',
                  'Way too loud to talk, between the clatter and the shouting of order numbers.',
                  'The hype is mostly nostalgia, the food is just okay for these prices.'],
          'mixed': ["Pastrami was good but I'm not sure it's worth a thirty minute line on a weekday.",
                    'Soup was great, sandwich was fine, service a bit gruff.',
                    "Decent deli for Maine, though it's not quite what I grew up with in Brooklyn.",
                    "Food's solid, the cash and card minimum thing is still annoying.",
                    'Big portions, a little pricey, kind of chaotic inside.',
                    'The corned beef was nice, the rye was a bit dry that day.',
                    "Good for takeout, I wouldn't bother trying to sit down at lunchtime.",
                    'Pretty good overall but the pickles were softer than I like.',
                    "Worth trying once, not sure it'll become a regular stop for me.",
                    'Friendly enough staff, an average knish, and a really great cookie.'],
          'long_good': ['I grew up going to delis in Queens with my grandfather and have been searching for something close since moving to Maine. '
                        'This is it. The pastrami on rye is thick, hand sliced, peppery at the edges, and the bread holds up. The pickles on the '
                        'table were crunchy and garlicky. I also got a cup of matzo ball soup and it tasted like it had simmered all morning. The '
                        "line was long at 12:15, about 20 minutes, and it's loud inside. But I walked out happy and with leftovers for dinner.",
                        "Came down with a nasty cold last week and my wife picked up two quarts of the chicken matzo ball soup from here. I'm not "
                        'exaggerating when I say it helped more than the cough medicine. The broth is rich, a bit of dill, lots of carrots, and the '
                        'balls are light and fluffy. When I felt better I went in myself and had the Reuben, which was also great. Only knock is '
                        "it's tough to find street parking nearby around lunch.",
                        "We ordered a catering platter for my father's shiva and the staff were incredibly kind on the phone. They helped us figure "
                        'out how much to get for about forty people, threw in extra rye and pickles, and delivered right on time. The corned beef, '
                        'turkey and pastrami were all excellent, and the rugelach tray disappeared first. It was one less thing to worry about on a '
                        "hard week and I'm really grateful. A little expensive but worth every dollar.",
                        'Quick lunch with coworkers and we got lucky with a booth. I had the brisket sandwich with gravy on the side, my coworker '
                        'went for the tuna melt and our boss got the Reuben. Everyone was quiet for about ten minutes which says it all. Service was '
                        'fast and the counter guys were cracking jokes with us. The only downside is they had a card minimum, so we had to combine '
                        'our orders on one card. Still five stars, will be back next week.',
                        'first time here, came with my girlfriend on a saturday morning. got the bagel with lox and a potato knish to share, plus an '
                        "egg cream because I'd never had one. the lox was silky and the knish was crispy and peppery, really good with the mustard. "
                        "egg cream was weird at first but I ended up finishing it lol. we waited maybe 10 min, not bad. seating is tight and you'll "
                        "probably bump elbows with somebody. great breakfast though, we're coming back for the pastrami",
                        "My brother visited from New Jersey and spent the whole drive from the airport telling me Maine couldn't do a real deli. I "
                        'brought him here to shut him up. He got the corned beef special with coleslaw and Russian, I got the pastrami. He finished '
                        'his in silence and then asked if they ship. The black and white cookies we grabbed at the register were soft and fresh. '
                        "Docking it nothing really, though the line at 1 pm was longer than I'd like.",
                        'Been coming here every Friday for about two years. The staff knows my order (half pastrami, cup of soup, extra full sours) '
                        'and usually start it before I hit the register. Quality has been consistent the whole time, which is rare. Prices went up a '
                        "little this year like everywhere else but the portions haven't shrunk. My only wish is a couple more tables, on cold days "
                        'everyone wants to eat inside and you can end up standing around holding a tray.',
                        'Stopped in after walking the Eastern Prom with my kids. My son is a picky eater and they made him a simple grilled cheese '
                        'on challah, no complaints. My daughter and I split the latkes and a turkey sandwich, and the turkey actually tasted '
                        'roasted, not processed. The applesauce for the latkes seemed homemade. We were in and out in about thirty minutes on a '
                        "Sunday. Bathroom was a bit small for wrangling two kids but that's my only complaint."],
          'long_bad': ['Waited 40 minutes in line on a Saturday only to be told at the counter they were out of pastrami. Fine, I got corned beef '
                       "instead, but it was fatty and the rye was so soggy from the dressing that it fell apart. Then they told me there's a $20 "
                       "minimum for cards, so I had to add a cookie I didn't want. The guy at the register was short with me the whole time. Not "
                       'sure what the hype is about.',
                       'Ordered takeout for my family and it was a disaster. Half the order was missing, no soup, no pickles, and they gave us a '
                       'tuna melt nobody asked for. Called and they said to come back and pick it up, which is a fifteen minute drive each way. The '
                       'sandwiches we did get were fine but for over $80 I expected them to at least get the order right.',
                       "The matzo ball soup was so salty I couldn't finish it and the ball was dense like it had been reheated a few times. Pastrami "
                       'was dry. The table we finally got was still sticky from the previous people and nobody came to wipe it. Staff were shouting '
                       "at each other the entire time. I really wanted to like this place but it felt like they've gotten lazy because they know "
                       "there'll always be a line.",
                       "Bring cash or be ready for a fight. The card machine was 'down' when I went, which apparently happens a lot according to the "
                       "guy behind me in line. There's no ATM inside. I had to walk two blocks to find one and then got back to the end of the line. "
                       'The Reuben, when I finally got it, was swimming in dressing and the bread had gone to mush. Never again.',
                       "Tried this place for the first time last week and won't be back. $19 for a sandwich that was mostly bread with a thin layer "
                       'of meat, nothing like the giant ones in the photos. Knish was soggy, clearly microwaved. I asked if it could be heated a bit '
                       "more and got a shrug. It's crowded, loud, and there's nowhere to sit. Plenty of better lunch options in the Old Port."]},
 'dental': {'short_good': ["Best dentist I've ever had.",
                           'Painless cleaning, super friendly staff.',
                           'Always on time, very professional.',
                           'They made my anxious kid comfortable.',
                           'Great hygienist, gentle and thorough.',
                           'Clean office, kind people.',
                           "Finally a dentist I don't dread.",
                           'Quick appointment, no upsell.',
                           "Filling didn't hurt one bit!",
                           'Front desk is so helpful.',
                           'Highly recommend for nervous patients.',
                           'Love this practice.',
                           'Fast, friendly and fair.',
                           'Insurance stuff handled easily.',
                           'Got me in same day!',
                           'My whole family goes here.',
                           'Crown fits perfectly, thanks!',
                           'Gentle hands, great results.',
                           'Explained everything clearly.',
                           'They actually listen to you.',
                           'Easy online booking, great care.',
                           'Teeth never felt cleaner.',
                           'Wonderful experience as always.',
                           'Nice waiting room, short wait.',
                           'No judgment, just good care.',
                           'Emergency visit handled quickly.',
                           'Very calm and reassuring dentist.',
                           'Five stars, every visit.',
                           'Kind, honest, and on schedule.',
                           'So glad I switched here.'],
            'short_bad': ['Waited an hour past my appointment.',
                          'Billing nightmare, avoid.',
                          'Rough hygienist, gums bled for days.',
                          'Pushy about unnecessary treatments.',
                          'Rude front desk staff.',
                          'Canceled on me twice.',
                          'Charged me a no-show fee unfairly.',
                          'Filling fell out in a month.',
                          'Too expensive without insurance.',
                          'Felt rushed and ignored.',
                          'Never called me back.',
                          'Painful and unpleasant visit.'],
            'good': ['The hygienist was gentle but thorough and explained what she was doing at each step.',
                     "I've had dental anxiety since childhood and the dentist let me take breaks whenever I raised my hand.",
                     'The front desk sorted out my insurance before the visit so there were no surprises on the bill.',
                     'They got me in the same afternoon when I cracked a molar on a popcorn kernel.',
                     'Waiting room is calm and bright, and I was called back within five minutes of my appointment time.',
                     'The dentist showed me the X-rays on a screen and walked me through what was actually wrong.',
                     'My filling was done in about thirty minutes and I barely felt the numbing shot.',
                     'They never push extra treatments, the dentist even told me one cavity could wait and be watched.',
                     'Online booking is easy and they send a text reminder two days before.',
                     'My six year old was nervous and they let her sit in the chair and play with the light first.',
                     'They have TVs on the ceiling so you can watch something during longer procedures.',
                     'Crown was done in one visit with the in-office milling machine, which saved me a second trip.',
                     'Parking lot right next to the building is free, which is a big deal in Portland.',
                     'Prices were clearly listed and they gave me a written estimate before starting anything.',
                     'The office is spotless and they wiped down everything in the room before I sat down.',
                     'The hygienist gave me practical flossing tips instead of a lecture, which I appreciated.',
                     'When I had pain after a root canal the dentist called me personally that evening to check in.',
                     'They offered nitrous for my extraction and it made the whole thing much easier.',
                     'Whitening results were noticeable after one session and the sensitivity faded in a day.',
                     'Reception remembered me from six months ago and asked about my new job.',
                     'They work with my insurance and helped me appeal a claim the company had denied.',
                     'Warm blankets and noise canceling headphones are offered, which sounds silly but really helps.',
                     'My kids actually look forward to their checkups now because of the prize box.',
                     'The new digital scanner meant no more gagging on that awful putty for impressions.',
                     "Appointments run on time, I've never waited more than ten minutes in three years.",
                     'They had early morning slots so I could come before work without taking time off.',
                     "The dentist was honest that my old fillings were fine and didn't need replacing.",
                     'Billing questions were answered by email the same day with a clear breakdown.',
                     "They referred me to a great oral surgeon and coordinated the records so I didn't have to.",
                     'Numbing was done slowly with a topical gel first, so I felt basically nothing.',
                     'I walked in with a swollen jaw on a Saturday and they still found a way to see me.',
                     'Staff speaks a bit of Spanish and helped my mother feel comfortable during her visit.',
                     'Cleaning took about forty five minutes and my teeth felt smooth for weeks.',
                     'Treatment plan came with options at different price points instead of just the most expensive one.',
                     'The building is accessible and they helped my grandfather into the chair carefully.',
                     'Night guard they made fits well and my jaw pain in the morning is basically gone.',
                     'They have a payment plan for people without insurance, which made my implant possible.',
                     'Every person in the office, from reception to assistants, was kind and patient.',
                     'The dentist has a calm voice and explains things without making you feel dumb.',
                     "Reminders by text and email mean I haven't missed a cleaning in two years.",
                     'Moved here from Boston and this is honestly better care than I got there.',
                     'They gave my teenager a straight answer about wisdom teeth instead of scaring him.',
                     'Sealants for both kids were quick and they made a game of it.',
                     'Office is a short walk from the Old Port so I can grab lunch after my appointment.',
                     'Assistant held my hand during the injection when she saw how tense I was.'],
            'bad': ['I sat in the waiting room for over fifty minutes past my appointment with no explanation.',
                    'They billed my insurance wrong and then sent me to collections without a single phone call.',
                    'The hygienist scraped so hard that my gums bled for two days afterward.',
                    "Every visit there's a new treatment they want to sell me, it feels like a sales pitch.",
                    'The front desk was curt and acted like my questions were an inconvenience.',
                    'They canceled my appointment the night before, twice in a row.',
                    'I was charged a fifty dollar no-show fee even though I called to reschedule a day ahead.',
                    'My filling cracked within a month and they wanted to charge me again to redo it.',
                    'Without insurance a simple cleaning and X-rays came to almost four hundred dollars.',
                    "The dentist was in and out in two minutes and didn't answer any of my questions.",
                    'I left three voicemails about pain after my extraction and nobody called back.',
                    "Numbing wore off halfway through and they didn't stop to give me more.",
                    'They told me I needed four fillings and a second opinion found zero cavities.',
                    'Office felt cramped and the chair was so worn the padding was coming through.',
                    'Billing statements are confusing and change every time I call to ask about them.',
                    'They stopped taking my insurance and never told me until I was standing at the desk.',
                    'My kid came out crying and the assistant just told her to stop being dramatic.',
                    'The temporary crown fell off twice before the permanent one was ready.',
                    "Booking online showed availability that didn't actually exist when I called to confirm.",
                    'They wanted a hundred dollar deposit just to schedule a new patient exam.',
                    'I felt rushed through the whole cleaning, like they were behind and trying to catch up.',
                    'Hygienist lectured me about flossing the entire time in a pretty condescending way.',
                    'Parking is a pain and the lot is tiny, I was late because I circled for twenty minutes.',
                    'The office smelled strongly of chemicals and the waiting room was overcrowded.',
                    'They lost my X-rays and made me pay to have them taken again.',
                    'The assistant kept poking at a sensitive spot even after I said it hurt.',
                    'Root canal was botched and I needed a specialist to fix it months later.',
                    'No evening or weekend hours so I have to take time off work for every visit.',
                    'Their reminder texts came at 6am which is ridiculous.',
                    'Refund for an overpayment took four months and multiple emails.'],
            'mixed': ['Cleaning was fine but the wait to get an appointment was almost two months.',
                      'Dentist was nice, billing department not so much.',
                      'Decent care overall, though they seem to recommend a lot of extras.',
                      'Good hygienist, but the people at reception could be a lot friendlier.',
                      'The work was solid, the price was a bit higher than my last dentist.',
                      'Nothing wrong exactly, just felt a little impersonal and quick.',
                      'Clean office and modern equipment, but I waited twenty minutes past my time.',
                      "Fine for routine cleanings, not sure I'd trust them with anything major.",
                      'They fixed my tooth but the follow up communication was lacking.',
                      'An average experience overall, not bad but nothing memorable either.'],
            'long_good': ["I hadn't been to a dentist in almost seven years because of anxiety and was honestly embarrassed walking in. Nobody made "
                          'me feel judged. The hygienist explained the deep cleaning plan over two visits, and the dentist went over my X-rays on a '
                          'monitor so I could see exactly what needed fixing. I got two fillings and barely felt them. They let me listen to my own '
                          "music with headphones the whole time. The only reason it isn't perfect is the parking lot fills up fast in the morning. "
                          'Grateful I finally came here.',
                          'Cracked a tooth on a Friday afternoon biting into a bagel and called in a panic. The receptionist found me a slot an hour '
                          'later. The dentist examined it, showed me the crack on a camera, and said it could be saved with a crown. They made the '
                          "crown same day with their machine, which I didn't even know was possible. I was in the chair about two and a half hours "
                          'total, but I walked out with a fixed tooth instead of a temporary. Pricey, but insurance covered more than I expected '
                          'thanks to the front desk.',
                          'Our whole family switched here last year, two adults and three kids. Scheduling everyone back to back on one morning used '
                          'to be impossible at our old office but they set it up without blinking. The kids love the hygienist with the dinosaur '
                          'scrubs and the prize box at the end. My middle son needed sealants and they talked him through it like it was a science '
                          'experiment. Billing is clear and they email statements. Small gripe: the waiting room can get crowded when all five of us '
                          'show up at once, ha.',
                          "I'm 74 and have had my share of dentists. This office is the most patient and respectful I've found. The building is easy "
                          'to get into with my walker and the assistant helped me into the chair without rushing me. The dentist explained why my '
                          'bridge was loose and gave me a couple of options, including a cheaper one, rather than just pushing the implant. The new '
                          "bridge fits well. My only wish is that they had some later afternoon appointments, since I don't love driving in morning "
                          'traffic.',
                          'Had my wisdom teeth out here (two of them, the other two were referred to a surgeon). They offered nitrous and walked me '
                          'through what to expect beforehand. The procedure itself was quick, maybe 40 minutes. That evening the dentist actually '
                          "called my cell to see how I was doing, which I've never had happen. Swelling was gone in about four days. The aftercare "
                          'sheet was clear and useful. Knocked a little off in my head for the half hour wait before I was seen, but the care itself '
                          'was excellent.',
                          'Moved to Portland from Chicago and needed a new dentist fast because of a lingering toothache. Booked online, got a text '
                          'confirmation right away, and was seen two days later. Turned out to be a small cavity next to an old filling. The dentist '
                          'was upfront that the rest of my old work looked fine, which I appreciated after years of being upsold elsewhere. Cleaning '
                          'was gentle and the hygienist was friendly and chatty in a good way. The office is bright and modern. Glad I found them on '
                          'the first try.',
                          'I have a real fear of needles and they handled it so well. The assistant used a numbing gel first, waited a few minutes, '
                          "then the dentist did the injection slowly while talking to me about the weekend. I honestly didn't feel the needle. They "
                          'also gave me a stress ball which sounds silly but helped. Root canal was done in one visit and the follow-up crown fit '
                          "great. The bill was higher than I'd hoped even with insurance, but they set up a payment plan without any hassle.",
                          'Took my 4 year old for her very first dental visit and was dreading a meltdown. The hygienist let her ride the chair up '
                          "and down, count her own teeth in a mirror, and pick a flavor for the polish. She didn't cry once. The dentist talked to "
                          'her directly, not just to me, and gave me a couple of practical tips about bedtime brushing. We were done in 25 minutes. '
                          "Now she tells everyone she has a 'tooth doctor.' My one note is the paperwork for new patients is long, so do it online "
                          'before you come.'],
            'long_bad': ["Showed up ten minutes early for a 9am cleaning and wasn't called back until almost 10. No one at the desk apologized or "
                         'explained. The cleaning itself felt rushed and the hygienist was rough, my gums were sore for days. Then the dentist came '
                         'in for maybe two minutes, said I needed a deep cleaning and three fillings, and left. A second office I went to found one '
                         "small cavity. I won't be going back.",
                         'Billing here is a mess. They submitted my claim with the wrong code, insurance denied it, and instead of fixing it they '
                         'sent me a bill for the full amount. I called four times over two months. Each time I was told someone would call me back '
                         "and nobody did. Eventually it went to collections. The actual dental work was fine but I can't recommend a practice that "
                         'treats patients like this.',
                         'My son is 7 and nervous at the dentist. The assistant was impatient with him from the start and when he started crying she '
                         "told him he was being a baby. The dentist didn't step in. We left without finishing the cleaning. I understand kids can be "
                         'difficult but this is a family practice and they should be better at this. Found a pediatric dentist elsewhere who was '
                         'wonderful with him.',
                         'Got a crown here last spring. The temporary came off twice and I had to come in each time, missing work. The permanent '
                         'crown never felt right and after three months it started hurting. They said it was fine and suggested a root canal, which '
                         "another dentist told me wasn't needed, the crown just didn't fit. Spent a lot of money and time for nothing and I'm still "
                         'dealing with it.',
                         'Was charged a $75 cancellation fee even though I called and left a message two days before my appointment. They said they '
                         'never got the message. When I asked to speak to the office manager I was told she was unavailable and to email. Emailed '
                         'twice, no response. Small thing maybe, but it tells you how they treat patients. Taking my family elsewhere.']},
 'towing': {'short_good': ['Fast, friendly, fair price.',
                           'Saved me at 2am, thank you!',
                           'Showed up in twenty minutes.',
                           'Honest driver, careful with my car.',
                           'Always fast and fair.',
                           'Best tow company in Portland.',
                           'Jump start in no time.',
                           'Super professional, would call again.',
                           'Got me out of a ditch!',
                           'Reasonable rates, great service.',
                           'Driver was so kind.',
                           'Quick lockout help, very polite.',
                           'Answered on the first ring.',
                           'No damage, no hassle.',
                           'Lifesavers in a snowstorm.',
                           'Arrived earlier than quoted.',
                           'Very good communication throughout.',
                           'Fair and fast, highly recommend.',
                           'Towed my truck, zero issues.',
                           "They really know what they're doing.",
                           'Changed my flat in minutes.',
                           'Great service on a holiday.',
                           'Polite, quick, reasonably priced.',
                           'Came out to the ferry lot fast.',
                           "Trustworthy, I'd use them again.",
                           'Got my motorcycle home safely.',
                           'Excellent roadside help.',
                           'Easy to work with.',
                           'Calm driver on a stressful night.',
                           'Thank you for the rescue!'],
            'short_bad': ['Waited three hours, never came.',
                          'Scratched my bumper, denied it.',
                          'Price doubled when they arrived.',
                          'Rude dispatcher, hung up on me.',
                          'Predatory towing, avoid.',
                          'Hidden fees everywhere.',
                          'Took my car from a legal spot.',
                          'Impound lot hours are ridiculous.',
                          'Cash only, no receipt.',
                          'Driver was on his phone.',
                          'Overcharged for a short tow.',
                          'Never answered the phone.'],
            'good': ['My car died on the Casco Bay Bridge during rush hour and the truck was there in about twenty five minutes.',
                     "Dispatcher gave me a clear price over the phone and that's exactly what I paid.",
                     'The driver put on his flashers, set out cones, and made sure I was safely off the road first.',
                     'Called at 3am after a flat on 295 and someone actually answered right away.',
                     'He was really careful loading my low car onto the flatbed, no scrapes at all.',
                     'They texted me a link to track the truck, which made the wait a lot less stressful.',
                     'Jump start took about five minutes and the driver even tested my battery afterward.',
                     'I locked my keys in the car with the engine running and they had it open in no time.',
                     'Pricing was lower than the other two companies I called that night.',
                     'Driver gave me and my dog a ride to the shop in the cab of the truck.',
                     'They towed my car to my mechanic on Forest Ave and dropped the keys in the night box.',
                     'During the big snowstorm they still got to me within an hour, which honestly surprised me.',
                     "Driver pulled my car out of a snowbank with a winch and there wasn't a scratch on it.",
                     'They accepted card payment right on the truck and emailed the receipt immediately.',
                     'The guy who came out was calm and friendly, which helped since I was pretty shaken up after the accident.',
                     'My roadside plan was quoting a three hour wait so I called these guys and they came in forty minutes.',
                     'They swapped my flat for the spare and checked the pressure on the other three too.',
                     'Dispatcher stayed on the phone with me for a bit since I was alone on a dark road.',
                     'Fair rate for a long tow from Freeport back into Portland.',
                     'Truck was clean and the driver was clearly experienced with all-wheel drive cars.',
                     'They called when they were five minutes out so I could wait in the warm store instead of outside.',
                     'They helped me move my car out of the Old Port during the parking ban without any fuss.',
                     'No hidden fees, the invoice matched the quote line for line.',
                     'Driver checked that my motorcycle was strapped down properly before every turn, very careful.',
                     'Got stuck in mud at a trailhead and they were the only company willing to come out.',
                     'Came out on Christmas Eve with no holiday surcharge, which was a nice surprise.',
                     'Their storage yard is secure and the staff let me grab my things from the car without hassle.',
                     'Fuel delivery was quick when I stupidly ran out of gas on Commercial Street.',
                     'The driver explained exactly what he thought was wrong with my car, and he turned out to be right.',
                     "They work with my insurance roadside coverage, so I didn't pay anything out of pocket.",
                     'Truck arrived earlier than the window they gave me, which never happens.',
                     'Office staff answered my billing question the next day and fixed a small mistake right away.',
                     'Driver wore a reflective vest and kept me well back from traffic while he worked.',
                     'They hauled my old van to the scrapyard and got me a fair price for it too.',
                     "Fast lockout service at the Maine Mall, and the tech didn't damage the door at all.",
                     'Even late on a Saturday night the driver was polite and in a good mood.',
                     "I've used them three times now and each time they've been on time and honest.",
                     'They took my car up to a dealership in Westbrook and kept me posted the whole way.',
                     "Driver brought a portable jump pack so he didn't have to block traffic with the truck.",
                     'Dispatch was clear about which truck was coming and when.',
                     'They winched my boat trailer off a slippery ramp when the hitch let go.',
                     "Prices are posted on their website so I knew roughly what I'd pay before I called.",
                     'Being stranded with two little kids was stressful, and the driver was patient and kind with them.',
                     'They cleared my car off the Eastern Prom after a fender bender before the police were even done.',
                     'Clear invoice, polite driver, and my car arrived at the shop in one piece.'],
            'bad': ['They quoted ninety dollars on the phone and the driver demanded almost two hundred when he arrived.',
                    'We waited three hours in the cold and they never showed up or called back.',
                    "There's a fresh scratch along my bumper that wasn't there before and they refuse to take responsibility.",
                    'The dispatcher was rude and hung up on me while I was still giving my location.',
                    'They towed my car from a spot that was clearly legal and charged me a fortune to get it back.',
                    'Impound lot is only open a few hours on weekdays, so I lost a day of work getting my car.',
                    "Driver insisted on cash only and wouldn't give me a receipt.",
                    'He was on his phone the entire drive with my car on the back of the truck.',
                    "Charged a 'winter fee' on top of the regular rate even though it wasn't snowing.",
                    'Phone rang and rang, never once got a live person.',
                    'They dropped my car at the wrong shop across town and wanted extra to move it.',
                    'Driver was impatient and acted like I was wasting his time.',
                    "My car's front spoiler was cracked after they dragged it onto the flatbed.",
                    'Storage fees piled up because they never told me where my car was taken.',
                    'They gave me a two hour window and showed up four hours later.',
                    'Truck smelled like cigarettes and the driver was smoking with the window up.',
                    "Invoice had three line items I never agreed to, like a 'dolly charge' for a regular tow.",
                    'Lockout guy scratched the paint around my door frame with his tool.',
                    'When I called to complain the manager was dismissive and blamed me.',
                    "They wouldn't take my insurance roadside coverage even though they're listed as a provider.",
                    "Dispatcher told me forty five minutes and then said it'd be another two hours when I called back.",
                    'My car came back with the parking brake damaged.',
                    "They wouldn't let me get my medication out of my car without paying first.",
                    'Towing from Old Orchard to Portland cost me more than my monthly car payment.',
                    'Driver left my car unlocked in the shop lot overnight with the window cracked.',
                    "Sent a truck that clearly wasn't right for my AWD car and they did it anyway.",
                    'Online reviews made them sound great but my experience was the opposite.',
                    'The lot attendant was rude and made me wait forty minutes while he finished his lunch.',
                    'They tried to upsell me on a repair shop they obviously have a deal with.',
                    'Absolutely no communication, no ETA, no call, nothing.'],
            'mixed': ['They got there eventually, about an hour later than they said.',
                      'Driver was nice but the final price was higher than the quote.',
                      'Got the job done, not much more to say.',
                      'Service was fine, the wait was long, it was a busy night I guess.',
                      'Decent tow, a bit pricey, and the dispatcher could work on manners.',
                      'No damage to the car, but communication about timing was pretty poor.',
                      'Okay experience overall, nothing great about it and nothing terrible.',
                      'Driver was quick once he showed up, getting him there was the slow part.',
                      'Fair enough price but they only took cash which was a hassle.',
                      "They were alright, I'd probably call someone else first next time."],
            'long_good': ['Had a blowout on 295 northbound around 11pm with my two kids asleep in the back. I was pretty rattled. Called them and '
                          'the dispatcher took my location, gave me a price, and stayed on the line for a minute to make sure I was safely on the '
                          'shoulder. The truck showed up in about 30 minutes. The driver set out flares, put my spare on in ten minutes, and checked '
                          'the other tires. He was calm and kind the whole time. Price was what they quoted. Only thing is the hold music when I '
                          'first called was super loud lol.',
                          "My car wouldn't start in the parking garage under my building in the West End, and most tow companies said they couldn't "
                          'fit. These guys sent a smaller wheel-lift truck and the driver navigated the tight ramp like it was nothing. He towed it '
                          'to my mechanic, texted me a photo when it was dropped, and the invoice came by email. Fair price for a tricky job. A bit '
                          'of a wait (just over an hour) but they told me that upfront.',
                          "January, 6 degrees out, and I slid into a snowbank on a back road in Falmouth. Called three companies; two didn't answer, "
                          'the third quoted four hours. These guys said 45 minutes and showed up in 40. The driver winched me out carefully, checked '
                          'under the car for damage, and gave me a tip about the tires I had on, which honestly needed replacing. He charged me less '
                          "than I expected given the weather. I've saved their number in my phone for good. Wish they had an app instead of just "
                          'calling.',
                          'Locked my keys in my car at the ferry terminal with my groceries in the trunk and a boat to catch to Peaks. Called in a '
                          'panic and they had someone there in 15 minutes. The tech popped the door open in under two minutes, no damage, and was '
                          "totally friendly about my stupidity. Made my ferry with time to spare. Lockout fee was reasonable. Only reason I'm "
                          'mentioning anything negative is that the first person who answered the phone sounded half asleep, but they were on it.',
                          "Used them to tow my late father's old truck, which hadn't run in years, from his house in South Portland to a scrapyard. "
                          'The driver was patient while we cleaned out the cab, helped me pull a few last things out of the bed, and was respectful '
                          'when I got a little emotional. He then got a fair price from the yard on my behalf. Not a typical tow but they handled it '
                          'with real care. Took a couple days to get on the schedule, which was fine for a non-emergency.',
                          "Got rear-ended at a light near the Old Port and my car wasn't drivable. The police called this company. The driver "
                          'arrived quickly, was very gentle getting the car on the flatbed, and took photos of the damage before loading it, which '
                          'ended up helping with my insurance claim. He gave me a ride to my apartment too. Their storage lot was clean and easy to '
                          "find when the adjuster went to see it. Billing went straight to the other driver's insurance. Would give six stars if I "
                          'could.',
                          'Battery died at the Maine Mall on a Sunday afternoon. Dispatcher was friendly and quoted me a flat price for a jump. The '
                          'driver came in about 25 minutes with a portable pack, got me started, then tested the battery and told me it was on its '
                          "last legs. He was right, it died again two days later, but I knew to go straight to a parts store. Quick, honest, didn't "
                          'try to sell me anything. My only complaint is I had to wait a bit to find out which truck was coming.',
                          'Our camper van broke down on the way back from Acadia and we limped to a rest stop outside Portland. Not every company '
                          'can tow something that size, but they sent a big truck within two hours and the driver handled it like a pro. He '
                          'suggested a shop in town that works on Sprinters and they ended up being great too. Price was high but fair for the size '
                          'and distance. Driver was easygoing and our dog loved him. Lifesavers on what could have been a ruined vacation.'],
            'long_bad': ['Called for a tow from Back Cove to my mechanic, about three miles. The dispatcher quoted $95. Driver showed up, hooked up '
                         "my car, and then said the total was $185 because of a 'mileage minimum' and an 'after-hours fee' at 6:30pm. I had no "
                         'choice at that point. When I called the office the next day they said the dispatcher must have been mistaken and refused '
                         'to adjust it. Get everything in writing if you use them.',
                         'Waited on the side of the road in the rain for over two hours. Called back three times and each time was told the driver '
                         "was 'ten minutes away.' He finally arrived, said nothing about the delay, and loaded my car so roughly that the front lip "
                         "got cracked. When I pointed it out he said it was already like that. It wasn't, I have photos from that morning. Still "
                         'waiting on a response from the office.',
                         'My car was towed from a lot I had permission to park in, and getting it back was a nightmare. The impound lot is only open '
                         '9 to 4 on weekdays, so I had to take a day off work. Then they wanted cash only, plus a storage fee for the night. The guy '
                         "at the window was rude and acted like I was a criminal. I understand they're hired by property owners but there's no "
                         'reason to treat people this way.',
                         'Dispatcher was short with me and hung up before I finished giving the cross street. Called back and got a different person '
                         "who said they'd send someone in 45 minutes. Nobody came. After two hours I called another company who came in 30. Never "
                         'got a call back from these guys. Maybe they were busy, but at least let people know so they can make other plans.',
                         'They towed my car to their own lot instead of my mechanic, which I had clearly said twice. Then they wanted another $120 '
                         'to move it the four miles to the right place, plus a storage fee for the day it sat there. The driver was polite enough '
                         "but the office staff were not willing to admit any mistake. Expensive lesson, and I'll be calling someone else from now "
                         'on.']},
 'steak': {'dishes': ['Dry-Aged Bone-In Ribeye',
                      '8 oz Filet Mignon',
                      'Wagyu Strip',
                      'Porterhouse for Two',
                      'Lobster Mac and Cheese',
                      'Creamed Spinach',
                      'Raw Bar Oysters',
                      'Wedge Salad',
                      'Duck Fat Potatoes',
                      'Bourbon Butterscotch Bread Pudding'],
           'short_good': ["Best ribeye I've had in Maine.",
                          'perfect medium rare every time',
                          'Worth every penny.',
                          'Anniversary dinner was perfect!',
                          'Great steaks, great martinis.',
                          'the filet melted. wow',
                          'Splurge worthy.',
                          'Service was polished and warm.',
                          'Excellent dry aged strip.',
                          'Classy without being stuffy.',
                          'lobster mac is ridiculous',
                          'Our new special occasion spot.',
                          'Fantastic wine list.',
                          'Steak cooked exactly right.',
                          'Loved the booth by the fireplace.',
                          'Pricey but you get it.',
                          "Old Port's best steak dinner.",
                          'great bar, great old fashioned',
                          'Everything was on point tonight.',
                          'Five stars, no notes.',
                          'the bread pudding!!',
                          'Solid, consistent, worth it.',
                          'Came for a birthday, loved it.',
                          'Best creamed spinach anywhere.',
                          'would go back tomorrow',
                          'Superb porterhouse for two.',
                          'Knowledgeable server, great pairing.',
                          'Oysters were super fresh.',
                          'A real steakhouse. Finally.',
                          'dad loved it, thanks guys'],
           'short_bad': ['Overcooked filet, sent back twice.',
                         'Way too expensive for this.',
                         'Waited 50 minutes with a reservation.',
                         'steak was cold. no apology',
                         'Not worth the price.',
                         'Snobby host, mediocre food.',
                         'Gristly ribeye. Very disappointed.',
                         'Loud and rushed. Skip it.',
                         '$18 for soggy potatoes??',
                         'Expected more for $300.',
                         'Felt like a tourist trap.',
                         'never got our sides'],
           'good': ['My ribeye came out a true medium rare with a dark crust that crackled when I cut into it.',
                    'The dry aged strip had that funky, nutty flavor you only get when they actually age it in house.',
                    "Our server walked us through the cuts without being condescending, which I appreciated since I'm not a steak expert.",
                    'The lobster mac and cheese had big chunks of claw meat, not just a few sad shreds on top.',
                    'Creamed spinach was rich and garlicky and we scraped the dish clean.',
                    'They brought out a little candle and a card for our anniversary without us even asking.',
                    "The old fashioned at the bar is made with a big clear ice cube and it's strong in the best way.",
                    'We sat in a booth near the fireplace and it felt cozy on a freezing January night.',
                    'The wine list is long but the sommelier steered us to a twenty-something cab that drank way above its price.',
                    'Bread comes out warm with a whipped honey butter that I could honestly eat by the spoonful.',
                    'The filet was so tender I barely needed the steak knife they gave me.',
                    'Oysters from the raw bar were briny and cold, clearly shucked right before they came out.',
                    'Duck fat potatoes were crispy outside and fluffy in the middle, easily the best side we ordered.',
                    'They split the porterhouse tableside for us which was a nice bit of theater.',
                    'Even though it was packed on a Saturday the kitchen kept the pacing between courses just right.',
                    "The wedge salad is old school with thick bacon and a blue cheese dressing that isn't too heavy.",
                    "When my wife's steak came out a little under they swapped it fast and comped her glass of wine.",
                    'Parking in the Old Port is a nightmare but they validate at the garage around the corner.',
                    'The bourbon bread pudding is big enough for two and tastes like caramel and toast.',
                    "Our server remembered we'd been in last fall and asked if we wanted the same bottle.",
                    'The room is dark wood and leather and actually quiet enough to have a conversation.',
                    'I asked for my strip Pittsburgh style and they nailed the char without overcooking the center.',
                    "They were super accommodating with my daughter's gluten allergy and the chef came out to talk to us.",
                    'Steaks come with your choice of three butters and the bone marrow one is the move.',
                    "The bar menu has a smaller steak frites that is a great deal if you don't want the full thing.",
                    'Dessert came with two spoons and a little happy birthday written in chocolate on the plate.',
                    'Martinis are ice cold and they give you the sidecar in a little carafe on ice.',
                    'The Wagyu strip was rich enough that we split one and were totally satisfied.',
                    'Staff were attentive but never hovering, water glasses were always full.',
                    'We had a business dinner for eight and they handled separate checks without any fuss.',
                    'The mushrooms side was loaded with chanterelles and a ton of butter, highly recommend.',
                    "I've been to the big chain steakhouses in Boston and this was better for less money.",
                    "The host found us a table at the bar on a busy night even though we didn't have a reservation.",
                    'Shrimp cocktail had five huge shrimp and a horseradish sauce that cleared my sinuses.',
                    "They cooked my husband's steak well done without any attitude, which honestly is rare.",
                    'Coat check at the door is a small thing but nice in winter when everyone is bundled up.',
                    'The chocolate cake was dense and fudgy and they warmed it slightly before serving.',
                    'The manager stopped by every table to check in and actually seemed to care about the answer.',
                    'Every steak is seasoned heavily with salt and pepper the way it should be.',
                    'Happy hour at the bar has half price oysters and a burger made from steak trimmings that is fantastic.',
                    'Their reservation system sent a reminder text the day before which saved me from forgetting.',
                    'The sauce béarnaise was buttery and tangy and clearly made from scratch.',
                    'We came in after a show at Merrill Auditorium and they kept the kitchen open for us.',
                    'Portions are generous enough that I took half my porterhouse home for steak and eggs.',
                    'Cocktail list has a few local spirits and the one with Maine blueberry gin was really good.'],
           'bad': ['I ordered my filet medium rare and it showed up gray all the way through.',
                   "We had a 7:30 reservation and weren't seated until almost 8:20.",
                   'For a $70 ribeye I expected better than a thin, chewy cut with a big strip of gristle.',
                   'Our server disappeared for twenty minutes after the entrees came and we never got the steak sauce.',
                   'The sides are all extra and the creamed spinach was mostly cream and barely warm.',
                   "The table next to us was a big birthday party and it was so loud we couldn't talk.",
                   "My wife's lobster tail was rubbery and clearly overcooked.",
                   'The host was rude when we asked to move away from the kitchen door.',
                   'They added an automatic 20 percent gratuity for a party of five without telling us.',
                   'The bread was stale and the butter came out rock hard from the fridge.',
                   'A glass of very ordinary house red was nineteen dollars.',
                   'My steak was under-seasoned and tasted like it had been sitting under a heat lamp.',
                   'We were rushed through dessert because they clearly wanted the table back.',
                   'I mentioned it was our anniversary when booking and nobody acknowledged it at all.',
                   'The bathroom was out of paper towels and the floor was wet the whole night.',
                   "The dry aged ribeye smelled off and the kitchen insisted that's just how aged beef tastes.",
                   'Our appetizer came out at the same time as our entrees which felt sloppy for this price point.',
                   'It took three requests to get a refill on water.',
                   "The potatoes were greasy and limp like they'd been fried hours before.",
                   'Valet took forever to bring our car around and scratched the bumper.',
                   'My medium steak came out bloody rare and then the replacement was well done.',
                   'The manager offered a free dessert after we complained but nobody actually brought it.',
                   'Oysters had bits of shell in them and one was dry.',
                   'The dress code feels stuffy and they made my son put on a jacket from their closet.',
                   'The music was weirdly loud for a fancy steakhouse, more like a club.',
                   'Our server pushed the most expensive bottle on the list pretty hard.',
                   'The wedge salad was a quarter head of iceberg with three crumbles of blue cheese.',
                   'We found a hair in the mac and cheese and they only took it off the bill after we asked.',
                   'The bill was over $400 for two and nothing about the night felt special.',
                   'They seated us at a tiny two-top wedged between the bar and the service station.'],
           'mixed': ['The steak itself was good but the sides were forgettable for what they charge.',
                     "Nice atmosphere and solid service, though I've had better filets for less elsewhere in Portland.",
                     "It's fine, just very expensive for what is basically a well cooked piece of beef.",
                     'Food was good, not amazing, and the wait for a table was long even with a reservation.',
                     'The bar area is fun but the dining room felt a little dated to me.',
                     'Ribeye was great, the lobster tail was overcooked, so kind of a wash.',
                     'Three stars mostly because of price, the cooking was okay.',
                     "Good for a special night out, but I wouldn't go out of my way to come back soon.",
                     'Desserts were the highlight honestly, the entrees were just okay.',
                     'Service was a bit slow but friendly, and my steak came out right on the second try.'],
           'long_good': ["Took my parents here for their 40th anniversary and I was nervous because they're not easy to impress. My dad ordered the "
                         'bone-in ribeye and went quiet for like five minutes, which is the highest compliment he gives. Mom had the filet and kept '
                         'stealing duck fat potatoes off my plate. Our server noticed the occasion when I mentioned it while booking and brought out '
                         'bread pudding with a candle. Only gripe is it was a bit loud near the bar so ask for a table in the back room. Bill was '
                         'steep but this was the night to do it.',
                         "I'm a pretty picky steak person and usually cook my own at home on cast iron because restaurants overcook everything. Not "
                         'here. Ordered the dry aged strip medium rare and it was exactly that, edge to edge pink with a proper salty crust. The '
                         'bone marrow butter on the side was a little much for me but my friend loved it. We split the wedge and the mushrooms and '
                         'both were great. Bartender made a really good Manhattan too. Parking was the usual Old Port hassle but they validate so '
                         'that helps.',
                         'Came in on a snowy Tuesday with no reservation and they gave us a booth by the fireplace right away. It was honestly '
                         'perfect. We started with a dozen oysters, they were cold and briny and the mignonette had a nice kick. I had the '
                         "porterhouse for two by myself (don't judge, I took half home) and my girlfriend had the scallops off the specials board. "
                         'Service was friendly and relaxed, never pushy about ordering more. Took a star off in my head for the $16 side of '
                         "asparagus but I'm still giving five because the night was great.",
                         "We booked this for my husband's 50th and they really went the extra mile. The host had a printed card on the table with "
                         "his name on it and a little glass of bubbly waiting. He got the Wagyu strip and said it was the richest steak he's ever "
                         'had. I went with the filet and lobster mac which was super decadent. The only downside was our entrees took a while to '
                         'come out, maybe 35 minutes after the salads, but the server kept checking in and topped off our wine. Would absolutely '
                         'book again for the next big birthday.',
                         'work dinner, eight of us, and i was the one who picked the place so the pressure was on lol. they put us in a semi private '
                         'room in the back which was great because we could actually hear each other. everyone ordered something different and all '
                         'the steaks came out right temp which is impressive for a big table. the sommelier picked two bottles for the table within '
                         'our budget and they were both great. dessert was the chocolate cake and the bread pudding. a little slow getting the check '
                         'at the end but nobody cared. boss was happy so im happy',
                         "Been coming here about twice a year since they opened and it's still my favorite special occasion spot in Portland. The "
                         "ribeye has always been consistent, and this time I tried the creamed spinach for the first time and can't believe I "
                         'skipped it before. Our server was new but knew the menu cold and gave an honest answer when I asked about the specials '
                         '(she said skip the halibut, get the steak, she was right). Small complaint: the room was a bit chilly by the windows. '
                         'Bring a sweater in winter.',
                         "My wife and I don't go out much since the baby came, so when we do it has to count. This place delivered. The bread with "
                         'honey butter came out warm, the martinis were strong, and my filet was buttery soft. She had the strip with au poivre '
                         'sauce and kept saying wow. The staff were super patient when we spent way too long looking at the wine list. Only thing '
                         "I'd change is the dessert menu, it's kind of small. We still split the bread pudding and it was perfect. Already planning "
                         'the next date night.',
                         'Visiting from Ohio for a week and asked around for a steak recommendation, a couple people at our hotel pointed us here. '
                         'Glad we listened. The dining room feels old school, dark wood, low lighting, white tablecloths. I had the bone-in ribeye '
                         'and my brother had the porterhouse, and we both cleaned our plates. The lobster mac was a nice Maine touch. Our server '
                         'gave us a bunch of tips for things to do in town the next day too. Prices are big city prices, so heads up, but the '
                         'quality was there.'],
           'long_bad': ['Really wanted to love this place for our anniversary. We had a 7pm reservation and sat at the bar until almost 7:45 with no '
                        'update. Once seated, my filet came out well done when I asked for medium rare. They took it back and the second one was raw '
                        'in the middle. By then my wife had finished eating. The manager came over and said the kitchen was slammed, and took the '
                        'steak off the bill, but the whole night was shot. Over $250 and we left disappointed.',
                        'Overpriced and underwhelming. The ribeye was $68 and had a huge chunk of fat and gristle running through it. Sides are a la '
                        'carte and small, the potatoes were lukewarm and greasy. Our server seemed annoyed when we asked questions about the menu '
                        'and pushed us toward a $150 bottle of wine. The dining room was so loud we had to shout. There are better steaks in this '
                        "town for half the price. Won't be back.",
                        "We came for my mom's birthday and I'd called ahead to mention it. Nothing. No candle, no acknowledgment, nothing. That "
                        "would've been fine if the food was good, but the lobster tail was rubbery and the steak was under-seasoned. We waited ages "
                        'between courses and nobody came by to refill water. When the check came there was an automatic 20 percent tip added for a '
                        "party of five that wasn't mentioned anywhere. Felt like a tourist trap in the Old Port.",
                        "Honestly not sure what the hype is about. Strip steak was fine but nothing I couldn't do at home. The oysters had grit in "
                        "them and one was clearly bad, which we pointed out and the server just shrugged. The host made a comment about my husband's "
                        'jacket being too casual which was embarrassing. Dessert was the best part. For the price of this dinner we could have had a '
                        'much nicer night somewhere else in Portland.',
                        "Ordered takeout during a busy weekend because we couldn't get a table. Paid almost $140 for two steaks and two sides. When "
                        'I got home one steak was cooked completely wrong and the creamed spinach was missing entirely. Called and they said they '
                        "could give me a credit for next time, but I don't want a next time. The steak that was right was decent, but this is not "
                        'how a supposedly high end place should treat customers.']},
 'locksmith': {'short_good': ['Fast, fair, and friendly.',
                              'Got me back in my car quick.',
                              'Showed up in 20 minutes!',
                              'honest price, no upsell',
                              'Saved my night. Thank you!',
                              'Rekeyed the whole house, great job.',
                              'Quoted price was the final price.',
                              'super quick lockout help',
                              'Professional and on time.',
                              'Made spare car keys cheap.',
                              'Highly recommend, very trustworthy.',
                              'Came out at 2am, legend.',
                              'Fixed our sticky deadbolt.',
                              'No damage to the door.',
                              'Way cheaper than the dealer.',
                              'will call again for sure',
                              'Great work on our new locks.',
                              'Answered on the first ring.',
                              'Easy to schedule, fair rate.',
                              'Explained everything clearly.',
                              'Our go-to locksmith now.',
                              'Quick fob programming, thanks!',
                              "Got my kid's bike unlocked lol",
                              'Reliable and reasonably priced.',
                              'Fixed it in ten minutes.',
                              'Polite, clean, and fast.',
                              'Locked out, back in quick.',
                              'Five stars for the emergency call.',
                              'solid local business',
                              'Excellent service, fair pricing.'],
               'short_bad': ['Quoted $75, charged $240.',
                             'Never showed up. Waited two hours.',
                             'Drilled my lock for no reason.',
                             'rude on the phone',
                             'Overpriced lockout fee.',
                             "Key they cut doesn't work.",
                             'Scratched up my car door.',
                             'Hidden fees everywhere.',
                             "Didn't call back. Ever.",
                             'Took forever, charged a fortune.',
                             'Would not recommend, total ripoff.',
                             'New lock broke in a week.'],
               'good': ['I locked my keys in the car at the Back Cove trail lot and they had me back in within half an hour.',
                        'The price they quoted over the phone was exactly what I paid, no surprise fees tacked on.',
                        "He opened my front door with a pick set and didn't leave a single scratch.",
                        'We just bought a house on Munjoy Hill and they rekeyed every lock in about an hour.',
                        'They cut and programmed a new key fob for my Honda for less than half what the dealership wanted.',
                        'Called at 11pm in the rain and the tech still showed up cheerful and got me inside fast.',
                        'He took the time to show me why my deadbolt was sticking instead of just selling me a new one.',
                        'They texted a photo of the tech and the van ahead of time, which made me feel a lot safer.',
                        'My landlord was out of town and they got me back into my apartment without any drama.',
                        'The new smart lock they installed was lined up perfectly and the door closes smoother than before.',
                        'They matched all our house keys to one key so I no longer carry around a giant ring.',
                        'I got stuck at a gas station off I-295 and they found me even though I gave terrible directions.',
                        'He double checked my ID and that I lived there before opening the door, which I actually appreciated.',
                        'The tech was patient with my elderly mom and explained how the new lock works three times without complaint.',
                        "They fixed the lock on our sliding back door that's been broken since we moved in.",
                        'Payment was easy, they took a card right on a phone reader in the van.',
                        'When my key snapped off in the ignition they extracted it and made a new one on the spot.',
                        "They installed a keypad on our side door so the kids don't need keys after school.",
                        'The dispatcher gave me a realistic arrival time and he showed up right inside that window.',
                        'He recommended a cheaper deadbolt than the one I picked because he said it was just as secure.',
                        'They came out to our small office on Forest Ave to change locks after an employee left.',
                        'I was locked out with a toddler inside the car and they treated it as the emergency it was.',
                        "He swept up the little bits of metal shavings before he left, which most people wouldn't bother with.",
                        'Cutting four spare house keys took about five minutes and cost less than lunch.',
                        "They opened an old safe of my grandfather's that nobody had the combination for.",
                        'The tech wore boot covers inside the house without being asked.',
                        'They got my trunk open after the latch broke without having to take apart the bumper.',
                        "Even though it was a Sunday they didn't charge some crazy after hours rate.",
                        "He told me upfront that the mailbox lock was a cheap fix and didn't try to upsell anything.",
                        'They replaced the entire handle set on our front door and it looks great with the new paint.',
                        'I called three places and they were the only one who picked up and gave a straight answer.',
                        'My elderly neighbor locked herself out and they were kind and quick with her.',
                        "The tech brought the right parts the first time so there wasn't a second trip.",
                        'They rekeyed our rental unit between tenants the same day I called.',
                        'He programmed a spare fob for my Subaru in the parking lot at work while I was in a meeting.',
                        'Our garage side door lock was rusted solid and they swapped it out quickly.',
                        'They gave me a written invoice with the parts listed, which helped for my landlord reimbursement.',
                        'I got locked out in South Portland at 6am before work and they were there before my coffee got cold.',
                        'The guy was friendly and chatted about the Sea Dogs while he worked, which made the whole thing less stressful.',
                        'They put in a lock box for our Airbnb guests and showed me how to change the code.',
                        'When the first key they cut was a little stiff he recut it on the spot without charge.',
                        'They had a reasonable flat rate for lockouts posted on their website so I knew what to expect.',
                        'He installed a Grade 1 deadbolt on our back door and explained what that rating actually means.',
                        "They called me when they were ten minutes away so I wasn't standing outside in the cold.",
                        "I've used them for my car, my house, and my office now and they've been consistent every time."],
               'bad': ['The phone quote was $85 but the bill came to over $200 with a bunch of fees I never heard about.',
                       'They said someone would be there in 30 minutes and I ended up waiting almost two hours in the cold.',
                       'Instead of picking the lock the tech went straight to drilling it out and then charged me for a new lock.',
                       "The key they cut for my car doesn't turn in the ignition and they won't refund it.",
                       "There's a long scratch down my driver side door from the tool they used to get in.",
                       'Nobody answered the phone and my voicemail was never returned.',
                       'The guy on the phone was short with me and kept trying to hang up.',
                       'The deadbolt they installed already feels loose after just a couple of weeks.',
                       'They charged an emergency rate at 4pm on a weekday.',
                       "The tech showed up in an unmarked car and wouldn't give me a business card.",
                       'He left the old lock parts and packaging on my porch.',
                       'The fob they programmed stopped working after three days.',
                       'They told me I needed all new locks when I really just needed a rekey, which another company did for much less.',
                       "They canceled my appointment the morning of and didn't offer a new time.",
                       'The tech was on his phone the whole time and seemed annoyed to be there.',
                       "Our front door doesn't latch properly anymore after they replaced the strike plate.",
                       "They couldn't get my car open and still charged me a trip fee.",
                       'The invoice was handwritten and impossible to read, with no breakdown of what I paid for.',
                       'It took three visits to get a simple smart lock installed correctly.',
                       'They lost one of my spare keys that I gave them to copy.',
                       'The price for a basic house key copy was way more than the hardware store.',
                       'He got the dispatch address wrong and went to Westbrook instead of Portland.',
                       'When I called to complain they blamed me for the lock being old.',
                       'The keypad they installed is crooked and the paint around it is chipped.',
                       'I was told they accept cards but when the tech arrived it was cash only.',
                       'They promised a callback with a quote for the office and never followed up.',
                       "The rekey didn't work on the back door so the old key still opens it.",
                       "He tracked mud all through our hallway and didn't seem to care.",
                       "They upsold me a high security cylinder I didn't need and wouldn't take it back.",
                       'My trunk lock is now worse than before they touched it.'],
               'mixed': ['They got the job done eventually but it took a lot longer than they said it would.',
                         'Fine service, a little pricey for a basic lockout.',
                         'The tech was nice but had to come back a second day for a part.',
                         'Okay experience, nothing special, but at least the door opens now.',
                         "The work is good but they're really hard to reach by phone.",
                         'Got me in the car but charged more than the quote, so three stars.',
                         'Decent rekey job, though they were an hour late.',
                         'The lock works but the install looks a little rough around the edges.',
                         'Pricey compared to others I called later, but they were the first available.',
                         'No complaints about the work itself, scheduling was just a hassle.'],
               'long_good': ['Locked myself out of my apartment on Munjoy Hill at about 10:30 at night in just socks and a hoodie. My phone was '
                             'thankfully in my pocket. Called a couple of places and these guys were the only ones who answered. The dispatcher '
                             'quoted me a flat rate and said 25 minutes, and the tech showed up in about 20. He checked my ID against my lease photo '
                             "on my phone, then picked the lock in under five minutes. No damage at all. Only reason I'd nitpick is the after hours "
                             "fee, but honestly at 10:30 I'd expect that.",
                             'We closed on our first house in South Portland and the inspector told us to rekey everything since who knows how many '
                             'keys the old owners handed out. Booked online and they came the next morning. The tech rekeyed six locks (front, back, '
                             'garage, two sliders and a shed padlock) and matched them all to one key. He also pointed out that the back door strike '
                             'plate only had tiny screws and swapped in longer ones for free. Took about an hour and a half. Price was very fair. '
                             "They're now saved in my phone.",
                             'Lost my only Toyota key on a hike and the dealership wanted $450 plus a tow. Called around and these folks came to my '
                             'driveway, cut a new key and programmed the fob for way less. It took the tech a bit longer than planned because the '
                             "first blank was wrong for my year, but he had the right one in the van and didn't charge extra for the time. He even "
                             'made a spare while he was there. Super relieved. Would definitely use them again for car stuff.',
                             'small business owner here, we have a shop on Forest Ave. had to let someone go and needed locks changed the same day. '
                             'called at 9am, they had someone over by noon. the tech swapped the front and back cylinders and installed a new lock '
                             'on the office door too. gave me a proper invoice for my bookkeeper. a little pricier than I hoped but same day service '
                             "on short notice is worth paying for. very professional, didn't disrupt customers at all",
                             'My mom is 84 and lives alone near Back Cove. She locked herself out while getting the mail and called me in a panic. '
                             "I'm 40 minutes away so I called these guys, explained the situation and they got there before I did. When I arrived he "
                             'was sitting on the porch steps chatting with her and she was totally calm. Got her inside quick and suggested a '
                             "lockbox with a spare key for next time, which they installed the following week. Can't thank them enough for being so "
                             'kind with her.',
                             'Had a deadbolt that had been sticky for months and finally gave up on WD-40. Expected to be told I needed a whole new '
                             'lock. Instead the tech took it apart, showed me the worn pin, replaced that and lubed it with graphite, and said the '
                             'rest of the lock was fine. Charged me for a service call and a tiny part. Honest people are hard to find in this '
                             "trade. Only small thing is their scheduling window was 4 hours wide, but he called ahead so I wasn't stuck waiting.",
                             'Got a flat on I-295 heading north and while getting stuff from the car I somehow managed to lock the keys in with the '
                             'engine running. Yeah. Embarrassing. Called and they were really nice about it, no judgment. Tech got there in maybe 35 '
                             'minutes, had the door open in two without any scratches. Price matched what they told me on the phone. He even waited '
                             'while I put the spare on to make sure I was okay. Seriously good people.',
                             'We manage a few rentals in Portland and have used a lot of locksmiths over the years. These guys are by far the most '
                             'reliable. Turnovers are always same day or next day, they text when they arrive and when they leave, and the invoices '
                             'are clear. Last month they installed keypads on two units and walked the tenants through setting codes. They do cost a '
                             "few bucks more than one or two others in the area but I don't have to chase them, which saves me way more than the "
                             'difference.'],
               'long_bad': ['Called for a simple house lockout and was quoted $79 on the phone. The guy showed up nearly two hours later and '
                            "immediately said the lock was high security and he'd have to drill it. He didn't even try picking it. Then he wanted "
                            "$280 including a new deadbolt that's obviously the cheapest one at the hardware store. I felt cornered because it was "
                            'late and cold. Total bait and switch. Please call someone else.',
                            "They made a spare key for my car and programmed a new fob. Fob died after four days and the key doesn't turn the "
                            "ignition. I've called five times. Twice they said they'd call back, they didn't. Once they said it was a problem with "
                            "my car. I'm out almost $200 and still have only one working key. The tech was friendly but that doesn't matter if the "
                            "work doesn't hold up.",
                            'Booked an appointment to rekey our house after moving in. They canceled the morning of with no explanation. '
                            'Rescheduled, and the tech arrived three hours past the window. He rekeyed the front door but said the back door would '
                            "need another visit. A week later our old key still opens the back door. They're not returning calls. Hiring another "
                            'company to finish the job.',
                            'Got locked out of my car downtown and they quoted me 30 minutes. 90 minutes later the tech arrives, uses some kind of '
                            'wedge and rod, and leaves a big scratch on my door frame and a chip in the paint. When I pointed it out he said that '
                            'happens sometimes. Then he charged me for a late night rate even though it was 7pm. Manager never called me back about '
                            'the damage.',
                            'The guy who answered the phone was rude from the start and acted like I was wasting his time asking what a rekey costs. '
                            'Went with them anyway because they were close. The install of our new handle set looks crooked and the door now sticks. '
                            'Asked them to come fix it and they want to charge another service call. Not worth the hassle.']},
 'carwash': {'short_good': ['Monthly plan pays for itself.',
                            'free vacuums are clutch',
                            'Car looks brand new!',
                            'Quick in and out.',
                            'Best wash in South Portland.',
                            'Great value, friendly attendants.',
                            'Got all the salt off.',
                            'love the unlimited plan',
                            'Fast, cheap, shiny.',
                            'Vacuums actually have suction!',
                            'Never a long wait.',
                            'The tire shine is great.',
                            'Clean facility, good wash.',
                            'My go-to after snowstorms.',
                            'Easy app, easy wash.',
                            'Kids love the colored foam lol',
                            'Truck came out spotless.',
                            'worth the drive every week',
                            'Friendly guy at the entrance.',
                            'Good wash for the price.',
                            'Ceramic option really beads water.',
                            'Plenty of vacuum spots.',
                            'Undercarriage spray saved my car.',
                            'Always clean, always quick.',
                            'Five stars from a car nerd.',
                            'nice towels by the vacuums',
                            'Membership cancel was easy too.',
                            'Super quick on my lunch break.',
                            'Better than any other tunnel nearby.',
                            'great wash, nice people'],
             'short_bad': ['Broke my side mirror.',
                           'Still dirty after the top wash.',
                           "Can't cancel the monthly plan!",
                           'vacuums never work',
                           'Charged me twice this month.',
                           'Line was 45 minutes long.',
                           'Left soap streaks everywhere.',
                           'Scratched my brand new paint.',
                           'Dryers barely do anything.',
                           'Rude attendant, dirty car.',
                           'Gate camera never reads my plate.',
                           'Total waste of money.'],
             'good': ['The undercarriage spray gets all the road salt off after a Maine winter, which is why I joined.',
                      'I signed up for the monthly plan and with how often I go it costs me less than two washes.',
                      'The free vacuums have really strong suction and there are plenty of spots even on a Saturday.',
                      "The license plate reader opens the gate automatically so I don't even have to roll down my window in January.",
                      'The attendant at the entrance pre-sprays the front bumper to get the bugs off before you go in.',
                      'They have microfiber towels and a mat clamp at every vacuum station, which is a nice touch.',
                      'My black SUV came out without any water spots thanks to the spot free rinse.',
                      'The tunnel is quick, maybe four minutes from start to finish.',
                      'The ceramic coating option makes rain bead right off for a couple of weeks.',
                      'Even on a busy day after a snowstorm the line moves fast because they have three lanes open.',
                      "The app lets me add my wife's car to the plan for a discount.",
                      'The dryers at the end are strong enough that I only need to wipe the mirrors.',
                      "They have a little air hose next to the vacuums that's great for blowing out cupholders.",
                      "Tire shine is even and doesn't sling all over the side of the car afterward.",
                      'The staff guided me onto the conveyor really patiently since it was my first time in a tunnel wash.',
                      'When the wash missed a spot on my tailgate they let me run through again for free.',
                      'The vacuum area is well lit so I can clean my car after work in the winter without squinting.',
                      'Canceling a month while I was traveling was easy and took two minutes in the app.',
                      'The location right off the main road makes it easy to swing by on my commute.',
                      'The pre-soak gets the pollen film off in the spring that other washes leave behind.',
                      'They have a mat washer that cleaned my rubber floor mats better than I could with a hose.',
                      "The lot is always plowed and salted, which isn't a given in Portland in February.",
                      'My kids think the rainbow foam is the best thing ever so we make it a weekend trip.',
                      'The guy at the entrance noticed my antenna and reminded me to take it off before going in.',
                      'The wheels come out actually clean, including the brake dust I can never get off myself.',
                      "I like that they show which wash level you're on with lights inside the tunnel.",
                      "Their basic wash is honestly good enough for most weeks and it's cheap.",
                      'After a muddy camping trip my Jeep came out looking better than when I bought it.',
                      'The trash cans at the vacuums are emptied regularly so it never gets gross over there.',
                      "They had a promo for the first month free which got me to try it and I've stayed.",
                      'I go almost every day in the winter and nobody gives me a hard time about it.',
                      'The bathrooms inside are clean and they have free coffee in the morning.',
                      'They fixed a billing mistake on my membership the same day I called.',
                      'Staff walked out with a towel to dry my side mirrors without me asking.',
                      'Pulling into the tunnel is easy because the guide lights tell you exactly when to stop.',
                      'Even the bug guts from a drive up from Boston came off in one pass.',
                      'My windshield is noticeably clearer after they started using the rain repellent.',
                      "The signs explaining each wash package are simple and they don't pressure you at the window.",
                      "There's a vending machine with air fresheners and glass wipes if you forget yours.",
                      'My convertible top came through fine and they told me which package was safest for it.',
                      'Hours are long so I can stop by at 7 at night after work.',
                      'Vacuum hoses reach all the way to the back of my minivan without stretching.',
                      'They put in a second vacuum row last year so I rarely wait for a spot anymore.',
                      "My car's paint still looks good after a year of weekly washes here.",
                      'Signing up at the kiosk took about a minute and the plate reader worked the very next day.'],
             'bad': ['The brushes ripped off my passenger side mirror and they made me fill out a form instead of fixing it.',
                     'There was still a strip of grime across my back window after paying for the top package.',
                     'I tried to cancel my membership three times and kept getting charged.',
                     'Half the vacuums were broken or had no suction at all.',
                     'My card was charged twice for the monthly plan and it took weeks to get a refund.',
                     'The line backed up onto the road and it took 40 minutes to get in.',
                     'The dryers barely work so my car came out soaking wet and spotty.',
                     "There are new swirl marks on my dark paint that weren't there before.",
                     'The plate reader never recognizes my car so I have to flag someone down every time.',
                     "The attendant was on his phone and didn't guide me onto the track, so I went in crooked.",
                     'My wipers got pulled up by the brushes and one of them is bent now.',
                     'The tire shine sprayed all over my rims and side panels and left a greasy mess.',
                     'The vacuum area is full of trash and the cans were overflowing.',
                     'They closed early with no notice even though the sign said open until eight.',
                     "My truck's bed came out dirtier than it went in somehow.",
                     "The ceramic upgrade costs a lot more and I couldn't tell any difference.",
                     'Soap residue dried on the windshield and I had to clean it myself at a gas station.',
                     'Staff were rude when I asked them to run me through again for a missed spot.',
                     'The conveyor jerked and my car bumped into the guide rail.',
                     "The mat clamps are all broken so there's nowhere to hang mats while vacuuming.",
                     'They raised the monthly price without telling members ahead of time.',
                     'Wheels were basically untouched, the brake dust was still caked on.',
                     "The app crashes constantly and won't let me update my card.",
                     "My rear wiper got snapped off and the manager said it's not their responsibility.",
                     'The entrance was icy and nobody had salted it.',
                     'Salt was still crusted along the rocker panels after the undercarriage package.',
                     'Water got into my car through the door seals for the first time ever.',
                     "They upsell hard at the window every single time even though I'm a member.",
                     'The vacuums shut off after a couple minutes and you have to go back and restart them.',
                     'The air freshener machine took my money and gave me nothing.'],
             'mixed': ['The wash is okay but the dryers leave a lot of water behind.',
                       'Good value with the membership, though it gets really crowded on weekends.',
                       "Basic wash is fine, I wouldn't bother paying for the fancy packages.",
                       'Vacuums are hit or miss depending on which spot you get.',
                       "It's a decent quick wash, not a detail, so set your expectations.",
                       'Car usually comes out clean but there are always a few spots it misses on the back.',
                       'Staff are friendly enough but the place could use some maintenance.',
                       "Three stars because it's convenient, not because it's great.",
                       'Works fine most of the time, but the app is annoying.',
                       "Pretty average tunnel wash, about what you'd expect for the price."],
             'long_good': ['Moved to Portland from Georgia last fall and had no idea what road salt does to a car. Coworker told me to get an '
                           "unlimited plan somewhere with an undercarriage wash, and I picked this one because it's on my way home. Best decision of "
                           'the winter. I went through probably three times a week from December to March and the bottom of my car still looks '
                           'clean. The free vacuums are strong and I like the little air hose for the vents. Only gripe is the line after a storm, '
                           'which can get long, but it moves.',
                           "I'm kind of picky about my car's paint so I was hesitant to use a tunnel wash at all. Tried it once with the top package "
                           'and checked the paint with a flashlight at home, no new swirls that I could see. The spot free rinse works well on my '
                           'black car, which is the real test. Joined the monthly plan after that. The guy at the entrance always sprays down the '
                           "front for bugs which makes a big difference in summer. Wish they had a towel dry option but that's not really what this "
                           'place is.',
                           'we have two kids and a dog and my minivan is basically a crime scene most of the time. the vacuums here are free and '
                           'actually powerful enough to pull dog hair out of the carpet, which is honestly the main reason we come. kids love '
                           'watching the colored foam go by. the monthly plan for two cars is a decent deal. one time a vacuum was broken and an '
                           'employee came over and moved me to another spot without me asking. the mat washer is great too. no complaints except '
                           "it's busy sunday mornings",
                           'Took my truck in after a weekend at a muddy camp up north and I honestly thought it might be too much for an automated '
                           'wash. Came out clean, even the wheel wells mostly. Paid for the mid tier package and they let me use the mat washer too. '
                           'The attendant was friendly and asked if I had anything on the roof rack before I went in. I knocked a star in my head '
                           'because the tailgate still had a bit of dried mud, but they ran me through again for free when I mentioned it. Five '
                           'stars for that alone.',
                           'Been a member here for two years now. The wash is consistent, the place is clean, and the people working are always '
                           "nice. Last winter my card on file expired and I didn't realize, so the gate wouldn't open. Instead of making me pay, the "
                           'attendant just took my new card at the window and updated it for me. Small thing but it stuck with me. The vacuums got '
                           "upgraded this year and they're even better. Wish they were open a bit later on Sundays, otherwise no complaints at all.",
                           "Honest review from someone who used to only hand wash. I don't have time anymore with a new job and a long commute on "
                           '295, so I tried this place. The ceramic package is genuinely noticeable, rain beads right off my windshield for about '
                           'two weeks. The tunnel takes maybe four minutes. Vacuums are free and there are tons of spots. I still do a proper wash '
                           'at home every couple of months, but for weekly upkeep this is perfect. Plate reader recognizes me every time which makes '
                           'it painless.',
                           'My dad is 79 and was nervous about driving into a car wash tunnel because he had a bad experience years ago somewhere '
                           'else. I went with him the first time. The attendant was so patient, walked over to his window, explained the steps, and '
                           'guided him on carefully. He came out grinning and now he goes by himself every Friday. They even helped him set up the '
                           "plate reader so he doesn't have to fumble with a card. It's nice when a business treats older customers like this.",
                           'Pollen season in Maine turns my white car yellow-green and this place gets it all off in one pass. I signed up for the '
                           'plan in April and have used it like 20 times since. The pre-soak and the triple foam actually seem to do something. Love '
                           'that the vacuums have both a crevice tool and a wide head. One star off for the time the app double charged me, but '
                           "customer service fixed it in a day once I emailed, so I'll round up to 5."],
             'long_bad': ['Went through the top package and the brushes caught my side mirror and tore it right off the housing. The attendant saw '
                          'it happen and told me to fill out a damage claim. Two weeks later they denied it, saying the mirror must have been loose '
                          "already. It wasn't. Now I'm paying $300 out of pocket. The wash wasn't even good, there was still dirt on the back "
                          'window. Never again.',
                          "Signed up for the monthly plan and tried to cancel when I moved out of state. The app wouldn't let me, the website sent "
                          'me in circles, and nobody at the location could help. Got charged for three more months before my bank finally blocked '
                          "it. I'm sure the wash is fine for some people but the way they handle memberships feels like a trap. Read the fine print "
                          'before you sign up.',
                          'The vacuums have been broken for weeks. Out of maybe ten stations only two worked and there was a line for those. Trash '
                          'cans were overflowing and blowing around the lot. The wash itself left my car spotty and still wet because the dryers '
                          'were barely running. I asked an employee about it and he just shrugged. Used to be a decent place, not anymore.',
                          'Took my new car through for the first time and came out with fine scratches all down the driver side. Clearly from dirty '
                          "brushes. Manager said they can't be responsible for paint since it's an automated wash, and pointed at a sign. Really "
                          'disappointing. I had read good reviews so I trusted it. Stick to touchless or hand washes if you care about your paint.',
                          'Waited 45 minutes in a line that went out onto the road after a snowstorm. Only one lane was open even though there were '
                          'three. When I finally got through, my car still had salt all over the lower doors even with the undercarriage package. '
                          "The plate reader didn't recognize my membership so I had to wait for someone to come out. Frustrating all around."]},
 'coffee': {'dishes': ['House Drip',
                       'Cold Brew',
                       'Maple Oat Latte',
                       'Cortado',
                       'Single Origin Pour Over',
                       'Cardamom Morning Bun',
                       'Blueberry Scone',
                       'Almond Croissant',
                       'Breakfast Sandwich on Brioche',
                       'Whoopie Pie'],
            'short_good': ['best cold brew in portland',
                           'Great beans, friendly baristas.',
                           'That morning bun though!!',
                           'My daily stop on Munjoy Hill.',
                           'Smells amazing in here.',
                           'Perfect cortado every time.',
                           'love the maple oat latte',
                           'Great spot to work.',
                           'Bought a bag, loved it.',
                           'Cozy and never too loud.',
                           'Pour over was fantastic.',
                           'Fresh pastries, strong coffee.',
                           'Worth the line.',
                           'Almond croissant is the move.',
                           'friendly folks, great espresso',
                           "Best scone I've had.",
                           'Dog friendly patio!',
                           'Coffee nerd approved.',
                           'Quick service, good vibes.',
                           'Fresh roasted, you can taste it.',
                           'So good I bought beans.',
                           'Lovely little roastery.',
                           'great latte art lol',
                           'Morning ritual, every day.',
                           'Super smooth drip coffee.',
                           'Excellent decaf, actually!',
                           'Chill spot, solid wifi.',
                           'Breakfast sandwich was perfect.',
                           "Can't beat their house blend.",
                           'Five stars for the cardamom bun.'],
            'short_bad': ['Burnt tasting espresso.',
                          '$7 for a small latte??',
                          'Waited 20 minutes for drip.',
                          'pastries were stale',
                          'Snobby baristas, mediocre coffee.',
                          'Wrong order, twice.',
                          'No seating, always packed.',
                          'Laptop people hog every table.',
                          'Cold brew tasted watered down.',
                          'Rude when I asked for sugar.',
                          'Wifi never works here.',
                          'Overpriced and overhyped.'],
            'good': ['You can see the roaster going in the back and the whole place smells like fresh beans.',
                     'The cold brew is smooth and chocolatey without that sour edge a lot of places have.',
                     'Their cardamom morning bun is sticky and flaky and sells out by ten on weekends.',
                     'The barista took the time to explain the difference between the two single origins on pour over.',
                     'My maple oat latte was sweet but not syrupy, with real Maine maple instead of flavored syrup.',
                     'There are plenty of outlets along the window bar so I can actually get work done here.',
                     'They let me sample a couple of beans before I bought a bag to take home.',
                     'The bags of coffee have the roast date printed right on them, usually within the last few days.',
                     'Even with a line out the door at 8am I had my drink in under five minutes.',
                     'My cortado was perfectly balanced and came in a little glass that felt very old school.',
                     "They have oat, almond, and soy and don't charge extra for any of them.",
                     'The almond croissant is filled to the edges and dusted with way too much powdered sugar in a good way.',
                     'I brought my dog and they had a water bowl outside and a biscuit for him.',
                     'The blueberry scone is tender and full of wild Maine blueberries, not the giant grocery store kind.',
                     'Decaf here actually tastes like coffee, which is rare and very appreciated.',
                     'The breakfast sandwich on brioche with a soft egg and cheddar is my Saturday treat.',
                     'Music is low enough that you can have a conversation or take a call.',
                     'They do a free coffee after nine punches on their card, which adds up fast if you come daily.',
                     'On a sunny day the patio is the best place on the Hill to sit and people watch.',
                     'The staff remember my order after only a couple of weeks of coming in.',
                     'Their house blend is a great everyday bean for my drip machine at home.',
                     'They grind my beans for my specific brewer if I ask, no attitude about it.',
                     'The whoopie pies are huge and the filling is light rather than greasy.',
                     'I like that they use real mugs for anyone staying in rather than paper cups.',
                     'They had a little tasting flight of espresso one Saturday and it was a fun way to learn.',
                     "My iced latte was strong enough that the ice didn't drown it.",
                     'Seating is limited but people seem good about sharing tables when it gets busy.',
                     'They sell their beans in a refill tin program that saves me a bit and cuts down on bags.',
                     'The pour over takes a few minutes but you can tell they care about getting it right.',
                     'Their chai is spicy and made in house, not from a box concentrate.',
                     'The cafe is bright and cheerful even on gray February days.',
                     'They opened at 6:30 which is perfect before my early shift at the hospital.',
                     "My kids love the hot chocolate and they make a little kid size that's not scalding.",
                     'The order app works well and my drink is always ready when I walk in.',
                     'The light roast Ethiopian tasted like blueberries and jasmine, just like the bag said.',
                     "There's a shelf of local zines and flyers by the door that I always browse while waiting.",
                     'They donate leftover pastries to a local shelter at the end of the day, which I love.',
                     'Espresso shots are pulled fresh for each drink, not left sitting under the machine.',
                     'I mentioned I was new to the neighborhood and the barista gave me a list of places to check out.',
                     'The banana bread is moist and they toast it with a little salted butter if you ask.',
                     "Bathroom is clean and there's a changing table, which as a parent I always notice.",
                     'They roast a seasonal holiday blend every winter that I buy as gifts every year.',
                     "Prices are fair for the quality, about what you'd pay at the chains for way better coffee.",
                     'The Americano was rich and full without any bitterness at all.',
                     'Big windows face the water so you can see the ferries heading out while you sip.'],
            'bad': ['My latte tasted burnt and bitter like the milk had been steamed way too hot.',
                    'I waited almost twenty minutes for a simple drip coffee while they made fancy pour overs for others.',
                    'The scone I bought was dry and clearly from the day before.',
                    'The barista rolled her eyes when I asked what a cortado was.',
                    "Every table was taken by people on laptops who looked like they'd been there for hours.",
                    'They got my order wrong two days in a row and I had to wait again both times.',
                    'Seven dollars for a twelve ounce latte is a lot even for Portland.',
                    'The cold brew was weak and tasted like it had been watered down.',
                    'The wifi password is posted but the connection kept dropping.',
                    'There was no milk or sugar station so I had to ask for half and half like it was a big deal.',
                    'My almond croissant was soggy in the middle.',
                    "The music was so loud I couldn't hear my friend across the table.",
                    'The floors were sticky and the trash by the door was overflowing.',
                    'They ran out of oat milk by 9am on a Tuesday.',
                    'The breakfast sandwich took twenty-five minutes and came out lukewarm.',
                    'The bag of beans I bought was roasted almost a month earlier.',
                    'Staff were chatting with each other behind the counter while the line kept growing.',
                    'My iced coffee was mostly ice, maybe a few sips of actual coffee.',
                    'The chairs are hard metal and uncomfortable to sit in for more than ten minutes.',
                    'They charge a dollar extra for an extra shot which feels steep.',
                    'The pour over came out lukewarm by the time they handed it to me.',
                    "My mobile order wasn't started until I showed up and asked about it.",
                    "There's no restroom for customers which is rough after a large coffee.",
                    'They switched to compostable lids that fall apart and dripped all over my car.',
                    'The espresso was sour and thin, like the grinder needed adjusting.',
                    'The barista acted annoyed when I paid with cash.',
                    'The morning bun was more like a regular roll with a little sugar on top.',
                    'The patio tables were dirty and covered in crumbs and bird droppings.',
                    'Line management is a mess with people crowding the pickup counter.',
                    "They gave me regular milk instead of oat after I specifically asked, and I'm lactose intolerant."],
            'mixed': ["The coffee is good but the pastries didn't do much for me.",
                      'Nice place, just always too crowded to get a seat.',
                      'Solid espresso, though pretty pricey for what it is.',
                      'Pretty good latte, but the service gets slow on weekends.',
                      'Good beans to take home, the cafe itself is just okay.',
                      'The cold brew is great but the hot drinks are a bit inconsistent.',
                      "It's fine, I don't get the hype but it's not bad.",
                      'Friendly staff, though my drink came out lukewarm.',
                      'Decent spot, could use more seating and better wifi.',
                      'Three stars, the morning bun was great but the coffee was too acidic for me.'],
            'long_good': ["I've lived on Munjoy Hill for six years and this has become my morning routine. I walk the dog around the Eastern Prom "
                          'and stop here on the way back. They know me by my order (maple oat latte, extra hot) and my dog by name. The coffee is '
                          "roasted right in the back and you can smell it from the street. My only complaint is the seating, there's never a table "
                          'after 8 on weekends, so I usually take it to go. Still my favorite cafe in the city by a mile.',
                          'Visiting Portland for a long weekend and this was the first stop on our list. We each got a different drink so we could '
                          "try more. The single origin pour over was bright and fruity, my husband's cortado was really balanced, and the cardamom "
                          'morning bun was honestly the best pastry I had the whole trip. The barista spent a few minutes telling us about where '
                          'they source their beans. We bought two bags to bring home to Pennsylvania. Wish we had a place like this at home.',
                          'i work remotely and rotate between a few cafes in town. this one has the best coffee hands down. good outlets along the '
                          'window, wifi is decent, and nobody gives you a look if you camp for a couple hours as long as you keep ordering. the '
                          'breakfast sandwich on brioche is filling enough to be lunch. it does get loud around noon so i bring headphones. bought '
                          "their house blend for home and it's way better than the supermarket stuff",
                          "My partner proposed to me on the patio here (he said it was because it's where we had our first date, which is true). The "
                          'staff were in on it and had our usual drinks ready with a little heart in the foam. They even brought out a whoopie pie '
                          "with a candle. It's a small thing but they made it feel really special. Coffee aside, which is excellent btw, the people "
                          'here are wonderful. Only gripe is the patio chairs are a bit wobbly, almost knocked mine over in the excitement!',
                          "I'm a bit of a coffee snob and most places in Portland either over roast or under extract. Tidewater gets it right. Their "
                          'espresso is sweet and syrupy with no bitterness, and the light roasts actually taste like what the bag says. I asked the '
                          'roaster about their profiles one afternoon and he was happy to nerd out with me. The beans are fresh, usually roasted '
                          'within the week. Pricey compared to grocery coffee but you get what you pay for. Their decaf is legit too.',
                          'Stopped in on a freezing January morning after the ferry back from Peaks. The place was warm and smelled amazing. I '
                          'ordered a chai and a blueberry scone and sat by the window for an hour watching the snow. The chai was spicy and clearly '
                          'made in house. The scone had real wild blueberries. The barista was super friendly even though it was obviously a slow '
                          "day. Small thing: there was only one bathroom and a bit of a wait, but that's not a big deal.",
                          "Took my mom here for Mother's Day brunch since she loves pastries. We got the almond croissant, banana bread toasted with "
                          'butter, and the morning bun to share. All three were excellent but the morning bun was the clear winner. My mom said the '
                          'latte was better than the ones she gets in Boston. It was busy but the line moved fast. The staff even helped carry our '
                          'tray to the table since I had my hands full with a stroller. Lovely morning.',
                          'Ordered a few pounds of their holiday blend as gifts last December and everyone loved them. This year I went into the '
                          'shop in person and finally tried the cafe. Got a cold brew even though it was October because people rave about it and '
                          "yes, it's smooth and chocolatey. The staff gave me a little sample of their new Colombian too. I'd give six stars if I "
                          'could, only nitpick is the parking out front is basically nonexistent so plan to walk a bit.'],
            'long_bad': ["Used to love this place but it's gone downhill. My latte this morning tasted burnt and the milk was scalded. When I "
                         "mentioned it, the barista said that's just how their espresso tastes and didn't offer to remake it. The scone was dry like "
                         'it was from yesterday. Seven dollars for a small latte and a stale pastry is not worth it. There are other good roasters '
                         "in Portland now, I'll go there.",
                         'Waited 25 minutes for a breakfast sandwich and a drip coffee. Nobody told us there would be a wait. Meanwhile the staff '
                         'were chatting and laughing behind the counter. When the sandwich finally came out it was lukewarm and the egg was rubbery. '
                         'Every table was taken by laptop people so we ate standing. Coffee was fine but not worth that experience.',
                         "I asked for oat milk because I'm lactose intolerant and they gave me regular milk. I didn't realize until I was already "
                         'sick. When I went back to tell them, the person at the counter was dismissive and just said sorry, mistakes happen. No '
                         'offer to refund or anything. Please be careful here if you have dietary restrictions.',
                         "The coffee is good, I'll admit that. But the attitude from some of the staff is ridiculous. I asked a simple question "
                         "about the difference between two beans and got an eye roll and a lecture. I just wanted a recommendation. Also there's "
                         "nowhere to sit, and the bathroom was closed for cleaning both times I've been. Overhyped.",
                         'Bought a bag of their beans as a gift and when I got home noticed the roast date was over three weeks old. For a place '
                         "that brags about roasting on site that's pretty bad. The coffee tasted flat. I went back to exchange it and they said they "
                         "can't take back opened bags. I hadn't opened it, just checked the date. Annoying."]},
 'books': {'short_good': ['Could spend hours in here.',
                          'best used section in town',
                          'Great staff picks shelf.',
                          'Cozy, quiet, and well curated.',
                          'Found three books I needed.',
                          'Lovely kids corner!',
                          'They special ordered it fast.',
                          'My favorite shop on Exchange St.',
                          'Fair prices on used books.',
                          'Friendly, helpful booksellers.',
                          'love the shop cat',
                          'Great poetry selection.',
                          'Real independent bookstore vibes.',
                          'Always leave with something.',
                          'Perfect rainy day stop.',
                          'Took my trade-ins, fair credit.',
                          'They gift wrap for free!',
                          'Great author events.',
                          'Wonderful Maine history shelf.',
                          'Best bookstore in Portland.',
                          'Excellent recommendations every time.',
                          'Smells like old books. Perfect.',
                          'kids storytime is great',
                          'Nice mix of new and used.',
                          'Small but so well chosen.',
                          'Support this place!',
                          'Rare finds in the back room.',
                          'Got a signed copy here!',
                          'Helpful even on busy days.',
                          'my happy place honestly'],
           'short_bad': ['Prices higher than online.',
                         'Staff ignored me completely.',
                         'Special order never arrived.',
                         'Lowball offer on my trade-ins.',
                         'too cramped to browse',
                         'Musty smell, dusty shelves.',
                         'Closed during posted hours.',
                         'Rude about my returns.',
                         'Tiny selection, nothing in stock.',
                         'Used books overpriced.',
                         'Owner was condescending.',
                         'No sci-fi section at all?'],
           'good': ["The handwritten staff picks cards are how I've found half my favorite books in the last few years.",
                    'Their used section in the back is huge and organized better than most libraries.',
                    'I special ordered an out of print cookbook and they had it for me within a week.',
                    'The kids corner has little chairs and a rug and my daughter refuses to leave it.',
                    'They gave me fair store credit for two boxes of books I was clearing out of my apartment.',
                    "The bookseller asked what I'd liked recently and came back with three spot on suggestions.",
                    "They have a whole shelf of Maine authors and local history I haven't seen anywhere else.",
                    'Gift wrapping is free and they do it with brown paper and twine which looks great.',
                    'The shop cat sleeps in the window and is very tolerant of being petted.',
                    'Prices on used paperbacks are really reasonable, most around five or six dollars.',
                    'They host author readings in the evenings and the last one I went to was packed and fun.',
                    "There's a cozy armchair by the poetry section where nobody minds if you read for a while.",
                    "I found a first edition of a book I've been hunting for years in their glass case.",
                    'Their Saturday morning storytime keeps my two kids entertained for a whole hour.',
                    "The staff are happy to call around to other stores if they don't have what you need.",
                    'Their newsletter has great recommendations and lists upcoming events.',
                    'I love that new and used copies are shelved together so you can choose which to buy.',
                    'They have a small but excellent selection of translated fiction, which is hard to find.',
                    'The graphic novel section is better than the dedicated comic shop I used to go to.',
                    'They had the new release I wanted on release day and held a copy for me.',
                    'The store is warm and smells like old paper, which is exactly what you want on a cold day.',
                    'Their book club picks are on a table up front with a discount for members.',
                    'I ordered online for in store pickup and it was ready and bagged the next afternoon.',
                    'The bookseller wrapped my purchase in a little paper bag with a free bookmark inside.',
                    'They carry nice journals and cards near the register for last minute gifts.',
                    "I sold them a box of old textbooks they couldn't use and they still pointed me to a donation spot.",
                    'Their rare books room in the back is like a little museum, and they let you browse.',
                    'Kids picture books are arranged face out so little ones can pick by the covers.',
                    "The person at the counter recognized me and asked how I liked the novel she'd recommended.",
                    'Their cookbook section has a lot of New England and seafood books that make great souvenirs.',
                    'They have a buy two used get one free shelf outside on nice days.',
                    'Their membership card gives ten percent off which adds up quickly for heavy readers.',
                    "I've never had them try to push a bestseller on me, the suggestions always feel personal.",
                    'The nautical and boating section is a treat for anyone who loves the water like I do.',
                    'They took my phone number when a used copy of a series I collect came in and called me.',
                    "There's a box of free books on the stoop that I check every time I walk by.",
                    'Their mystery section is enormous and well organized by author.',
                    "The store is easy to browse with a stroller, which isn't true of many shops in the Old Port.",
                    'They let my son pay for his own book with his allowance coins and were very sweet about it.',
                    'Their Little Free Library collaboration downtown is a great community touch.',
                    'The bookseller helped me find a gift for a picky teen and she loved it.',
                    'They have a big selection of Maine trail guides and maps right by the door.',
                    'I found an old local photo book of Portland in the 1950s that my dad loved.',
                    'The stairs to the basement level are steep but the used fiction down there is worth it.',
                    "They stock a lot of small press titles that you won't see at the big chains."],
           'bad': ["New books here cost a good bit more than what you'd pay online.",
                   'I stood at the register for five minutes while two employees talked to each other.',
                   'My special order took six weeks and they never called when it arrived.',
                   'They offered me twelve dollars for a box of almost new hardcovers.',
                   "The aisles are so narrow you can't browse if more than two people are in a row.",
                   'The used section in the basement smells musty and the shelves are dusty.',
                   'The sign said open until six but the door was locked at 5:30.',
                   "They wouldn't take back a gift I had a receipt for because it was past fourteen days.",
                   "The selection of new releases is tiny and they didn't have any of what I was looking for.",
                   'Some of the used books are priced higher than a new copy would be.',
                   'The owner was condescending when I asked if they had any romance novels.',
                   'Their sci-fi and fantasy shelves are barely a single bookcase.',
                   "The used books I bought had pages falling out and they didn't mention it.",
                   "They don't take credit cards for purchases under ten dollars.",
                   "The website said the book was in stock but when I got there they couldn't find it.",
                   'Kids section was a mess with books all over the floor.',
                   "The author event was so crowded that I couldn't hear anything from the back.",
                   "They have a cat in the store which isn't posted anywhere and I'm very allergic.",
                   'The shelving is so disorganized that I found three mysteries in the cookbook section.',
                   'I called twice to ask about a title and nobody picked up during business hours.',
                   'The person at the counter made a snide comment about my book choice.',
                   "There's no restroom available for customers even during a long event.",
                   'The store is freezing in winter because the door is propped open.',
                   'They put a sticker on the cover of a gift book that tore the jacket when I peeled it off.',
                   'They lost the book I had on hold and sold it to someone else.',
                   "It's a steep, narrow staircase down to the used books which isn't accessible at all.",
                   "The membership discount doesn't apply to used books, which nobody told me when I signed up.",
                   "Prices on the rare books seem wildly inflated compared to what I've seen elsewhere.",
                   'I waited in line for a signed copy and they ran out before I got to the front.',
                   'They gave me the wrong change and argued with me about it.'],
           'mixed': ["Nice little shop but the new books are pricier than I'd like.",
                     'Good used section, small selection of new releases.',
                     "Staff are friendly but it's hard to move around when it's busy.",
                     "I like the atmosphere, but I rarely find what I'm looking for.",
                     'Decent store, a bit cramped and dusty in the back.',
                     'Their trade-in offers are low but the store credit is handy.',
                     'Fine for browsing, I usually end up ordering elsewhere though.',
                     'Charming place, though the hours are kind of unpredictable.',
                     'Three stars, good poetry and local stuff, weak on everything else.',
                     'Pleasant enough, nothing that really stood out to me.'],
           'long_good': ["I'm a retired English teacher and have been in a lot of bookshops. This one is special. The staff actually read, and the "
                         'handwritten recommendation cards are thoughtful instead of just copy from the publisher. I spent two hours in the used '
                         'section downstairs and left with eight books for under fifty dollars. The only drawback is the basement stairs, which are '
                         "a bit steep for my knees. But I'll keep coming back. It's the kind of shop that makes a city feel like a real place.",
                         'We visit Portland every summer and this is a must stop for our family. My kids (7 and 10) each get to pick out a book as '
                         'their vacation souvenir. The kids section is set up so well, with little chairs and books facing out. This year my son '
                         "found a graphic novel series he's now obsessed with, and the bookseller recommended the next three in the series. They "
                         'even wrote down titles for us to look for at our library back home. Only small thing, it gets crowded on rainy days when '
                         'everyone in the Old Port ducks in.',
                         'Moved to Portland in the fall and was missing my old neighborhood bookstore in Chicago. Found this place on a walk and '
                         "immediately felt at home. The selection is smaller than the big stores, but it's so well chosen that I always find "
                         "something. I've traded in two boxes of books from the move and got enough credit to keep me going for months. The "
                         'booksellers are friendly and have great taste. Signed up for their newsletter and now go to the author nights too. Already '
                         'met a couple of friends there.',
                         "Ordered a pretty obscure book on Maine shipbuilding for my dad's 70th. I figured it would take forever, but they tracked "
                         'down a used copy from a dealer in Bath and had it in five days. They called me when it came in and wrapped it with brown '
                         'paper and twine. My dad, who is very hard to shop for, teared up a bit when he opened it. The price was a little higher '
                         "than I'd hoped, but honestly worth it for the service.",
                         'rainy sunday, no plans, wandered in and lost an entire afternoon. the used section in back is really deep, i found a bunch '
                         'of old penguin classics and a weird 70s cookbook. the shop cat followed me around for a while which was adorable. the '
                         'person at the register chatted with me about one of the books i bought and gave me a couple more suggestions. only '
                         'complaint is they could use a couple more chairs. otherwise perfect',
                         "I host a small book club and we've started buying our picks here instead of online. They give our group a discount and set "
                         'aside copies for us so we can pick them up whenever. Last month one of the booksellers even came to our meeting to talk '
                         'about the book, which was a really fun surprise. Prices are a bit higher than Amazon, but supporting a local store matters '
                         'to us and the personal touch is worth it.',
                         "Came in looking for a gift for my teenage niece who is a really picky reader. I explained what she'd liked and disliked, "
                         'and the bookseller spent like 15 minutes pulling options and telling me about each one. I left with two books she ended up '
                         'loving. They also gift wrapped them for free. The store itself is charming, with creaky floors and stacks everywhere. A '
                         "bit hard to navigate with a crowd but that's part of the charm.",
                         'I collect old nautical books and the back room here has some real finds. Last visit I picked up an early 1900s pilot guide '
                         "to the Maine coast in great condition. The owner knew a lot about it and showed me a couple of other things he'd been "
                         'saving. Prices in the rare room are fair compared to what I see online. One star off in my head because the room is only '
                         "open certain hours, but I'm rounding up because it's a treasure."],
           'long_bad': ['Brought in two boxes of books in great condition, mostly recent hardcovers. The person who looked through them was '
                        "dismissive and offered me $15 in cash or $25 in credit for the whole lot. I've sold books elsewhere and gotten much better "
                        'offers. When I asked about the low price she said they have too much stock. Fine, but then why take any? Felt like a waste '
                        'of time.',
                        'Special ordered a book in March and was told it would take a week. After three weeks I called and nobody knew anything '
                        "about it. They said they'd look into it and call back, and never did. When I went in person, they found the order had never "
                        "been placed. The staff apologized but didn't offer anything. I ended up buying it online.",
                        "The store is charming from the outside but inside it's cramped, dusty and smells musty, especially in the basement. I'm "
                        "allergic to cats and nothing on the door says there's a cat in the store, which I found out the hard way. Staff were busy "
                        "talking and didn't acknowledge me. Left without buying anything.",
                        'I asked an employee for help finding a romance novel and got a long sigh and a comment about how they focus on literary '
                        "fiction. Very condescending. I'm an adult who can read what I want. The selection was tiny anyway and the prices on new "
                        "books were higher than everywhere else. Won't be back.",
                        'Tried to return a book I got as a gift (with a gift receipt) and they refused because it was past 14 days. It was a '
                        "duplicate gift and still had the receipt. They wouldn't even give store credit. I understand small shops have tight "
                        'margins, but this policy is going to cost them more customers than it saves.']}}
