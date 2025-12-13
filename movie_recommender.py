import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import textwrap
import random

# ==========================================
# PART 1: DATABASE (120+ MOVIES)
# ==========================================
MOVIE_DB = [
    {"id": 1, "title": "Avatar", "year": 2009, "rating": 7.8, "cert": "PG-13", "genre": "Action Adventure Sci-Fi", "director": "James Cameron", "plot": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home."},
    {"id": 2, "title": "The Avengers", "year": 2012, "rating": 8.0, "cert": "PG-13", "genre": "Action Adventure Sci-Fi", "director": "Joss Whedon", "plot": "Earth's mightiest heroes must come together and learn to fight as a team if they are to stop the mischievous Loki and his alien army from enslaving humanity."},
    {"id": 3, "title": "The Godfather", "year": 1972, "rating": 9.2, "cert": "R", "genre": "Crime Drama", "director": "Francis Ford Coppola", "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
    {"id": 4, "title": "Inception", "year": 2010, "rating": 8.8, "cert": "PG-13", "genre": "Action Adventure Sci-Fi", "director": "Christopher Nolan", "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."},
    {"id": 5, "title": "Pulp Fiction", "year": 1994, "rating": 8.9, "cert": "R", "genre": "Crime Drama", "director": "Quentin Tarantino", "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."},
    {"id": 6, "title": "The Dark Knight", "year": 2008, "rating": 9.0, "cert": "PG-13", "genre": "Action Crime Drama", "director": "Christopher Nolan", "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."},
    {"id": 7, "title": "Interstellar", "year": 2014, "rating": 8.6, "cert": "PG-13", "genre": "Adventure Drama Sci-Fi", "director": "Christopher Nolan", "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
    {"id": 8, "title": "Fight Club", "year": 1999, "rating": 8.8, "cert": "R", "genre": "Drama", "director": "David Fincher", "plot": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more."},
    {"id": 9, "title": "Forrest Gump", "year": 1994, "rating": 8.8, "cert": "PG-13", "genre": "Drama Romance", "director": "Robert Zemeckis", "plot": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate and other historical events unfold through the perspective of an Alabama man with an IQ of 75."},
    {"id": 10, "title": "The Matrix", "year": 1999, "rating": 8.7, "cert": "R", "genre": "Action Sci-Fi", "director": "Lana Wachowski", "plot": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."},
    {"id": 11, "title": "Goodfellas", "year": 1990, "rating": 8.7, "cert": "R", "genre": "Biography Crime Drama", "director": "Martin Scorsese", "plot": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito."},
    {"id": 12, "title": "Star Wars: A New Hope", "year": 1977, "rating": 8.6, "cert": "PG", "genre": "Action Adventure Fantasy", "director": "George Lucas", "plot": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station."},
    {"id": 13, "title": "Parasite", "year": 2019, "rating": 8.6, "cert": "R", "genre": "Comedy Drama Thriller", "director": "Bong Joon Ho", "plot": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."},
    {"id": 14, "title": "The Lion King", "year": 1994, "rating": 8.5, "cert": "G", "genre": "Animation Adventure Drama", "director": "Roger Allers", "plot": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."},
    {"id": 15, "title": "Titanic", "year": 1997, "rating": 7.8, "cert": "PG-13", "genre": "Drama Romance", "director": "James Cameron", "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."},
    {"id": 16, "title": "Gladiator", "year": 2000, "rating": 8.5, "cert": "R", "genre": "Action Adventure Drama", "director": "Ridley Scott", "plot": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery."},
    {"id": 17, "title": "Jurassic Park", "year": 1993, "rating": 8.1, "cert": "PG-13", "genre": "Action Adventure Sci-Fi", "director": "Steven Spielberg", "plot": "A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the cloned dinosaurs to run loose."},
    {"id": 18, "title": "The Silence of the Lambs", "year": 1991, "rating": 8.6, "cert": "R", "genre": "Crime Drama Thriller", "director": "Jonathan Demme", "plot": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."},
    {"id": 19, "title": "Coco", "year": 2017, "rating": 8.4, "cert": "G", "genre": "Animation Adventure Family", "director": "Lee Unkrich", "plot": "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer."},
    {"id": 20, "title": "Whiplash", "year": 2014, "rating": 8.5, "cert": "R", "genre": "Drama Music", "director": "Damien Chazelle", "plot": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential."},
    {"id": 21, "title": "Spider-Man: Into the Spider-Verse", "year": 2018, "rating": 8.4, "cert": "PG", "genre": "Animation Action Adventure", "director": "Bob Persichetti", "plot": "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities."},
    {"id": 22, "title": "Back to the Future", "year": 1985, "rating": 8.5, "cert": "PG", "genre": "Adventure Comedy Sci-Fi", "director": "Robert Zemeckis", "plot": "Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean invented by his close friend, the eccentric scientist Doc Brown."},
    {"id": 23, "title": "The Shining", "year": 1980, "rating": 8.4, "cert": "R", "genre": "Drama Horror", "director": "Stanley Kubrick", "plot": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from the past and future."},
    {"id": 24, "title": "Alien", "year": 1979, "rating": 8.4, "cert": "R", "genre": "Horror Sci-Fi", "director": "Ridley Scott", "plot": "After a space merchant vessel receives an unknown transmission as a distress call, one of the crew is attacked by a mysterious life form and they soon realize that its life cycle has merely begun."},
    {"id": 25, "title": "Toy Story", "year": 1995, "rating": 8.3, "cert": "G", "genre": "Animation Adventure Comedy", "director": "John Lasseter", "plot": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room."},
    {"id": 26, "title": "The Shawshank Redemption", "year": 1994, "rating": 9.3, "cert": "R", "genre": "Drama", "director": "Frank Darabont", "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
    {"id": 27, "title": "Schindler's List", "year": 1993, "rating": 8.9, "cert": "R", "genre": "Biography Drama History", "director": "Steven Spielberg", "plot": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis."},
    {"id": 28, "title": "Lord of the Rings: Return of the King", "year": 2003, "rating": 8.9, "cert": "PG-13", "genre": "Action Adventure Drama", "director": "Peter Jackson", "plot": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring."},
    {"id": 29, "title": "Spirited Away", "year": 2001, "rating": 8.6, "cert": "PG", "genre": "Animation Adventure Family", "director": "Hayao Miyazaki", "plot": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts."},
    {"id": 30, "title": "Saving Private Ryan", "year": 1998, "rating": 8.6, "cert": "R", "genre": "Drama War", "director": "Steven Spielberg", "plot": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action."},
    {"id": 31, "title": "The Green Mile", "year": 1999, "rating": 8.6, "cert": "R", "genre": "Crime Drama Fantasy", "director": "Frank Darabont", "plot": "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift."},
    {"id": 32, "title": "Terminator 2: Judgment Day", "year": 1991, "rating": 8.5, "cert": "R", "genre": "Action Sci-Fi", "director": "James Cameron", "plot": "A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son, John, from a more advanced and powerful cyborg."},
    {"id": 33, "title": "Se7en", "year": 1995, "rating": 8.6, "cert": "R", "genre": "Crime Drama Mystery", "director": "David Fincher", "plot": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives."},
    {"id": 34, "title": "The Pianist", "year": 2002, "rating": 8.5, "cert": "R", "genre": "Biography Drama Music", "director": "Roman Polanski", "plot": "A Polish Jewish radio station pianist struggles to survive the destruction of the Warsaw ghetto of World War II."},
    {"id": 35, "title": "Psycho", "year": 1960, "rating": 8.5, "cert": "R", "genre": "Horror Mystery Thriller", "director": "Alfred Hitchcock", "plot": "A Phoenix secretary embezzles $40,000 from her employer's client, goes on the run, and checks into a remote motel run by a young man under the domination of his mother."},
    {"id": 36, "title": "Casablanca", "year": 1942, "rating": 8.5, "cert": "PG", "genre": "Drama Romance War", "director": "Michael Curtiz", "plot": "A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover and her fugitive husband escape the Nazis in French Morocco."},
    {"id": 37, "title": "The Departed", "year": 2006, "rating": 8.5, "cert": "R", "genre": "Crime Drama Thriller", "director": "Martin Scorsese", "plot": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston."},
    {"id": 38, "title": "The Prestige", "year": 2006, "rating": 8.5, "cert": "PG-13", "genre": "Drama Mystery Sci-Fi", "director": "Christopher Nolan", "plot": "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other."},
    {"id": 39, "title": "Memento", "year": 2000, "rating": 8.4, "cert": "R", "genre": "Mystery Thriller", "director": "Christopher Nolan", "plot": "A man with short-term memory loss attempts to track down his wife's murderer."},
    {"id": 40, "title": "Apocalypse Now", "year": 1979, "rating": 8.4, "cert": "R", "genre": "Drama Mystery War", "director": "Francis Ford Coppola", "plot": "A U.S. Army officer serving in Vietnam is tasked with assassinating a renegade Special Forces Colonel who sees himself as a god."},
    {"id": 41, "title": "Joker", "year": 2019, "rating": 8.4, "cert": "R", "genre": "Crime Drama Thriller", "director": "Todd Phillips", "plot": "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime."},
    {"id": 42, "title": "Django Unchained", "year": 2012, "rating": 8.4, "cert": "R", "genre": "Drama Western", "director": "Quentin Tarantino", "plot": "With the help of a German bounty hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner."},
    {"id": 43, "title": "WALL·E", "year": 2008, "rating": 8.4, "cert": "G", "genre": "Animation Adventure Family", "director": "Andrew Stanton", "plot": "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind."},
    {"id": 44, "title": "Oldboy", "year": 2003, "rating": 8.4, "cert": "R", "genre": "Action Drama Mystery", "director": "Park Chan-wook", "plot": "After being kidnapped and imprisoned for fifteen years, Oh Dae-Su is released, only to find that he must find his captor in five days."},
    {"id": 45, "title": "Once Upon a Time in America", "year": 1984, "rating": 8.4, "cert": "R", "genre": "Crime Drama", "director": "Sergio Leone", "plot": "A former Prohibition-era Jewish gangster returns to the Lower East Side of Manhattan over thirty years later, where he must confront the ghosts and regrets of his old life."},
    {"id": 46, "title": "Your Name", "year": 2016, "rating": 8.4, "cert": "PG", "genre": "Animation Drama Fantasy", "director": "Makoto Shinkai", "plot": "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?"},
    {"id": 47, "title": "Avengers: Infinity War", "year": 2018, "rating": 8.4, "cert": "PG-13", "genre": "Action Adventure Sci-Fi", "director": "Anthony Russo", "plot": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe."},
    {"id": 48, "title": "Das Boot", "year": 1981, "rating": 8.3, "cert": "R", "genre": "Drama War", "director": "Wolfgang Petersen", "plot": "The claustrophobic world of a WWII German U-boat; boredom, filth and sheer terror."},
    {"id": 49, "title": "Amélie", "year": 2001, "rating": 8.3, "cert": "R", "genre": "Comedy Romance", "director": "Jean-Pierre Jeunet", "plot": "Amélie is an innocent and naive girl in Paris with her own sense of justice. She decides to help those around her and, along the way, discovers love."},
    {"id": 50, "title": "Toy Story 3", "year": 2010, "rating": 8.2, "cert": "G", "genre": "Animation Adventure Comedy", "director": "Lee Unkrich", "plot": "The toys are mistakenly delivered to a day-care center instead of the attic right before Andy leaves for college, and it's up to Woody to convince the other toys that they weren't abandoned."},
    {"id": 51, "title": "Inglourious Basterds", "year": 2009, "rating": 8.3, "cert": "R", "genre": "Adventure Drama War", "director": "Quentin Tarantino", "plot": "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans for the same."},
    {"id": 52, "title": "Good Will Hunting", "year": 1997, "rating": 8.3, "cert": "R", "genre": "Drama Romance", "director": "Gus Van Sant", "plot": "Will Hunting, a janitor at M.I.T., has a gift for mathematics, but needs help from a psychologist to find direction in his life."},
    {"id": 53, "title": "The Hunt", "year": 2012, "rating": 8.3, "cert": "R", "genre": "Drama", "director": "Thomas Vinterberg", "plot": "A teacher lives a lonely life, all the while struggling over his son's custody. His life slowly gets better as he finds love and receives good news from his son, but his new luck is about to be brutally shattered by an innocent little lie."},
    {"id": 54, "title": "Blade Runner 2049", "year": 2017, "rating": 8.0, "cert": "R", "genre": "Action Drama Sci-Fi", "director": "Denis Villeneuve", "plot": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years."},
    {"id": 55, "title": "Arrival", "year": 2016, "rating": 7.9, "cert": "PG-13", "genre": "Drama Sci-Fi", "director": "Denis Villeneuve", "plot": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world."},
    {"id": 56, "title": "Her", "year": 2013, "rating": 8.0, "cert": "R", "genre": "Drama Romance Sci-Fi", "director": "Spike Jonze", "plot": "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need."},
    {"id": 57, "title": "Ex Machina", "year": 2014, "rating": 7.7, "cert": "R", "genre": "Drama Sci-Fi Thriller", "director": "Alex Garland", "plot": "A young programmer is selected to participate in a ground-breaking experiment in synthetic intelligence by evaluating the human qualities of a highly advanced humanoid A.I."},
    {"id": 58, "title": "Mad Max: Fury Road", "year": 2015, "rating": 8.1, "cert": "R", "genre": "Action Adventure Sci-Fi", "director": "George Miller", "plot": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max."},
    {"id": 59, "title": "Knives Out", "year": 2019, "rating": 7.9, "cert": "PG-13", "genre": "Comedy Crime Drama", "director": "Rian Johnson", "plot": "A detective investigates the death of a patriarch of an eccentric, combative family."},
    {"id": 60, "title": "Grand Budapest Hotel", "year": 2014, "rating": 8.1, "cert": "R", "genre": "Adventure Comedy Crime", "director": "Wes Anderson", "plot": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge."},
    {"id": 61, "title": "Gone Girl", "year": 2014, "rating": 8.1, "cert": "R", "genre": "Drama Mystery Thriller", "director": "David Fincher", "plot": "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent."},
    {"id": 62, "title": "Dune", "year": 2021, "rating": 8.0, "cert": "PG-13", "genre": "Action Adventure Sci-Fi", "director": "Denis Villeneuve", "plot": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future."},
    {"id": 63, "title": "1917", "year": 2019, "rating": 8.3, "cert": "R", "genre": "Drama War", "director": "Sam Mendes", "plot": "April 6th, 1917. As a regiment assembles to wage war deep in enemy territory, two soldiers are assigned to race against time and deliver a message that will stop 1,600 men from walking straight into a deadly trap."},
    {"id": 64, "title": "Ford v Ferrari", "year": 2019, "rating": 8.1, "cert": "PG-13", "genre": "Action Biography Drama", "director": "James Mangold", "plot": "American car designer Carroll Shelby and driver Ken Miles battle corporate interference and the laws of physics to build a revolutionary race car for Ford in order to defeat Ferrari at the 24 Hours of Le Mans in 1966."},
    {"id": 65, "title": "Logan", "year": 2017, "rating": 8.1, "cert": "R", "genre": "Action Drama Sci-Fi", "director": "James Mangold", "plot": "In a future where mutants are nearly extinct, an elderly and weary Logan leads a quiet life. But when Laura, a mutant child pursued by scientists, comes to him for help, he must get her to safety."},
    {"id": 66, "title": "Spotlight", "year": 2015, "rating": 8.1, "cert": "R", "genre": "Biography Crime Drama", "director": "Tom McCarthy", "plot": "The true story of how the Boston Globe uncovered the massive scandal of child molestation and cover-up within the local Catholic Archdiocese."},
    {"id": 67, "title": "Prisoners", "year": 2013, "rating": 8.1, "cert": "R", "genre": "Crime Drama Mystery", "director": "Denis Villeneuve", "plot": "When Keller Dover's daughter and her friend go missing, he takes matters into his own hands as the police pursue multiple leads and the pressure mounts."},
    {"id": 68, "title": "12 Years a Slave", "year": 2013, "rating": 8.1, "cert": "R", "genre": "Biography Drama History", "director": "Steve McQueen", "plot": "In the antebellum United States, Solomon Northup, a free black man from upstate New York, is abducted and sold into slavery."},
    {"id": 69, "title": "Warrior", "year": 2011, "rating": 8.2, "cert": "PG-13", "genre": "Action Drama Sport", "director": "Gavin O'Connor", "plot": "The youngest son of an alcoholic former boxer returns home, where he's trained by his father for competition in a mixed martial arts tournament - a path that puts the fighter on a collision course with his estranged, older brother."},
    {"id": 70, "title": "V for Vendetta", "year": 2005, "rating": 8.1, "cert": "R", "genre": "Action Drama Sci-Fi", "director": "James McTeigue", "plot": "In a future British tyranny, a shadowy freedom fighter, known only by the alias of \"V\", plots to overthrow it with the help of a young woman."},
    {"id": 71, "title": "Howl's Moving Castle", "year": 2004, "rating": 8.2, "cert": "G", "genre": "Animation Adventure Family", "director": "Hayao Miyazaki", "plot": "When an unconfident young woman is cursed with an old body by a spiteful witch, her only chance of breaking the spell lies with a self-indulgent yet insecure young wizard and his companions in his legged, walking castle."},
    {"id": 72, "title": "A Beautiful Mind", "year": 2001, "rating": 8.2, "cert": "PG-13", "genre": "Biography Drama", "director": "Ron Howard", "plot": "After John Nash, a brilliant but asocial mathematician, accepts secret work in cryptography, his life takes a turn for the nightmarish as he grapples with paranoia."},
    {"id": 73, "title": "Catch Me If You Can", "year": 2002, "rating": 8.1, "cert": "PG-13", "genre": "Biography Crime Drama", "director": "Steven Spielberg", "plot": "Barely 21 yet, Frank is a skilled forger who has passed as a doctor, lawyer and pilot. FBI agent Carl becomes obsessed with tracking down the con man, who only revels in the pursuit."},
    {"id": 74, "title": "No Country for Old Men", "year": 2007, "rating": 8.1, "cert": "R", "genre": "Crime Drama Thriller", "director": "Ethan Coen", "plot": "Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and more than two million dollars in cash near the Rio Grande."},
    {"id": 75, "title": "Pan's Labyrinth", "year": 2006, "rating": 8.2, "cert": "R", "genre": "Drama Fantasy War", "director": "Guillermo del Toro", "plot": "In the Falangist Spain of 1944, the bookish young stepdaughter of a sadistic army officer escapes into an eerie but captivating fantasy world."},
    {"id": 76, "title": "There Will Be Blood", "year": 2007, "rating": 8.2, "cert": "R", "genre": "Drama", "director": "Paul Thomas Anderson", "plot": "A story of family, religion, hatred, oil and madness, focusing on a turn-of-the-century prospector in the early days of the business."},
    {"id": 77, "title": "The Truman Show", "year": 1998, "rating": 8.1, "cert": "PG", "genre": "Comedy Drama", "director": "Peter Weir", "plot": "An insurance salesman discovers his whole life is actually a reality TV show."},
    {"id": 78, "title": "Trainspotting", "year": 1996, "rating": 8.1, "cert": "R", "genre": "Drama", "director": "Danny Boyle", "plot": "Renton, deeply immersed in the Edinburgh drug scene, tries to clean up and get out, despite the allure of the drugs and influence of friends."},
    {"id": 79, "title": "Fargo", "year": 1996, "rating": 8.1, "cert": "R", "genre": "Crime Drama Thriller", "director": "Joel Coen", "plot": "Jerry Lundegaard's inept crime falls apart due to his and his henchmen's bungling and the persistent police work of the quite pregnant Marge Gunderson."},
    {"id": 80, "title": "Heat", "year": 1995, "rating": 8.2, "cert": "R", "genre": "Action Crime Drama", "director": "Michael Mann", "plot": "A group of professional bank robbers start to feel the heat from police when they unknowingly leave a clue at their latest heist."},
    {"id": 81, "title": "Casino", "year": 1995, "rating": 8.2, "cert": "R", "genre": "Crime Drama", "director": "Martin Scorsese", "plot": "A tale of greed, deception, money, power, and murder occur between two best friends: a mafia enforcer and a casino executive compete against each other over a gambling empire, and over a fast living and fast loving socialite."},
    {"id": 82, "title": "Before Sunrise", "year": 1995, "rating": 8.1, "cert": "R", "genre": "Drama Romance", "director": "Richard Linklater", "plot": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. Unfortunately, both know that this will probably be their only night together."},
    {"id": 83, "title": "Princess Mononoke", "year": 1997, "rating": 8.4, "cert": "PG-13", "genre": "Animation Action Adventure", "director": "Hayao Miyazaki", "plot": "On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony."},
    {"id": 84, "title": "Eternal Sunshine", "year": 2004, "rating": 8.3, "cert": "R", "genre": "Drama Romance Sci-Fi", "director": "Michel Gondry", "plot": "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories."},
    {"id": 85, "title": "Finding Nemo", "year": 2003, "rating": 8.1, "cert": "G", "genre": "Animation Adventure Comedy", "director": "Andrew Stanton", "plot": "After his son is captured in the Great Barrier Reef and taken to Sydney, a timid clownfish sets out on a journey to bring him home."},
    {"id": 86, "title": "Kill Bill: Vol. 1", "year": 2003, "rating": 8.1, "cert": "R", "genre": "Action Crime Drama", "director": "Quentin Tarantino", "plot": "After awakening from a four-year coma, a former assassin wreaks vengeance on the team of assassins who betrayed her."},
    {"id": 87, "title": "Monsters, Inc.", "year": 2001, "rating": 8.1, "cert": "G", "genre": "Animation Adventure Comedy", "director": "Pete Docter", "plot": "In order to power the city, monsters have to scare children so that they scream. However, the children are toxic to the monsters, and after a child gets through, two monsters realize things may not be what they think."},
    {"id": 88, "title": "Snatch", "year": 2000, "rating": 8.3, "cert": "R", "genre": "Comedy Crime", "director": "Guy Ritchie", "plot": "Unscrupulous boxing promoters, violent bookmakers, a Russian gangster, incompetent amateur robbers and supposedly Jewish jewelers fight to track down a priceless stolen diamond."},
    {"id": 89, "title": "Requiem for a Dream", "year": 2000, "rating": 8.3, "cert": "R", "genre": "Drama", "director": "Darren Aronofsky", "plot": "The drug-induced utopias of four Coney Island people are shattered when their addictions run deep."},
    {"id": 90, "title": "American Beauty", "year": 1999, "rating": 8.3, "cert": "R", "genre": "Drama", "director": "Sam Mendes", "plot": "A sexually frustrated suburban father has a mid-life crisis after becoming infatuated with his daughter's best friend."},
    {"id": 91, "title": "The Sixth Sense", "year": 1999, "rating": 8.1, "cert": "PG-13", "genre": "Drama Mystery Thriller", "director": "M. Night Shyamalan", "plot": "A boy who communicates with spirits seeks the help of a disheartened child psychologist."},
    {"id": 92, "title": "The Big Lebowski", "year": 1998, "rating": 8.1, "cert": "R", "genre": "Comedy Crime", "director": "Joel Coen", "plot": "Jeff \"The Dude\" Lebowski, mistaken for a millionaire of the same name, seeks restitution for his ruined rug and enlists his bowling buddies to help get it."},
    {"id": 93, "title": "L.A. Confidential", "year": 1997, "rating": 8.2, "cert": "R", "genre": "Crime Drama Mystery", "director": "Curtis Hanson", "plot": "As corruption grows in 1950s Los Angeles, three policemen - one strait-laced, one brutal, and one sleazy - investigate a series of murders with their own brand of justice."},
    {"id": 94, "title": "Die Hard", "year": 1988, "rating": 8.2, "cert": "R", "genre": "Action Thriller", "director": "John McTiernan", "plot": "An NYPD officer tries to save his wife and several others taken hostage by German terrorists during a Christmas party at the Nakatomi Plaza in Los Angeles."},
    {"id": 95, "title": "Full Metal Jacket", "year": 1987, "rating": 8.3, "cert": "R", "genre": "Drama War", "director": "Stanley Kubrick", "plot": "A pragmatic U.S. Marine observes the dehumanizing effects the Vietnam War has on his fellow recruits from their brutal boot camp training to the bloody street fighting in Hue."},
    {"id": 96, "title": "Scarface", "year": 1983, "rating": 8.3, "cert": "R", "genre": "Crime Drama", "director": "Brian De Palma", "plot": "In 1980 Miami, a determined Cuban immigrant takes over a drug cartel and succumbs to greed."},
    {"id": 97, "title": "Taxi Driver", "year": 1976, "rating": 8.2, "cert": "R", "genre": "Crime Drama", "director": "Martin Scorsese", "plot": "A mentally unstable veteran works as a nighttime taxi driver in New York City, where the perceived decadence and sleaze fuels his urge for violent action."},
    {"id": 98, "title": "Chinatown", "year": 1974, "rating": 8.1, "cert": "R", "genre": "Drama Mystery Thriller", "director": "Roman Polanski", "plot": "A private detective hired to expose an adulterer finds himself caught up in a web of deceit, corruption, and murder."},
    {"id": 99, "title": "A Clockwork Orange", "year": 1971, "rating": 8.3, "cert": "R", "genre": "Crime Drama Sci-Fi", "director": "Stanley Kubrick", "plot": "In the future, a sadistic gang leader is imprisoned and volunteers for a conduct-aversion experiment, but it doesn't go as planned."},
    {"id": 100, "title": "2001: A Space Odyssey", "year": 1968, "rating": 8.3, "cert": "G", "genre": "Adventure Sci-Fi", "director": "Stanley Kubrick", "plot": "After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000."},
    {"id": 101, "title": "Everything Everywhere", "year": 2022, "rating": 7.9, "cert": "R", "genre": "Action Adventure Sci-Fi", "director": "Daniel Kwan", "plot": "A middle-aged Chinese immigrant is swept up into an insane adventure in which she alone can save the existence by exploring other universes and connecting with the lives she could have led."},
    {"id": 102, "title": "Oppenheimer", "year": 2023, "rating": 8.6, "cert": "R", "genre": "Biography Drama History", "director": "Christopher Nolan", "plot": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb."},
    {"id": 103, "title": "Barbie", "year": 2023, "rating": 7.0, "cert": "PG-13", "genre": "Adventure Comedy Fantasy", "director": "Greta Gerwig", "plot": "Barbie suffers a crisis that leads her to question her world and her existence."},
    {"id": 104, "title": "Top Gun: Maverick", "year": 2022, "rating": 8.3, "cert": "PG-13", "genre": "Action Drama", "director": "Joseph Kosinski", "plot": "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on a mission that demands the ultimate sacrifice from those chosen to fly it."},
    {"id": 105, "title": "The Batman", "year": 2022, "rating": 7.8, "cert": "PG-13", "genre": "Action Crime Drama", "director": "Matt Reeves", "plot": "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement."},
    {"id": 106, "title": "Singin' in the Rain", "year": 1952, "rating": 8.3, "cert": "G", "genre": "Comedy Musical Romance", "director": "Stanley Donen", "plot": "A silent film star falls for a chorus girl just as he and his delusionally jealous screen partner are trying to make the difficult transition to talking pictures."},
    {"id": 107, "title": "Modern Times", "year": 1936, "rating": 8.5, "cert": "G", "genre": "Comedy Drama Family", "director": "Charles Chaplin", "plot": "The Tramp struggles to live in modern industrial society with the help of a young homeless woman."},
    {"id": 108, "title": "City Lights", "year": 1931, "rating": 8.5, "cert": "G", "genre": "Comedy Drama Romance", "director": "Charles Chaplin", "plot": "With the aid of a wealthy erratic drunkard, a dewy-eyed tramp who has fallen in love with a sightless flower girl accumulates money to be able to help her medically."},
    {"id": 109, "title": "Citizen Kane", "year": 1941, "rating": 8.3, "cert": "PG", "genre": "Drama Mystery", "director": "Orson Welles", "plot": "Following the death of publishing tycoon Charles Foster Kane, reporters scramble to uncover the meaning of his final utterance; 'Rosebud'."},
    {"id": 110, "title": "Vertigo", "year": 1958, "rating": 8.3, "cert": "PG", "genre": "Mystery Romance Thriller", "director": "Alfred Hitchcock", "plot": "A former police detective juggles wrestling with his personal demons and becoming obsessed with a hauntingly beautiful woman."},
    {"id": 111, "title": "Rear Window", "year": 1954, "rating": 8.5, "cert": "PG", "genre": "Mystery Thriller", "director": "Alfred Hitchcock", "plot": "A wheelchair-bound photographer spies on his neighbors from his apartment window and becomes convinced one of them has committed murder."},
    {"id": 112, "title": "North by Northwest", "year": 1959, "rating": 8.3, "cert": "PG", "genre": "Action Adventure Mystery", "director": "Alfred Hitchcock", "plot": "A New York City advertising executive goes on the run after being mistaken for a government agent by a group of foreign spies."},
    {"id": 113, "title": "Lawrence of Arabia", "year": 1962, "rating": 8.3, "cert": "PG", "genre": "Adventure Biography Drama", "director": "David Lean", "plot": "The story of T.E. Lawrence, the English officer who successfully united and led the diverse, often warring, Arab tribes during World War I in order to fight the Turks."},
    {"id": 114, "title": "Ben-Hur", "year": 1959, "rating": 8.1, "cert": "G", "genre": "Adventure Drama History", "director": "William Wyler", "plot": "After a Jewish prince is betrayed and sent to slavery by a Roman friend in 1st-century Jerusalem, he regains his freedom and comes back for revenge."},
    {"id": 115, "title": "The Apartment", "year": 1960, "rating": 8.3, "cert": "PG", "genre": "Comedy Drama Romance", "director": "Billy Wilder", "plot": "A Manhattan insurance clerk tries to rise in his company by letting its executives use his apartment for trysts, but complications and a romance of his own ensue."},
    {"id": 116, "title": "Double Indemnity", "year": 1944, "rating": 8.3, "cert": "PG", "genre": "Crime Drama Film-Noir", "director": "Billy Wilder", "plot": "An insurance representative lets himself be talked by a seductive housewife into a murder/insurance fraud scheme that arouses the suspicion of his insurance investigator."},
    {"id": 117, "title": "Sunset Blvd.", "year": 1950, "rating": 8.4, "cert": "PG", "genre": "Drama Film-Noir", "director": "Billy Wilder", "plot": "A screenwriter develops a dangerous relationship with a faded film star determined to make a triumphant return."},
    {"id": 118, "title": "Dr. Strangelove", "year": 1964, "rating": 8.4, "cert": "PG", "genre": "Comedy War", "director": "Stanley Kubrick", "plot": "An insane American general orders a bombing attack on the Soviet Union, triggering a path to nuclear holocaust that a war room full of politicians and generals frantically tries to stop."},
    {"id": 119, "title": "Some Like It Hot", "year": 1959, "rating": 8.2, "cert": "PG", "genre": "Comedy Music Romance", "director": "Billy Wilder", "plot": "After two male musicians witness a mob hit, they flee the state in an all-female band disguised as women, but further complications set in."},
    {"id": 120, "title": "The Bridge on the River Kwai", "year": 1957, "rating": 8.1, "cert": "PG", "genre": "Adventure Drama War", "director": "David Lean", "plot": "British POWs are forced to build a railway bridge across the river Kwai for their Japanese captors, not knowing that the allied forces are planning to destroy it."}
]

# ==========================================
# PART 2: ADVANCED RECOMMENDATION ENGINE
# ==========================================

class RecommendationEngine:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        self.setup_engine()

    def setup_engine(self):
        """Prepares the TF-IDF matrix and Linear Kernel."""
        self.df['features'] = (
            self.df['genre'] + " " + 
            self.df['genre'] + " " + 
            self.df['director'] + " " + 
            self.df['director'] + " " + 
            self.df['plot']
        )
        
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['features'])
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()

    def get_recommendations(self, title, num_recommendations=8):
        if title not in self.indices:
            return []

        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations+1]
        
        results = []
        for i, score in sim_scores:
            movie_data = self.df.iloc[i].to_dict()
            movie_data['match_score'] = round(score * 100) 
            results.append(movie_data)
            
        return results
    
    def get_filtered_movies(self, genre_filter="All Genres", rating_min=0, 
                           year_start=1900, year_end=2024, 
                           cert_filter="All", user_age=None):
        filtered = self.df.copy()
        
        # 1. Genre
        if genre_filter and genre_filter != "All Genres":
            filtered = filtered[filtered['genre'].str.contains(genre_filter, case=False)]
            
        # 2. Minimum Rating
        filtered = filtered[filtered['rating'] >= rating_min]

        # 3. Year Range
        filtered = filtered[(filtered['year'] >= year_start) & (filtered['year'] <= year_end)]

        # 4. Certification (Specific)
        if cert_filter and cert_filter != "All":
            filtered = filtered[filtered['cert'] == cert_filter]

        # 5. User Age (Smart Filtering)
        if user_age is not None and user_age > 0:
            if user_age < 7:
                allowed = ['G', 'U']
            elif user_age < 13:
                allowed = ['G', 'U', 'PG', 'UA']
            elif user_age < 17:
                allowed = ['G', 'U', 'PG', 'UA', 'PG-13', '12A']
            else:
                allowed = ['G', 'U', 'PG', 'UA', 'PG-13', '12A', 'R', 'A', 'MA']
            
            filtered = filtered[filtered['cert'].isin(allowed)]
        
        return filtered.sample(frac=1).head(25).to_dict('records')

    def get_all_titles(self):
        return sorted(self.df['title'].tolist())

    def get_all_genres(self):
        genres = set()
        for g_str in self.df['genre']:
            for g in g_str.split():
                genres.add(g)
        return sorted(list(genres))
    
    def get_all_certs(self):
        return sorted(list(set(self.df['cert'])))

# ==========================================
# PART 3: UI CONSTANTS & STYLES
# ==========================================

class Colors:
    BG_MAIN = "#141414"        
    BG_SIDEBAR = "#000000"    
    SURFACE = "#181818"       
    SURFACE_HOVER = "#282828"
    ACCENT = "#E50914"         
    TEXT_MAIN = "#FFFFFF"
    TEXT_SUB = "#AAAAAA"
    BORDER = "#333333"
    SUCCESS = "#46d369"       
    CERT_BOX = "#333333"

# ==========================================
# PART 4: UI COMPONENTS
# ==========================================

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        self.bg_color = kwargs.get("bg", Colors.SURFACE)
        self.hover_color = kwargs.get("activebackground", Colors.SURFACE_HOVER)
        super().__init__(master, **kwargs)
        self.configure(relief="flat", cursor="hand2", bd=0)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = self.hover_color

    def on_leave(self, e):
        self['bg'] = self.bg_color

class MovieCard(tk.Frame):
    def __init__(self, parent, movie_data, click_callback, fav_callback, is_fav=False):
        super().__init__(parent, bg=Colors.SURFACE, padx=15, pady=15)
        self.movie_data = movie_data
        self.click_callback = click_callback
        self.fav_callback = fav_callback
        self.is_fav = is_fav
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.columnconfigure(1, weight=1) # Text expands
        
        # --- LAYOUT ---
        # Column 0: Image
        # Column 1: Text Details
        # Column 2: Fav Button

        # 0. Image Placeholder / Actual Image
        self.img_frame = tk.Frame(self, bg=Colors.SURFACE, width=80, height=120)
        self.img_frame.grid(row=0, column=0, rowspan=4, padx=(0, 15))
        self.img_frame.pack_propagate(False) # Force size

        # ####### IMAGE LOADING SECTION #######
        # To use real images, replace the block below with:
        # try:
        #     self.poster_img = tk.PhotoImage(file=f"your_images_folder/{movie_data['title']}.png")
        #     tk.Label(self.img_frame, image=self.poster_img, bg=Colors.SURFACE).pack(expand=True, fill="both")
        # except:
        #     self.create_placeholder_image()
        
        # For now, we use the placeholder generator:
        self.create_placeholder_image()
        # #####################################

        # 1. Top Row: Match % + Cert Badge
        top_frame = tk.Frame(self, bg=Colors.SURFACE)
        top_frame.grid(row=0, column=1, sticky="w")

        lbl_cert = tk.Label(top_frame, text=f" {movie_data['cert']} ", font=("Segoe UI", 8, "bold"), fg="white", bg=Colors.CERT_BOX)
        lbl_cert.pack(side="left", padx=(0, 10))

        match_score = movie_data.get('match_score', None)
        if match_score:
            color = Colors.SUCCESS if match_score > 80 else Colors.TEXT_SUB
            tk.Label(top_frame, text=f"{match_score}% Match", font=("Segoe UI", 10, "bold"), fg=color, bg=Colors.SURFACE).pack(side="left")

        # 2. Title & Year
        title_text = f"{movie_data['title']} ({movie_data['year']})"
        self.lbl_title = tk.Label(self, text=title_text, font=("Segoe UI", 14, "bold"), fg=Colors.TEXT_MAIN, bg=Colors.SURFACE, anchor="w")
        self.lbl_title.grid(row=1, column=1, sticky="ew", pady=(5,0))
        
        # 3. Meta Data
        meta = f"⭐ {movie_data['rating']}  |  {movie_data['genre']}  |  🎬 {movie_data['director']}"
        self.lbl_meta = tk.Label(self, text=meta, font=("Segoe UI", 9), fg=Colors.TEXT_SUB, bg=Colors.SURFACE, anchor="w")
        self.lbl_meta.grid(row=2, column=1, sticky="ew", pady=(0, 8))

        # 4. Plot
        plot = textwrap.shorten(movie_data['plot'], width=90, placeholder="...")
        self.lbl_plot = tk.Label(self, text=plot, font=("Segoe UI", 10), fg="#DDDDDD", bg=Colors.SURFACE, justify="left", anchor="w")
        self.lbl_plot.grid(row=3, column=1, sticky="ew")

        # 5. Fav Button
        heart_char = "❤️" if is_fav else "🤍"
        self.btn_fav = tk.Button(self, text=heart_char, font=("Segoe UI", 16), bg=Colors.SURFACE, fg=Colors.ACCENT, bd=0, cursor="hand2", 
                                 command=self.toggle_fav, activebackground=Colors.SURFACE, activeforeground=Colors.ACCENT)
        self.btn_fav.grid(row=0, column=2, sticky="ne", padx=5)
        
        self._bind_rec(self)

    def create_placeholder_image(self):
        """Generates a colored box with initials if no image is found."""
        initial = self.movie_data['title'][0]
        colors = ["#b71c1c", "#0d47a1", "#1b5e20", "#f57f17", "#4a148c", "#3e2723"]
        bg_col = random.choice(colors)
        
        canvas = tk.Canvas(self.img_frame, bg=bg_col, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_text(40, 60, text=initial, font=("Impact", 30), fill="white")

    def _bind_rec(self, widget):
        for child in widget.winfo_children():
            if child != self.btn_fav:
                child.bind("<Enter>", self.on_enter)
                child.bind("<Leave>", self.on_leave)
                child.bind("<Button-1>", self.on_click)
                self._bind_rec(child)

    def toggle_fav(self):
        self.is_fav = not self.is_fav
        self.btn_fav.config(text="❤️" if self.is_fav else "🤍")
        self.fav_callback(self.movie_data)

    def on_enter(self, e):
        self.config(bg=Colors.SURFACE_HOVER)
        for child in self.winfo_children():
            if child != self.btn_fav:
                try: child.config(bg=Colors.SURFACE_HOVER)
                except: pass

    def on_leave(self, e):
        self.config(bg=Colors.SURFACE)
        for child in self.winfo_children():
            if child != self.btn_fav:
                try: child.config(bg=Colors.SURFACE)
                except: pass

    def on_click(self, e):
        self.click_callback(self.movie_data)

class Sidebar(tk.Frame):
    def __init__(self, parent, engine, on_filter_change, on_tab_change):
        super().__init__(parent, bg=Colors.BG_SIDEBAR, width=300)
        self.pack_propagate(False)
        self.engine = engine
        self.on_filter_change = on_filter_change
        self.on_tab_change = on_tab_change
        
        # Logo
        tk.Label(self, text="NETFLIX", font=("Impact", 30), fg=Colors.ACCENT, bg=Colors.BG_SIDEBAR).pack(pady=(20, 10))
        
        # Tabs
        self.create_nav_btn("🏠  Home", "home")
        self.create_nav_btn("❤️  My List", "favorites")
        
        tk.Frame(self, bg=Colors.BORDER, height=1).pack(fill="x", padx=20, pady=15)
        
        # --- FILTERS SECTION ---
        tk.Label(self, text="SMART FILTERS", font=("Segoe UI", 10, "bold"), fg=Colors.TEXT_SUB, bg=Colors.BG_SIDEBAR).pack(anchor="w", padx=20)

        # 1. Genre
        self.create_label("Genre")
        self.genre_var = tk.StringVar(value="All Genres")
        genres = ["All Genres"] + engine.get_all_genres()
        self.cb_genre = ttk.Combobox(self, textvariable=self.genre_var, values=genres, state="readonly")
        self.cb_genre.pack(padx=20, fill="x")
        self.cb_genre.bind("<<ComboboxSelected>>", self.trigger_filter)

        # 2. Rating
        self.create_label("Min Rating")
        self.rating_var = tk.DoubleVar(value=0.0)
        tk.Scale(self, from_=5.0, to=9.0, resolution=0.1, orient="horizontal", bg=Colors.BG_SIDEBAR, fg="white", highlightthickness=0, variable=self.rating_var, command=lambda x: self.trigger_filter()).pack(padx=20, fill="x")

        # 3. Year Range (From - To)
        self.create_label("Year of Launch")
        year_frame = tk.Frame(self, bg=Colors.BG_SIDEBAR)
        year_frame.pack(padx=20, fill="x")
        
        self.year_from_var = tk.StringVar(value="1900")
        self.year_to_var = tk.StringVar(value="2024")
        years = [str(y) for y in range(1920, 2025)]
        
        self.cb_year_from = ttk.Combobox(year_frame, textvariable=self.year_from_var, values=years, width=5)
        self.cb_year_from.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Label(year_frame, text="-", bg=Colors.BG_SIDEBAR, fg="white").pack(side="left")
        
        self.cb_year_to = ttk.Combobox(year_frame, textvariable=self.year_to_var, values=years, width=5)
        self.cb_year_to.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        self.cb_year_from.bind("<<ComboboxSelected>>", self.trigger_filter)
        self.cb_year_to.bind("<<ComboboxSelected>>", self.trigger_filter)

        # 4. Certification
        self.create_label("Certification")
        self.cert_var = tk.StringVar(value="All")
        certs = ["All"] + engine.get_all_certs()
        self.cb_cert = ttk.Combobox(self, textvariable=self.cert_var, values=certs, state="readonly")
        self.cb_cert.pack(padx=20, fill="x")
        self.cb_cert.bind("<<ComboboxSelected>>", self.trigger_filter)

        tk.Frame(self, bg=Colors.BORDER, height=1).pack(fill="x", padx=20, pady=15)

        # 5. User Age (Auto Filter)
        self.create_label("Viewer Age (Auto-Filter)")
        self.age_var = tk.StringVar(value="")
        self.age_entry = tk.Spinbox(self, from_=0, to=100, textvariable=self.age_var, width=5, command=self.trigger_filter)
        self.age_entry.pack(padx=20, fill="x")
        self.age_entry.bind("<KeyRelease>", self.trigger_filter)
        
        # Info Label
        self.lbl_age_info = tk.Label(self, text="Enter age to hide mature content.", font=("Segoe UI", 8), fg=Colors.TEXT_SUB, bg=Colors.BG_SIDEBAR)
        self.lbl_age_info.pack(padx=20, pady=2)

        # Reset
        ModernButton(self, text="Reset Filters", bg=Colors.SURFACE, fg=Colors.TEXT_MAIN, command=self.reset_filters).pack(pady=20)

    def create_label(self, text):
        tk.Label(self, text=text, font=("Segoe UI", 9), fg=Colors.TEXT_SUB, bg=Colors.BG_SIDEBAR).pack(anchor="w", padx=20, pady=(10, 2))

    def create_nav_btn(self, text, tab_name):
        ModernButton(self, text=text, font=("Segoe UI", 12), bg=Colors.BG_SIDEBAR, fg=Colors.TEXT_MAIN, anchor="w", padx=20, pady=8, command=lambda: self.on_tab_change(tab_name)).pack(fill="x")

    def trigger_filter(self, event=None):
        try:
            y_from = int(self.year_from_var.get())
        except: y_from = 1900
        
        try:
            y_to = int(self.year_to_var.get())
        except: y_to = 2025

        try:
            age = int(self.age_var.get())
        except: age = 0

        self.on_filter_change(
            genre=self.genre_var.get(),
            rating=self.rating_var.get(),
            year_start=y_from,
            year_end=y_to,
            cert=self.cert_var.get(),
            age=age
        )

    def reset_filters(self):
        self.genre_var.set("All Genres")
        self.rating_var.set(0)
        self.year_from_var.set("1900")
        self.year_to_var.set("2024")
        self.cert_var.set("All")
        self.age_var.set("")
        self.trigger_filter()

class ScrollableFrame(tk.Frame):
    def __init__(self, container, bg_color, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=800)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollable_frame.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

# ==========================================
# PART 5: MAIN APP
# ==========================================

class NetflixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Netflix AI Ultra - Image & Dynamic Search")
        self.geometry("1200x850")
        self.configure(bg=Colors.BG_MAIN)
        
        self.engine = RecommendationEngine(MOVIE_DB)
        self.favorites = set()
        self.current_tab = "home"
        
        self.setup_styles()
        
        # Layout
        self.sidebar = Sidebar(self, self.engine, self.apply_filters, self.switch_tab)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_area = tk.Frame(self, bg=Colors.BG_MAIN)
        self.main_area.pack(side="right", fill="both", expand=True)
        
        self.create_header()
        self.create_hero()
        
        self.lbl_section_title = tk.Label(self.main_area, text="Trending Now", font=("Segoe UI", 18, "bold"), bg=Colors.BG_MAIN, fg=Colors.TEXT_MAIN)
        self.lbl_section_title.pack(anchor="w", padx=40, pady=(10, 15))
        
        self.scroll_container = ScrollableFrame(self.main_area, bg_color=Colors.BG_MAIN)
        self.scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        self.results_frame = self.scroll_container.scrollable_frame
        
        self.show_home_default()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=Colors.SURFACE, background=Colors.ACCENT, foreground=Colors.TEXT_MAIN)
        self.option_add('*TCombobox*Listbox.background', Colors.SURFACE)
        self.option_add('*TCombobox*Listbox.foreground', Colors.TEXT_MAIN)

    def create_header(self):
        header = tk.Frame(self.main_area, bg=Colors.BG_MAIN, height=60)
        header.pack(fill="x", padx=40, pady=20)
        
        self.search_var = tk.StringVar()
        self.search_box = ttk.Combobox(header, textvariable=self.search_var, font=("Segoe UI", 12), width=40)
        self.search_box.pack(side="left")
        
        # Bind key release for dynamic updating (Type 'Toy' -> see matching list)
        self.search_box.bind("<KeyRelease>", self.update_search_list)
        self.search_box.bind("<<ComboboxSelected>>", self.on_search_click)
        self.search_box.bind("<Return>", self.on_search_enter)
        
        ModernButton(header, text="🔍 SEARCH", bg=Colors.ACCENT, fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=5, command=self.on_search_enter).pack(side="left", padx=10)

    def create_hero(self):
        self.hero_frame = tk.Frame(self.main_area, bg=Colors.BG_MAIN)
        self.hero_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        self.lbl_hero_title = tk.Label(self.hero_frame, text="", font=("Segoe UI", 28, "bold"), bg=Colors.BG_MAIN, fg=Colors.TEXT_MAIN)
        self.lbl_hero_title.pack(anchor="w")
        
        self.lbl_hero_info = tk.Label(self.hero_frame, text="", font=("Segoe UI", 12, "bold"), bg=Colors.BG_MAIN, fg=Colors.SUCCESS)
        self.lbl_hero_info.pack(anchor="w", pady=5)
        
        self.lbl_hero_desc = tk.Label(self.hero_frame, text="Welcome. Start typing in the search box above (e.g., 'Toy') to see matches.", font=("Segoe UI", 11), bg=Colors.BG_MAIN, fg=Colors.TEXT_SUB, wraplength=800, justify="left")
        self.lbl_hero_desc.pack(anchor="w")

    # --- DYNAMIC SEARCH LOGIC ---
    def update_search_list(self, event):
        """Update dropdown values based on typing."""
        # Don't filter on arrow keys or enter
        if event.keysym in ['Up', 'Down', 'Return', 'Left', 'Right']:
            return

        typed = self.search_box.get().lower()
        all_titles = self.engine.get_all_titles()
        
        if typed == '':
            self.search_box['values'] = all_titles
        else:
            # Filter titles that contain the typed string
            filtered_data = [item for item in all_titles if typed in item.lower()]
            self.search_box['values'] = filtered_data
            
            # Optional: Open the dropdown list automatically
            if filtered_data:
                # This works on most systems to pop open the list
                try: self.search_box.event_generate('<Down>')
                except: pass

    def on_search_click(self, event):
        """Triggered when user clicks an item in the dropdown."""
        self.on_search_enter()

    def on_search_enter(self, event=None):
        """Triggered on Enter key or Button click."""
        query = self.search_var.get().strip()
        if not query: return

        # Find exact or partial match
        movie_obj = next((item for item in MOVIE_DB if item["title"].lower() == query.lower()), None)
        if not movie_obj:
            # Fallback to partial match if they typed "Toy" and hit enter without selecting
            movie_obj = next((item for item in MOVIE_DB if query.lower() in item["title"].lower()), None)

        if movie_obj:
            self.on_movie_select(movie_obj)
            self.search_box.set(movie_obj['title'])
            # Clear the dropdown values back to default
            self.search_box['values'] = self.engine.get_all_titles()
        else:
            messagebox.showerror("Oops", "Movie not found!")

    def render_movies(self, movie_list):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not movie_list:
            tk.Label(self.results_frame, text="No movies found matching your criteria.", bg=Colors.BG_MAIN, fg=Colors.TEXT_SUB, font=("Segoe UI", 14)).pack(pady=50)
            return

        for movie in movie_list:
            is_fav = movie['title'] in self.favorites
            card = MovieCard(self.results_frame, movie, self.on_movie_select, self.on_toggle_fav, is_fav=is_fav)
            card.pack(fill="x", pady=5)

    def show_home_default(self):
        self.current_tab = "home"
        self.lbl_section_title.config(text="Trending & Random Picks")
        self.render_movies(random.sample(MOVIE_DB, 20))

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        if tab_name == "home":
            self.sidebar.reset_filters()
        elif tab_name == "favorites":
            self.lbl_section_title.config(text="My Watchlist ❤️")
            fav_movies = [m for m in MOVIE_DB if m['title'] in self.favorites]
            self.render_movies(fav_movies)

    def apply_filters(self, genre, rating, year_start, year_end, cert, age):
        if self.current_tab == "favorites": return 
        self.current_tab = "browse"
        
        title_str = f"Browsing: {genre} | {year_start}-{year_end}"
        if age > 0: title_str += f" | Age: {age}"
        self.lbl_section_title.config(text=title_str)
        
        results = self.engine.get_filtered_movies(genre, rating, year_start, year_end, cert, age)
        self.render_movies(results)

    def on_movie_select(self, movie):
        self.lbl_hero_title.config(text=movie['title'])
        self.lbl_hero_info.config(text=f"{movie['year']}  •  {movie['cert']}  •  {movie['rating']}/10")
        self.lbl_hero_desc.config(text=movie['plot'])
        self.lbl_section_title.config(text=f"Because you liked '{movie['title']}'")
        recs = self.engine.get_recommendations(movie['title'])
        self.render_movies(recs)

    def on_toggle_fav(self, movie_data):
        title = movie_data['title']
        if title in self.favorites: self.favorites.remove(title)
        else: self.favorites.add(title)
        if self.current_tab == "favorites": self.switch_tab("favorites")

if __name__ == "__main__":
    app = NetflixApp()
    app.mainloop()