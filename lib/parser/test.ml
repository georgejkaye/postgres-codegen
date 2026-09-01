open Angstrom
open Core

let parselist p s sh =
  parse_string p ~consume:All s |> function
  | Ok bs -> List.iter ~f:(fun b -> printf "|%s|\n" (sh b)) bs
  | Error msg -> failwith msg

let parsestring p s sh =
  parse_string p ~consume:All s |> function
  | Ok b -> printf "|%s|\n" (sh b)
  | Error msg -> printf "%s\n" msg
