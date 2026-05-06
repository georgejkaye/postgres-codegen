let split s pattern =
  match Core.String.substr_index s ~pattern with
  | None -> (s, None)
  | Some i ->
      ( Core.String.slice s 0 i,
        Some
          (Core.String.slice s
             (i + Core.String.length pattern)
             (Core.String.length s)) )

let split_on_commas = Core.String.split ~on:','
let split_on_semicolons = Core.String.split ~on:';'
let split_on_first_space = Core.String.lsplit2 ~on:' '
