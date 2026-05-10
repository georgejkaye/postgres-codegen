open Angstrom
open Core
open Util

type 'a char_map_node = More of bool * (char, 'a char_map_node, 'a) Map.t

let get_char_map_from_string_list ss =
  let get_char_map_from_string_list' map ss =
    let get_char_map_from_string map s =
      let rec get_char_map_from_char_list map cs =
        match cs with
        | [] ->
            let (More (_, mmap)) = map in
            More (true, mmap)
        | c :: cs ->
            let (More (a, mmap)) = map in
            More
              ( a,
                Map.update mmap c ~f:(function
                  | None ->
                      get_char_map_from_char_list
                        (More (false, Map.empty (module Char)))
                        cs
                  | Some x -> get_char_map_from_char_list x cs) )
      in
      get_char_map_from_char_list map (String.to_list s)
    in
    List.fold ss ~f:(fun acc cur -> get_char_map_from_string acc cur) ~init:map
  in
  get_char_map_from_string_list' (More (false, Map.empty (module Char))) ss

let take_till_string_tree allow_empty original_map =
  scan_state ([], [], [original_map]) (fun (s_w, s_wr, maps) c ->
      let next_s_w = c :: s_w in
      let check_map = function
        | More (true, _) -> None
        | More (_, nmap) -> (
            match Map.find nmap c with
            | Some next_map -> Some (next_s_w, s_wr, next_map :: maps)
            | None -> Some (next_s_w, next_s_w, original_map))
  in)
  List.fol
  >>= function
  | _, s_wr, More (true, _) -> (
      match s_wr with
      | [] when not allow_empty -> fail "Only found empty"
      | s_wr -> return (s_wr |> List.rev |> String.of_list))
  | _ -> fail "String not found"

let take_till_strings ss =
  get_char_map_from_string_list ss |> take_till_string_tree true

let take_till_strings1 ss =
  get_char_map_from_string_list ss |> take_till_string_tree false

let take_till_string s = take_till_strings [ s ]
let take_till_string1 s = take_till_strings1 [ s ]

let take_till_distinct_strings' allow_empty ss =
  get_char_map_from_string_list ss |> fun mmap ->
  More
    ( false,
      Map.add_exn
        (Map.add_exn (Map.empty (module Char)) ~key:' ' ~data:mmap)
        ~key:'\n' ~data:mmap )
  |> take_till_string_tree allow_empty

let take_till_distinct_strings = take_till_distinct_strings' true
let take_till_distinct_strings1 = take_till_distinct_strings' false
let take_till_distinct_string s = take_till_distinct_strings [ s ]
let take_till_distinct_string1 s = take_till_distinct_strings1 [ s ]

let ws =
  skip_while (function
    | '\x20' | '\x0a' | '\x0d' | '\x09' | '\x85' -> true
    | _ -> false)

let char_ws c = char c <* ws
let string_ci_ws s = string_ci s <* ws
let ( ^^ ) = both
