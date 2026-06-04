open Angstrom
open Util

let ws =
  skip_while (function
    | '\x20' | '\x0a' | '\x0d' | '\x09' | '\x85' -> true
    | _ -> false)

let char_ws c = char c <* ws
let string_ci_ws s = string_ci s <* ws
let ( ^^ ) = both

let ( <?> ) p l =
  let* remaining = available in
  let remaining = min remaining 20 in
  let* s = peek_string remaining in
  p <?> Printf.sprintf "%s, got: [%s]" l s

let take_till_strings' ~distinct ~allow_empty strings =
  (let sorted_strings =
     List.sort strings ~compare:(fun a b ->
         Int.compare (String.length a) (String.length b))
   in
   let rec go acc =
     (let rec try_strings distinct = function
        | [] -> fail "try next char"
        | current_string :: rest ->
            let peek_string =
              let len = String.length current_string in
              peek_string len >>= fun str ->
              if String.is_prefix str ~prefix:current_string then
                return (String.of_char_list (List.rev acc))
              else try_strings false rest
            in
            let peek_distinct =
              peek_string >>= fun s ->
              match String.to_list_rev s with
              | [] -> if allow_empty then return s else fail "only empty found"
              | c :: cs -> (
                  match c with
                  | ' ' | '\r' | '\n' ->
                      return (String.of_char_list (List.rev cs))
                  | _ -> fail "Not distinct match")
            in
            if distinct then peek_distinct else peek_string
      in
      try_strings distinct sorted_strings)
     <|> (any_char >>= fun c -> go (c :: acc))
   in
   go [] >>= fun x ->
   match String.length x with
   | 0 when not allow_empty -> fail "Only empty found"
   | _ -> return x)
  <?> "expected " ^ String.concat ~sep:" or " strings

let take_till_string' s = take_till_strings' [ s ]
let take_till_distinct_strings' = take_till_strings' ~distinct:true
let take_till_distinct_string' s = take_till_distinct_strings' [ s ]
let take_till_string = take_till_string' ~distinct:false ~allow_empty:true
let take_till_string1 = take_till_string' ~distinct:false ~allow_empty:false
let take_till_strings = take_till_strings' ~distinct:false ~allow_empty:true
let take_till_strings1 = take_till_strings' ~distinct:false ~allow_empty:false
let take_till_distinct_string = take_till_distinct_string' ~allow_empty:true
let take_till_distinct_string1 = take_till_distinct_string' ~allow_empty:false
let take_till_distinct_strings = take_till_distinct_strings' ~allow_empty:true
let take_till_distinct_strings1 = take_till_distinct_strings' ~allow_empty:false
let take_till_char c = take_till (Char.equal c)

let at_most_one p =
  many p >>= fun rs ->
  let n = List.length rs in
  match n with 0 | 1 -> return (n, rs) | _ -> fail "Too many"
