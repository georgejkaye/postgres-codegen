open Core

type parameter = {
  parameter_name : string;
  parameter_type : Types.postgres_type;
}
[@@deriving show, compare]
