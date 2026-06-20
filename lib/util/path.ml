open Core
open Fpath

let of_string path_string =
  match Fpath.of_string path_string with
  | Error (`Msg msg) -> Second msg
  | Ok a -> First a

let append_child parent seg =
  match parent with Some p -> p / seg | None -> Fpath.v seg
