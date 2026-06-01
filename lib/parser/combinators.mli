open Angstrom

val take_until_string : string -> string t
val take_until_string1 : string -> string t
val take_until_strings : string list -> string t
val take_until_strings1 : string list -> string t
val take_until_distinct_string : string -> string t
val take_until_distinct_strings : string list -> string t
val take_until_distinct_string1 : string -> string t
val take_until_distinct_strings1 : string list -> string t
val ws : unit t
val char_ws : char -> char t
val string_ci_ws : string -> string t
val ( ^^ ) : 'a t -> 'b t -> ('a * 'b) t
