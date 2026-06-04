type parameter = {
  parameter_name : string;
  parameter_type : Types.postgres_type;
}
[@@deriving show]

type pg_object =
  | Type of string * parameter list
  | Function of
      string * parameter list * Types.postgres_type * Language.language * string
  | Domain of string * string
[@@deriving show]

type statement =
  | Create of pg_object
  | Drop of Object_type.pg_object_type * string
[@@deriving show]
