## Generated Story 1
* Default Fallback Intent
	- input_unknown
## Generated Story 2
* Default Fallback Intent
	- input_unknown
## Generated Story 3
* Default Welcome Intent
	- input_welcome
## Generated Story 4
* Default Welcome Intent
	- input_welcome
## Generated Story 5
* discover-artist{"doremus-artist": "Vivaldi"}
	- slot{"doremus-artist": "Vivaldi"}
	- discover_artist
## Generated Story 6
* discover-artist
	- discover_artist
* inform_artist{"doremus-artist": "Vivaldi"} 
	- slot{"doremus-artist": "Vivaldi"}
	- discover_artist
## Generated Story 6

* discover-artist
	- discover_artist

* Default Fallback Intent
	- input_unknown  

* inform_artist{"doremus-artist": "Vivaldi"} 
	- slot{"doremus-artist": "Vivaldi"}
	- discover_artist  
## Generated Story 7
* find-artist
	- find_artist
## Generated Story 8
* find-artist
	- find_artist
## Generated Story 9
* find-performance{"date-period": "en 1875"}
	- slot{"date-period": "en 1875"}
	- find_performance
## Generated Story 10
* find-performance
	- find_performance
* inform_period{"date-period": "en 1875"}
	- slot{"date-period": "en 1875"}
	- find_performance  
## Generated Story 10
* find-performance
	- find_performance

* Default Fallback Intent
	- input_unknown  

* inform_period{"date-period": "en 1875"}
	- slot{"date-period": "en 1875"}
	- find_performance

## Generated Story 11
* hello
	- input_welcome
## Generated Story 12
* hello
	- input_welcome
## Generated Story 13
* help
	- help
## Generated Story 14
* help
	- help
## Generated Story 15
* reset
	- reset
## Generated Story 16
* reset
	- reset
## Generated Story 17
* works-by - no{"works-by-followup": "1"}
	- works_by_works_by_no
## Generated Story 18
* works-by - no
	- works_by_works_by_no
## Generated Story 19
* works-by - yes{"works-by-followup": "1"}
	- works_by_works_by_yes
## Generated Story 20
* works-by - yes
	- works_by_works_by_yes
## Generated Story 21
* works-by-artist{"doremus-artist": "Bach","works-by-followup": "1"}
	- slot{"doremus-artist": "Bach"}
	- works_by_artist
## Generated Story 22
* works-by-artist
	- works_by_artist
* inform_artist{"doremus-artist": "Bach","works-by-followup": "1"}
	- slot{"doremus-artist": "Bach"}
	- works_by_artist  

## Generated Story 22
* works-by-artist
	- works_by_artist
* Default Fallback Intent
	- input_unknown 
* inform_artist{"doremus-artist": "Bach","works-by-followup": "1"}
	- slot{"doremus-artist": "Bach"}
	- works_by_artist   
## Generated Story 23
* works-by-genre{"doremus-genre": "melodies","works-by-followup": "1"}
	- slot{"doremus-genre": "melodies"}
	- works_by_genre
## Generated Story 24
* works-by-genre
	- works_by_genre
* inform_genre{"doremus-genre": "melodies","works-by-followup": "1"}
	- slot{"doremus-genre": "melodies"}
	- works_by_genre
## Generated Story 24
* works-by-genre
	- works_by_genre
* Default Fallback Intent
	- input_unknown   
* inform_genre{"doremus-genre": "melodies","works-by-followup": "1"}
	- slot{"doremus-genre": "melodies"}
	- works_by_genre

## Generated Story 25
* works-by-instrument{"doremus-instrument": "clarinet","works-by-followup": "1"}
	- slot{"doremus-instrument": "clarinet"}
	- works_by_instrument
## Generated Story 26
* works-by-instrument
	- works_by_instrument
* inform_instrument{"doremus-instrument": "clarinet","works-by-followup": "1"}
	- slot{"doremus-instrument": "clarinet"}
	- works_by_instrument
## Generated Story 26
* works-by-instrument
	- works_by_instrument
* Default Fallback Intent
	- input_unknown  
* inform_instrument{"doremus-instrument": "clarinet","works-by-followup": "1"}
	- slot{"doremus-instrument": "clarinet"}
	- works_by_instrument      
## Generated Story 27
* works-by-years{"date-period": "during 1900","works-by-followup": "1"}
	- slot{"date-period": "during 1900"}
	- works_by_years
## Generated Story 28
* works-by-years
	- works_by_years
* inform_period{"date-period": "during 1900","works-by-followup": "1"}
	- slot{"date-period": "during 1900"}
	- works_by_years  
## Generated Story 28
* works-by-years
	- works_by_years
* Default Fallback Intent
	- input_unknown   
* inform_period{"date-period": "during 1900","works-by-followup": "1"}
	- slot{"date-period": "during 1900"}
	- works_by_years  
## Generated Story 29
* works-by
	- works_by
## Generated Story 30
* works-by
	- works_by        


## Generated Story 5
* discover-artist{"doremus-artist": "Bach"}
	- slot{"doremus-artist": "Bach"}
	- discover_artist
## Generated Story 7
* find-artist{"number": "3","doremus-instrument": "piano","date-period": "between 1777 and 1899","geo-city": "nearby","doremus-strictly": "e","doremus-genre": "sonate"}
	- slot{"number": "3"}
	- slot{"doremus-instrument": "piano"}
	- slot{"date-period": "between 1777 and 1899"}
	- slot{"geo-city": "nearby"}
	- slot{"doremus-strictly": "e"}
	- slot{"doremus-genre": "sonate"}
	- find_artist
## Generated Story 9
* find-performance{"date-period": "during 1745","geo-city": "Paris","number": "due"}
	- slot{"date-period": "during 1745"}
	- slot{"geo-city": "Paris"}
	- slot{"number": "due"}
	- find_performance


## Generated Story 17
* works-by - no{"works-by-followup": "1"}
	- works_by_works_by_no
## Generated Story 19
* works-by - yes{"works-by-followup": "1"}
	- works_by_works_by_yes
## Generated Story 21
* works-by-artist{"doremus-artist": "Debussy","works-by-followup": "1"}
	- slot{"doremus-artist": "Debussy"}
	- works_by_artist
## Generated Story 23
* works-by-genre{"doremus-genre": "aria","works-by-followup": "1"}
	- slot{"doremus-genre": "aria"}
	- works_by_genre
## Generated Story 25
* works-by-instrument{"doremus-strictly": "e","doremus-instrument": "violin","works-by-followup": "1"}
	- slot{"doremus-strictly": "e"}
	- slot{"doremus-instrument": "violin"}
	- works_by_instrument
## Generated Story 27
* works-by-years{"date-period": "next month","works-by-followup": "1"}
	- slot{"date-period": "next month"}
	- works_by_years
## Generated Story 29
* works-by{"number": "3","doremus-artist": "Vivaldi","doremus-instrument": "clarinetto","doremus-strictly": "and","doremus-genre": "aria","date-period": "en 1876"}
	- slot{"number": "3"}
	- slot{"doremus-artist": "Vivaldi"}
	- slot{"doremus-instrument": "clarinetto"}
	- slot{"doremus-strictly": "and"}
	- slot{"doremus-genre": "aria"}
	- slot{"date-period": "en 1876"}
	- works_by

