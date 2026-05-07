open Core

module type Postgres_object_parser_t = sig
  type t

  val get_statement_regex : string
  val of_match : Re.Group.t -> (t, string) Either.t
  val to_object : t -> Postgres.Object.postgres_object
end
