open Core
include List

let map_with_fail xs ~message ~f =
  Core.List.fold_right xs
    ~f:(fun cur acc ->
      match acc with
      | Second msg -> Second msg
      | First acc -> (
          match f cur with
          | None -> Second [%string "%{message}"]
          | Some result -> First (result :: acc)))
    ~init:(First [])

let filter_seconds =
  List.fold_right
    ~f:(fun cur acc -> match cur with Second _ -> acc | First f -> f :: acc)
    ~init:[]
