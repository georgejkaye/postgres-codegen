module type Postgres_object = sig
  type t
  val get_name : t -> string

  val get_drop_statement: t -> string
end