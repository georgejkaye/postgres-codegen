open Core

module type Make_parser_t = sig
  type t

  val of_match : Re.Group.t -> (t, string) Either.t
  val to_object : t -> Postgres.Object.postgres_object

  val object_of_statement :
    string -> (Postgres.Object.postgres_object, string) Either.t
end

module Make_parser (P : Object.Postgres_object_parser_t) = struct
  type t = P.t

  let get_match_for_statement =
    P.get_statement_regex |> Re.Perl.re |> Re.compile |> Re.exec_opt

  let of_match = P.of_match
  let to_object = P.to_object

  let variant_of_match m =
    match P.of_match m with
    | First obj -> First (P.to_object obj)
    | Second msg -> Second msg

  let object_of_statement statement =
    match get_match_for_statement statement with
    | None ->
        Second
          [%string "Could not parse %{P.get_object_type_name}: %{statement}"]
    | Some m -> variant_of_match m
end
