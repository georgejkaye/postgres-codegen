module type Postgres_object_t = sig
  type t

  val get_object_type_name : string
  val get_name : t -> string
  val get_drop_statement : t -> string
end
