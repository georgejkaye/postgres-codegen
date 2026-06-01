open Angstrom
open Util

let take_until_strings' ~allow_empty strings =
  let sorted_strings =
    List.sort strings ~compare:(fun a b ->
        Int.compare (String.length a) (String.length b))
  in
  let rec go acc =
    (let rec try_strings = function
       | [] -> fail "try next char"
       | current_string :: rest ->
           let len = String.length current_string in
           peek_string len
           >>= (fun str ->
                 if String.is_prefix str ~prefix:current_string then
                   return (String.of_char_list (List.rev acc))
                   <* string current_string
                 else try_strings rest)
           <|> try_strings rest
     in
     try_strings sorted_strings)
    <|> (any_char >>= fun c -> go (c :: acc))
  in
  go [] >>= fun x ->
  match String.length x with
  | 0 when not allow_empty -> fail "Only empty found"
  | _ -> return x

let take_until_string' s = take_until_strings' [ s ]

let take_until_distinct_strings' ss =
  take_until_strings' (List.map ~f:(fun x -> " " ^ x) ss)

let take_until_distinct_string' s = take_until_distinct_strings' [ s ]
let take_until_string = take_until_string' ~allow_empty:false
let take_until_string1 = take_until_string' ~allow_empty:true
let take_until_strings = take_until_strings' ~allow_empty:false
let take_until_strings1 = take_until_strings' ~allow_empty:true
let take_until_distinct_string = take_until_distinct_string' ~allow_empty:false
let take_until_distinct_string1 = take_until_distinct_string' ~allow_empty:true

let take_until_distinct_strings =
  take_until_distinct_strings' ~allow_empty:false

let take_until_distinct_strings1 =
  take_until_distinct_strings' ~allow_empty:true

let ws =
  skip_while (function
    | '\x20' | '\x0a' | '\x0d' | '\x09' | '\x85' -> true
    | _ -> false)

let char_ws c = char c <* ws
let string_ci_ws s = string_ci s <* ws
let ( ^^ ) = both
