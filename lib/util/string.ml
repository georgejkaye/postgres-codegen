include Core.String

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

let drop_pattern s pattern =
  match split_on_pattern s pattern with
  | _, None -> None
  | first, Some _ -> Some first
