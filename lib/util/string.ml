include Core.String
open Core

let split_on_pattern s pattern =
  match Core.String.substr_index s ~pattern with
  | None -> (s, None)
  | Some i ->
      ( Core.String.slice s 0 i,
        Some
          (Core.String.slice s
             (i + Core.String.length pattern)
             (Core.String.length s)) )

let split_on_commas = split ~on:','
let split_on_semicolons = split ~on:';'
let split_on_first_space = lsplit2 ~on:' '

let starts_with s pattern =
  match split_on_pattern s pattern with _, None -> false | _, Some _ -> true

let drop_pattern_from_end s pattern =
  match split_on_pattern s pattern with
  | _, None -> None
  | first, Some second -> if String.length second = 0 then Some first else None

let drop_pattern_from_start s pattern =
  match split_on_pattern s pattern with
  | _, None -> None
  | first, Some second -> if String.length first = 0 then Some second else None
