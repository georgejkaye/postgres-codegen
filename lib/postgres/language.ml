open Core

type language = Sql | C | Internal | Plpgsql [@@deriving show]

let of_string s =
  match String.lowercase s with
  | "sql" -> Some Sql
  | "c" -> Some C
  | "internal" -> Some Internal
  | "plpgsql" -> Some Plpgsql
  | _ -> None
