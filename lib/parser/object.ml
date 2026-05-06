open Core

module type Postgres_object_parser = sig
  type t

  val get_statement_regex : string
  val postgres_object_of_match : Re.Group.t -> (t, string) Either.t
end
