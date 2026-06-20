open Core

type parameter = {
  parameter_name : string;
  parameter_type : Types.postgres_type;
}
[@@deriving show, compare]

let make_parameter parameter_name parameter_type =
  { parameter_name; parameter_type }
