import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import textwrap
import random
import time
import threading

# =====================================================================
# PART 1: MASSIVE MOVIE DATABASE (RICH METADATA)
# =====================================================================
MOVIE_DB = [
    {
        "id": 1,
        "title": "Avatar",
        "year": 2009,
        "rating": 7.8,
        "cert": "PG-13",
        "duration": "162 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "James Cameron",
        "cast": "Sam Worthington, Zoe Saldana, Sigourney Weaver",
        "plot": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home."
    },
    {
        "id": 2,
        "title": "The Avengers",
        "year": 2012,
        "rating": 8.0,
        "cert": "PG-13",
        "duration": "143 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "Joss Whedon",
        "cast": "Robert Downey Jr., Chris Evans, Scarlett Johansson",
        "plot": "Earth's mightiest heroes must come together and learn to fight as a team if they are to stop the mischievous Loki and his alien army from enslaving humanity."
    },
    {
        "id": 3,
        "title": "The Godfather",
        "year": 1972,
        "rating": 9.2,
        "cert": "R",
        "duration": "175 min",
        "genre": "Crime Drama",
        "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan",
        "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    },
    {
        "id": 4,
        "title": "Inception",
        "year": 2010,
        "rating": 8.8,
        "cert": "PG-13",
        "duration": "148 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "id": 5,
        "title": "Pulp Fiction",
        "year": 1994,
        "rating": 8.9,
        "cert": "R",
        "duration": "154 min",
        "genre": "Crime Drama",
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Uma Thurman, Samuel L. Jackson",
        "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
    },
    {
        "id": 6,
        "title": "The Dark Knight",
        "year": 2008,
        "rating": 9.0,
        "cert": "PG-13",
        "duration": "152 min",
        "genre": "Action Crime Drama",
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "id": 7,
        "title": "Interstellar",
        "year": 2014,
        "rating": 8.6,
        "cert": "PG-13",
        "duration": "169 min",
        "genre": "Adventure Drama Sci-Fi",
        "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        "id": 8,
        "title": "Fight Club",
        "year": 1999,
        "rating": 8.8,
        "cert": "R",
        "duration": "139 min",
        "genre": "Drama",
        "director": "David Fincher",
        "cast": "Brad Pitt, Edward Norton, Meat Loaf",
        "plot": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more."
    },
    {
        "id": 9,
        "title": "Forrest Gump",
        "year": 1994,
        "rating": 8.8,
        "cert": "PG-13",
        "duration": "142 min",
        "genre": "Drama Romance",
        "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise",
        "plot": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate and other historical events unfold through the perspective of an Alabama man with an IQ of 75."
    },
    {
        "id": 10,
        "title": "The Matrix",
        "year": 1999,
        "rating": 8.7,
        "cert": "R",
        "duration": "136 min",
        "genre": "Action Sci-Fi",
        "director": "Lana Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "plot": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
    },
    {
        "id": 11,
        "title": "Goodfellas",
        "year": 1990,
        "rating": 8.7,
        "cert": "R",
        "duration": "145 min",
        "genre": "Biography Crime Drama",
        "director": "Martin Scorsese",
        "cast": "Robert De Niro, Ray Liotta, Joe Pesci",
        "plot": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito."
    },
    {
        "id": 12,
        "title": "Star Wars: A New Hope",
        "year": 1977,
        "rating": 8.6,
        "cert": "PG",
        "duration": "121 min",
        "genre": "Action Adventure Fantasy",
        "director": "George Lucas",
        "cast": "Mark Hamill, Harrison Ford, Carrie Fisher",
        "plot": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station."
    },
    {
        "id": 13,
        "title": "Parasite",
        "year": 2019,
        "rating": 8.6,
        "cert": "R",
        "duration": "132 min",
        "genre": "Comedy Drama Thriller",
        "director": "Bong Joon Ho",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "plot": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."
    },
    {
        "id": 14,
        "title": "The Lion King",
        "year": 1994,
        "rating": 8.5,
        "cert": "G",
        "duration": "88 min",
        "genre": "Animation Adventure Drama",
        "director": "Roger Allers",
        "cast": "Matthew Broderick, Jeremy Irons, James Earl Jones",
        "plot": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."
    },
    {
        "id": 15,
        "title": "Titanic",
        "year": 1997,
        "rating": 7.8,
        "cert": "PG-13",
        "duration": "194 min",
        "genre": "Drama Romance",
        "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
    },
    {
        "id": 16,
        "title": "Gladiator",
        "year": 2000,
        "rating": 8.5,
        "cert": "R",
        "duration": "155 min",
        "genre": "Action Adventure Drama",
        "director": "Ridley Scott",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
        "plot": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery."
    },
    {
        "id": 17,
        "title": "Jurassic Park",
        "year": 1993,
        "rating": 8.1,
        "cert": "PG-13",
        "duration": "127 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "Steven Spielberg",
        "cast": "Sam Neill, Laura Dern, Jeff Goldblum",
        "plot": "A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the cloned dinosaurs to run loose."
    },
    {
        "id": 18,
        "title": "The Silence of the Lambs",
        "year": 1991,
        "rating": 8.6,
        "cert": "R",
        "duration": "118 min",
        "genre": "Crime Drama Thriller",
        "director": "Jonathan Demme",
        "cast": "Jodie Foster, Anthony Hopkins, Lawrence A. Bonney",
        "plot": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."
    },
    {
        "id": 19,
        "title": "Coco",
        "year": 2017,
        "rating": 8.4,
        "cert": "G",
        "duration": "105 min",
        "genre": "Animation Adventure Family",
        "director": "Lee Unkrich",
        "cast": "Anthony Gonzalez, Gael García Bernal, Benjamin Bratt",
        "plot": "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer."
    },
    {
        "id": 20,
        "title": "Whiplash",
        "year": 2014,
        "rating": 8.5,
        "cert": "R",
        "duration": "106 min",
        "genre": "Drama Music",
        "director": "Damien Chazelle",
        "cast": "Miles Teller, J.K. Simmons, Melissa Benoist",
        "plot": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential."
    },
    {
        "id": 21,
        "title": "Spider-Man: Into the Spider-Verse",
        "year": 2018,
        "rating": 8.4,
        "cert": "PG",
        "duration": "117 min",
        "genre": "Animation Action Adventure",
        "director": "Bob Persichetti",
        "cast": "Shameik Moore, Jake Johnson, Hailee Steinfeld",
        "plot": "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities."
    },
    {
        "id": 22,
        "title": "Back to the Future",
        "year": 1985,
        "rating": 8.5,
        "cert": "PG",
        "duration": "116 min",
        "genre": "Adventure Comedy Sci-Fi",
        "director": "Robert Zemeckis",
        "cast": "Michael J. Fox, Christopher Lloyd, Lea Thompson",
        "plot": "Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean invented by his close friend, the eccentric scientist Doc Brown."
    },
    {
        "id": 23,
        "title": "The Shining",
        "year": 1980,
        "rating": 8.4,
        "cert": "R",
        "duration": "146 min",
        "genre": "Drama Horror",
        "director": "Stanley Kubrick",
        "cast": "Jack Nicholson, Shelley Duvall, Danny Lloyd",
        "plot": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from the past and future."
    },
    {
        "id": 24,
        "title": "Alien",
        "year": 1979,
        "rating": 8.4,
        "cert": "R",
        "duration": "117 min",
        "genre": "Horror Sci-Fi",
        "director": "Ridley Scott",
        "cast": "Sigourney Weaver, Tom Skerritt, John Hurt",
        "plot": "After a space merchant vessel receives an unknown transmission as a distress call, one of the crew is attacked by a mysterious life form and they soon realize that its life cycle has merely begun."
    },
    {
        "id": 25,
        "title": "Toy Story",
        "year": 1995,
        "rating": 8.3,
        "cert": "G",
        "duration": "81 min",
        "genre": "Animation Adventure Comedy",
        "director": "John Lasseter",
        "cast": "Tom Hanks, Tim Allen, Don Rickles",
        "plot": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room."
    },
    {
        "id": 26,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "rating": 9.3,
        "cert": "R",
        "duration": "142 min",
        "genre": "Drama",
        "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "id": 27,
        "title": "Schindler's List",
        "year": 1993,
        "rating": 8.9,
        "cert": "R",
        "duration": "195 min",
        "genre": "Biography Drama History",
        "director": "Steven Spielberg",
        "cast": "Liam Neeson, Ralph Fiennes, Ben Kingsley",
        "plot": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis."
    },
    {
        "id": 28,
        "title": "Lord of the Rings: Return of the King",
        "year": 2003,
        "rating": 8.9,
        "cert": "PG-13",
        "duration": "201 min",
        "genre": "Action Adventure Drama",
        "director": "Peter Jackson",
        "cast": "Elijah Wood, Viggo Mortensen, Ian McKellen",
        "plot": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring."
    },
    {
        "id": 29,
        "title": "Spirited Away",
        "year": 2001,
        "rating": 8.6,
        "cert": "PG",
        "duration": "125 min",
        "genre": "Animation Adventure Family",
        "director": "Hayao Miyazaki",
        "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki",
        "plot": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts."
    },
    {
        "id": 30,
        "title": "Saving Private Ryan",
        "year": 1998,
        "rating": 8.6,
        "cert": "R",
        "duration": "169 min",
        "genre": "Drama War",
        "director": "Steven Spielberg",
        "cast": "Tom Hanks, Matt Damon, Tom Sizemore",
        "plot": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action."
    },
    {
        "id": 31,
        "title": "The Green Mile",
        "year": 1999,
        "rating": 8.6,
        "cert": "R",
        "duration": "189 min",
        "genre": "Crime Drama Fantasy",
        "director": "Frank Darabont",
        "cast": "Tom Hanks, Michael Clarke Duncan, David Morse",
        "plot": "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift."
    },
    {
        "id": 32,
        "title": "Terminator 2: Judgment Day",
        "year": 1991,
        "rating": 8.5,
        "cert": "R",
        "duration": "137 min",
        "genre": "Action Sci-Fi",
        "director": "James Cameron",
        "cast": "Arnold Schwarzenegger, Linda Hamilton, Edward Furlong",
        "plot": "A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son, John, from a more advanced and powerful cyborg."
    },
    {
        "id": 33,
        "title": "Se7en",
        "year": 1995,
        "rating": 8.6,
        "cert": "R",
        "duration": "127 min",
        "genre": "Crime Drama Mystery",
        "director": "David Fincher",
        "cast": "Morgan Freeman, Brad Pitt, Kevin Spacey",
        "plot": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives."
    },
    {
        "id": 34,
        "title": "The Pianist",
        "year": 2002,
        "rating": 8.5,
        "cert": "R",
        "duration": "150 min",
        "genre": "Biography Drama Music",
        "director": "Roman Polanski",
        "cast": "Adrien Brody, Thomas Kretschmann, Frank Finlay",
        "plot": "A Polish Jewish radio station pianist struggles to survive the destruction of the Warsaw ghetto of World War II."
    },
    {
        "id": 35,
        "title": "Psycho",
        "year": 1960,
        "rating": 8.5,
        "cert": "R",
        "duration": "109 min",
        "genre": "Horror Mystery Thriller",
        "director": "Alfred Hitchcock",
        "cast": "Anthony Perkins, Janet Leigh, Vera Miles",
        "plot": "A Phoenix secretary embezzles $40,000 from her employer's client, goes on the run, and checks into a remote motel run by a young man under the domination of his mother."
    },
    {
        "id": 36,
        "title": "Casablanca",
        "year": 1942,
        "rating": 8.5,
        "cert": "PG",
        "duration": "102 min",
        "genre": "Drama Romance War",
        "director": "Michael Curtiz",
        "cast": "Humphrey Bogart, Ingrid Bergman, Paul Henreid",
        "plot": "A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover and her fugitive husband escape the Nazis in French Morocco."
    },
    {
        "id": 37,
        "title": "The Departed",
        "year": 2006,
        "rating": 8.5,
        "cert": "R",
        "duration": "151 min",
        "genre": "Crime Drama Thriller",
        "director": "Martin Scorsese",
        "cast": "Leonardo DiCaprio, Matt Damon, Jack Nicholson",
        "plot": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston."
    },
    {
        "id": 38,
        "title": "The Prestige",
        "year": 2006,
        "rating": 8.5,
        "cert": "PG-13",
        "duration": "130 min",
        "genre": "Drama Mystery Sci-Fi",
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Hugh Jackman, Scarlett Johansson",
        "plot": "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other."
    },
    {
        "id": 39,
        "title": "Memento",
        "year": 2000,
        "rating": 8.4,
        "cert": "R",
        "duration": "113 min",
        "genre": "Mystery Thriller",
        "director": "Christopher Nolan",
        "cast": "Guy Pearce, Carrie-Anne Moss, Joe Pantoliano",
        "plot": "A man with short-term memory loss attempts to track down his wife's murderer."
    },
    {
        "id": 40,
        "title": "Apocalypse Now",
        "year": 1979,
        "rating": 8.4,
        "cert": "R",
        "duration": "147 min",
        "genre": "Drama Mystery War",
        "director": "Francis Ford Coppola",
        "cast": "Martin Sheen, Marlon Brando, Robert Duvall",
        "plot": "A U.S. Army officer serving in Vietnam is tasked with assassinating a renegade Special Forces Colonel who sees himself as a god."
    },
    {
        "id": 41,
        "title": "Joker",
        "year": 2019,
        "rating": 8.4,
        "cert": "R",
        "duration": "122 min",
        "genre": "Crime Drama Thriller",
        "director": "Todd Phillips",
        "cast": "Joaquin Phoenix, Robert De Niro, Zazie Beetz",
        "plot": "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime."
    },
    {
        "id": 42,
        "title": "Django Unchained",
        "year": 2012,
        "rating": 8.4,
        "cert": "R",
        "duration": "165 min",
        "genre": "Drama Western",
        "director": "Quentin Tarantino",
        "cast": "Jamie Foxx, Christoph Waltz, Leonardo DiCaprio",
        "plot": "With the help of a German bounty hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner."
    },
    {
        "id": 43,
        "title": "WALL·E",
        "year": 2008,
        "rating": 8.4,
        "cert": "G",
        "duration": "98 min",
        "genre": "Animation Adventure Family",
        "director": "Andrew Stanton",
        "cast": "Ben Burtt, Elissa Knight, Jeff Garlin",
        "plot": "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind."
    },
    {
        "id": 44,
        "title": "Oldboy",
        "year": 2003,
        "rating": 8.4,
        "cert": "R",
        "duration": "120 min",
        "genre": "Action Drama Mystery",
        "director": "Park Chan-wook",
        "cast": "Choi Min-sik, Yoo Ji-tae, Kang Hye-jeong",
        "plot": "After being kidnapped and imprisoned for fifteen years, Oh Dae-Su is released, only to find that he must find his captor in five days."
    },
    {
        "id": 45,
        "title": "Once Upon a Time in America",
        "year": 1984,
        "rating": 8.4,
        "cert": "R",
        "duration": "229 min",
        "genre": "Crime Drama",
        "director": "Sergio Leone",
        "cast": "Robert De Niro, James Woods, Elizabeth McGovern",
        "plot": "A former Prohibition-era Jewish gangster returns to the Lower East Side of Manhattan over thirty years later, where he must confront the ghosts and regrets of his old life."
    },
    {
        "id": 46,
        "title": "Your Name",
        "year": 2016,
        "rating": 8.4,
        "cert": "PG",
        "duration": "106 min",
        "genre": "Animation Drama Fantasy",
        "director": "Makoto Shinkai",
        "cast": "Ryunosuke Kamiki, Mone Kamishiraishi, Ryo Narita",
        "plot": "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?"
    },
    {
        "id": 47,
        "title": "Avengers: Infinity War",
        "year": 2018,
        "rating": 8.4,
        "cert": "PG-13",
        "duration": "149 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "Anthony Russo",
        "cast": "Robert Downey Jr., Chris Hemsworth, Mark Ruffalo",
        "plot": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe."
    },
    {
        "id": 48,
        "title": "Das Boot",
        "year": 1981,
        "rating": 8.3,
        "cert": "R",
        "duration": "149 min",
        "genre": "Drama War",
        "director": "Wolfgang Petersen",
        "cast": "Jürgen Prochnow, Herbert Grönemeyer, Klaus Wennemann",
        "plot": "The claustrophobic world of a WWII German U-boat; boredom, filth and sheer terror."
    },
    {
        "id": 49,
        "title": "Amélie",
        "year": 2001,
        "rating": 8.3,
        "cert": "R",
        "duration": "122 min",
        "genre": "Comedy Romance",
        "director": "Jean-Pierre Jeunet",
        "cast": "Audrey Tautou, Mathieu Kassovitz, Rufus",
        "plot": "Amélie is an innocent and naive girl in Paris with her own sense of justice. She decides to help those around her and, along the way, discovers love."
    },
    {
        "id": 50,
        "title": "Toy Story 3",
        "year": 2010,
        "rating": 8.2,
        "cert": "G",
        "duration": "103 min",
        "genre": "Animation Adventure Comedy",
        "director": "Lee Unkrich",
        "cast": "Tom Hanks, Tim Allen, Joan Cusack",
        "plot": "The toys are mistakenly delivered to a day-care center instead of the attic right before Andy leaves for college, and it's up to Woody to convince the other toys that they weren't abandoned."
    },
    {
        "id": 51,
        "title": "Inglourious Basterds",
        "year": 2009,
        "rating": 8.3,
        "cert": "R",
        "duration": "153 min",
        "genre": "Adventure Drama War",
        "director": "Quentin Tarantino",
        "cast": "Brad Pitt, Diane Kruger, Eli Roth",
        "plot": "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans for the same."
    },
    {
        "id": 52,
        "title": "Good Will Hunting",
        "year": 1997,
        "rating": 8.3,
        "cert": "R",
        "duration": "126 min",
        "genre": "Drama Romance",
        "director": "Gus Van Sant",
        "cast": "Robin Williams, Matt Damon, Ben Affleck",
        "plot": "Will Hunting, a janitor at M.I.T., has a gift for mathematics, but needs help from a psychologist to find direction in his life."
    },
    {
        "id": 53,
        "title": "The Hunt",
        "year": 2012,
        "rating": 8.3,
        "cert": "R",
        "duration": "115 min",
        "genre": "Drama",
        "director": "Thomas Vinterberg",
        "cast": "Mads Mikkelsen, Thomas Bo Larsen, Annika Wedderkopp",
        "plot": "A teacher lives a lonely life, all the while struggling over his son's custody. His life slowly gets better as he finds love and receives good news from his son, but his new luck is about to be brutally shattered by an innocent little lie."
    },
    {
        "id": 54,
        "title": "Blade Runner 2049",
        "year": 2017,
        "rating": 8.0,
        "cert": "R",
        "duration": "164 min",
        "genre": "Action Drama Sci-Fi",
        "director": "Denis Villeneuve",
        "cast": "Ryan Gosling, Harrison Ford, Ana de Armas",
        "plot": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years."
    },
    {
        "id": 55,
        "title": "Arrival",
        "year": 2016,
        "rating": 7.9,
        "cert": "PG-13",
        "duration": "116 min",
        "genre": "Drama Sci-Fi",
        "director": "Denis Villeneuve",
        "cast": "Amy Adams, Jeremy Renner, Forest Whitaker",
        "plot": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world."
    },
    {
        "id": 56,
        "title": "Her",
        "year": 2013,
        "rating": 8.0,
        "cert": "R",
        "duration": "126 min",
        "genre": "Drama Romance Sci-Fi",
        "director": "Spike Jonze",
        "cast": "Joaquin Phoenix, Amy Adams, Scarlett Johansson",
        "plot": "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need."
    },
    {
        "id": 57,
        "title": "Ex Machina",
        "year": 2014,
        "rating": 7.7,
        "cert": "R",
        "duration": "108 min",
        "genre": "Drama Sci-Fi Thriller",
        "director": "Alex Garland",
        "cast": "Alicia Vikander, Domhnall Gleeson, Oscar Isaac",
        "plot": "A young programmer is selected to participate in a ground-breaking experiment in synthetic intelligence by evaluating the human qualities of a highly advanced humanoid A.I."
    },
    {
        "id": 58,
        "title": "Mad Max: Fury Road",
        "year": 2015,
        "rating": 8.1,
        "cert": "R",
        "duration": "120 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "George Miller",
        "cast": "Tom Hardy, Charlize Theron, Nicholas Hoult",
        "plot": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max."
    },
    {
        "id": 59,
        "title": "Knives Out",
        "year": 2019,
        "rating": 7.9,
        "cert": "PG-13",
        "duration": "130 min",
        "genre": "Comedy Crime Drama",
        "director": "Rian Johnson",
        "cast": "Daniel Craig, Chris Evans, Ana de Armas",
        "plot": "A detective investigates the death of a patriarch of an eccentric, combative family."
    },
    {
        "id": 60,
        "title": "Grand Budapest Hotel",
        "year": 2014,
        "rating": 8.1,
        "cert": "R",
        "duration": "99 min",
        "genre": "Adventure Comedy Crime",
        "director": "Wes Anderson",
        "cast": "Ralph Fiennes, F. Murray Abraham, Mathieu Amalric",
        "plot": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge."
    },
    {
        "id": 61,
        "title": "Gone Girl",
        "year": 2014,
        "rating": 8.1,
        "cert": "R",
        "duration": "149 min",
        "genre": "Drama Mystery Thriller",
        "director": "David Fincher",
        "cast": "Ben Affleck, Rosamund Pike, Neil Patrick Harris",
        "plot": "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent."
    },
    {
        "id": 62,
        "title": "Dune",
        "year": 2021,
        "rating": 8.0,
        "cert": "PG-13",
        "duration": "155 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "Denis Villeneuve",
        "cast": "Timothée Chalamet, Rebecca Ferguson, Zendaya",
        "plot": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future."
    },
    {
        "id": 63,
        "title": "1917",
        "year": 2019,
        "rating": 8.3,
        "cert": "R",
        "duration": "119 min",
        "genre": "Drama War",
        "director": "Sam Mendes",
        "cast": "Dean-Charles Chapman, George MacKay, Daniel Mays",
        "plot": "April 6th, 1917. As a regiment assembles to wage war deep in enemy territory, two soldiers are assigned to race against time and deliver a message that will stop 1,600 men from walking straight into a deadly trap."
    },
    {
        "id": 64,
        "title": "Ford v Ferrari",
        "year": 2019,
        "rating": 8.1,
        "cert": "PG-13",
        "duration": "152 min",
        "genre": "Action Biography Drama",
        "director": "James Mangold",
        "cast": "Matt Damon, Christian Bale, Jon Bernthal",
        "plot": "American car designer Carroll Shelby and driver Ken Miles battle corporate interference and the laws of physics to build a revolutionary race car for Ford in order to defeat Ferrari at the 24 Hours of Le Mans in 1966."
    },
    {
        "id": 65,
        "title": "Logan",
        "year": 2017,
        "rating": 8.1,
        "cert": "R",
        "duration": "137 min",
        "genre": "Action Drama Sci-Fi",
        "director": "James Mangold",
        "cast": "Hugh Jackman, Patrick Stewart, Dafne Keen",
        "plot": "In a future where mutants are nearly extinct, an elderly and weary Logan leads a quiet life. But when Laura, a mutant child pursued by scientists, comes to him for help, he must get her to safety."
    },
    {
        "id": 66,
        "title": "Spotlight",
        "year": 2015,
        "rating": 8.1,
        "cert": "R",
        "duration": "129 min",
        "genre": "Biography Crime Drama",
        "director": "Tom McCarthy",
        "cast": "Mark Ruffalo, Michael Keaton, Rachel McAdams",
        "plot": "The true story of how the Boston Globe uncovered the massive scandal of child molestation and cover-up within the local Catholic Archdiocese."
    },
    {
        "id": 67,
        "title": "Prisoners",
        "year": 2013,
        "rating": 8.1,
        "cert": "R",
        "duration": "153 min",
        "genre": "Crime Drama Mystery",
        "director": "Denis Villeneuve",
        "cast": "Hugh Jackman, Jake Gyllenhaal, Viola Davis",
        "plot": "When Keller Dover's daughter and her friend go missing, he takes matters into his own hands as the police pursue multiple leads and the pressure mounts."
    },
    {
        "id": 68,
        "title": "12 Years a Slave",
        "year": 2013,
        "rating": 8.1,
        "cert": "R",
        "duration": "134 min",
        "genre": "Biography Drama History",
        "director": "Steve McQueen",
        "cast": "Chiwetel Ejiofor, Michael Kenneth Williams, Michael Fassbender",
        "plot": "In the antebellum United States, Solomon Northup, a free black man from upstate New York, is abducted and sold into slavery."
    },
    {
        "id": 69,
        "title": "Warrior",
        "year": 2011,
        "rating": 8.2,
        "cert": "PG-13",
        "duration": "140 min",
        "genre": "Action Drama Sport",
        "director": "Gavin O'Connor",
        "cast": "Tom Hardy, Nick Nolte, Joel Edgerton",
        "plot": "The youngest son of an alcoholic former boxer returns home, where he's trained by his father for competition in a mixed martial arts tournament - a path that puts the fighter on a collision course with his estranged, older brother."
    },
    {
        "id": 70,
        "title": "V for Vendetta",
        "year": 2005,
        "rating": 8.1,
        "cert": "R",
        "duration": "132 min",
        "genre": "Action Drama Sci-Fi",
        "director": "James McTeigue",
        "cast": "Hugo Weaving, Natalie Portman, Rupert Graves",
        "plot": "In a future British tyranny, a shadowy freedom fighter, known only by the alias of 'V', plots to overthrow it with the help of a young woman."
    },
    {
        "id": 71,
        "title": "Howl's Moving Castle",
        "year": 2004,
        "rating": 8.2,
        "cert": "G",
        "duration": "119 min",
        "genre": "Animation Adventure Family",
        "director": "Hayao Miyazaki",
        "cast": "Chieko Baishô, Takuya Kimura, Tatsuya Gashûin",
        "plot": "When an unconfident young woman is cursed with an old body by a spiteful witch, her only chance of breaking the spell lies with a self-indulgent yet insecure young wizard and his companions in his legged, walking castle."
    },
    {
        "id": 72,
        "title": "A Beautiful Mind",
        "year": 2001,
        "rating": 8.2,
        "cert": "PG-13",
        "duration": "135 min",
        "genre": "Biography Drama",
        "director": "Ron Howard",
        "cast": "Russell Crowe, Ed Harris, Jennifer Connelly",
        "plot": "After John Nash, a brilliant but asocial mathematician, accepts secret work in cryptography, his life takes a turn for the nightmarish as he grapples with paranoia."
    },
    {
        "id": 73,
        "title": "Catch Me If You Can",
        "year": 2002,
        "rating": 8.1,
        "cert": "PG-13",
        "duration": "141 min",
        "genre": "Biography Crime Drama",
        "director": "Steven Spielberg",
        "cast": "Leonardo DiCaprio, Tom Hanks, Christopher Walken",
        "plot": "Barely 21 yet, Frank is a skilled forger who has passed as a doctor, lawyer and pilot. FBI agent Carl becomes obsessed with tracking down the con man, who only revels in the pursuit."
    },
    {
        "id": 74,
        "title": "No Country for Old Men",
        "year": 2007,
        "rating": 8.1,
        "cert": "R",
        "duration": "122 min",
        "genre": "Crime Drama Thriller",
        "director": "Ethan Coen",
        "cast": "Tommy Lee Jones, Javier Bardem, Josh Brolin",
        "plot": "Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and more than two million dollars in cash near the Rio Grande."
    },
    {
        "id": 75,
        "title": "Pan's Labyrinth",
        "year": 2006,
        "rating": 8.2,
        "cert": "R",
        "duration": "118 min",
        "genre": "Drama Fantasy War",
        "director": "Guillermo del Toro",
        "cast": "Ivana Baquero, Ariadna Gil, Sergi López",
        "plot": "In the Falangist Spain of 1944, the bookish young stepdaughter of a sadistic army officer escapes into an eerie but captivating fantasy world."
    },
    {
        "id": 76,
        "title": "There Will Be Blood",
        "year": 2007,
        "rating": 8.2,
        "cert": "R",
        "duration": "158 min",
        "genre": "Drama",
        "director": "Paul Thomas Anderson",
        "cast": "Daniel Day-Lewis, Paul Dano, Ciarán Hinds",
        "plot": "A story of family, religion, hatred, oil and madness, focusing on a turn-of-the-century prospector in the early days of the business."
    },
    {
        "id": 77,
        "title": "The Truman Show",
        "year": 1998,
        "rating": 8.1,
        "cert": "PG",
        "duration": "103 min",
        "genre": "Comedy Drama",
        "director": "Peter Weir",
        "cast": "Jim Carrey, Ed Harris, Laura Linney",
        "plot": "An insurance salesman discovers his whole life is actually a reality TV show."
    },
    {
        "id": 78,
        "title": "Trainspotting",
        "year": 1996,
        "rating": 8.1,
        "cert": "R",
        "duration": "93 min",
        "genre": "Drama",
        "director": "Danny Boyle",
        "cast": "Ewan McGregor, Ewen Bremner, Jonny Lee Miller",
        "plot": "Renton, deeply immersed in the Edinburgh drug scene, tries to clean up and get out, despite the allure of the drugs and influence of friends."
    },
    {
        "id": 79,
        "title": "Fargo",
        "year": 1996,
        "rating": 8.1,
        "cert": "R",
        "duration": "98 min",
        "genre": "Crime Drama Thriller",
        "director": "Joel Coen",
        "cast": "William H. Macy, Frances McDormand, Steve Buscemi",
        "plot": "Jerry Lundegaard's inept crime falls apart due to his and his henchmen's bungling and the persistent police work of the quite pregnant Marge Gunderson."
    },
    {
        "id": 80,
        "title": "Heat",
        "year": 1995,
        "rating": 8.2,
        "cert": "R",
        "duration": "170 min",
        "genre": "Action Crime Drama",
        "director": "Michael Mann",
        "cast": "Al Pacino, Robert De Niro, Val Kilmer",
        "plot": "A group of professional bank robbers start to feel the heat from police when they unknowingly leave a clue at their latest heist."
    },
    {
        "id": 81,
        "title": "Casino",
        "year": 1995,
        "rating": 8.2,
        "cert": "R",
        "duration": "178 min",
        "genre": "Crime Drama",
        "director": "Martin Scorsese",
        "cast": "Robert De Niro, Sharon Stone, Joe Pesci",
        "plot": "A tale of greed, deception, money, power, and murder occur between two best friends: a mafia enforcer and a casino executive compete against each other over a gambling empire, and over a fast living and fast loving socialite."
    },
    {
        "id": 82,
        "title": "Before Sunrise",
        "year": 1995,
        "rating": 8.1,
        "cert": "R",
        "duration": "101 min",
        "genre": "Drama Romance",
        "director": "Richard Linklater",
        "cast": "Ethan Hawke, Julie Delpy, Andrea Eckert",
        "plot": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. Unfortunately, both know that this will probably be their only night together."
    },
    {
        "id": 83,
        "title": "Princess Mononoke",
        "year": 1997,
        "rating": 8.4,
        "cert": "PG-13",
        "duration": "134 min",
        "genre": "Animation Action Adventure",
        "director": "Hayao Miyazaki",
        "cast": "Yôji Matsuda, Yuriko Ishida, Yûko Tanaka",
        "plot": "On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony."
    },
    {
        "id": 84,
        "title": "Eternal Sunshine",
        "year": 2004,
        "rating": 8.3,
        "cert": "R",
        "duration": "108 min",
        "genre": "Drama Romance Sci-Fi",
        "director": "Michel Gondry",
        "cast": "Jim Carrey, Kate Winslet, Tom Wilkinson",
        "plot": "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories."
    },
    {
        "id": 85,
        "title": "Finding Nemo",
        "year": 2003,
        "rating": 8.1,
        "cert": "G",
        "duration": "100 min",
        "genre": "Animation Adventure Comedy",
        "director": "Andrew Stanton",
        "cast": "Albert Brooks, Ellen DeGeneres, Alexander Gould",
        "plot": "After his son is captured in the Great Barrier Reef and taken to Sydney, a timid clownfish sets out on a journey to bring him home."
    },
    {
        "id": 86,
        "title": "Kill Bill: Vol. 1",
        "year": 2003,
        "rating": 8.1,
        "cert": "R",
        "duration": "111 min",
        "genre": "Action Crime Drama",
        "director": "Quentin Tarantino",
        "cast": "Uma Thurman, David Carradine, Daryl Hannah",
        "plot": "After awakening from a four-year coma, a former assassin wreaks vengeance on the team of assassins who betrayed her."
    },
    {
        "id": 87,
        "title": "Monsters, Inc.",
        "year": 2001,
        "rating": 8.1,
        "cert": "G",
        "duration": "92 min",
        "genre": "Animation Adventure Comedy",
        "director": "Pete Docter",
        "cast": "Billy Crystal, John Goodman, Mary Gibbs",
        "plot": "In order to power the city, monsters have to scare children so that they scream. However, the children are toxic to the monsters, and after a child gets through, two monsters realize things may not be what they think."
    },
    {
        "id": 88,
        "title": "Snatch",
        "year": 2000,
        "rating": 8.3,
        "cert": "R",
        "duration": "104 min",
        "genre": "Comedy Crime",
        "director": "Guy Ritchie",
        "cast": "Jason Statham, Brad Pitt, Benicio Del Toro",
        "plot": "Unscrupulous boxing promoters, violent bookmakers, a Russian gangster, incompetent amateur robbers and supposedly Jewish jewelers fight to track down a priceless stolen diamond."
    },
    {
        "id": 89,
        "title": "Requiem for a Dream",
        "year": 2000,
        "rating": 8.3,
        "cert": "R",
        "duration": "102 min",
        "genre": "Drama",
        "director": "Darren Aronofsky",
        "cast": "Ellen Burstyn, Jared Leto, Jennifer Connelly",
        "plot": "The drug-induced utopias of four Coney Island people are shattered when their addictions run deep."
    },
    {
        "id": 90,
        "title": "American Beauty",
        "year": 1999,
        "rating": 8.3,
        "cert": "R",
        "duration": "122 min",
        "genre": "Drama",
        "director": "Sam Mendes",
        "cast": "Kevin Spacey, Annette Bening, Thora Birch",
        "plot": "A sexually frustrated suburban father has a mid-life crisis after becoming infatuated with his daughter's best friend."
    },
    {
        "id": 91,
        "title": "The Sixth Sense",
        "year": 1999,
        "rating": 8.1,
        "cert": "PG-13",
        "duration": "107 min",
        "genre": "Drama Mystery Thriller",
        "director": "M. Night Shyamalan",
        "cast": "Bruce Willis, Haley Joel Osment, Toni Collette",
        "plot": "A boy who communicates with spirits seeks the help of a disheartened child psychologist."
    },
    {
        "id": 92,
        "title": "The Big Lebowski",
        "year": 1998,
        "rating": 8.1,
        "cert": "R",
        "duration": "117 min",
        "genre": "Comedy Crime",
        "director": "Joel Coen",
        "cast": "Jeff Bridges, John Goodman, Julianne Moore",
        "plot": "Jeff 'The Dude' Lebowski, mistaken for a millionaire of the same name, seeks restitution for his ruined rug and enlists his bowling buddies to help get it."
    },
    {
        "id": 93,
        "title": "L.A. Confidential",
        "year": 1997,
        "rating": 8.2,
        "cert": "R",
        "duration": "138 min",
        "genre": "Crime Drama Mystery",
        "director": "Curtis Hanson",
        "cast": "Kevin Spacey, Russell Crowe, Guy Pearce",
        "plot": "As corruption grows in 1950s Los Angeles, three policemen - one strait-laced, one brutal, and one sleazy - investigate a series of murders with their own brand of justice."
    },
    {
        "id": 94,
        "title": "Die Hard",
        "year": 1988,
        "rating": 8.2,
        "cert": "R",
        "duration": "132 min",
        "genre": "Action Thriller",
        "director": "John McTiernan",
        "cast": "Bruce Willis, Alan Rickman, Bonnie Bedelia",
        "plot": "An NYPD officer tries to save his wife and several others taken hostage by German terrorists during a Christmas party at the Nakatomi Plaza in Los Angeles."
    },
    {
        "id": 95,
        "title": "Full Metal Jacket",
        "year": 1987,
        "rating": 8.3,
        "cert": "R",
        "duration": "116 min",
        "genre": "Drama War",
        "director": "Stanley Kubrick",
        "cast": "Matthew Modine, R. Lee Ermey, Vincent D'Onofrio",
        "plot": "A pragmatic U.S. Marine observes the dehumanizing effects the Vietnam War has on his fellow recruits from their brutal boot camp training to the bloody street fighting in Hue."
    },
    {
        "id": 96,
        "title": "Scarface",
        "year": 1983,
        "rating": 8.3,
        "cert": "R",
        "duration": "170 min",
        "genre": "Crime Drama",
        "director": "Brian De Palma",
        "cast": "Al Pacino, Michelle Pfeiffer, Steven Bauer",
        "plot": "In 1980 Miami, a determined Cuban immigrant takes over a drug cartel and succumbs to greed."
    },
    {
        "id": 97,
        "title": "Taxi Driver",
        "year": 1976,
        "rating": 8.2,
        "cert": "R",
        "duration": "114 min",
        "genre": "Crime Drama",
        "director": "Martin Scorsese",
        "cast": "Robert De Niro, Jodie Foster, Cybill Shepherd",
        "plot": "A mentally unstable veteran works as a nighttime taxi driver in New York City, where the perceived decadence and sleaze fuels his urge for violent action."
    },
    {
        "id": 98,
        "title": "Chinatown",
        "year": 1974,
        "rating": 8.1,
        "cert": "R",
        "duration": "130 min",
        "genre": "Drama Mystery Thriller",
        "director": "Roman Polanski",
        "cast": "Jack Nicholson, Faye Dunaway, John Huston",
        "plot": "A private detective hired to expose an adulterer finds himself caught up in a web of deceit, corruption, and murder."
    },
    {
        "id": 99,
        "title": "A Clockwork Orange",
        "year": 1971,
        "rating": 8.3,
        "cert": "R",
        "duration": "136 min",
        "genre": "Crime Drama Sci-Fi",
        "director": "Stanley Kubrick",
        "cast": "Malcolm McDowell, Patrick Magee, Michael Bates",
        "plot": "In the future, a sadistic gang leader is imprisoned and volunteers for a conduct-aversion experiment, but it doesn't go as planned."
    },
    {
        "id": 100,
        "title": "2001: A Space Odyssey",
        "year": 1968,
        "rating": 8.3,
        "cert": "G",
        "duration": "149 min",
        "genre": "Adventure Sci-Fi",
        "director": "Stanley Kubrick",
        "cast": "Keir Dullea, Gary Lockwood, William Sylvester",
        "plot": "After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000."
    },
    {
        "id": 101,
        "title": "Everything Everywhere",
        "year": 2022,
        "rating": 7.9,
        "cert": "R",
        "duration": "139 min",
        "genre": "Action Adventure Sci-Fi",
        "director": "Daniel Kwan",
        "cast": "Michelle Yeoh, Stephanie Hsu, Ke Huy Quan",
        "plot": "A middle-aged Chinese immigrant is swept up into an insane adventure in which she alone can save the existence by exploring other universes and connecting with the lives she could have led."
    },
    {
        "id": 102,
        "title": "Oppenheimer",
        "year": 2023,
        "rating": 8.6,
        "cert": "R",
        "duration": "180 min",
        "genre": "Biography Drama History",
        "director": "Christopher Nolan",
        "cast": "Cillian Murphy, Emily Blunt, Matt Damon",
        "plot": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb."
    },
    {
        "id": 103,
        "title": "Barbie",
        "year": 2023,
        "rating": 7.0,
        "cert": "PG-13",
        "duration": "114 min",
        "genre": "Adventure Comedy Fantasy",
        "director": "Greta Gerwig",
        "cast": "Margot Robbie, Ryan Gosling, Issa Rae",
        "plot": "Barbie suffers a crisis that leads her to question her world and her existence."
    },
    {
        "id": 104,
        "title": "Top Gun: Maverick",
        "year": 2022,
        "rating": 8.3,
        "cert": "PG-13",
        "duration": "130 min",
        "genre": "Action Drama",
        "director": "Joseph Kosinski",
        "cast": "Tom Cruise, Jennifer Connelly, Miles Teller",
        "plot": "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on a mission that demands the ultimate sacrifice from those chosen to fly it."
    },
    {
        "id": 105,
        "title": "The Batman",
        "year": 2022,
        "rating": 7.8,
        "cert": "PG-13",
        "duration": "176 min",
        "genre": "Action Crime Drama",
        "director": "Matt Reeves",
        "cast": "Robert Pattinson, Zoë Kravitz, Jeffrey Wright",
        "plot": "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement."
    }
]

# =====================================================================
# PART 2: THEME & COLOR CONFIGURATIONS (LIGHT/DARK TOGGLE)
# =====================================================================
class Colors:
    """Dynamic Theme Colors supporting Dark and Light Modes."""
    mode = "dark"
    
    # Class attributes assigned dynamically below
    BG_MAIN = ""
    BG_SIDEBAR = ""
    SURFACE = ""
    SURFACE_HOVER = ""
    SURFACE_LIGHT = ""
    ACCENT = "#E50914"
    ACCENT_HOVER = "#F40612"
    TEXT_MAIN = ""
    TEXT_SUB = ""
    TEXT_MUTED = ""
    BORDER = ""
    SUCCESS = "#34C759"
    WARNING = "#FF9500"
    CERT_BOX = ""

    @classmethod
    def set_theme(cls, mode):
        cls.mode = mode
        if mode == "dark":
            cls.BG_MAIN = "#0F0F0F"
            cls.BG_SIDEBAR = "#141414"
            cls.SURFACE = "#1E1E1E"
            cls.SURFACE_HOVER = "#2D2D2D"
            cls.SURFACE_LIGHT = "#3A3A3A"
            cls.TEXT_MAIN = "#FFFFFF"
            cls.TEXT_SUB = "#B3B3B3"
            cls.TEXT_MUTED = "#808080"
            cls.BORDER = "#2B2B2B"
            cls.CERT_BOX = "#333333"
        else:
            cls.BG_MAIN = "#F5F5F7"         # Apple-like light grey
            cls.BG_SIDEBAR = "#FFFFFF"
            cls.SURFACE = "#FFFFFF"
            cls.SURFACE_HOVER = "#F0F0F0"
            cls.SURFACE_LIGHT = "#E5E5E5"
            cls.TEXT_MAIN = "#1D1D1F"       # Near black text
            cls.TEXT_SUB = "#515154"
            cls.TEXT_MUTED = "#86868B"
            cls.BORDER = "#D2D2D7"
            cls.CERT_BOX = "#E8E8ED"

# Initialize colors
Colors.set_theme("dark")

class Fonts:
    H1 = ("Segoe UI", 32, "bold")
    H2 = ("Segoe UI", 24, "bold")
    H3 = ("Segoe UI", 18, "bold")
    BODY_LARGE = ("Segoe UI", 14)
    BODY = ("Segoe UI", 11)
    BODY_SMALL = ("Segoe UI", 9)
    BODY_BOLD = ("Segoe UI", 11, "bold")
    META = ("Segoe UI", 10, "italic")

# =====================================================================
# PART 3: ADVANCED ML RECOMMENDATION ENGINE
# =====================================================================
class RecommendationEngine:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        self.setup_engine()

    def setup_engine(self):
        self.df['features'] = (
            self.df['genre'] + " " + 
            self.df['genre'] + " " + 
            self.df['genre'] + " " + 
            self.df['director'] + " " + 
            self.df['director'] + " " + 
            self.df['cast'] + " " + 
            self.df['plot']
        )
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['features'])
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()

    def get_recommendations(self, title, num_recommendations=10):
        if title not in self.indices: return []
        idx = self.indices[title]
        sim_scores = sorted(list(enumerate(self.cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:num_recommendations+1]
        
        results = []
        for i, score in sim_scores:
            movie_data = self.df.iloc[i].to_dict()
            match_val = min(99, max(50, round((score * 100) + random.randint(15, 30)))) 
            movie_data['match_score'] = match_val 
            results.append(movie_data)
        return results
    
    def get_filtered_movies(self, genre_filter="All Genres", rating_min=0, year_start=1900, year_end=2024, cert_filter="All", user_age=None):
        filtered = self.df.copy()
        if genre_filter and genre_filter != "All Genres":
            filtered = filtered[filtered['genre'].str.contains(genre_filter, case=False)]
        filtered = filtered[filtered['rating'] >= float(rating_min)]
        filtered = filtered[(filtered['year'] >= int(year_start)) & (filtered['year'] <= int(year_end))]
        if cert_filter and cert_filter != "All":
            filtered = filtered[filtered['cert'] == cert_filter]
            
        if user_age is not None and user_age > 0:
            allowed = ['G', 'U'] if user_age < 7 else ['G', 'U', 'PG', 'UA'] if user_age < 13 else ['G', 'U', 'PG', 'UA', 'PG-13', '12A'] if user_age < 17 else ['G', 'U', 'PG', 'UA', 'PG-13', '12A', 'R', 'A', 'MA']
            filtered = filtered[filtered['cert'].isin(allowed)]
            
        return filtered.sample(frac=1).head(25).to_dict('records')

    def get_all_titles(self): return sorted(self.df['title'].tolist())
    def get_all_genres(self): return sorted(list(set(g for g_str in self.df['genre'] for g in g_str.split())))
    def get_all_certs(self): return sorted(list(set(self.df['cert'])))


# =====================================================================
# PART 4: UTILITY & ANIMATION CLASSES
# =====================================================================
class Utils:
    @staticmethod
    def hex_to_rgb(hex_code):
        hex_code = hex_code.lstrip('#')
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(rgb):
        return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

    @staticmethod
    def blend_color(c1, c2, factor):
        rgb1 = Utils.hex_to_rgb(c1)
        rgb2 = Utils.hex_to_rgb(c2)
        r = rgb1[0] + (rgb2[0] - rgb1[0]) * factor
        g = rgb1[1] + (rgb2[1] - rgb1[1]) * factor
        b = rgb1[2] + (rgb2[2] - rgb1[2]) * factor
        return Utils.rgb_to_hex((r, g, b))

    @staticmethod
    def animate_color(widget, attribute, start_color, end_color, steps=15, duration=150):
        if not widget.winfo_exists(): return
        step_time = duration // steps
        for step in range(steps + 1):
            factor = step / steps
            current_color = Utils.blend_color(start_color, end_color, factor)
            widget.after(step_time * step, lambda c=current_color: Utils._apply_color(widget, attribute, c))

    @staticmethod
    def _apply_color(widget, attribute, color):
        # BUG FIX: Allow animation of custom 'bg_color' on RoundedCanvas
        if hasattr(widget, "set_bg_color") and attribute == "bg_color":
            widget.set_bg_color(color)
        else:
            try: widget[attribute] = color
            except tk.TclError: pass


# =====================================================================
# PART 5: CUSTOM UI WIDGETS (CANVAS-BASED UI FRAMEWORK)
# =====================================================================

class RoundedCanvas(tk.Canvas):
    """Draws a rounded rectangle without destroying embedded windows."""
    def __init__(self, parent, radius=20, bg=Colors.SURFACE, border_color=None, border_width=0, **kwargs):
        super().__init__(parent, bg=Colors.BG_MAIN, highlightthickness=0, **kwargs)
        self.radius = radius
        self.bg_color = bg
        self.border_color = border_color
        self.border_width = border_width
        self.rect_id = None
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.delete("bg_rect")
        self.rect_id = self.create_rounded_rect(0, 0, event.width, event.height, self.radius, 
                                                fill=self.bg_color, outline=self.border_color or "", 
                                                width=self.border_width, tags="bg_rect")
        self.tag_lower("bg_rect") # Keep background behind inner content

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def set_bg_color(self, new_color):
        self.bg_color = new_color
        if self.rect_id: self.itemconfig(self.rect_id, fill=new_color)

class ModernToggle(tk.Canvas):
    """Modern iOS style toggle switch."""
    def __init__(self, parent, variable, command=None, bg_color=None):
        super().__init__(parent, width=46, height=24, bg=bg_color, highlightthickness=0)
        self.variable = variable
        self.command = command
        
        self.bg_id = self.create_rounded_rect(2, 2, 44, 22, 10, fill=Colors.TEXT_MUTED)
        self.thumb_id = self.create_oval(4, 4, 20, 20, fill="white", outline="")
        
        self.bind("<Button-1>", self.toggle)
        self.update_ui()
        
    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def toggle(self, event):
        self.variable.set(not self.variable.get())
        self.update_ui()
        if self.command: self.command()
            
    def update_ui(self):
        if self.variable.get():
            self.itemconfig(self.bg_id, fill=Colors.SUCCESS)
            self.coords(self.thumb_id, 26, 4, 42, 20)
        else:
            self.itemconfig(self.bg_id, fill=Colors.TEXT_MUTED)
            self.coords(self.thumb_id, 4, 4, 20, 20)

class ModernSlider(tk.Canvas):
    """Modern pill-shaped slider widget."""
    def __init__(self, parent, variable, from_=0.0, to=9.0, command=None, bg_color=None):
        super().__init__(parent, height=30, bg=bg_color, highlightthickness=0)
        self.variable = variable
        self.from_ = from_
        self.to = to
        self.command = command
        self.bind("<Configure>", self.draw)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Button-1>", self.drag)
        self.bind("<ButtonRelease-1>", self.release)

    def draw(self, event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10: return
        
        # Track Background
        self.create_line(15, h/2, w-15, h/2, fill=Colors.SURFACE_LIGHT, width=6, capstyle="round")
        
        # Track Active Fill
        val = self.variable.get()
        pct = (val - self.from_) / (self.to - self.from_)
        x = 15 + pct * (w - 30)
        self.create_line(15, h/2, x, h/2, fill=Colors.ACCENT, width=6, capstyle="round")
        
        # Thumb & Value text
        self.create_oval(x-8, h/2-8, x+8, h/2+8, fill="white", outline=Colors.BORDER, width=1)
        self.create_text(w/2, 5, text=f"{val:.1f}+", fill=Colors.TEXT_SUB, font=("Segoe UI", 8, "bold"))

    def drag(self, event):
        w = self.winfo_width()
        x = min(max(event.x, 15), w-15)
        pct = (x - 15) / (w - 30)
        val = self.from_ + pct * (self.to - self.from_)
        # Step resolution of 0.5
        val = round(val * 2) / 2
        self.variable.set(val)
        self.draw()

    def release(self, event):
        if self.command: self.command()

class ModernButton(tk.Frame):
    def __init__(self, master, text, command=None, bg=None, hover_bg=None, fg=None, font=Fonts.BODY_BOLD, width=120, height=40, corner_radius=10, icon=None, **kwargs):
        super().__init__(master, bg=Colors.BG_MAIN)
        self.command = command
        self.bg_color = bg or Colors.SURFACE
        self.hover_color = hover_bg or Colors.SURFACE_HOVER
        self.fg_color = fg or Colors.TEXT_MAIN
        
        self.canvas = RoundedCanvas(self, radius=corner_radius, bg=self.bg_color, width=width, height=height)
        self.canvas.pack(fill="both", expand=True)
        
        display_text = f"{icon} {text}" if icon else text
        self.text_id = self.canvas.create_text(width/2, height/2, text=display_text, font=font, fill=self.fg_color, justify="center")
        
        for w in (self.canvas,):
            w.bind("<Enter>", self.on_enter)
            w.bind("<Leave>", self.on_leave)
            w.bind("<Button-1>", self.on_click)
            w.bind("<ButtonRelease-1>", self.on_release)
            self.canvas.tag_bind(self.text_id, "<Enter>", self.on_enter)
            self.canvas.tag_bind(self.text_id, "<Leave>", self.on_leave)
            self.canvas.tag_bind(self.text_id, "<Button-1>", self.on_click)
            self.canvas.tag_bind(self.text_id, "<ButtonRelease-1>", self.on_release)

    def on_enter(self, e):
        self.canvas.config(cursor="hand2")
        Utils.animate_color(self.canvas, "bg_color", self.bg_color, self.hover_color, steps=10, duration=100)

    def on_leave(self, e):
        self.canvas.config(cursor="")
        Utils.animate_color(self.canvas, "bg_color", self.hover_color, self.bg_color, steps=10, duration=100)

    def on_click(self, e): self.canvas.move(self.text_id, 0, 2)
    def on_release(self, e):
        self.canvas.move(self.text_id, 0, -2)
        if self.command: self.after(50, self.command)

class ScrollableFrame(tk.Frame):
    def __init__(self, container, bg_color, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # BUG FIX: Bind mousewheel ONLY when hovering over this specific canvas, to avoid modal scroll conflicts
        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)


# =====================================================================
# PART 6: MOVIE CARD & MODAL COMPONENTS
# =====================================================================
class MovieCard(tk.Frame):
    """Rich movie card with star ratings, badges, and progress bars."""
    def __init__(self, parent, movie_data, click_callback, fav_callback, is_fav=False):
        super().__init__(parent, bg=Colors.BG_MAIN, padx=5, pady=8)
        self.movie_data = movie_data
        self.click_callback = click_callback
        self.fav_callback = fav_callback
        self.is_fav = is_fav
        
        self.container = RoundedCanvas(self, radius=15, bg=Colors.SURFACE, height=155)
        self.container.pack(fill="both", expand=True)
        
        self.inner_frame = tk.Frame(self.container, bg=Colors.SURFACE)
        self.window_id = self.container.create_window((10, 10), window=self.inner_frame, anchor="nw")
        self.container.bind("<Configure>", lambda e: self.container.itemconfig(self.window_id, width=e.width-20), add="+")
        
        self.inner_frame.columnconfigure(1, weight=1) 
        
        # 0. Image Placeholder w/ Simulated Watch Progress
        self.img_frame = tk.Frame(self.inner_frame, bg=Colors.SURFACE, width=90, height=135)
        self.img_frame.grid(row=0, column=0, rowspan=5, padx=(0, 15))
        self.img_frame.pack_propagate(False)
        self.create_placeholder_image()
        
        # 1. Top Row: Match %, Cert, Tech Badges
        top_frame = tk.Frame(self.inner_frame, bg=Colors.SURFACE)
        top_frame.grid(row=0, column=1, sticky="w", pady=(2, 5))

        if movie_data.get('match_score'):
            color = Colors.SUCCESS if movie_data['match_score'] > 75 else Colors.WARNING
            tk.Label(top_frame, text=f"{movie_data['match_score']}% Match", font=("Segoe UI", 10, "bold"), fg=color, bg=Colors.SURFACE).pack(side="left", padx=(0, 10))

        tk.Label(top_frame, text=f" {movie_data['cert']} ", font=("Segoe UI", 8, "bold"), fg="white", bg=Colors.CERT_BOX).pack(side="left", padx=(0, 10))
        
        # Generate dynamic quality badge based on year
        quality = "4K" if int(movie_data['year']) >= 2017 else "HD"
        tk.Label(top_frame, text=f" {quality} ", font=("Segoe UI", 7, "bold"), fg=Colors.TEXT_MUTED, bg=Colors.SURFACE, highlightbackground=Colors.TEXT_MUTED, highlightthickness=1).pack(side="left", padx=(0, 10))
        tk.Label(top_frame, text=movie_data.get('duration', ''), font=Fonts.BODY_SMALL, fg=Colors.TEXT_SUB, bg=Colors.SURFACE).pack(side="left")

        # 2. Title & Year
        tk.Label(self.inner_frame, text=f"{movie_data['title']} ({movie_data['year']})", font=Fonts.BODY_LARGE, fg=Colors.TEXT_MAIN, bg=Colors.SURFACE, anchor="w").grid(row=1, column=1, sticky="ew")
        
        # 3. Star Ratings & Meta Data
        meta_frame = tk.Frame(self.inner_frame, bg=Colors.SURFACE)
        meta_frame.grid(row=2, column=1, sticky="ew", pady=(2, 5))
        
        rating_val = float(movie_data['rating'])
        stars = "★" * int(rating_val / 2) + "☆" * (5 - int(rating_val / 2))
        tk.Label(meta_frame, text=stars, font=("Segoe UI", 12), fg=Colors.WARNING, bg=Colors.SURFACE).pack(side="left", padx=(0, 8))
        tk.Label(meta_frame, text=f"{rating_val}/10  |  {movie_data['genre']}", font=Fonts.META, fg=Colors.TEXT_SUB, bg=Colors.SURFACE, anchor="w").pack(side="left")

        # 4. Plot Snippet
        plot = textwrap.shorten(movie_data['plot'], width=130, placeholder="...")
        tk.Label(self.inner_frame, text=plot, font=Fonts.BODY, fg=Colors.TEXT_MUTED, bg=Colors.SURFACE, justify="left", anchor="w").grid(row=3, column=1, sticky="ew")

        # 5. Actions (Heart & Play Icon)
        action_frame = tk.Frame(self.inner_frame, bg=Colors.SURFACE)
        action_frame.grid(row=0, column=2, rowspan=2, sticky="ne")
        
        self.btn_fav = tk.Button(action_frame, text="❤️" if is_fav else "🤍", font=("Segoe UI", 18), bg=Colors.SURFACE, fg=Colors.ACCENT, bd=0, cursor="hand2", command=self.toggle_fav, activebackground=Colors.SURFACE_HOVER, activeforeground=Colors.ACCENT_HOVER)
        self.btn_fav.pack(side="right", padx=5)
        
        self.bind_events(self.container)
        self.bind_events(self.inner_frame)

    def bind_events(self, widget):
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Button-1>", self.on_click)
        for child in widget.winfo_children():
            if child != self.btn_fav: self.bind_events(child)

    def create_placeholder_image(self):
        initial = self.movie_data['title'][0].upper()
        random.seed(self.movie_data['title']) 
        bg_col = random.choice(["#8E0000", "#002B5E", "#1b5e20", "#B33C00", "#3E147F", "#1A2226"])
        
        canvas = tk.Canvas(self.img_frame, bg=bg_col, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_polygon(0, 135, 90, 0, 90, 135, fill="black", stipple="gray50")
        
        if random.random() > 0.6:
            progress = random.randint(20, 80)
            canvas.create_rectangle(0, 130, 90, 135, fill="#444", outline="")
            canvas.create_rectangle(0, 130, (progress/100)*90, 135, fill=Colors.ACCENT, outline="")
            
        self.play_icon = canvas.create_text(45, 67, text="▶", font=("Segoe UI", 30), fill="white", state="hidden")
        self.title_initial = canvas.create_text(45, 60, text=initial, font=("Impact", 45), fill="white")
        random.seed()

    def toggle_fav(self):
        self.is_fav = not self.is_fav
        self.btn_fav.config(text="❤️" if self.is_fav else "🤍")
        self.fav_callback(self.movie_data)

    def on_enter(self, e):
        self.container.set_bg_color(Colors.SURFACE_HOVER)
        self._update_bg_color(self.inner_frame, Colors.SURFACE_HOVER)
        
        for widget in self.img_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.itemconfig(self.title_initial, state="hidden")
                widget.itemconfig(self.play_icon, state="normal")

    def on_leave(self, e):
        self.container.set_bg_color(Colors.SURFACE)
        self._update_bg_color(self.inner_frame, Colors.SURFACE)
        
        for widget in self.img_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.itemconfig(self.play_icon, state="hidden")
                widget.itemconfig(self.title_initial, state="normal")

    def _update_bg_color(self, widget, color):
        try: widget.config(bg=color)
        except tk.TclError: pass
        for child in widget.winfo_children():
            if child != self.btn_fav and not isinstance(child, tk.Canvas):
                try: child.config(bg=color)
                except: pass

    def on_click(self, e): self.click_callback(self.movie_data)


class MovieDetailsModal(tk.Toplevel):
    """A highly immersive modal resembling the official UI with full metadata."""
    def __init__(self, parent, movie_data, engine, fav_callback):
        super().__init__(parent)
        self.movie_data = movie_data
        self.engine = engine
        self.fav_callback = fav_callback
        
        self.title(movie_data['title'])
        self.geometry("900x750")
        self.configure(bg=Colors.BG_MAIN)
        self.transient(parent)
        self.grab_set()
        
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 450
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 375
        self.geometry(f"+{x}+{y}")
        self.build_ui()
        
    def build_ui(self):
        # --- Top Hero Banner Area ---
        if Colors.mode == "dark":
            gradient_opts = ["#2C0000", "#001A33", "#0F2600", "#331800", "#1D0A3B"]
            banner_bg = "#111"
        else:
            gradient_opts = ["#FFDDDD", "#DDEEFF", "#DDFFEA", "#FFEADD", "#EADDFF"]
            banner_bg = "#FFF"
            
        banner = tk.Canvas(self, height=280, bg=banner_bg, highlightthickness=0)
        banner.pack(fill="x")
        
        random.seed(self.movie_data['title'])
        gradient_color = random.choice(gradient_opts)
        banner.create_rectangle(0, 0, 900, 280, fill=gradient_color, outline="")
        banner.create_polygon(0, 280, 900, 0, 900, 280, fill=Colors.BG_MAIN, stipple="gray50")
        banner.create_rectangle(0, 180, 900, 280, fill=Colors.BG_MAIN, outline="", stipple="gray75") 
        
        banner.create_text(40, 200, text=self.movie_data['title'], font=("Segoe UI", 42, "bold"), fill=Colors.TEXT_MAIN, anchor="w")
        random.seed()
        
        # --- Main Content Scroll Area ---
        scroll_area = ScrollableFrame(self, bg_color=Colors.BG_MAIN)
        scroll_area.pack(fill="both", expand=True)
        content = scroll_area.scrollable_frame
        content.config(padx=40, pady=10)
        
        # --- Metadata & Badges Row ---
        meta_row = tk.Frame(content, bg=Colors.BG_MAIN)
        meta_row.pack(fill="x", pady=(0, 20))
        
        if self.movie_data.get('match_score'):
            tk.Label(meta_row, text=f"{self.movie_data['match_score']}% Match", font=Fonts.BODY_BOLD, fg=Colors.SUCCESS, bg=Colors.BG_MAIN).pack(side="left", padx=(0, 15))
            
        tk.Label(meta_row, text=self.movie_data['year'], font=Fonts.BODY, fg=Colors.TEXT_MAIN, bg=Colors.BG_MAIN).pack(side="left", padx=(0, 15))
        tk.Label(meta_row, text=f" {self.movie_data.get('cert','NR')} ", font=("Segoe UI", 8, "bold"), fg="white", bg=Colors.CERT_BOX).pack(side="left", padx=(0, 15))
        tk.Label(meta_row, text=self.movie_data.get('duration','120 min'), font=Fonts.BODY, fg=Colors.TEXT_MAIN, bg=Colors.BG_MAIN).pack(side="left", padx=(0, 15))
        
        # Tech Badges
        tech_font = ("Segoe UI", 8, "bold")
        tk.Label(meta_row, text=" HD " if int(self.movie_data['year']) < 2016 else " 4K Ultra HD ", font=tech_font, fg=Colors.TEXT_MUTED, bg=Colors.BG_MAIN, highlightbackground=Colors.TEXT_MUTED, highlightthickness=1).pack(side="left", padx=(0, 10))
        tk.Label(meta_row, text=" 5.1 " if int(self.movie_data['year']) < 2020 else " Spatial Audio ", font=tech_font, fg=Colors.TEXT_MUTED, bg=Colors.BG_MAIN, highlightbackground=Colors.TEXT_MUTED, highlightthickness=1).pack(side="left")
        
        # --- Action Buttons Row ---
        btn_frame = tk.Frame(content, bg=Colors.BG_MAIN)
        btn_frame.pack(fill="x", pady=(0, 25))
        
        play_lbl = "Resume" if random.random() > 0.5 else "Play"
        ModernButton(btn_frame, text=play_lbl, icon="▶", bg=Colors.TEXT_MAIN, fg=Colors.BG_MAIN, width=140, command=lambda: messagebox.showinfo("Player", f"Buffering {self.movie_data['title']}...")).pack(side="left", padx=(0, 15))
        
        action_btn_style = {"font": ("Segoe UI", 16), "bg": Colors.BG_MAIN, "fg": Colors.TEXT_MAIN, "bd": 0, "cursor": "hand2", "activebackground": Colors.BG_MAIN, "activeforeground": Colors.TEXT_SUB}
        tk.Button(btn_frame, text="↓", **action_btn_style, command=lambda: messagebox.showinfo("Download", "Downloading to device...")).pack(side="left", padx=(0, 15))
        tk.Button(btn_frame, text="+" if self.movie_data['title'] not in self.fav_callback.__self__.favorites else "✓", **action_btn_style, command=lambda: self.fav_callback(self.movie_data)).pack(side="left", padx=(0, 15))
        tk.Button(btn_frame, text="👍", **action_btn_style).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="👎", **action_btn_style).pack(side="left")

        # --- Details Split View ---
        info_frame = tk.Frame(content, bg=Colors.BG_MAIN)
        info_frame.pack(fill="x")
        info_frame.columnconfigure(0, weight=6)
        info_frame.columnconfigure(1, weight=4)
        
        # Left Side
        left_col = tk.Frame(info_frame, bg=Colors.BG_MAIN)
        left_col.grid(row=0, column=0, sticky="nsew", padding=(0, 0, 40, 0))
        
        tk.Label(left_col, text=self.movie_data['plot'], font=Fonts.BODY_LARGE, fg=Colors.TEXT_MAIN, bg=Colors.BG_MAIN, wraplength=480, justify="left", anchor="nw").pack(fill="x", pady=(0, 20))
        
        warnings = ["Violence", "Language", "Substances", "Nudity", "Fear"]
        sim_warnings = ", ".join(random.sample(warnings, k=random.randint(1, 3)))
        if self.movie_data['cert'] in ['G', 'PG', 'U']: sim_warnings = "Mild peril, Family friendly"
        
        warn_frame = tk.Frame(left_col, bg=Colors.BG_MAIN)
        warn_frame.pack(fill="x")
        tk.Label(warn_frame, text="Rating Reasons: ", font=Fonts.BODY_BOLD, fg=Colors.TEXT_SUB, bg=Colors.BG_MAIN).pack(side="left")
        tk.Label(warn_frame, text=sim_warnings, font=Fonts.BODY, fg=Colors.TEXT_MUTED, bg=Colors.BG_MAIN).pack(side="left")
        
        # Right Side
        right_col = tk.Frame(info_frame, bg=Colors.BG_MAIN)
        right_col.grid(row=0, column=1, sticky="nsew")
        
        self._build_right_meta_row(right_col, "Cast: ", self.movie_data.get('cast', 'Unknown'))
        self._build_right_meta_row(right_col, "Director: ", self.movie_data['director'])
        self._build_right_meta_row(right_col, "Genres: ", self.movie_data['genre'].replace(" ", ", "))
        self._build_right_meta_row(right_col, "Rating: ", f"{self.movie_data['rating']} / 10 IMDb")
        
        tk.Frame(content, bg=Colors.BORDER, height=1).pack(fill="x", pady=30)
        
        # --- More Like This Section ---
        tk.Label(content, text="More Like This", font=Fonts.H3, fg=Colors.TEXT_MAIN, bg=Colors.BG_MAIN).pack(anchor="w", pady=(0, 15))
        
        sim_frame = tk.Frame(content, bg=Colors.BG_MAIN)
        sim_frame.pack(fill="both", expand=True)
        
        col, row_idx = 0, 0
        for i, sim in enumerate(self.engine.get_recommendations(self.movie_data['title'], 6)):
            card_wrap = tk.Frame(sim_frame, bg=Colors.BG_MAIN)
            card_wrap.grid(row=row_idx, column=col, sticky="nsew", padx=10, pady=10)
            MovieCard(card_wrap, sim, self.open_new_modal, self.fav_callback).pack(fill="both", expand=True)
            
            col += 1
            if col > 1:
                col = 0
                row_idx += 1
                
        sim_frame.columnconfigure(0, weight=1)
        sim_frame.columnconfigure(1, weight=1)

    def _build_right_meta_row(self, parent, label, value):
        row = tk.Frame(parent, bg=Colors.BG_MAIN)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label, font=Fonts.BODY_SMALL, fg=Colors.TEXT_SUB, bg=Colors.BG_MAIN).pack(side="left", anchor="nw")
        tk.Label(row, text=value, font=Fonts.BODY_SMALL, fg=Colors.TEXT_MAIN, bg=Colors.BG_MAIN, wraplength=200, justify="left").pack(side="left", anchor="nw")

    def open_new_modal(self, new_movie_data):
        self.destroy()
        MovieDetailsModal(self.master, new_movie_data, self.engine, self.fav_callback)


# =====================================================================
# PART 7: SPLASH SCREEN & LOADING
# =====================================================================
class SplashScreen(tk.Toplevel):
    def __init__(self, parent, init_callback):
        super().__init__(parent)
        self.parent = parent
        self.init_callback = init_callback
        
        self.overrideredirect(True)
        self.geometry("500x300")
        self.configure(bg="#0F0F0F") 
        
        x = int((self.winfo_screenwidth()/2) - (500/2))
        y = int((self.winfo_screenheight()/2) - (300/2))
        self.geometry(f"+{x}+{y}")
        
        tk.Label(self, text="NETFLIX", font=("Impact", 50), fg="#E50914", bg="#0F0F0F").pack(expand=True, pady=(60, 0))
        tk.Label(self, text="ULTRA EDITION", font=("Segoe UI", 12, "bold"), fg="white", bg="#0F0F0F").pack(pady=(0, 20))
        
        self.bar_bg = tk.Frame(self, bg="#1E1E1E", width=400, height=4)
        self.bar_bg.pack(pady=(20, 10))
        self.bar_bg.pack_propagate(False)
        self.bar_fg = tk.Frame(self.bar_bg, bg="#E50914", width=0, height=4)
        self.bar_fg.pack(side="left", fill="y")
        
        self.status_lbl = tk.Label(self, text="Initializing Machine Learning Engine...", font=Fonts.BODY_SMALL, fg="#B3B3B3", bg="#0F0F0F")
        self.status_lbl.pack(pady=10)
        threading.Thread(target=self.run_init_task, daemon=True).start()

    def run_init_task(self):
        for msg, target in [("Loading DB...", 30), ("Vectorizing...", 60), ("Ready.", 100)]:
            self.parent.after(0, lambda m=msg: self.status_lbl.config(text=m))
            cw = self.bar_fg.winfo_width()
            tw = int((target / 100) * 400)
            for i in range(20):
                self.parent.after(0, lambda w=int(cw+((tw-cw)/20)*i): self.bar_fg.config(width=w))
                time.sleep(0.02)
        self.parent.after(300, lambda: [self.init_callback(), self.destroy()])

# =====================================================================
# PART 8: PROFILE SELECTION
# =====================================================================
class ProfileScreen(tk.Frame):
    def __init__(self, parent, on_select_callback):
        super().__init__(parent, bg=Colors.BG_MAIN)
        self.center_frame = tk.Frame(self, bg=Colors.BG_MAIN)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self.center_frame, text="Who's watching?", font=Fonts.H1, fg=Colors.TEXT_MAIN, bg=Colors.BG_MAIN).pack(pady=(0, 40))
        
        self.profile_row = tk.Frame(self.center_frame, bg=Colors.BG_MAIN)
        self.profile_row.pack()
        
        for name, color, is_kids in [("Adult", "#E50914", False), ("Kids", "#0071eb", True), ("Guest", "#555555", False)]:
            self.create_profile(name, color, is_kids)
            
        ModernButton(self.center_frame, text="MANAGE PROFILES", bg=Colors.BG_MAIN, fg=Colors.TEXT_SUB).pack(pady=(60, 0))

    def create_profile(self, name, color, is_kids):
        container = tk.Frame(self.profile_row, bg=Colors.BG_MAIN, padx=20)
        container.pack(side="left")
        
        canvas = tk.Canvas(container, width=150, height=150, bg=Colors.BG_MAIN, highlightthickness=0)
        canvas.pack()
        avatar_id = canvas.create_rectangle(0, 0, 150, 150, fill=color, outline=Colors.BG_MAIN, width=3)
        canvas.create_text(75, 75, text=name[0], font=("Segoe UI", 60, "bold"), fill="white")
        
        lbl = tk.Label(container, text=name, font=Fonts.BODY_LARGE, fg=Colors.TEXT_SUB, bg=Colors.BG_MAIN)
        lbl.pack(pady=(10, 0))
        
        for w in (canvas, lbl):
            w.bind("<Enter>", lambda e: [canvas.itemconfig(avatar_id, outline=Colors.TEXT_MAIN), lbl.config(fg=Colors.TEXT_MAIN), canvas.config(cursor="hand2")])
            w.bind("<Leave>", lambda e: [canvas.itemconfig(avatar_id, outline=Colors.BG_MAIN), lbl.config(fg=Colors.TEXT_SUB), canvas.config(cursor="")])
            w.bind("<Button-1>", lambda e: self.master.on_profile_selected(name, is_kids))


# =====================================================================
# PART 9: SIDEBAR NAVIGATION & FILTERS
# =====================================================================
class Sidebar(tk.Frame):
    def __init__(self, parent, engine, on_filter_change, on_tab_change):
        super().__init__(parent, bg=Colors.BG_SIDEBAR, width=250)
        self.pack_propagate(False)
        self.engine, self.on_filter_change, self.on_tab_change = engine, on_filter_change, on_tab_change
        self.active_btn = None
        
        tk.Label(self, text="NETFLIX", font=("Impact", 30), fg=Colors.ACCENT, bg=Colors.BG_SIDEBAR).pack(pady=(30, 20))
        
        self.nav_frame = tk.Frame(self, bg=Colors.BG_SIDEBAR)
        self.nav_frame.pack(fill="x", pady=10)
        self.btn_home = self.create_nav_btn("🏠 Home", "home")
        self.btn_fav = self.create_nav_btn("❤️ My List", "favorites")
        self.btn_settings = self.create_nav_btn("⚙️ Settings", "settings")
        self.set_active_tab(self.btn_home)
        
        tk.Frame(self, bg=Colors.BORDER, height=1).pack(fill="x", padx=20, pady=20)
        
        self.filter_canvas = tk.Canvas(self, bg=Colors.BG_SIDEBAR, highlightthickness=0)
        self.filter_frame = tk.Frame(self.filter_canvas, bg=Colors.BG_SIDEBAR)
        self.filter_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.filter_canvas.yview)
        self.filter_canvas.configure(yscrollcommand=self.filter_scrollbar.set)
        
        self.filter_scrollbar.pack(side="right", fill="y")
        self.filter_canvas.pack(side="left", fill="both", expand=True)
        self.filter_canvas.create_window((0, 0), window=self.filter_frame, anchor="nw", width=230)
        self.filter_frame.bind("<Configure>", lambda e: self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all")))

        tk.Label(self.filter_frame, text="DISCOVER", font=("Segoe UI", 10, "bold"), fg=Colors.TEXT_MUTED, bg=Colors.BG_SIDEBAR).pack(anchor="w", padx=20, pady=(0, 10))
        self.build_filters()

    def create_nav_btn(self, text, tab_name):
        btn = tk.Button(self.nav_frame, text=text, font=Fonts.BODY_LARGE, bg=Colors.BG_SIDEBAR, fg=Colors.TEXT_SUB, anchor="w", padx=20, pady=10, bd=0, activebackground=Colors.SURFACE_HOVER, activeforeground=Colors.TEXT_MAIN, cursor="hand2")
        btn.config(command=lambda b=btn, t=tab_name: [self.set_active_tab(b), self.on_tab_change(t)])
        btn.pack(fill="x")
        btn.bind("<Enter>", lambda e, b=btn: b.config(fg=Colors.TEXT_MAIN) if b != self.active_btn else None)
        btn.bind("<Leave>", lambda e, b=btn: b.config(fg=Colors.TEXT_SUB) if b != self.active_btn else None)
        return btn

    def set_active_tab(self, active_btn):
        if self.active_btn: self.active_btn.config(fg=Colors.TEXT_SUB, font=Fonts.BODY_LARGE)
        self.active_btn = active_btn
        self.active_btn.config(fg=Colors.TEXT_MAIN, font=("Segoe UI", 14, "bold"))

    def build_filters(self):
        self.create_label("Genre")
        self.genre_var = tk.StringVar(value="All Genres")
        self.cb_genre = ttk.Combobox(self.filter_frame, textvariable=self.genre_var, values=["All Genres"] + self.engine.get_all_genres(), state="readonly")
        self.cb_genre.pack(padx=20, fill="x", pady=(0,15))
        self.cb_genre.bind("<<ComboboxSelected>>", self.trigger_filter)

        self.create_label("Minimum Rating")
        self.rating_var = tk.DoubleVar(value=0.0)
        self.scale_rating = ModernSlider(self.filter_frame, variable=self.rating_var, from_=0.0, to=9.0, command=self.trigger_filter, bg_color=Colors.BG_SIDEBAR)
        self.scale_rating.pack(padx=20, fill="x", pady=(0,15))

        self.create_label("Year Range")
        year_frame = tk.Frame(self.filter_frame, bg=Colors.BG_SIDEBAR)
        year_frame.pack(padx=20, fill="x", pady=(0,15))
        self.year_from_var, self.year_to_var = tk.StringVar(value="1960"), tk.StringVar(value="2024")
        years = [str(y) for y in range(1930, 2025)]
        
        self.cb_from = ttk.Combobox(year_frame, textvariable=self.year_from_var, values=years, width=5)
        self.cb_from.pack(side="left", fill="x", expand=True)
        tk.Label(year_frame, text=" - ", bg=Colors.BG_SIDEBAR, fg=Colors.TEXT_SUB).pack(side="left")
        self.cb_to = ttk.Combobox(year_frame, textvariable=self.year_to_var, values=years, width=5)
        self.cb_to.pack(side="left", fill="x", expand=True)
        self.cb_from.bind("<<ComboboxSelected>>", self.trigger_filter)
        self.cb_to.bind("<<ComboboxSelected>>", self.trigger_filter)

        self.create_label("Certification")
        self.cert_var = tk.StringVar(value="All")
        self.cb_cert = ttk.Combobox(self.filter_frame, textvariable=self.cert_var, values=["All"] + self.engine.get_all_certs(), state="readonly")
        self.cb_cert.pack(padx=20, fill="x", pady=(0,15))
        self.cb_cert.bind("<<ComboboxSelected>>", self.trigger_filter)
        
        self.lbl_kids_mode = tk.Label(self.filter_frame, text="KIDS MODE ACTIVE", font=Fonts.BODY_SMALL, fg=Colors.ACCENT, bg=Colors.BG_SIDEBAR)

    def create_label(self, text): tk.Label(self.filter_frame, text=text, font=Fonts.BODY_SMALL, fg=Colors.TEXT_SUB, bg=Colors.BG_SIDEBAR).pack(anchor="w", padx=20, pady=(0, 5))

    def trigger_filter(self, event=None):
        self.on_filter_change(genre=self.genre_var.get(), rating=self.rating_var.get(), year_start=self.year_from_var.get(), year_end=self.year_to_var.get(), cert=self.cert_var.get())

    def force_kids_mode(self, is_kids):
        if is_kids:
            self.cert_var.set("PG")
            self.cb_cert.config(state="disabled")
            self.lbl_kids_mode.pack(padx=20, pady=10)
        else:
            self.cb_cert.config(state="readonly")
            self.lbl_kids_mode.pack_forget()

# =====================================================================
# PART 10: MAIN APPLICATION ORCHESTRATOR
# =====================================================================
class NetflixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("Netflix Ultra - Deep Search Engine")
        self.geometry("1400x900")
        self.eval('tk::PlaceWindow . center')
        
        self.favorites = set()
        self.current_tab = "home"
        self.active_profile = None
        self.is_kids_profile = False
        
        self.setup_styles()
        SplashScreen(self, self.initialize_engine)

    def setup_styles(self):
        self.configure(bg=Colors.BG_MAIN)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=Colors.SURFACE_LIGHT, background=Colors.SURFACE, foreground=Colors.TEXT_MAIN, bordercolor=Colors.BORDER, arrowcolor=Colors.TEXT_MAIN)
        style.map("TCombobox", fieldbackground=[("readonly", Colors.SURFACE_LIGHT)])
        
        # Search Box Special Style
        style.configure("Search.TCombobox", fieldbackground=Colors.SURFACE_LIGHT, background=Colors.SURFACE_LIGHT, foreground=Colors.TEXT_MAIN, borderwidth=0, arrowcolor=Colors.TEXT_SUB)
        
        self.option_add('*TCombobox*Listbox.background', Colors.SURFACE)
        self.option_add('*TCombobox*Listbox.foreground', Colors.TEXT_MAIN)
        self.option_add('*TCombobox*Listbox.selectBackground', Colors.ACCENT)
        
        style.configure("Vertical.TScrollbar", gripcount=0, background=Colors.SURFACE_LIGHT, darkcolor=Colors.BG_MAIN, lightcolor=Colors.BG_MAIN, troughcolor=Colors.BG_MAIN, bordercolor=Colors.BG_MAIN, arrowcolor=Colors.TEXT_MAIN)

    def initialize_engine(self):
        self.engine = RecommendationEngine(MOVIE_DB)
        self.deiconify()
        self.show_profile_screen()

    def show_profile_screen(self):
        self.profile_screen = ProfileScreen(self, self.on_profile_selected)
        self.profile_screen.pack(fill="both", expand=True)

    def on_profile_selected(self, profile_name, is_kids):
        self.active_profile, self.is_kids_profile = profile_name, is_kids
        self.profile_screen.destroy()
        self.build_main_dashboard()

    def rebuild_ui(self):
        self.sidebar.destroy()
        self.main_area.destroy()
        self.setup_styles()
        self.build_main_dashboard()
        if self.current_tab == "settings":
            self.switch_tab("settings")
            self.sidebar.set_active_tab(self.sidebar.btn_settings)

    def build_main_dashboard(self):
        self.sidebar = Sidebar(self, self.engine, self.apply_filters, self.switch_tab)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.force_kids_mode(self.is_kids_profile)
        
        self.main_area = tk.Frame(self, bg=Colors.BG_MAIN)
        self.main_area.pack(side="right", fill="both", expand=True)
        
        self.create_header()
        self.create_hero()
        
        self.lbl_section_title = tk.Label(self.main_area, text="Trending Now", font=Fonts.H2, bg=Colors.BG_MAIN, fg=Colors.TEXT_MAIN)
        self.lbl_section_title.pack(anchor="w", padx=40, pady=(10, 15))
        
        self.scroll_container = ScrollableFrame(self.main_area, bg_color=Colors.BG_MAIN)
        self.scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        self.results_frame = self.scroll_container.scrollable_frame
        
        self.settings_frame = tk.Frame(self.main_area, bg=Colors.BG_MAIN)
        self.build_settings_page()
        
        self.show_home_default()

    def create_header(self):
        header = tk.Frame(self.main_area, bg=Colors.BG_MAIN, height=80)
        header.pack(fill="x", padx=40, pady=20)
        
        search_bg = RoundedCanvas(header, radius=22, bg=Colors.SURFACE_LIGHT, border_color=Colors.BORDER, border_width=1, width=600, height=45)
        search_bg.pack(side="left")
        search_bg.pack_propagate(False)
        
        tk.Label(search_bg, text="🔍", font=("Segoe UI", 12), bg=Colors.SURFACE_LIGHT, fg=Colors.TEXT_SUB).pack(side="left", padx=(15, 5))
        
        self.search_var = tk.StringVar()
        self.search_box = ttk.Combobox(search_bg, textvariable=self.search_var, font=Fonts.BODY, style="Search.TCombobox")
        self.search_box.pack(side="left", fill="both", expand=True, pady=10, padx=(0, 5))
        
        clear_btn = tk.Label(search_bg, text="✖", font=Fonts.BODY_BOLD, bg=Colors.SURFACE_LIGHT, fg=Colors.TEXT_MUTED, cursor="hand2")
        clear_btn.pack(side="right", padx=15)
        clear_btn.bind("<Button-1>", lambda e: [self.search_var.set(""), self.update_search_list(e)])
        
        self.search_box.bind("<KeyRelease>", self.update_search_list)
        self.search_box.bind("<<ComboboxSelected>>", self.on_search_enter)
        self.search_box.bind("<Return>", self.on_search_enter)
        
        profile_frame = tk.Frame(header, bg=Colors.BG_MAIN)
        profile_frame.pack(side="right")
        tk.Label(profile_frame, text=self.active_profile, font=Fonts.BODY_BOLD, fg=Colors.TEXT_MAIN, bg=Colors.BG_MAIN).pack(side="left", padx=10)
        avatar = RoundedCanvas(profile_frame, radius=5, bg="#0071eb" if self.is_kids_profile else Colors.ACCENT, width=40, height=40)
        avatar.pack(side="left")
        avatar.create_text(20, 20, text=self.active_profile[0], font=Fonts.BODY_BOLD, fill="white")

    def build_settings_page(self):
        tk.Label(self.settings_frame, text="Account & App Settings", font=Fonts.H1, bg=Colors.BG_MAIN, fg=Colors.TEXT_MAIN).pack(anchor="w", padx=40, pady=(40, 20))
        
        content = RoundedCanvas(self.settings_frame, radius=20, bg=Colors.SURFACE, height=550)
        content.pack(fill="x", padx=40)
        content.pack_propagate(False)
        
        inner = tk.Frame(content, bg=Colors.SURFACE)
        content.create_window((30, 30), window=inner, anchor="nw")
        
        tk.Label(inner, text="Membership Details", font=Fonts.H3, bg=Colors.SURFACE, fg=Colors.TEXT_MAIN).grid(row=0, column=0, sticky="w", pady=(0, 10))
        tk.Label(inner, text="user@example.com\nPassword: ********\nPlan: Ultra HD 4K", justify="left", font=Fonts.BODY, bg=Colors.SURFACE, fg=Colors.TEXT_SUB).grid(row=1, column=0, sticky="w")
        ModernButton(inner, text="Update Billing", bg=Colors.SURFACE_LIGHT, fg=Colors.TEXT_MAIN, width=150).grid(row=1, column=1, padx=40, sticky="n")
        
        tk.Frame(inner, bg=Colors.BORDER, height=1, width=800).grid(row=2, column=0, columnspan=3, sticky="ew", pady=25)
        
        tk.Label(inner, text="App Preferences", font=Fonts.H3, bg=Colors.SURFACE, fg=Colors.TEXT_MAIN).grid(row=3, column=0, sticky="w", pady=(0, 15))
        
        auto_frame = tk.Frame(inner, bg=Colors.SURFACE)
        auto_frame.grid(row=4, column=0, sticky="w", pady=5)
        self.autoplay_var = tk.BooleanVar(value=True)
        ModernToggle(auto_frame, variable=self.autoplay_var, bg_color=Colors.SURFACE).pack(side="left", padx=(0, 15))
        tk.Label(auto_frame, text="Autoplay next episode", bg=Colors.SURFACE, fg=Colors.TEXT_SUB, font=Fonts.BODY).pack(side="left")
        
        theme_frame = tk.Frame(inner, bg=Colors.SURFACE)
        theme_frame.grid(row=5, column=0, sticky="w", pady=10)
        self.is_light_mode = tk.BooleanVar(value=(Colors.mode == "light"))
        ModernToggle(theme_frame, variable=self.is_light_mode, command=self.toggle_theme, bg_color=Colors.SURFACE).pack(side="left", padx=(0, 15))
        tk.Label(theme_frame, text="Light Theme Mode", bg=Colors.SURFACE, fg=Colors.TEXT_SUB, font=Fonts.BODY).pack(side="left")
        
        age_frame = tk.Frame(inner, bg=Colors.SURFACE)
        age_frame.grid(row=6, column=0, sticky="w", pady=10)
        self.age_restricted_var = tk.BooleanVar(value=self.is_kids_profile)
        ModernToggle(age_frame, variable=self.age_restricted_var, command=self.toggle_age_restriction, bg_color=Colors.SURFACE).pack(side="left", padx=(0, 15))
        tk.Label(age_frame, text="Age Restricted Content (Kids Mode)", bg=Colors.SURFACE, fg=Colors.TEXT_SUB, font=Fonts.BODY).pack(side="left")
        
        tk.Frame(inner, bg=Colors.BORDER, height=1, width=800).grid(row=7, column=0, columnspan=3, sticky="ew", pady=25)
        ModernButton(inner, text="Switch Profile", bg=Colors.ACCENT, fg="white", command=lambda: [self.sidebar.destroy(), self.main_area.destroy(), self.show_profile_screen()]).grid(row=8, column=0, sticky="w")

    def toggle_theme(self):
        mode = "light" if self.is_light_mode.get() else "dark"
        Colors.set_theme(mode)
        self.rebuild_ui()

    def toggle_age_restriction(self):
        self.is_kids_profile = self.age_restricted_var.get()
        self.sidebar.force_kids_mode(self.is_kids_profile)
        if self.current_tab in ["home", "browse"]:
            self.show_home_default()

    def create_hero(self):
        self.hero_frame = RoundedCanvas(self.main_area, radius=20, bg=Colors.SURFACE, height=320)
        self.hero_frame.pack(fill="x", padx=40, pady=(0, 20))
        self.hero_frame.pack_propagate(False)
        
        self.hero_bg = tk.Canvas(self.hero_frame, bg=Colors.SURFACE, highlightthickness=0)
        self.hero_bg.place(relwidth=1, relheight=1)
        self.hero_bg_rect = self.hero_bg.create_rectangle(0, 0, 300, 350, fill=Colors.SURFACE_HOVER, outline="")
        
        inner = tk.Frame(self.hero_frame, bg=Colors.SURFACE)
        self.hero_bg.create_window((40, 35), window=inner, anchor="nw")
        
        top_row = tk.Frame(inner, bg=Colors.SURFACE)
        top_row.pack(anchor="w")
        tk.Label(top_row, text="N", font=("Impact", 16), fg=Colors.ACCENT, bg=Colors.SURFACE).pack(side="left")
        tk.Label(top_row, text=" F E A T U R E D", font=Fonts.BODY_BOLD, fg=Colors.TEXT_MUTED, bg=Colors.SURFACE).pack(side="left")
        
        self.lbl_hero_title = tk.Label(inner, text="", font=Fonts.H1, bg=Colors.SURFACE, fg=Colors.TEXT_MAIN)
        self.lbl_hero_title.pack(anchor="w", pady=(5, 0))
        self.lbl_hero_info = tk.Label(inner, text="", font=Fonts.BODY_BOLD, bg=Colors.SURFACE, fg=Colors.SUCCESS)
        self.lbl_hero_info.pack(anchor="w", pady=5)
        
        self.lbl_hero_desc = tk.Label(inner, text="", font=Fonts.BODY, bg=Colors.SURFACE, fg=Colors.TEXT_SUB, wraplength=950, justify="left")
        self.lbl_hero_desc.pack(anchor="w", pady=(5, 20))
        
        btn_row = tk.Frame(inner, bg=Colors.SURFACE)
        btn_row.pack(anchor="w")
        self.btn_hero_play = ModernButton(btn_row, text="Play", icon="▶", bg=Colors.TEXT_MAIN, fg=Colors.BG_MAIN, width=120)
        self.btn_hero_play.pack(side="left", padx=(0, 15))
        self.btn_hero_info = ModernButton(btn_row, text="More Info", icon="ⓘ", bg=Colors.SURFACE_LIGHT, fg=Colors.TEXT_MAIN, width=140)
        self.btn_hero_info.pack(side="left")
        
        self.set_hero_movie(random.choice(MOVIE_DB))

    def set_hero_movie(self, movie):
        random.seed(movie['title'])
        if Colors.mode == "dark":
            bg_opts = ["#2D1313", "#131E2D", "#132D1A", "#2D1A13", "#22132D", Colors.SURFACE_HOVER]
        else:
            bg_opts = ["#FFEEEE", "#EEF5FF", "#EEFFE5", "#FFF3EE", "#F9EEFF", Colors.SURFACE_HOVER]
        
        self.hero_bg.itemconfig(self.hero_bg_rect, fill=random.choice(bg_opts))
        random.seed()
        
        self.lbl_hero_title.config(text=movie['title'])
        self.lbl_hero_info.config(text=f"{movie['year']}   |   {movie.get('cert','NR')}   |   {movie.get('duration','Unknown')}   |   ⭐ {movie['rating']}")
        self.lbl_hero_desc.config(text=textwrap.shorten(movie['plot'], width=220, placeholder="..."))
        self.btn_hero_play.command = lambda: messagebox.showinfo("Playing", f"Playing {movie['title']}")
        self.btn_hero_info.command = lambda: self.on_movie_select(movie)

    def update_search_list(self, event):
        if event.keysym in ['Up', 'Down', 'Return', 'Left', 'Right', 'Escape']: return
        typed = self.search_box.get().lower()
        all_titles = self.engine.get_all_titles()
        if not typed:
            self.search_box['values'] = all_titles
        else:
            filtered = [t for t in all_titles if typed in t.lower()]
            self.search_box['values'] = filtered
            if filtered:
                try: self.search_box.event_generate('<Down>')
                except: pass

    def on_search_enter(self, event=None):
        query = self.search_var.get().strip()
        if not query: return
        movie_obj = next((i for i in MOVIE_DB if i["title"].lower() == query.lower()), None) or next((i for i in MOVIE_DB if query.lower() in i["title"].lower()), None)
        if movie_obj:
            self.search_box.set('') 
            self.master.focus()
            self.set_hero_movie(movie_obj)
            self.on_movie_select(movie_obj)
        else:
            messagebox.showwarning("Not Found", "We couldn't find a movie matching that title.")

    def show_skeleton_loaders(self):
        for widget in self.results_frame.winfo_children(): widget.destroy()
        for _ in range(4):
            skel = RoundedCanvas(self.results_frame, radius=15, bg=Colors.SURFACE_LIGHT, height=140)
            skel.pack(fill="x", pady=5)
            
            def shimmer(canvas=skel, toggle=True):
                if not canvas.winfo_exists(): return
                Utils.animate_color(canvas, "bg_color", canvas.bg_color, Colors.SURFACE_HOVER if toggle else Colors.SURFACE_LIGHT, steps=5, duration=500)
                # BUG FIX: Bind arguments appropriately inside lambda to prevent scope bleed
                self.after(600, lambda c=canvas, t=not toggle: shimmer(c, t))
            shimmer()
            
        self.update_idletasks()

    def render_movies(self, movie_list):
        for widget in self.results_frame.winfo_children(): widget.destroy()
        if not movie_list:
            tk.Label(self.results_frame, text="No matches found for your criteria.", font=Fonts.BODY_LARGE, fg=Colors.TEXT_SUB, bg=Colors.BG_MAIN).pack(pady=50)
            return
        for movie in movie_list:
            MovieCard(self.results_frame, movie, self.on_movie_select, self.on_toggle_fav, is_fav=movie['title'] in self.favorites).pack(fill="x", pady=5)

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        if tab_name == "settings":
            self.scroll_container.pack_forget()
            self.lbl_section_title.pack_forget()
            self.hero_frame.pack_forget()
            self.settings_frame.pack(fill="both", expand=True)
            return
        
        self.settings_frame.pack_forget()
        self.hero_frame.pack(fill="x", padx=40, pady=(0, 20))
        self.lbl_section_title.pack(anchor="w", padx=40, pady=(10, 15))
        self.scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        if tab_name == "home":
            self.lbl_section_title.config(text="Trending & Recommended")
            self.show_skeleton_loaders()
            self.after(400, lambda: self.render_movies(self.engine.get_filtered_movies(user_age=10 if self.is_kids_profile else None)))
        elif tab_name == "favorites":
            self.lbl_section_title.config(text="My Watchlist")
            self.render_movies([m for m in MOVIE_DB if m['title'] in self.favorites])

    def show_home_default(self):
        self.sidebar.set_active_tab(self.sidebar.btn_home)
        self.switch_tab("home")

    def apply_filters(self, genre, rating, year_start, year_end, cert):
        if self.current_tab == "settings":
            self.sidebar.set_active_tab(self.sidebar.btn_home)
            self.switch_tab("home")
            
        self.current_tab = "browse"
        self.lbl_section_title.config(text=f"Exploring: {genre}")
        try: y_s, y_e = int(year_start), int(year_end)
        except: y_s, y_e = 1900, 2025
        
        self.show_skeleton_loaders()
        self.after(400, lambda: self.render_movies(self.engine.get_filtered_movies(genre, rating, y_s, y_e, cert, 10 if self.is_kids_profile else None)))

    def on_movie_select(self, movie): MovieDetailsModal(self, movie, self.engine, self.on_toggle_fav)

    def on_toggle_fav(self, movie_data):
        t = movie_data['title']
        self.favorites.remove(t) if t in self.favorites else self.favorites.add(t)
        if self.current_tab == "favorites": self.switch_tab("favorites")


if __name__ == "__main__":
    app = NetflixApp()
    app.mainloop()
